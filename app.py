"""Puppy Vet · Consulta de precios (Streamlit)."""

import html
import re
import unicodedata
from datetime import date, datetime
from pathlib import Path

import pandas as pd
import streamlit as st

BASE = Path(__file__).parent
PRODUCTOS = BASE / "productos.csv"
SERVICIOS = BASE / "servicios_vet.csv"
PELUQUERIA = BASE / "precios_peluqueria.csv"

FUCSIA = "#C85BB5"
GRIS = "#3A3A3A"
PREFIJO_ACC = "Accesorios – "

NOTA_PELUQUERIA = (
    "Peluquería incluye baño y cepillado, corte según raza, corte de uñas, "
    "limpieza de oídos y perfume. El valor es aproximado, depende del pelaje "
    "y lo evalúa el peluquero."
)
NOTA_BANO = "Baño incluye corte de uñas, limpieza de oídos y perfume."


# ---------- Lógica (sin UI, testeable) ----------

def hoy() -> date:
    try:
        from zoneinfo import ZoneInfo
        return datetime.now(ZoneInfo("America/Santiago")).date()
    except Exception:
        return date.today()


def normalizar(texto) -> str:
    """Minúsculas, sin tildes y con guiones unificados."""
    texto = unicodedata.normalize("NFKD", str(texto))
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    return texto.lower().replace("–", "-").replace("—", "-").strip()


def solo_alfanum(texto) -> str:
    return re.sub(r"[^0-9a-z]", "", normalizar(texto))


def clp(valor) -> str:
    return "$" + f"{int(round(float(valor))):,}".replace(",", ".")


def leer_productos(path=PRODUCTOS) -> pd.DataFrame:
    df = pd.read_csv(path, sep=";", encoding="utf-8", dtype={"codigo": str})
    df["codigo"] = df["codigo"].str.strip()
    df["precio"] = pd.to_numeric(df["precio"], errors="coerce").fillna(0).astype(int)
    df["categoria"] = df["categoria"].str.strip()
    df["_nombre"] = df["producto"].map(normalizar)
    df["_texto"] = (df["producto"] + " " + df["codigo"] + " " + df["categoria"]).map(normalizar)
    df["_codigo"] = df["codigo"].map(solo_alfanum)
    return df


def leer_servicios(path=SERVICIOS) -> pd.DataFrame:
    df = pd.read_csv(path, sep=";", encoding="utf-8", dtype=str, keep_default_na=False)
    if "vigente_hasta" not in df.columns:
        df["vigente_hasta"] = ""
    if "nota" not in df.columns:
        df["nota"] = ""
    df["precio"] = pd.to_numeric(df["precio"], errors="coerce").fillna(0).astype(int)
    df["vigente_hasta"] = pd.to_datetime(df["vigente_hasta"].str.strip(), errors="coerce").dt.date
    return df


def leer_peluqueria(path=PELUQUERIA) -> pd.DataFrame:
    df = pd.read_csv(path, sep=";", encoding="utf-8")
    for col in ("peso_min", "peso_max"):
        df[col] = pd.to_numeric(df[col].astype(str).str.replace(",", "."), errors="coerce")
    return df.sort_values("peso_max").reset_index(drop=True)


def buscar(df: pd.DataFrame, consulta: str) -> pd.DataFrame:
    """Todas las palabras deben aparecer (nombre, código o categoría); coincidencias exactas primero."""
    q = normalizar(consulta)
    if not q:
        return df.assign(_rank=0)
    q_cod = solo_alfanum(q)
    palabras = q.split()
    por_palabras = df["_texto"].apply(lambda t: all(p in t for p in palabras))
    por_codigo = df["_codigo"].str.contains(q_cod, regex=False) if q_cod else False
    res = df[por_palabras | por_codigo].copy()
    res["_rank"] = 2
    res.loc[res["_nombre"].str.contains(q, regex=False), "_rank"] = 1
    if q_cod:
        res.loc[res["_codigo"].str.startswith(q_cod), "_rank"] = 1
        res.loc[res["_codigo"] == q_cod, "_rank"] = 0
    return res


def parse_peso(texto: str):
    try:
        valor = float(str(texto).strip().replace(",", "."))
    except ValueError:
        return None
    return valor if valor > 0 else None


def tramo_peluqueria(tabla: pd.DataFrame, peso: float):
    """Primer tramo cuyo peso_max sea >= al peso. None si supera el máximo."""
    fila = tabla[tabla["peso_max"] >= peso]
    return None if fila.empty else fila.iloc[0]


def promo_vigente(fila, dia: date) -> bool:
    venc = fila["vigente_hasta"]
    return pd.notna(venc) and venc is not None and dia <= venc


def fmt_kg(valor) -> str:
    return f"{valor:g}".replace(".", ",")


# ---------- UI ----------

@st.cache_data
def cargar(nombre: str, mtime: float) -> pd.DataFrame:
    # mtime forma parte de la clave: si el CSV cambia, se relee
    lectores = {"productos": leer_productos, "servicios": leer_servicios, "peluqueria": leer_peluqueria}
    return lectores[nombre]()


def datos(nombre: str, path: Path) -> pd.DataFrame:
    return cargar(nombre, path.stat().st_mtime)


CSS = f"""
<style>
.stApp {{ background: #FAF7FA; }}
html, body, [class*="css"] {{ font-size: 18px; }}
h1.titulo {{ color: {GRIS}; font-size: 1.9rem; margin: 0 0 .2rem 0; line-height: 1.2; }}
h1.titulo span {{ color: {FUCSIA}; }}
.stTabs [data-baseweb="tab"] {{ font-size: 1.1rem; font-weight: 600; padding: .6rem .9rem; }}
.stTabs [aria-selected="true"] {{ color: {FUCSIA} !important; }}
.stTextInput input {{ font-size: 1.25rem; padding: .8rem; }}
.card {{ background: #fff; border-radius: 14px; padding: .9rem 1.1rem; margin-bottom: .7rem;
        border-left: 6px solid {FUCSIA}; box-shadow: 0 1px 4px rgba(0,0,0,.08);
        display: flex; justify-content: space-between; align-items: center; gap: 1rem; }}
.card .nombre {{ font-size: 1.15rem; font-weight: 600; color: {GRIS}; }}
.card .meta {{ font-size: .9rem; color: #777; margin-top: .2rem; }}
.card .precio {{ font-size: 1.6rem; font-weight: 800; color: {FUCSIA}; white-space: nowrap; }}
.promo {{ border-left-color: #E8A33A; background: #FFF6E8; }}
.badge {{ background: {FUCSIA}; color: #fff; font-size: .8rem; font-weight: 700; border-radius: 6px;
         padding: .1rem .5rem; margin-right: .4rem; vertical-align: middle; }}
.grande {{ background: #fff; border-radius: 16px; padding: 1.2rem; text-align: center;
          box-shadow: 0 1px 4px rgba(0,0,0,.08); margin-bottom: .8rem; }}
.grande .lbl {{ font-size: 1.2rem; color: {GRIS}; font-weight: 600; }}
.grande .val {{ font-size: 2.6rem; font-weight: 800; color: {FUCSIA}; }}
.aviso {{ background: #fff; border-radius: 14px; padding: 1rem; font-size: 1.2rem; color: {GRIS};
         border: 2px dashed {FUCSIA}; text-align: center; font-weight: 600; }}
@media (max-width: 640px) {{
  .card {{ flex-direction: column; align-items: flex-start; gap: .3rem; }}
  .grande .val {{ font-size: 2.2rem; }}
}}
</style>
"""


def card(nombre: str, meta: str, precio: int, promo: bool = False) -> str:
    badge = '<span class="badge">PROMO</span>' if promo else ""
    meta_html = f'<div class="meta">{html.escape(meta)}</div>' if meta else ""
    return (
        f'<div class="card{" promo" if promo else ""}"><div>'
        f'<div class="nombre">{badge}{html.escape(nombre)}</div>{meta_html}</div>'
        f'<div class="precio">{clp(precio)}</div></div>'
    )


def tab_productos():
    df = datos("productos", PRODUCTOS)
    consulta = st.text_input("Buscar por nombre o código", placeholder="Ej: simparica trio, arnes, 06032")

    cats = sorted(df["categoria"].unique())
    padres = sorted({PREFIJO_ACC.strip(" –") if c.startswith(PREFIJO_ACC) else c for c in cats})
    padre = st.pills("Categoría", ["Todas"] + padres, default="Todas", key="cat") or "Todas"

    filtrado = df
    if padre == "Accesorios":
        subs = [c.removeprefix(PREFIJO_ACC) for c in cats if c.startswith(PREFIJO_ACC)]
        sub = st.pills("Subcategoría", ["Todas"] + subs, default="Todas", key="sub") or "Todas"
        filtrado = df[df["categoria"].str.startswith(PREFIJO_ACC)]
        if sub != "Todas":
            filtrado = df[df["categoria"] == PREFIJO_ACC + sub]
    elif padre != "Todas":
        filtrado = df[df["categoria"] == padre]

    orden = st.radio("Ordenar por", ["Relevancia", "Nombre", "Precio menor", "Precio mayor"],
                     horizontal=True)
    res = buscar(filtrado, consulta)
    if orden == "Nombre":
        res = res.sort_values("_nombre")
    elif orden == "Precio menor":
        res = res.sort_values(["precio", "_nombre"])
    elif orden == "Precio mayor":
        res = res.sort_values(["precio", "_nombre"], ascending=[False, True])
    else:
        res = res.sort_values(["_rank", "_nombre"])

    if res.empty:
        st.markdown('<div class="aviso">No encontrado – consulta con administración</div>',
                    unsafe_allow_html=True)
        return
    st.caption(f"{len(res)} resultado(s)")
    st.markdown("".join(
        card(r.producto, f"Código {r.codigo} · {r.categoria}", r.precio) for r in res.itertuples()
    ), unsafe_allow_html=True)


def tab_peluqueria():
    tabla = datos("peluqueria", PELUQUERIA)
    texto = st.text_input("Peso de la mascota (kg)", placeholder="Ej: 4,5")
    if texto.strip():
        peso = parse_peso(texto)
        if peso is None:
            st.warning("Ingresa un peso válido, por ejemplo 7,5")
        else:
            fila = tramo_peluqueria(tabla, peso)
            if fila is None:
                st.markdown('<div class="aviso">Consultar con el peluquero</div>', unsafe_allow_html=True)
            else:
                st.caption(f"{fmt_kg(peso)} kg → tramo {fmt_kg(fila.peso_min)} a {fmt_kg(fila.peso_max)} kg")
                c1, c2 = st.columns(2)
                c1.markdown(f'<div class="grande"><div class="lbl">🛁 Baño</div>'
                            f'<div class="val">{clp(fila.bano)}</div></div>', unsafe_allow_html=True)
                c2.markdown(f'<div class="grande"><div class="lbl">✂️ Peluquería</div>'
                            f'<div class="val">{clp(fila.peluqueria)}</div></div>', unsafe_allow_html=True)

    st.info(f"**Peluquería:** {NOTA_PELUQUERIA}\n\n**Baño:** {NOTA_BANO}")
    st.subheader("Tabla completa")
    vista = pd.DataFrame({
        "Peso": [f"{fmt_kg(a)} – {fmt_kg(b)} kg" for a, b in zip(tabla.peso_min, tabla.peso_max)],
        "Baño": tabla.bano.map(clp),
        "Peluquería": tabla.peluqueria.map(clp),
    })
    st.dataframe(vista, hide_index=True, width="stretch")
    st.caption(f"Sobre {fmt_kg(tabla.peso_max.max())} kg: consultar con el peluquero.")


def tab_veterinaria():
    df = datos("servicios", SERVICIOS)
    dia = hoy()
    es_promo = df.apply(lambda f: promo_vigente(f, dia), axis=1)
    con_fecha = df["vigente_hasta"].notna()
    promos, normales = df[es_promo], df[~con_fecha]  # promociones vencidas no se muestran
    bloques = [card(r.servicio, r.nota, r.precio, promo=True) for r in promos.itertuples()]
    bloques += [card(r.servicio, r.nota, r.precio) for r in normales.itertuples()]
    st.markdown("".join(bloques), unsafe_allow_html=True)


def main():
    st.set_page_config(page_title="Puppy Vet · Precios", page_icon="🐾", layout="centered")
    st.markdown(CSS, unsafe_allow_html=True)
    st.markdown('<h1 class="titulo">🐾 <span>Puppy Vet</span> · Consulta de precios</h1>',
                unsafe_allow_html=True)
    t1, t2, t3 = st.tabs(["🛍️ Productos", "✂️ Peluquería", "🩺 Veterinaria"])
    with t1:
        tab_productos()
    with t2:
        tab_peluqueria()
    with t3:
        tab_veterinaria()


if __name__ == "__main__":
    main()
