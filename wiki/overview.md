---
title: Overview
type: synthesis
tags: [overview, synthesis, AM, HEA, structural-alloys, MLIP, GNN, computational]
sources: [ko-2025-matgl]
last_updated: 2026-04-16
---

# Field Overview: Metal AM, Structural Alloys, and Computational Tools

## Synthesis (as of 2026-04-16)

This wiki covers the intersection of **metal additive manufacturing** (AM), **structural alloy development**, and **computational materials science tools**, with focus on:

### Experimental / Processing
- Process–microstructure–property relationships in L-PBF, EBM, DED
- Alloy families: Ti64, IN718, SS316L, AlSi10Mg, HEA/MPEA
- Emerging themes: alloy design for AM, in-situ monitoring, qualification

### Computational / Simulation
- **Machine learning interatomic potentials (MLIPs):** Foundation potentials (M3GNet, TensorNet-MatPES, MACE-MP-0, SevenNet-0) now cover the full periodic table and support ASE/LAMMPS MD at near-DFT accuracy. The Ong group's [[entities/software-tools#matgl|MatGL]] library is the primary open-source framework for training and deploying these models.
- **Graph neural networks:** Equivariant architectures (TensorNet, SO3Net) outperform invariant ones (MEGNet, M3GNet) for force prediction by 10–40%. TensorNet is the current recommended default for MLIP applications.
- **Simulation gap:** No existing FP has been validated specifically for AM alloy systems or far-from-equilibrium solidification. This is an open opportunity.

## Open Questions

- Can universal FPs (TensorNet-MatPES, MACE-MP-0) reproduce solidification behavior in AM alloys (e.g., Ti64, IN718) without fine-tuning?
- What training data is needed to fine-tune a general FP for AM-relevant conditions (10⁵–10⁷ K/s cooling rates)?

## Key Tensions in the Literature

> ⚠️ **MACE-MP-0 vs. MatGL FPs:** Both claim to be general-purpose full-periodic-table potentials. MatGL benchmarks show TensorNet-MatPES competitive with MACE-Large on organic PES. No head-to-head comparison on metallic alloys has been published (as of 2025).

> This page evolves with every ingest. It should reflect the current state of the 
> accumulated knowledge, not just the last paper read.
