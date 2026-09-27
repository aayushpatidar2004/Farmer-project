"""
Rule-based Crop Recommendation Engine using Pandas and NumPy.

DISCLAIMER: Recommendations are for informational purposes only.
Farmers should consult local agricultural experts before making
important farming decisions. This is NOT a scientifically certified
recommendation system.
"""
import numpy as np

try:
    import pandas as pd
except Exception:  # pragma: no cover - fallback for restricted environments
    pd = None


# ---------------------------------------------------------------------------
# Crop requirement reference data
# ---------------------------------------------------------------------------
_RAW_CROP_DATA = [
    {
        "crop": "Rice",
        "soil_types": ["alluvial", "clay", "loamy"],
        "ph_min": 5.5, "ph_max": 7.0,
        "n_min": 80, "n_max": 280,
        "p_min": 20, "p_max": 60,
        "k_min": 40, "k_max": 120,
        "temp_min": 20, "temp_max": 35,
        "rain_min": 150, "rain_max": 300,
        "hum_min": 60, "hum_max": 90,
        "description": "Staple cereal requiring flooded or waterlogged fields.",
        "season": "Kharif (Jun – Oct)",
        "water": "High",
        "category": "cereal",
    },
    {
        "crop": "Wheat",
        "soil_types": ["alluvial", "loamy", "clay"],
        "ph_min": 6.0, "ph_max": 7.5,
        "n_min": 60, "n_max": 200,
        "p_min": 15, "p_max": 50,
        "k_min": 30, "k_max": 100,
        "temp_min": 10, "temp_max": 25,
        "rain_min": 50, "rain_max": 100,
        "hum_min": 40, "hum_max": 70,
        "description": "Major rabi crop grown in cool, dry conditions.",
        "season": "Rabi (Nov – Apr)",
        "water": "Moderate",
        "category": "cereal",
    },
    {
        "crop": "Maize",
        "soil_types": ["alluvial", "loamy", "red", "sandy"],
        "ph_min": 5.5, "ph_max": 7.5,
        "n_min": 60, "n_max": 200,
        "p_min": 15, "p_max": 50,
        "k_min": 30, "k_max": 100,
        "temp_min": 18, "temp_max": 35,
        "rain_min": 60, "rain_max": 110,
        "hum_min": 50, "hum_max": 80,
        "description": "Versatile cereal for food, feed, and industrial use.",
        "season": "Kharif (Jun – Sep)",
        "water": "Moderate",
        "category": "cereal",
    },
    {
        "crop": "Cotton",
        "soil_types": ["black", "alluvial", "loamy"],
        "ph_min": 6.0, "ph_max": 8.0,
        "n_min": 50, "n_max": 180,
        "p_min": 20, "p_max": 60,
        "k_min": 40, "k_max": 120,
        "temp_min": 20, "temp_max": 40,
        "rain_min": 60, "rain_max": 110,
        "hum_min": 40, "hum_max": 70,
        "description": "Important cash crop for the textile industry.",
        "season": "Kharif (May – Dec)",
        "water": "Moderate",
        "category": "cash_crop",
    },
    {
        "crop": "Sugarcane",
        "soil_types": ["alluvial", "loamy", "black"],
        "ph_min": 6.0, "ph_max": 7.5,
        "n_min": 80, "n_max": 280,
        "p_min": 30, "p_max": 80,
        "k_min": 60, "k_max": 180,
        "temp_min": 20, "temp_max": 38,
        "rain_min": 150, "rain_max": 250,
        "hum_min": 60, "hum_max": 90,
        "description": "Major cash crop used for sugar, jaggery, and ethanol.",
        "season": "Feb – Mar planting, harvest after 10–12 months",
        "water": "High",
        "category": "cash_crop",
    },
    {
        "crop": "Groundnut",
        "soil_types": ["sandy", "loamy", "red"],
        "ph_min": 6.0, "ph_max": 7.0,
        "n_min": 10, "n_max": 60,
        "p_min": 20, "p_max": 60,
        "k_min": 20, "k_max": 80,
        "temp_min": 20, "temp_max": 35,
        "rain_min": 50, "rain_max": 130,
        "hum_min": 40, "hum_max": 70,
        "description": "Oilseed and protein-rich food crop suited to light soils.",
        "season": "Kharif (Jun – Sep)",
        "water": "Low",
        "category": "oilseed",
    },
    {
        "crop": "Tomato",
        "soil_types": ["alluvial", "loamy", "sandy"],
        "ph_min": 6.0, "ph_max": 7.0,
        "n_min": 60, "n_max": 200,
        "p_min": 30, "p_max": 80,
        "k_min": 40, "k_max": 120,
        "temp_min": 18, "temp_max": 32,
        "rain_min": 60, "rain_max": 120,
        "hum_min": 50, "hum_max": 80,
        "description": "High-value vegetable crop with year-round demand.",
        "season": "Year-round (avoid frost)",
        "water": "Moderate",
        "category": "vegetable",
    },
    {
        "crop": "Potato",
        "soil_types": ["alluvial", "loamy", "sandy"],
        "ph_min": 5.0, "ph_max": 6.5,
        "n_min": 60, "n_max": 180,
        "p_min": 30, "p_max": 80,
        "k_min": 60, "k_max": 150,
        "temp_min": 10, "temp_max": 25,
        "rain_min": 50, "rain_max": 100,
        "hum_min": 40, "hum_max": 70,
        "description": "Widely consumed root vegetable. Thrives in cool weather.",
        "season": "Rabi (Oct – Mar)",
        "water": "Moderate",
        "category": "vegetable",
    },
    {
        "crop": "Chickpea",
        "soil_types": ["alluvial", "loamy", "black", "sandy"],
        "ph_min": 6.0, "ph_max": 8.5,
        "n_min": 10, "n_max": 60,
        "p_min": 20, "p_max": 60,
        "k_min": 20, "k_max": 80,
        "temp_min": 10, "temp_max": 30,
        "rain_min": 30, "rain_max": 80,
        "hum_min": 30, "hum_max": 60,
        "description": "Drought-tolerant legume and important protein source.",
        "season": "Rabi (Oct – Apr)",
        "water": "Low",
        "category": "legume",
    },
    {
        "crop": "Soybean",
        "soil_types": ["alluvial", "loamy", "black"],
        "ph_min": 6.0, "ph_max": 7.5,
        "n_min": 20, "n_max": 80,
        "p_min": 20, "p_max": 60,
        "k_min": 30, "k_max": 100,
        "temp_min": 18, "temp_max": 35,
        "rain_min": 60, "rain_max": 120,
        "hum_min": 50, "hum_max": 80,
        "description": "High-protein oilseed crop with multiple industrial uses.",
        "season": "Kharif (Jun – Oct)",
        "water": "Moderate",
        "category": "oilseed",
    },
    {
        "crop": "Onion",
        "soil_types": ["alluvial", "loamy", "sandy"],
        "ph_min": 6.0, "ph_max": 7.5,
        "n_min": 50, "n_max": 150,
        "p_min": 30, "p_max": 80,
        "k_min": 40, "k_max": 120,
        "temp_min": 13, "temp_max": 30,
        "rain_min": 40, "rain_max": 80,
        "hum_min": 40, "hum_max": 70,
        "description": "Key vegetable and spice crop with stable market demand.",
        "season": "Kharif / Rabi",
        "water": "Moderate",
        "category": "vegetable",
    },
    {
        "crop": "Bajra (Pearl Millet)",
        "soil_types": ["sandy", "loamy", "red"],
        "ph_min": 6.0, "ph_max": 7.5,
        "n_min": 30, "n_max": 120,
        "p_min": 10, "p_max": 40,
        "k_min": 20, "k_max": 80,
        "temp_min": 22, "temp_max": 40,
        "rain_min": 30, "rain_max": 80,
        "hum_min": 30, "hum_max": 60,
        "description": "Extremely drought-tolerant cereal suited to arid and semi-arid regions.",
        "season": "Kharif (Jun – Sep)",
        "water": "Low",
        "category": "cereal",
    },
    {
        "crop": "Jowar (Sorghum)",
        "soil_types": ["alluvial", "loamy", "black", "red"],
        "ph_min": 5.5, "ph_max": 8.0,
        "n_min": 30, "n_max": 120,
        "p_min": 10, "p_max": 40,
        "k_min": 20, "k_max": 80,
        "temp_min": 18, "temp_max": 38,
        "rain_min": 40, "rain_max": 100,
        "hum_min": 30, "hum_max": 70,
        "description": "Drought-tolerant cereal suitable for both food and fodder.",
        "season": "Kharif and Rabi",
        "water": "Low",
        "category": "cereal",
    },
]

CROP_DF = pd.DataFrame(_RAW_CROP_DATA) if pd is not None else _RAW_CROP_DATA


# ---------------------------------------------------------------------------
# Scoring helpers
# ---------------------------------------------------------------------------

def _range_score(value: float, vmin: float, vmax: float, sensitivity: float = 30.0) -> float:
    """
    Score a numeric value against a [vmin, vmax] range using NumPy.
    Returns 100 if within range, decaying linearly outside.
    """
    span = max(vmax - vmin, 1.0)
    v = np.float64(value)
    lo = np.float64(vmin)
    hi = np.float64(vmax)

    if lo <= v <= hi:
        return 100.0
    deviation = np.minimum(np.abs(v - lo), np.abs(v - hi))
    score = np.maximum(0.0, 100.0 - (deviation / span) * sensitivity)
    return float(score)


def _row_value(row, key, default=None):
    if isinstance(row, dict):
        return row.get(key, default)
    return row.get(key, default)


def _score_crop(row, inp: dict) -> float:
    """Compute a weighted match score (0–100) for one crop."""
    scores = np.array([
        _range_score(inp["ph"], _row_value(row, "ph_min"), _row_value(row, "ph_max"), 40),
        _range_score(inp["nitrogen"], _row_value(row, "n_min"), _row_value(row, "n_max")),
        _range_score(inp["phosphorus"], _row_value(row, "p_min"), _row_value(row, "p_max")),
        _range_score(inp["potassium"], _row_value(row, "k_min"), _row_value(row, "k_max")),
    ])
    weights = np.array([2.5, 1.5, 1.0, 1.0])

    if inp.get("temperature") is not None:
        scores = np.append(scores, _range_score(inp["temperature"], _row_value(row, "temp_min"), _row_value(row, "temp_max"), 25))
        weights = np.append(weights, 1.5)

    if inp.get("rainfall") is not None:
        scores = np.append(scores, _range_score(inp["rainfall"], _row_value(row, "rain_min"), _row_value(row, "rain_max")))
        weights = np.append(weights, 1.0)

    if inp.get("humidity") is not None:
        scores = np.append(scores, _range_score(inp["humidity"], _row_value(row, "hum_min"), _row_value(row, "hum_max")))
        weights = np.append(weights, 0.5)

    # Soil-type bonus (add to score pool)
    soil = inp.get("soil_type", "")
    soil_types = _row_value(row, "soil_types", [])
    if soil and soil in soil_types:
        scores = np.append(scores, np.float64(100.0))
        weights = np.append(weights, 2.5)
    elif soil:
        scores = np.append(scores, np.float64(30.0))
        weights = np.append(weights, 2.5)

    return float(np.average(scores, weights=weights))


def _match_quality(score: float) -> str:
    if score >= 80:
        return "Excellent"
    elif score >= 65:
        return "Good"
    elif score >= 45:
        return "Moderate"
    else:
        return "Low"


def _build_reasons(row, inp: dict) -> list[str]:
    reasons = []
    ph = inp["ph"]
    if _row_value(row, "ph_min") <= ph <= _row_value(row, "ph_max"):
        reasons.append(f"Soil pH {ph} is ideal (optimal: {_row_value(row, 'ph_min')}–{_row_value(row, 'ph_max')})")
    soil = inp.get("soil_type", "")
    soil_types = _row_value(row, "soil_types", [])
    if soil and soil in soil_types:
        reasons.append(f"{soil.title()} soil is well-suited for {_row_value(row, 'crop')}")
    temp = inp.get("temperature")
    if temp is not None and _row_value(row, "temp_min") <= temp <= _row_value(row, "temp_max"):
        reasons.append(f"Temperature {temp}°C is within optimal range ({_row_value(row, 'temp_min')}–{_row_value(row, 'temp_max')}°C)")
    rain = inp.get("rainfall")
    if rain is not None and _row_value(row, "rain_min") <= rain <= _row_value(row, "rain_max"):
        reasons.append(f"Rainfall {rain} mm/month suits {_row_value(row, 'crop')} requirements")
    if not reasons:
        reasons.append(f"Partial nutrient compatibility with {_row_value(row, 'crop')}")
    return reasons


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def get_recommendations(inputs: dict, top_n: int = 5) -> list[dict]:
    """
    Generate crop recommendations ranked by match score.

    Args:
        inputs (dict): Keys — soil_type, ph, nitrogen, phosphorus, potassium,
                       and optionally: temperature, rainfall, humidity.
        top_n (int): Number of top crops to return.

    Returns:
        list[dict]: Sorted recommendations with score, reasons, and metadata.
    """
    if pd is not None and isinstance(CROP_DF, pd.DataFrame):
        df = CROP_DF.copy()
        df["score"] = df.apply(lambda r: _score_crop(r, inputs), axis=1)
        top = df.nlargest(top_n, "score").reset_index(drop=True)

        results = []
        for _, row in top.iterrows():
            results.append({
                "crop": row["crop"],
                "score": round(row["score"], 1),
                "match_quality": _match_quality(row["score"]),
                "description": row["description"],
                "season": row["season"],
                "water_requirement": row["water"],
                "category": row["category"],
                "suitable_soil_types": ", ".join(s.title() for s in row["soil_types"]),
                "ph_range": f"{row['ph_min']} – {row['ph_max']}",
                "reasons": _build_reasons(row, inputs),
            })
        return results

    scored = []
    for row in CROP_DF:
        score = _score_crop(row, inputs)
        scored.append({
            "crop": row["crop"],
            "score": score,
            "description": row["description"],
            "season": row["season"],
            "water_requirement": row["water"],
            "category": row["category"],
            "soil_types": row["soil_types"],
            "ph_min": row["ph_min"],
            "ph_max": row["ph_max"],
        })

    scored = sorted(scored, key=lambda x: x["score"], reverse=True)[:top_n]
    results = []
    for row in scored:
        results.append({
            "crop": row["crop"],
            "score": round(row["score"], 1),
            "match_quality": _match_quality(row["score"]),
            "description": row["description"],
            "season": row["season"],
            "water_requirement": row["water_requirement"],
            "category": row["category"],
            "suitable_soil_types": ", ".join(s.title() for s in row["soil_types"]),
            "ph_range": f"{row['ph_min']} – {row['ph_max']}",
            "reasons": _build_reasons(row, inputs),
        })
    return results
