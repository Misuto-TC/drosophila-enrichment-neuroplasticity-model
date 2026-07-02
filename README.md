# Drosophila environmental enrichment negative geotaxis model

This repository contains code and data used for the computational Plasticity Index model described in the manuscript **"Dose-dependent effects of environmental enrichment on Drosophila negative geotaxis."**

## Purpose

The model was used as a hypothesis-generating framework to test whether literature-informed pathway dynamics could reproduce the general enrichment-dependent ordering observed in negative geotaxis performance.

The modeled pathway indices represent:
- early transient dopamine-related signaling
- delayed cAMP/PKA-related signaling
- progressive synaptic remodeling-related change

These are model-generated indices only. They do **not** represent direct molecular measurements of dopamine, cAMP/PKA, CREB, or synaptic remodeling.

## Files

- `plasticity_model.py` — Python script used to calculate pathway indices, Plasticity Index values, normalized Plasticity Index values, and predicted climbing success.
- `observed_climbing_data.csv` — Observed mean climbing success values used in the manuscript.
- `model_outputs.csv` — Model-generated output values.
- `requirements.txt` — Python package requirements. The model uses only the Python standard library.

## How to run

Install Python 3, then run:

```bash
python plasticity_model.py
```

This will generate `model_outputs.csv`.

## Model equations

Dopamine index:

```text
DA(I,t) = I * exp(-((t - 24)^2) / (2 * 24^2))
```

cAMP/PKA index:

```text
cAMP(I,t) = I / (1 + exp(-(t - 72) / 24))
```

Synaptic remodeling index:

```text
Syn(I,t) = I * [1 + (t / 240)^1.5]
```

Plasticity Index:

```text
Plasticity(I,t) = 0.30*DA(I,t) + 0.35*cAMP(I,t) + 0.35*Syn(I,t)
```

Predicted climbing success:

```text
Predicted climbing success (%) = 15.2 + 38.7*Plasticity(I,t)
```

Predicted climbing success values are bounded to the biological range of 0-100% in the script.
