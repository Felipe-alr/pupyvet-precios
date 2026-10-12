# Prompt para Claude Code – Dashboard de precios PupyVet

Quiero que construyas un dashboard de consulta de precios para los vendedores de PupyVet (pet shop + peluquería + veterinaria en Concepción, Chile). El objetivo es que encuentren el precio de cualquier producto o servicio en segundos, sin abrir ni filtrar Excel.

## Stack
- Python + Streamlit, en una sola app (`app.py`) con `requirements.txt`.
- Debe verse bien en celular y tablet (layout simple, botones y texto grandes), porque se usará en el mostrador.
- Incluye un `README.md` corto: cómo instalar, cómo ejecutar (`streamlit run app.py`), cómo abrirlo desde el celular en la misma red wifi (`--server.address 0.0.0.0`) y cómo actualizar precios editando los CSV.

## Datos: crea 3 archivos CSV editables (separador `;`, UTF-8)
Los precios viven en CSV para poder cambiarlos sin tocar el código. La app los relee cuando cambian (usa `st.cache_data` con la fecha de modificación del archivo como parte de la clave).

### 1) `productos.csv` – productos y accesorios (precios de venta con IVA, CLP)
Crea el archivo exactamente con este contenido. Lee la columna `codigo` siempre como texto, porque hay códigos con ceros a la izquierda ("06032", "0000000435456") y alfanuméricos ("K-234", "X06494", "BA-2306").

```
codigo;producto;categoria;precio
12450068;Pro Plan Adult Cat 3 kg;Alimento seco gato;24490
12449850;Pro Plan Kitten 1 kg;Alimento seco gato;10650
12452939;Pro Plan Adult Small Breed 3 kg;Alimento seco perro;24990
12452753;Pro Plan Puppy Small Breed 1 kg;Alimento seco perro;10900
12627579;Dentalife Gatos 40 g;Snacks;1990
12343166;Dentalife Dogs Small Breed 42 g;Snacks;2390
12341820;Pro Plan Adulto Carne sobre 100 g;Alimento húmedo;1690
80207;Churu Meal Topper Dog Pollo Calabaza (caja);Snacks;2890
80204;Churu Meal Topper Atún (caja);Snacks;2890
80205;Ciao Churu Meal Topper Pollo (caja);Snacks;2890
4548;Cat Fest barras de carne cordero 45 g;Snacks;2100
7072;Rahue Jerky pote vacuno 250 g;Snacks;7990
11781;Rahue fémur de cerdo;Snacks;3000
10799;Rahue tráquea vacuno corta 50 g;Snacks;2000
3538;Caja Fellini Lollipop Cranberry 3 x 15 un;Snacks;2490
10755;Simparica 2,6–5 kg (10 mg);Antiparasitarios;7990
10727;Simparica 5–10 kg (20 mg);Antiparasitarios;8490
10723;Simparica 10–20 kg (40 mg);Antiparasitarios;9390
10725;Simparica 20–40 kg (80 mg);Antiparasitarios;13990
10726;Simparica 40–60 kg (120 mg);Antiparasitarios;17950
451222;Simparica Trio 1,25–2,5 kg;Antiparasitarios;8590
500504;Simparica Trio 2,6–5 kg;Antiparasitarios;9140
500506;Simparica Trio 5–10 kg;Antiparasitarios;10590
500507;Simparica Trio 10–20 kg;Antiparasitarios;11690
500505;Simparica Trio 20–40 kg;Antiparasitarios;16990
504647;Caja Backhome Super Chip (10 unid);Snacks;8000
211;Advantage gatos hasta 4 kg (pipeta);Antiparasitarios;8690
3286;Advantage gatos 4–8 kg (pipeta);Antiparasitarios;11990
10534;Traper shampoo neutro puppy 260 ml;Higiene;4990
1762;Traper shampoo neutro perro adulto 260 ml;Higiene;4990
11034;Alfa Dog Premium adulto razas pequeñas 3 kg;Alimento seco perro;9990
166851;Alfa Dog Premium cachorro 3 kg;Alimento seco perro;9990
504022;Alfa Dog Premium cachorro razas pequeñas 3 kg;Alimento seco perro;9990
10254;Alfa Dog Premium adulto 20 kg;Alimento seco perro;37990
258926;Arena Stay Happy aglutinante lavanda 4 kg;Arena sanitaria;6000
279934;Arena Stay Happy aglutinante café 4 kg;Arena sanitaria;6000
258920;Arena Stay Happy aglutinante lavanda 10 kg;Arena sanitaria;13690
7800006002854;Drag Pharma Mebermic x 50 comprimidos;Medicamentos y suplementos;1500
0000000435456;Drag Pharma Mamistop perro 125 g;Medicamentos y suplementos;8990
000DRO1006105;Drag Pharma Mamistop gato 100 g;Medicamentos y suplementos;7490
0009-0001-0000537;Drag Pharma Superpet Omega 6 gato 125 ml;Medicamentos y suplementos;7390
0009-0001-0000538;Drag Pharma Superpet Omega perro 125 ml;Medicamentos y suplementos;7390
0009-0001-0000539;Drag Pharma Superpet Omega Puppy 125 ml;Medicamentos y suplementos;7390
0009-0001-0000540;Drag Pharma Superpet Omega Senior 125 ml;Medicamentos y suplementos;6990
0000000645805;Elanco Credelio 56,25 mg (1,3–2,5 kg) 1 comp.;Antiparasitarios;7990
7766;Brit Care GF Adulto Salmón 3 kg;Alimento seco perro;25990
10817;Brit Care Puppy Lamb & Rice 3 kg;Alimento seco perro;25990
156853;Brit Care Cat GF Sterilized Weight Control 2 kg;Alimento seco gato;23990
156854;Brit Care Cat GF Sterilized Urinary 2 kg;Alimento seco gato;23990
443948;Bravery gato adulto chicken 2 kg;Alimento seco gato;23990
506390;Bravery adulto chicken small 2 kg;Alimento seco perro;22990
35324;Collar isabelino talla M;Accesorios – isabelinos;4990
35556;Collar isabelino talla S;Accesorios – isabelinos;4490
06032;Collar isabelino N° 25;Accesorios – isabelinos;5990
60923;Bebedero para perro 500 ml;Accesorios – platos y bebederos;3590
X06494;Collar piel sintética c/gemas 3,0 cm;Accesorios – collares;4990
31006;Collar con bufanda 2,5;Accesorios – collares;2990
31008;Collar con bufanda 3,5;Accesorios – collares;3490
60456;Collar para gato talla S-M-L;Accesorios – collares;1990
K-234;Collar de cuero 3,0 x 58 cm;Accesorios – collares;4990
96948;Collar corbata;Accesorios – collares;2990
31776;Plato comida lenta (modelo 31776);Accesorios – platos y bebederos;2990
90040;Plato comida lenta (modelo 90040);Accesorios – platos y bebederos;3990
05610;Plato metálico 18 cm;Accesorios – platos y bebederos;3490
93800;Cuenco 23 x 13 x 4 cm;Accesorios – platos y bebederos;1990
01230;Pala recolectora arena gato 28 x 10,5 cm;Accesorios – higiene;1990
X01046;Pala dosificadora multiuso 20,5 x 7,5 cm;Accesorios – higiene;1990
92206;Bolsa higiénica + dispensador hueso;Accesorios – higiene;1990
92227;Bolsa sanitaria mascota (3 rollos);Accesorios – higiene;1990
X-76;Pelota sandía pequeña 5 cm;Accesorios – juguetes;2990
S-271;Pollo gritando M 31 cm;Accesorios – juguetes;2990
K-161;Animal de peluche 19 x 8 cm;Accesorios – juguetes;3500
93422;Juguete para mascota 6,3 cm;Accesorios – juguetes;1990
90456;Bola de cuerda bicolor 18 cm;Accesorios – juguetes;2990
61379;Varita divertida (gato);Accesorios – juguetes;1990
11527;Ratón con pluma;Accesorios – juguetes;1990
11526;Ratón vibratorio;Accesorios – juguetes;2500
S-123;Cepillo para mascotas 13 x 6 cm;Accesorios – higiene;2990
BA-2306;Caja de arena mediana + pala;Accesorios – higiene;9990
27386;Arnés + correa 1 metro;Accesorios – arneses y correas;7990
27321;Arnés + correa acolchada XL;Accesorios – arneses y correas;8990
27226;Arnés + correa L;Accesorios – arneses y correas;5990
27221;Arnés + correa para gato 1,0;Accesorios – arneses y correas;5990
K-100;Ropa quirúrgica talla XS-S-M;Accesorios – post-operatorio;7990
S-74;Bozal para mascotas talla S;Accesorios – bozales;2990
S-75;Bozal para perros talla M;Accesorios – bozales;2990
84073;Cama redonda 45 x 10 cm;Accesorios – camas y sabanillas;8990
32988;Tijera corta uñas para gatos;Accesorios – higiene;2790
S-86;Cepillo de dientes 5,1 x 2,3 cm;Accesorios – higiene;1990
14632;Sabanillas para mascota 60 x 45 cm;Accesorios – camas y sabanillas;4990
```

### 2) `servicios_vet.csv` – veterinaria
```
servicio;precio;nota
Consulta veterinaria;12000;
Vacunas anuales;18000;
Microchip;10000;
Promoción octubre: Consulta + vacuna;15000;Válida solo en octubre
```
- La promoción debe mostrarse destacada (badge "PROMO") solo mientras la fecha actual esté en octubre. Agrega una columna opcional `vigente_hasta` (aaaa-mm-dd) para manejar futuras promociones de forma genérica, y usa 2026-10-31 para esta.

### 3) `precios_peluqueria.csv` – baño y peluquería
```
peso_min;peso_max;bano;peluqueria
0;5;20000;25000
5.1;10;22000;26000
10.1;15;24000;30000
15.1;20;25000;35000
20.1;25;26000;42000
25.1;30;28000;47000
30.1;35;32000;50000
```

## Pestaña 1 – Productos y accesorios
- Un buscador único: "Buscar por nombre o código". Sin distinguir mayúsculas ni tildes ("arnes" encuentra "Arnés", "simparica trio 5" encuentra "Simparica Trio 5–10 kg"), con búsqueda parcial también por código.
- Filtro de categoría con chips más la opción "Todas". Agrupa todas las "Accesorios – …" bajo un filtro padre "Accesorios" con sus subcategorías.
- Resultados en tarjetas o tabla grande: Producto, Código, Categoría y **Precio** destacado en formato chileno ($24.990).
- Opción de ordenar por nombre o por precio.
- Sin resultados: "No encontrado – consulta con administración".

## Pestaña 2 – Peluquería y baños
- Calculadora: el vendedor ingresa el peso (acepta coma o punto decimal) y ve en grande **ambos** precios, baño y peluquería. Para elegir el tramo, toma el primero cuyo `peso_max` sea ≥ al peso ingresado (10 kg cae en 5,1–10; 10,05 kg cae en 10,1–15).
- Sobre 35 kg: "Consultar con el peluquero".
- Muestra también la tabla completa y siempre estas notas:
  - Peluquería incluye baño y cepillado, corte según raza, corte de uñas, limpieza de oídos y perfume. El valor es aproximado, depende del pelaje y lo evalúa el peluquero.
  - Baño incluye corte de uñas, limpieza de oídos y perfume.

## Pestaña 3 – Veterinaria
- Lista de servicios con su precio en tarjetas grandes, con la promoción vigente destacada arriba.

## Diseño
- Colores de marca: fucsia/magenta (#C85BB5 aprox.) y gris oscuro (#3A3A3A), fondo claro. Título "Puppy Vet · Consulta de precios".
- Sin costos, márgenes, proveedores ni gráficos. Es solo una herramienta de consulta para vendedores.

## Entrega y pruebas
1. Crea los 3 CSV, `app.py`, `requirements.txt` y `README.md`.
2. Verifica que `productos.csv` tenga 90 productos y que los códigos con ceros a la izquierda se conserven.
3. Prueba la búsqueda con "churu", "simparica trio", "35324", "k-234", "arnes" y "06032". Confirma que Simparica Trio 5–10 kg muestra $10.590.
4. Prueba la calculadora con 4,5 / 5 / 10 / 10,05 / 30 / 40 kg y muéstrame los resultados.
5. Ejecuta la app y dime la URL local.
