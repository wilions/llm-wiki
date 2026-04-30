---
title: Log
type: log
---

# Wiki Log

Append-only. Format: `## [YYYY-MM-DD] <operation> | <title>`

---

## [2026-04-16] init
- Wiki initialized. Schema written. Seed entity and concept pages created.

## [2026-04-16] lint
- Orphans: 6 | Contradictions: 0 | Stubs: 5 | Dead links: 2 | Missing cross-refs: 7
- Report: [[lint-2026-04-16]]

## [2026-04-29] lint
- Orphans: 5 | Contradictions: 0 | Stubs: 0 | Broken links: 3 | Missing cross-refs: 6
- Report: [[lint-2026-04-29]]

## [2026-04-30] maintenance | Fix lint errors and add cross-references
- Fixed: broken `[[researchers]]` → `[[entities/researchers]]` in software-tools
- Fixed: removed `[[autoMD]]` dead links in software-tools (2×)
- Fixed: removed `[[sources/...]]` placeholder syntax in alloy-systems and am-processes
- Added: Related Pages sections to solidification, microstructure, mechanical-properties
- Added: Related Concepts sections to alloy-systems and am-processes
- Added: Related Concepts + researchers link to software-tools

## [2026-04-16] ingest | MatGL: Materials Graph Library (Ko et al., 2025)
- Summary page: [[sources/ko-2025-matgl]]
- Pages created: [[entities/software-tools]], [[concepts/graph-neural-networks]], [[concepts/machine-learning-potentials]]
- Pages updated: [[entities/researchers]] (Ong group, Ceder group), [[index]], [[overview]]
- Key finding: TensorNet-MatPES-PBE-v2025.1 is a viable drop-in alternative to MACE-MP-0 for autoMD; equivariant GNNs outperform invariant by 10–40% on forces; no existing FP validated for AM alloy systems.
