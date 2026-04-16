# LLM Wiki — Schema

## Purpose
This is a persistent, compounding knowledge base for materials-science research,
focused on metal additive manufacturing (AM), high-entropy alloys (HEA/MPEA),
and structural alloy development.

You (Claude) own the `wiki/` layer entirely. You read `raw/` but never modify it.
The human reads the wiki and directs analysis; you do the maintenance.

---

## Directory Conventions

| Path | Owner | Description |
|------|-------|-------------|
| `raw/` | Human | Immutable source documents (markdown clips, PDFs converted to text) |
| `raw/assets/` | Human | Images referenced in raw sources |
| `wiki/` | Claude | All wiki pages — summaries, entities, concepts, syntheses |
| `wiki/index.md` | Claude | Content catalog; updated on every ingest |
| `wiki/log.md` | Claude | Append-only chronological log |
| `wiki/overview.md` | Claude | Evolving field synthesis |
| `wiki/entities/` | Claude | Named entities: alloy systems, AM processes, researchers, journals |
| `wiki/concepts/` | Claude | Scientific concepts, mechanisms, phenomena |

---

## Page Conventions

Every wiki page (except index.md and log.md) uses this frontmatter:

```yaml
---
title: <page title>
type: entity | concept | source | synthesis
tags: [<relevant tags>]
sources: [<source filenames that inform this page>]
last_updated: YYYY-MM-DD
---
```

Cross-references use standard Obsidian wiki-link syntax: `[[page-name]]`.

Contradictions or unresolved conflicts are marked:
```
> ⚠️ **Conflict:** Source A reports X; Source B reports Y. Needs resolution.
```

---

## Operation: Ingest

Triggered when the human says "ingest [filename]" or drops a file in `raw/`.

Steps (do all in one session):
1. Read the source file in `raw/`.
2. Discuss key takeaways with the human (2-3 questions max).
3. Write a summary page to `wiki/sources/<slug>.md`.
4. Update `wiki/index.md` — add the new source entry under the Sources section.
5. Identify all entities mentioned (alloy systems, processes, researchers). Update or create pages in `wiki/entities/`.
6. Identify all concepts discussed. Update or create pages in `wiki/concepts/`.
7. Update `wiki/overview.md` if the source shifts or strengthens the field synthesis.
8. Append an entry to `wiki/log.md`:
   ```
   ## [YYYY-MM-DD] ingest | <source title>
   - Summary page: [[sources/<slug>]]
   - Pages updated: [[entities/...]], [[concepts/...]]
   - Key finding: <one sentence>
   ```
9. Commit: `git add wiki/ && git commit -m "ingest: <source title>"`

A single ingest typically touches 8-15 wiki pages.

---

## Operation: Query

Triggered when the human asks a question.

Steps:
1. Read `wiki/index.md` to find relevant pages.
2. Read those pages.
3. Synthesize an answer with citations (use `[[page]]` links).
4. Ask the human: "Should I file this answer as a wiki page?"
5. If yes, write it to `wiki/` (type: synthesis) and update `wiki/index.md`.
6. Append to `wiki/log.md`:
   ```
   ## [YYYY-MM-DD] query | <question summary>
   - Answer filed: [[synthesis/<slug>]] (or "not filed")
   ```

---

## Operation: Lint

Triggered when the human says "lint the wiki".

Check for and report:
- **Contradictions**: pages making conflicting claims about the same entity/concept
- **Stale claims**: claims superseded by newer source summaries
- **Orphan pages**: pages with no inbound `[[links]]` from other wiki pages
- **Concept stubs**: concepts mentioned in passing but lacking their own page
- **Missing cross-references**: entity/concept mentioned in a page without a `[[link]]`
- **Data gaps**: important questions the wiki can't answer (suggest new sources)

Output a lint report to `wiki/lint-YYYY-MM-DD.md`. Do not auto-fix — report only, then ask the human what to address.

Append to log:
```
## [YYYY-MM-DD] lint
- Orphans: N | Contradictions: N | Stubs: N
- Report: [[lint-YYYY-MM-DD]]
```

---

## Domain Vocabulary

### Alloy Systems
- HEA / MPEA / RHEA (high/multi/refractory principal element alloys)
- Ti-6Al-4V (Ti64), IN718, IN625, SS316L, AlSi10Mg, CoCrFeMnNi (Cantor)

### AM Processes
- SLM / L-PBF (selective laser melting / laser powder bed fusion)
- EBM / EB-PBF (electron beam melting)
- DED (directed energy deposition): LMD, LENS, WAAM
- BINDER JET

### Key Properties
- UTS, YS, elongation, hardness (HV/HRC)
- Fatigue life, fracture toughness (K_IC)
- Porosity (%), relative density (%)
- Grain size (μm), texture (crystallographic)
- Melt pool dimensions, cooling rate (K/s)

### Key Concepts
- VED (volumetric energy density, J/mm³)
- Keyhole / lack-of-fusion defects
- Columnar-to-equiaxed transition (CET)
- LPSO, Laves phase, γ' / γ'' precipitates
- Hall-Petch, Taylor factor, Schmid factor

---

## Index Conventions

`wiki/index.md` is organized by section:

```markdown
# Wiki Index

## Sources (N)
| Slug | Title | Year | Key finding |
|------|-------|------|-------------|

## Entities
### Alloy Systems
- [[entities/alloy-systems]] — ...

### AM Processes
- [[entities/am-processes]] — ...

### Researchers
- [[entities/researchers]] — ...

## Concepts
- [[concepts/solidification]] — ...
- [[concepts/microstructure]] — ...
- [[concepts/mechanical-properties]] — ...

## Syntheses
(filed query answers)

## Log
See [[log]]
```

---

## Commit Discipline

| Operation | Commit message format |
|-----------|-----------------------|
| Ingest | `ingest: <source title>` |
| Query filed | `query: <question slug>` |
| Lint | `lint: YYYY-MM-DD` |
| Schema update | `schema: <what changed>` |
