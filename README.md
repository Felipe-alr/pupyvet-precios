# Puppy Vet · Consulta de precios

Dashboard para que los vendedores encuentren precios de productos, peluquería y veterinaria en segundos.

## Instalar
```
pip install -r requirements.txt
```

## Ejecutar
```
streamlit run app.py
```
Se abre en http://localhost:8501

## Abrir desde el celular (misma red wifi)
```
streamlit run app.py --server.address 0.0.0.0
```
Luego, en el celular, abre `http://<IP-del-PC>:8501` (la IP se ve con `ipconfig`, campo "Dirección IPv4", ej. `http://192.168.1.20:8501`). Si no carga, permite Python en el Firewall de Windows.

## Abrir desde cualquier navegador (Internet)
La app está publicada en Streamlit Community Cloud desde el repositorio de GitHub. Cada `git push` a `main` actualiza la app en línea en ~1 minuto.

## Actualizar precios
Edita los CSV (separador `;`, codificación UTF-8) con un editor de texto o Excel → "Guardar como CSV UTF-8 (delimitado por punto y coma)". La app los relee sola al detectar el cambio (recarga la página).

- `productos.csv`: `codigo;producto;categoria;precio`. Las categorías que empiezan con `Accesorios – ` se agrupan bajo "Accesorios".
- `servicios_vet.csv`: `servicio;precio;nota;vigente_hasta`. Si `vigente_hasta` (aaaa-mm-dd) tiene fecha, el servicio es una promoción: se muestra destacada con "PROMO" hasta esa fecha y luego se oculta.
- `precios_peluqueria.csv`: `peso_min;peso_max;bano;peluqueria`. Se usa el primer tramo cuyo `peso_max` sea ≥ al peso ingresado.

Precios en CLP con IVA, sin puntos (ej. `24990`).
