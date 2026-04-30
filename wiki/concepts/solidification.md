---
title: Solidification
type: concept
tags: [solidification, microstructure, grain, columnar, equiaxed, CET]
sources: []
last_updated: 2026-04-30
---

# Solidification in AM

## Overview
AM solidification is far-from-equilibrium: cooling rates 10⁵–10⁷ K/s (L-PBF) produce 
fine microstructures, metastable phases, and strong crystallographic textures.

## Key Phenomena

### Columnar Grain Growth
- Epitaxial growth along build direction (∥ to thermal gradient).
- Common in L-PBF of SS316L, IN718, Ti64.
- Results in anisotropic mechanical properties (build direction vs. transverse).

### Columnar-to-Equiaxed Transition (CET)
- Equiaxed grains nucleate ahead of solidification front when constitutional supercooling exceeds threshold.
- Promoted by: high nucleant density, lower thermal gradient G, higher solidification velocity V.
- Hunt criterion: CET when G/V^0.5 < threshold.

### Melt Pool Dynamics
- Marangoni flow (surface tension gradient) drives convection in melt pool.
- Keyhole mode: deep, narrow pool at high energy density → vapor cavity → porosity.
- Conduction mode: shallow, wide pool at low energy density.

## Relevant Properties
- G (thermal gradient, K/m), R (solidification rate, m/s), G·R = cooling rate
- Undercooling ΔT drives nucleation; higher ΔT → finer grain size

## Related Pages
- [[entities/alloy-systems]] — martensite in Ti64, Laves in IN718, columnar grains in SS316L
- [[entities/am-processes]] — L-PBF/EBM melt pool modes, VED, cooling rate regimes
- [[concepts/microstructure]] — resulting phases and defects from solidification conditions

> Update with citations as sources are ingested.
