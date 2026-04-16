---
title: AM Processes
type: entity
tags: [L-PBF, SLM, EBM, DED, WAAM, binder-jet]
sources: []
last_updated: 2026-04-16
---

# Additive Manufacturing Processes

## Powder Bed Fusion (PBF)

### L-PBF / SLM (Laser Powder Bed Fusion)
- Laser scans over a powder layer (~20-60 μm); melts and solidifies line-by-line.
- VED = P / (v · h · t) where P=power, v=scan speed, h=hatch spacing, t=layer thickness.
- Typical defects: keyhole porosity (high VED), lack-of-fusion (low VED), balling, cracking.
- Cooling rates: 10⁵–10⁷ K/s → fine grain, metastable phases.

### EBM / EB-PBF (Electron Beam Melting)
- Electron beam in high vacuum. Higher build temperature (pre-heating ~700°C for Ti64).
- Less residual stress than L-PBF. Rougher surface finish.

## Directed Energy Deposition (DED)
- Laser or electron beam melts powder/wire as it is deposited.
- Higher deposition rate, lower resolution than PBF.
- Sub-types: LMD (laser metal deposition), LENS, WAAM (wire arc AM).

## Binder Jetting
- Binder printed onto powder bed; sintered post-process. No melt pool during build.
- No residual stress from printing; shrinkage (~15-20%) during sintering.

> This page is seeded from domain knowledge. Update with `[[sources/...]]` citations on ingest.
