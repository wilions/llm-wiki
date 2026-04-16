---
title: Graph Neural Networks for Materials
type: concept
tags: [GNN, graph-learning, message-passing, invariant, equivariant, deep-learning]
sources: [ko-2025-matgl]
last_updated: 2026-04-16
---

# Graph Neural Networks for Materials Science

## What Makes GNNs Natural for Atomistic Systems

Atoms are nodes; bonds (within a cutoff radius) are edges. This graph representation encodes the **local chemical environment** of each atom in a physically meaningful way. Unlike descriptor-based MLIPs (SNAP, GAP), GNNs learn their own representations end-to-end and have a distinct advantage for **chemically complex systems** (HEAs, multi-component alloys).

---

## Architecture: Message Passing / Graph Convolution

A GNN processes a graph through **L layers** of update operations:

```
Layer n → Layer n+1:
  Edge update:   E_n  →(f_E)→  E_{n+1}
  Node update:   V_n  →(f_V)→  V_{n+1}
  State update:  U_n  →(f_U)→  U_{n+1}
```

`f_E`, `f_V`, `f_U` are typically MLPs. After L layers, node/edge/state embeddings are pooled and passed through a final MLP for prediction.

---

## Invariant vs. Equivariant GNNs

| Property | Invariant | Equivariant |
|----------|-----------|-------------|
| Input features | Scalar: bond distances, angles | Vector/tensor: bond vectors, relative positions |
| Output under rotation | Unchanged (scalar properties) | Transforms correctly (forces, dipoles, tensors) |
| Examples | MEGNet, M3GNet, CHGNet | TensorNet, SO3Net, MACE, NequIP |
| Accuracy (energy) | Lower | Higher (10–40% better MAE) |
| Accuracy (forces) | Lower | Significantly better |
| Compute cost | Lower | Higher |

**Key insight:** Equivariant models use directional information from bond vectors, making them essential for accurate force prediction in MLIPs. Invariant models are competitive for scalar property prediction at lower cost.

---

## Models in MatGL

### MEGNet (Invariant)
- GNN with global state vector **u** (encodes global properties like temperature, pressure)
- Distance-only features; fastest inference (~12s for 6500 structures on A6000)
- Highest MAE among MatGL models; useful for rapid screening

### M3GNet (Invariant)
- Extends MEGNet with **3-body interactions** (bond angles)
- First foundation potential from Ong group; covers full periodic table
- Transfer learning from ANI-1x pre-trained embedding reduces MAE 10–15%

### CHGNet (Invariant)
- Incorporates **DFT magnetic moments** as node features
- Outperforms M3GNet for energies/forces/stresses on crystalline systems
- Useful for magnetic or charge-sensitive systems (oxides, Li-battery materials)
- Cannot be used for property prediction (MLIP only)

### TensorNet (Equivariant)
- O(3)-equivariant via **Cartesian tensor representations**
- More computationally efficient than higher-rank spherical tensor models
- **Best accuracy/speed tradeoff** — recommended default for MLIP applications
- Basis: TensorNet-MatPES-PBE-v2025.1 = current best general-purpose FP in MatGL

### SO3Net (Equivariant)
- SO(3)-equivariant via **spherical harmonics + Clebsch-Gordan tensor products**
- Minimalist architecture; achieves **lowest MAE on ANI-1x** (2.28 meV/atom energy, 0.046 eV/Å force)
- Significantly slower than TensorNet for >100 atoms; not recommended for large-scale MD

---

## Practical Guidance (from [[sources/ko-2025-matgl]])

- **Property prediction only (no forces needed):** TensorNet or M3GNet. MEGNet for speed.
- **MLIPs for MD/relaxation:** TensorNet (default); SO3Net if accuracy is critical and system is small.
- **Magnetic/ionic systems:** CHGNet.
- **Transfer learning:** M3GNet-TL with pre-trained ANI-1x embedding is a cost-effective path for organic or molecular systems.

---

## Broader Landscape

Other notable GNN architectures **not in MatGL**:
- **MACE** (Batatia et al.) — higher-order equivariant; MACE-MP-0/Large are currently dominant general FPs
- **SevenNet-0** — alternative universal MLIP
- **NequIP** (Batzner et al.) — E(3)-equivariant; architectural precursor to MACE
- **Equiformer** (Liao & Smidt) — equivariant graph attention transformer

See [[entities/software-tools]] for library implementations.

---

## Related Concepts
- [[concepts/machine-learning-potentials]]
- [[entities/software-tools#matgl]]
