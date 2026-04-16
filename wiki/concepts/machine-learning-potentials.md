---
title: Machine Learning Interatomic Potentials (MLIPs)
type: concept
tags: [MLIP, foundation-potential, PES, MD, force-field, interatomic-potential]
sources: [ko-2025-matgl]
last_updated: 2026-04-16
---

# Machine Learning Interatomic Potentials (MLIPs)

## What Are MLIPs?

MLIPs are ML models that map atomic positions and species to **potential energy surfaces (PESs)**: they predict the total energy of a configuration and its gradient (forces, stresses) with near-DFT accuracy at a fraction of the cost.

The key assumption: **total energy = sum of atomic contributions** (locality approximation). This makes MLIPs linear in system size and enables large-scale MD simulations.

---

## Why MLIPs Matter for AM

Classical force fields (EAM, MEAM) are fast but limited to specific alloy systems and don't handle complex chemistries. DFT is accurate but costs O(N³) — intractable beyond ~1000 atoms. MLIPs bridge this gap:

| Method | Cost | Accuracy | System size |
|--------|------|----------|-------------|
| DFT | Very high | Reference | ~100–500 atoms |
| Classical FF | Very low | Low | Any |
| MLIP | Low–medium | Near-DFT | 10³–10⁶ atoms |

For AM simulation: MLIPs enable **atomistic MD of melt pool solidification**, grain boundary migration, and defect formation at realistic timescales.

---

## Foundation Potentials (FPs)

**Foundation potentials** are MLIPs pre-trained on massive datasets covering the **entire periodic table** (or large portions of it). They are designed for **zero-shot** use across diverse chemistries.

### Available FPs (as of 2025)

| Model | Library | Training data | Elements | Key strength |
|-------|---------|--------------|----------|-------------|
| M3GNet | [[entities/software-tools#matgl|MatGL]] | MPF-2021.2.8 | 89 | First universal GNN FP |
| TensorNet-MatPES-PBE-v2025.1 | [[entities/software-tools#matgl|MatGL]] | MatPES (434k, 300K MD) | 89 | Best general-purpose FP in MatGL |
| CHGNet | [[entities/software-tools#matgl|MatGL]] | MPF-2021.2.8 + DFT mag. moments | 89 | Magnetic/charge-informed |
| MACE-MP-0 | MACE | MPF-2021.2.8 | 89 | Leading community FP |
| MACE-Large | MACE | Large multi-dataset | 89 | Highest accuracy |
| SevenNet-0 | SevenNet | — | — | Alternative universal FP |

**TensorNet-MatPES-PBE-v2025.1 vs. MACE-MP-0:**  
Both cover 89 elements and use ASE interfaces. MatGL benchmarks show TensorNet-MatPES comparable to or competitive with MACE-Large on torsion PES for organic molecules (0.9–1.2 eV barriers vs. 1.0–1.5 eV from MACE-Large). Direct head-to-head comparison on AM alloy systems is absent from literature.

---

## Training a Custom MLIP

The standard workflow (as in [[sources/ko-2025-matgl]]):

1. **Reference calculations:** DFT energies, forces, stresses on representative structures (static + MD snapshots)
2. **Dataset construction:** Convert to Pymatgen `Structure` objects → `MGLDataset` → train/val/test split
3. **Model setup:** Initialize GNN (TensorNet recommended) with `PotentialLightningModule`
4. **Training:** PyTorch Lightning `Trainer.fit()`; AMS optimizer, cosine annealing LR scheduler
5. **Validation:** Check energy, force, stress MAEs; compare relaxed structures to DFT via fingerprint distance

**DIRECT sampling** (from MatPES training): dimensionality-reduction method that covers configuration space efficiently with fewer MD snapshots — useful when AIMD is expensive.

---

## Performance Metrics

| Metric | Good threshold | Notes |
|--------|---------------|-------|
| Energy MAE | < 5 meV/atom | Training quality |
| Force MAE | < 0.1 eV/Å | Critical for dynamics |
| Stress MAE | < 0.5 GPa | For mechanical properties |
| Fingerprint distance | < 0.01 | Structural fidelity of relaxed configs |

---

## Known Limitations and Open Challenges

> ⚠️ **AM alloy validation gap:** Current FPs (M3GNet, TensorNet-MatPES, MACE-MP-0) are trained on equilibrium and near-equilibrium structures from the Materials Project and similar DFT databases. Far-from-equilibrium conditions in AM (10⁵–10⁷ K/s cooling, keyhole dynamics, metastable phase formation) are not represented in training data. Transferability to AM microstructure simulation is assumed but unvalidated. See [[sources/ko-2025-matgl#known-limitations]].

- **Long-range interactions:** Locality approximation breaks down for ionic systems (electrostatics, charge transfer). CHGNet partially addresses this via magnetic moments.
- **Noisy training data:** SO3Net was excluded from MPF-2021.2.8 benchmark due to high sensitivity to noisy DFT stresses.
- **Extrapolation:** MLIPs can fail catastrophically outside training distribution — uncertainty quantification (GP surrogates, ensembles) is an active research area.

---

## Related Pages
- [[concepts/graph-neural-networks]]
- [[entities/software-tools]]
