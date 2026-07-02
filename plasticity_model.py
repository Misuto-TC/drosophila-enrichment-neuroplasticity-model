"""
Plasticity Index model for environmental enrichment and negative geotaxis in Drosophila.

This script calculates literature-informed pathway indices used in the manuscript:
- dopamine_index: early transient response
- camp_pka_index: delayed sigmoidal response
- synaptic_index: progressive accumulation
- plasticity_index: weighted combined index
- predicted_climbing_success_raw: scaled behavioral prediction
- predicted_climbing_success_bounded: raw prediction bounded to 0-100%

The model is hypothesis-generating. It does not represent direct molecular measurements of
dopamine, cAMP/PKA, CREB, or synaptic remodeling.
"""

import csv
import math
from pathlib import Path

TIMES_H = [24, 48, 72, 96, 120, 144, 168, 192, 216, 240]

CONDITIONS = {
    "Control": 0,
    "Low": 1,
    "Medium": 2,
    "High": 3,
}


def dopamine_index(enrichment_level: int, time_h: float) -> float:
    """Early transient dopamine-related index."""
    return enrichment_level * math.exp(-((time_h - 24) ** 2) / (2 * (24 ** 2)))


def camp_pka_index(enrichment_level: int, time_h: float) -> float:
    """Delayed cAMP/PKA-related index."""
    return enrichment_level / (1 + math.exp(-(time_h - 72) / 24))


def synaptic_index(enrichment_level: int, time_h: float) -> float:
    """Progressive synaptic remodeling-related index."""
    return enrichment_level * (1 + (time_h / 240) ** 1.5)


def plasticity_index(enrichment_level: int, time_h: float) -> float:
    """Weighted combined Plasticity Index."""
    return (
        0.30 * dopamine_index(enrichment_level, time_h)
        + 0.35 * camp_pka_index(enrichment_level, time_h)
        + 0.35 * synaptic_index(enrichment_level, time_h)
    )


def predicted_climbing_success_raw(enrichment_level: int, time_h: float) -> float:
    """Raw scaled climbing success prediction."""
    return 15.2 + 38.7 * plasticity_index(enrichment_level, time_h)


def predicted_climbing_success_bounded(enrichment_level: int, time_h: float) -> float:
    """Prediction bounded to the biological range of 0-100%."""
    raw_prediction = predicted_climbing_success_raw(enrichment_level, time_h)
    return max(0, min(100, raw_prediction))


def main() -> None:
    rows = []

    max_pi = max(
        plasticity_index(level, time_h)
        for level in CONDITIONS.values()
        for time_h in TIMES_H
    )

    for time_h in TIMES_H:
        for condition, enrichment_level in CONDITIONS.items():
            pi = plasticity_index(enrichment_level, time_h)
            normalized_pi = pi / max_pi if max_pi else 0

            rows.append({
                "time_h": time_h,
                "condition": condition,
                "enrichment_level": enrichment_level,
                "dopamine_index": dopamine_index(enrichment_level, time_h),
                "camp_pka_index": camp_pka_index(enrichment_level, time_h),
                "synaptic_index": synaptic_index(enrichment_level, time_h),
                "plasticity_index": pi,
                "normalized_plasticity_index": normalized_pi,
                "predicted_climbing_success_raw": predicted_climbing_success_raw(enrichment_level, time_h),
                "predicted_climbing_success_bounded": predicted_climbing_success_bounded(enrichment_level, time_h),
            })

    output_path = Path("model_outputs.csv")
    with output_path.open("w", newline="") as f:
        fieldnames = [
            "time_h",
            "condition",
            "enrichment_level",
            "dopamine_index",
            "camp_pka_index",
            "synaptic_index",
            "plasticity_index",
            "normalized_plasticity_index",
            "predicted_climbing_success_raw",
            "predicted_climbing_success_bounded",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Saved model outputs to {output_path}")


if __name__ == "__main__":
    main()
