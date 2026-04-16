---
title: "MatGL: Materials Graph Library (Ko et al., 2025)"
type: source
tags: [GNN, MLIP, foundation-potential, software, matgl, graph-neural-network]
sources: [2025 - Ko et al. - Materials Graph Library (MatGL), an open.pdf]
last_updated: 2026-04-16
---

# MatGL: Materials Graph Library (Ko et al., 2025)

**Full title:** Materials Graph Library (MatGL), an open-source graph deep learning library for materials science and chemistry  
**Authors:** Tsz Wai Ko, Bowen Deng, Marcel Nassar, Luis Barroso-Luque, Runze Liu, Ji Qi, Atul C. Thakur, Adesh Rohan Mishra, Elliott Liu, Gerbrand Ceder, Santiago Miret, Shyue Ping Ong  
**Journal:** npj Computational Materials, 2025, 11:253  
**DOI:** 10.1038/s41524-025-01742-y  
**Institutions:** UC San Diego; UC Berkeley / Lawrence Berkeley National Lab; Intel Labs  

---

## Summary

[[concepts/graph-neural-networks|MatGL]] is an open-source Python library for graph deep learning in materials science, built on the Deep Graph Library (DGL) and [[entities/software-tools#pymatgen|Pymatgen]]. It provides a unified, extensible framework for both **property prediction models** and **machine learning interatomic potentials (MLIPs)**, integrated with PyTorch Lightning for training and [[entities/software-tools#ase|ASE]]/[[entities/software-tools#lammps|LAMMPS]] for simulation.

---

## Architecture: Four Components

| Component | Python package | Purpose |
|-----------|---------------|---------|
| Data pipeline | `matgl.data` | `MGLDataset` + `MGLDataLoader`; converts Pymatgen `Structure`/`Molecule` to DGL graphs |
| Model architectures | `matgl.models` + `matgl.layers` | 5 GNN models (see below); all subclass `MatGLModel` |
| Training | `matgl.util.training` | PyTorch Lightning `ModelLightningModule` + `PotentialLightningModule` |
| Simulation interfaces | `matgl.apps.pes` + CLI | ASE `PESCalculator`, `Relaxer`, `MolecularDynamics`; LAMMPS via AdvanceSoft |

---

## GNN Models Implemented

| Model | Symmetry | Prop. Pred. | MLIP | Notes |
|-------|----------|-------------|------|-------|
| MEGNet | Invariant | ✓ | — | GNN with global state vector; fastest inference |
| M3GNet | Invariant | ✓ | ✓ | Extends MEGNet with 3-body interactions; first published FP from Ong group |
| CHGNet | Invariant | — | ✓ | Incorporates DFT magnetic moments; outperforms M3GNet on MPF-2021.2.8 |
| TensorNet | Equivariant | ✓ | ✓ | O(3)-equivariant via Cartesian tensors; best accuracy/speed tradeoff |
| SO3Net | Equivariant | ✓ | ✓ | SO(3)-equivariant via spherical harmonics; highest accuracy, slowest |

All models expose a `predict_structure(structure)` convenience method.

---

## Pre-trained Foundation Potentials

Pre-trained FPs covering the **full periodic table** are provided:
- **TensorNet-MatPES-PBE-v2025.1** — trained on MatPES dataset (434k structures, 89 elements, 300K MD snapshots via DIRECT sampling). Best general-purpose FP for periodic systems.
- **M3GNet universal** — first-generation FP, widely cited
- **CHGNet universal** — charge-informed; useful for ionic/magnetic systems

All FPs expose an ASE `PESCalculator` interface for drop-in MD/relaxation use.

---

## Benchmark Performance

### Property prediction (QM9 organic molecules)
| Model | Free energy MAE (eV) | Polarizability MAE (a₀³) |
|-------|---------------------|--------------------------|
| MEGNet | 0.037 | 0.079–0.114 |
| M3GNet | 0.025 | 0.087 |
| TensorNet | 0.027 | 0.064–0.083 |
| SO3Net | 0.027 | 0.059–0.069 |

### Property prediction (Matbench crystals)
| Model | E_form MAE (eV/atom) | K_VRH MAE (log GPa) |
|-------|---------------------|---------------------|
| MEGNet | 0.037 | 0.075 |
| M3GNet | 0.020 | 0.065 |
| TensorNet | 0.024 | 0.060 |
| SO3Net | 0.022 | 0.060 |

MEGNet consistently highest errors. TensorNet and SO3Net comparable; equivariant models outperform invariant overall.

### PES/MLIP (ANI-1x organic conformers)
| Model | Energy MAE (meV/atom) | Force MAE (eV/Å) |
|-------|----------------------|------------------|
| M3GNet | 4.59 | 0.092 |
| M3GNet-TL (transfer from ANI-1x) | 3.97 | 0.082 |
| TensorNet | 4.45 | 0.088 |
| SO3Net | **2.28** | **0.046** |

Transfer learning (M3GNet-TL) reduces MAE 10–15% vs. training from scratch.

### Simulation speed (single Nvidia RTX A6000 GPU)
- **MEGNet**: fastest property prediction (~12s for 6500 structures)
- **TensorNet**: fastest MD for small–medium systems; most efficient across all cases in LAMMPS NPT
- **SO3Net**: significantly slower for >100 atoms (NVT water clusters)
- **CHGNet**: highest computational cost in LAMMPS NPT due to larger cutoff for triplet interactions

---

## Key Findings

1. **Equivariant > invariant** for forces and PES: TensorNet and SO3Net outperform MEGNet and M3GNet by 10–40% on energy MAE; SO3Net lowest force MAE.
2. **TensorNet** is the practical choice: best accuracy/speed tradeoff for both property prediction and MLIP; avoids costly three-body tensor products.
3. **Transfer learning** is effective: pre-trained embedding from ANI-1x embedded layer provides consistent gains.
4. **CHGNet** beats M3GNet for energies/forces/stresses on crystalline systems (MPF-2021.2.8) due to magnetic moment message passing.
5. **MatGL FPs are viable** for surface energies, phonon dispersion, heat capacity, and amorphous structure properties — tested against SNAP, GAP, DeepMD.

---

## Relevance to autoMD / AlloyGen

- **Drop-in MACE-MP-0 alternative**: TensorNet-MatPES-PBE-v2025.1 is a full-periodic-table FP with direct ASE and LAMMPS interfaces, matching the planned autoMD architecture. Benchmarks show competitive accuracy with MACE-Large on torsion PES.
- **API compatibility**: `PESCalculator` is a standard ASE `Calculator` subclass — no integration friction.
- **Fine-tuning supported**: DIRECT sampling + MatGL fine-tuning workflow documented in GitHub tutorials; relevant if AM alloy-specific training data becomes available.

---

## Known Limitations

> ⚠️ **AM alloy gap:** All benchmarks target organic molecules (QM9, ANI-1x, COMP6) or generic inorganic crystals (Matbench, MPF-2021.2.8, MatPES). No validation on AM-relevant alloy systems (Ti64, IN718, AlSi10Mg) or far-from-equilibrium conditions (rapid solidification, keyhole dynamics). Transferability to AM microstructures is assumed but unverified.

---

## Related Pages
- [[concepts/graph-neural-networks]]
- [[concepts/machine-learning-potentials]]
- [[entities/software-tools]]
- [[entities/researchers#ong-group]]
