---
title: Software Tools
type: entity
tags: [software, tools, GNN, simulation, data, library]
sources: [ko-2025-matgl]
last_updated: 2026-04-16
---

# Software Tools in Computational Materials Science

## Graph Deep Learning / MLIP Libraries

### MatGL
- **Full name:** Materials Graph Library
- **Authors/Group:** [[researchers#ong-group|Ong group]] (UCSD) + [[researchers#ceder-group|Ceder group]] (Berkeley)
- **Repo:** https://github.com/materialsvirtuallab/matgl
- **Built on:** DGL (Deep Graph Library), Pymatgen, PyTorch Lightning
- **Purpose:** Unified framework for GNN property models and MLIPs; "batteries included" with pre-trained foundation potentials
- **Models:** MEGNet, M3GNet, CHGNet, TensorNet, SO3Net
- **Simulation interfaces:** ASE, LAMMPS
- **Status (2025):** Production; integrated into MatSciML and Amsterdam Modeling Suite
- See: [[sources/ko-2025-matgl]]

### MACE
- **Authors/Group:** Batatia et al. (Cambridge / DeepMind)
- **Purpose:** Higher-order equivariant message passing; MACE-MP-0 / MACE-Large are leading general-purpose foundation potentials
- **Status:** Planned MLIP for [[autoMD]] (alternative to MatGL FPs)

### SevenNet-0
- **Purpose:** Universal MLIP; considered alongside MACE-MP-0 for [[autoMD]]

### Nequip
- **Authors/Group:** Batzner et al.
- **Purpose:** E(3)-equivariant GNNs; precursor architecture to MACE

---

## Simulation Environments

### ASE
- **Full name:** Atomic Simulation Environment
- **Purpose:** Python library for atomistic simulations; standard calculator interface used by MatGL `PESCalculator`, MACE, and most MLIPs
- **Key classes used with MatGL:** `PESCalculator`, `Relaxer`, `MolecularDynamics`

### LAMMPS
- **Full name:** Large-scale Atomic/Molecular Massively Parallel Simulator
- **Purpose:** High-performance classical and ML MD; MatGL integrates via AdvanceSoft interface
- **Advantage over ASE:** Scales to tens of thousands of atoms; better parallelism for large-scale AM simulations

---

## Materials Data / Structure Libraries

### Pymatgen (PMG)
- **Full name:** Python Materials Genomics
- **Authors/Group:** Ong group
- **Purpose:** Materials data structures (`Structure`, `Molecule`), phase diagrams, VASP/POSCAR I/O, periodic table database
- **Role in MatGL:** Core input format; `Structure` objects are converted to DGL graphs by `GraphConverter`

### DGL
- **Full name:** Deep Graph Library
- **Purpose:** General-purpose graph deep learning framework; MatGL's graph backend
- **Advantage over PyTorch-Geometric:** Better memory efficiency and speed, especially for large batches

---

## Training / Reference Datasets

| Dataset | Contents | Size | Used for |
|---------|----------|------|---------|
| QM9 | Organic molecules (H,C,N,O,F), DFT/B3LYP | 130k | Property prediction benchmark |
| Matbench | Bulk crystals, DFT/PBE | 132–10k | Property prediction benchmark |
| ANI-1x | Organic conformers, DFT/wB97x | ~5M | MLIP training/benchmark |
| MPF-2021.2.8 | Crystal relaxation trajectories (89 elements) | 185k | MLIP benchmark |
| MatPES-PBE-v2025.1 | 300K MD snapshots, DIRECT sampling (89 elements) | 434k | Foundation potential training |

> ⚠️ **AM alloy gap:** None of these datasets specifically target AM alloy systems or far-from-equilibrium solidification conditions. See [[sources/ko-2025-matgl#known-limitations]].
