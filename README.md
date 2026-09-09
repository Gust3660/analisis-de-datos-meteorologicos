# Análisis de datos meteorológicos

Aplicación Streamlit para resumir y visualizar series de temperatura y precipitación. Incluye datos demostrativos y acepta un CSV propio.

## Funciones

- Calcula temperaturas media, mínima y máxima, precipitación acumulada y tendencia lineal.
- Grafica temperatura y promedio móvil configurable.
- Agrupa temperatura y precipitación por mes.
- Acepta datos de ejemplo o carga de un archivo CSV.

## Estructura

```text
.
├── backend.py       # Métricas y análisis de series
├── frontend.py      # Interfaz Streamlit y visualizaciones
├── requirements.txt
└── README.md
```

## Formato del CSV

Columnas obligatorias: `fecha`, `temp_c`. Columna opcional: `precip_mm` (si falta, se toma como cero). Ejemplo:

```csv
fecha,temp_c,precip_mm
2025-01-01,18.2,0
2025-01-02,17.5,2.4
2025-01-03,19.1,0
```

Las fechas deben ser únicas y debe haber al menos dos filas. La app ordena los datos por fecha.

## Instalación y ejecución

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m streamlit run frontend.py
```

En macOS o Linux, activa el entorno con `source .venv/bin/activate`.

## Uso

Selecciona los datos de ejemplo o sube un CSV, ajusta el promedio móvil y explora las gráficas y métricas. La tendencia se expresa por fila observada; para interpretar ese valor como tendencia diaria, usa datos diarios regulares.
