"""Interfaz Streamlit para explorar datos meteorológicos."""

from __future__ import annotations

import numpy as np
import pandas as pd
import streamlit as st

from backend import analyze_weather


def demo_weather() -> pd.DataFrame:
    dates = pd.date_range("2025-01-01", periods=365, freq="D")
    day = np.arange(len(dates))
    rng = np.random.default_rng(19)
    temperature = 17 + 9 * np.sin(2 * np.pi * (day - 30) / 365) + rng.normal(0, 2.2, len(day))
    wet_season = np.sin(2 * np.pi * (day - 150) / 365).clip(0, None)
    precipitation = rng.gamma(1.2, 2.0, len(day)) * wet_season
    return pd.DataFrame({"fecha": dates, "temp_c": temperature.round(1), "precip_mm": precipitation.round(1)})


def load_weather(file) -> pd.DataFrame:
    data = pd.read_csv(file)
    data.columns = [str(column).strip().lower() for column in data.columns]
    required = {"fecha", "temp_c"}
    if not required.issubset(data.columns):
        raise ValueError("El CSV debe tener columnas fecha y temp_c; precip_mm es opcional.")
    data = data[["fecha", "temp_c"] + (["precip_mm"] if "precip_mm" in data else [])].copy()
    data["fecha"] = pd.to_datetime(data["fecha"], errors="coerce")
    data["temp_c"] = pd.to_numeric(data["temp_c"], errors="coerce")
    if "precip_mm" not in data:
        data["precip_mm"] = 0.0
    data["precip_mm"] = pd.to_numeric(data["precip_mm"], errors="coerce")
    if data.isna().any().any():
        raise ValueError("El CSV contiene fechas o medidas vacías/no válidas.")
    data = data.sort_values("fecha").reset_index(drop=True)
    if data["fecha"].duplicated().any() or len(data) < 2:
        raise ValueError("Las fechas deben ser únicas y debe haber al menos dos observaciones.")
    return data


st.set_page_config(page_title="Datos meteorológicos", page_icon="🌦️", layout="wide")
st.title("Análisis de datos meteorológicos")
st.write("Resume temperatura y precipitación, revisa tendencias y compara meses.")

with st.sidebar:
    source = st.radio("Datos", ["Ejemplo", "Subir CSV"])
    uploaded = st.file_uploader("CSV meteorológico", type=["csv"]) if source == "Subir CSV" else None
    window = st.slider("Ventana de promedio móvil (días/filas)", 2, 60, 7)

if source == "Subir CSV" and uploaded is None:
    st.info("Sube un CSV con fecha y temp_c para comenzar.")
    st.stop()
try:
    data = demo_weather() if source == "Ejemplo" else load_weather(uploaded)
    summary = analyze_weather(data["temp_c"], data["precip_mm"], min(window, len(data)))
except (ValueError, pd.errors.ParserError, UnicodeDecodeError) as error:
    st.error(str(error))
    st.stop()

metrics = st.columns(5)
metrics[0].metric("Temperatura media", f"{summary.mean_temperature:.1f} °C")
metrics[1].metric("Mínima", f"{summary.minimum_temperature:.1f} °C")
metrics[2].metric("Máxima", f"{summary.maximum_temperature:.1f} °C")
metrics[3].metric("Precipitación total", f"{summary.total_precipitation:.1f} mm")
metrics[4].metric("Tendencia", f"{summary.trend_per_day:+.3f} °C/fila")

temperature_frame = data.assign(promedio_movil=summary.rolling_temperature).set_index("fecha")
st.subheader("Temperatura")
st.line_chart(temperature_frame[["temp_c", "promedio_movil"]], use_container_width=True)

monthly = data.assign(mes=data["fecha"].dt.to_period("M").astype(str)).groupby("mes").agg(
    temperatura_media=("temp_c", "mean"), precipitacion_total=("precip_mm", "sum")
)
left, right = st.columns(2)
left.subheader("Temperatura media por mes")
left.bar_chart(monthly[["temperatura_media"]])
right.subheader("Precipitación por mes")
right.bar_chart(monthly[["precipitacion_total"]])

with st.expander("Datos cargados"):
    st.dataframe(data, use_container_width=True, hide_index=True)
