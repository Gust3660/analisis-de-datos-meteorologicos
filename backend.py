"""Resumen y tendencias sencillas para series meteorológicas."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class WeatherSummary:
    mean_temperature: float
    minimum_temperature: float
    maximum_temperature: float
    total_precipitation: float
    trend_per_day: float
    rolling_temperature: np.ndarray


def analyze_weather(temperatures: list[float] | np.ndarray, precipitation: list[float] | np.ndarray, window: int = 7) -> WeatherSummary:
    temp = np.asarray(temperatures, dtype=float)
    rain = np.asarray(precipitation, dtype=float)
    if temp.ndim != 1 or temp.size < 2 or rain.shape != temp.shape:
        raise ValueError("Se requieren al menos dos temperaturas y una precipitación por fecha.")
    if not np.all(np.isfinite(temp)) or not np.all(np.isfinite(rain)) or np.any(rain < 0):
        raise ValueError("Los datos deben ser finitos y la precipitación no puede ser negativa.")
    if window < 1:
        raise ValueError("La ventana móvil debe ser positiva.")
    x = np.arange(temp.size, dtype=float)
    slope = float(np.polyfit(x, temp, 1)[0])
    rolling = np.convolve(temp, np.ones(window) / window, mode="valid")
    prefix = np.full(window - 1, np.nan)
    return WeatherSummary(
        mean_temperature=float(np.mean(temp)),
        minimum_temperature=float(np.min(temp)),
        maximum_temperature=float(np.max(temp)),
        total_precipitation=float(np.sum(rain)),
        trend_per_day=slope,
        rolling_temperature=np.concatenate((prefix, rolling)),
    )
