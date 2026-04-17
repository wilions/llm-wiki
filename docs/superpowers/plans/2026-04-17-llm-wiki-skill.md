# llm-wiki Skill Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create a Claude Code skill at `~/.claude/skills/llm-wiki/` that triggers the ingest / query / lint wiki operations from any working directory.

**Architecture:** Lean `SKILL.md` with path config and routing logic; full procedures in `references/` subdirectory. Wiki files stay in the repo at `/Users/pei/Documents/Coding/Claude/llm-wiki`. Skill reads/writes via absolute path.

**Tech Stack:** Markdown skill files only — no code, no dependencies.

---

## File Map

| File | Action | Purpose |
|------|--------|---------|
| `~/.claude/skills/llm-wiki/SKILL.md` | Create | Frontmatter trigger, WIKI_ROOT constant, routing logic |
| `~/.claude/skills/llm-wiki/references/schema.md` | Create | Page frontmatter, conventions, domain vocabulary |
| `~/.claude/skills/llm-wiki/references/ingest.md` | Create | Full 9-step ingest procedure |
| `~/.claude/skills/llm-wiki/references/query.md` | Create | Full 6-step query procedure |
| `~/.claude/skills/llm-wiki/references/lint.md` | Create | Lint checks, report format, log format |

---

## Task 1: Create skill directory structure

**Files:**
- Create: `~/.claude/skills/llm-wiki/`
- Create: `~/.claude/skills/llm-wiki/references/`

- [ ] **Step 1: Create directories**

```bash
mkdir -p ~/.claude/skills/llm-wiki/references
```

Expected: no output, directories exist.

- [ ] **Step 2: Verify**

```bash
ls ~/.claude/skills/llm-wiki/
```

Expected: `references/`

- [ ] **Step 3: No commit yet** — nothing to commit until files exist.

---

## Task 2: Write `references/schema.md`

**Files:**
- Create: `~/.claude/skills/llm-wiki/references/schema.md`

- [ ] **Step 1: Write the file**

Write the following content to `~/.claude/skills/llm-wiki/references/schema.md`:

```markdown
# Wiki Schema

## Page Frontmatter

Every wiki page (except `index.md` and `log.md`) uses this frontmatter:

​```yaml
---
title: <page title>
type: entity | concept | source | synthesis
tags: [<relevant tags>]
sources: [<source filenames that inform this page>]
last_updated: YYYY-MM-DD
---
​```

## Cross-References

Use Obsidian wiki-link syntax: `[[page-name]]`

Examples:
- `[[entities/alloy-systems]]`
- `[[concepts/solidification]]`
- `[[sources/ko-2025-matgl]]`

## Conflict Markup

When two sources make conflicting claims:

```
> ⚠️ **Conflict:** Source A reports X; Source B reports Y. Needs resolution.
```

## Index Conventions

`wiki/index.md` sections:

```markdown
## Sources (N)
| Slug | Title | Year | Key finding |
|------|-------|------|-------------|

## Entities
### Alloy Systems
- [[entities/alloy-systems]] — one-line summary

### AM Processes
- [[entities/am-processes]] — one-line summary

### Researchers
- [[entities/researchers]] — one-line summary

### Software Tools
- [[entities/software-tools]] — one-line summary

## Concepts
- [[concepts/solidification]] — one-line summary
- [[concepts/microstructure]] — one-line summary
- [[concepts/mechanical-properties]] — one-line summary

## Syntheses
(filed query answers)

## Log
See [[log]]
```

## Commit Message Format

| Operation | Format |
|-----------|--------|
| Ingest | `ingest: <source title>` |
| Query filed | `query: <question slug>` |
| Lint | `lint: YYYY-MM-DD` |
| Schema update | `schema: <what changed>` |

---

## Domain Vocabulary

### Alloy Systems
- HEA / MPEA / RHEA (high/multi/refractory principal element alloys)
- Ti-6Al-4V (Ti64), IN718, IN625, SS316L, AlSi10Mg, CoCrFeMnNi (Cantor alloy)

### AM Processes
- SLM / L-PBF (selective laser melting / laser powder bed fusion)
- EBM / EB-PBF (electron beam melting / electron beam powder bed fusion)
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
```

- [ ] **Step 2: Verify**

```bash
wc -l ~/.claude/skills/llm-wiki/references/schema.md
```

Expected: ~85 lines.

---

## Task 3: Write `references/ingest.md`

**Files:**
- Create: `~/.claude/skills/llm-wiki/references/ingest.md`

- [ ] **Step 1: Write the file**

Write the following content to `~/.claude/skills/llm-wiki/references/ingest.md`:

```markdown
# Ingest Procedure

WIKI_ROOT: `/Users/pei/Documents/Coding/Claude/llm-wiki`

A single ingest typically touches 8–15 wiki pages. Complete all steps in one session.

---

## Step 0: Resolve filename (if not provided)

If the user said "ingest" with no filename:
1. List files in `WIKI_ROOT/raw/` (excluding `assets/`)
2. List slugs already in `WIKI_ROOT/wiki/sources/`
3. Show the user files in `raw/` that have no matching source page — ask which one to ingest

## Step 1: Read the source

Read the file from `WIKI_ROOT/raw/<filename>`.

## Step 2: Discuss key takeaways

Ask the human 2–3 focused questions to surface:
- The most surprising or counter-intuitive finding
- Any claims that conflict with existing wiki pages
- Which entities and concepts are most relevant to track

## Step 3: Write source summary page

Write to `WIKI_ROOT/wiki/sources/<slug>.md` using the frontmatter from `schema.md`:

```yaml
---
title: "<Full Paper Title>"
type: source
tags: [<relevant tags>]
sources: [<original filename in raw/>]
last_updated: YYYY-MM-DD
---
```

Include: authors, journal, year, DOI, summary, key findings, methods, limitations, cross-links to entities and concepts.

## Step 4: Update index

Edit `WIKI_ROOT/wiki/index.md` — add a row to the Sources table:

```markdown
| [<slug>](sources/<slug>.md) | <Title> | <Year> | <one-sentence key finding> |
```

Update the Sources count in the section header: `## Sources (N)`.

## Step 5: Update entity pages

For each entity mentioned (alloy systems, AM processes, researchers, software tools):
- If the page exists: add a section or bullet referencing this source
- If the page doesn't exist: create it in `WIKI_ROOT/wiki/entities/<slug>.md` using `entity` frontmatter

## Step 6: Update concept pages

For each concept discussed (solidification, microstructure, GNNs, MLIPs, etc.):
- If the page exists: add new findings with a citation `[[sources/<slug>]]`
- If the page doesn't exist: create it in `WIKI_ROOT/wiki/concepts/<slug>.md` using `concept` frontmatter

Mark any conflicts with the conflict markup from `schema.md`.

## Step 7: Update overview

Read `WIKI_ROOT/wiki/overview.md`. If the new source:
- Strengthens an existing claim: add the citation
- Shifts the synthesis: update the relevant paragraph
- Introduces a new theme: add a new section

If nothing changes, leave overview untouched.

## Step 8: Append to log

Append to `WIKI_ROOT/wiki/log.md`:

```
## [YYYY-MM-DD] ingest | <source title>
- Summary page: [[sources/<slug>]]
- Pages updated: [[entities/...]], [[concepts/...]]
- Key finding: <one sentence>
```

## Step 9: Commit

```bash
git -C /Users/pei/Documents/Coding/Claude/llm-wiki add wiki/ && \
git -C /Users/pei/Documents/Coding/Claude/llm-wiki commit -m "ingest: <source title>"
```
```

- [ ] **Step 2: Verify**

```bash
wc -l ~/.claude/skills/llm-wiki/references/ingest.md
```

Expected: ~90 lines.

---

## Task 4: Write `references/query.md`

**Files:**
- Create: `~/.claude/skills/llm-wiki/references/query.md`

- [ ] **Step 1: Write the file**

Write the following content to `~/.claude/skills/llm-wiki/references/query.md`:

```markdown
# Query Procedure

WIKI_ROOT: `/Users/pei/Documents/Coding/Claude/llm-wiki`

---

## Step 1: Find relevant pages

Read `WIKI_ROOT/wiki/index.md`. Identify which entity pages, concept pages, and source summaries are relevant to the question.

## Step 2: Read those pages

Read each relevant page. Cross-reference linked pages as needed.

## Step 3: Synthesize an answer

Write the answer with citations using `[[page]]` wiki-link syntax. If sources conflict, surface the conflict explicitly using the conflict markup from `schema.md`.

## Step 4: Offer to file

Ask: "Should I file this answer as a wiki page?"

## Step 5: If yes — write synthesis page

Write to `WIKI_ROOT/wiki/syntheses/<slug>.md`:

```yaml
---
title: "<Question as title>"
type: synthesis
tags: [<relevant tags>]
sources: [<source pages consulted>]
last_updated: YYYY-MM-DD
---
```

Add a row to the Syntheses section in `WIKI_ROOT/wiki/index.md`:
```markdown
- [[syntheses/<slug>]] — <one-line answer summary>
```

## Step 6: Append to log

Append to `WIKI_ROOT/wiki/log.md`:

```
## [YYYY-MM-DD] query | <question summary>
- Answer filed: [[syntheses/<slug>]] (or "not filed")
```
```

- [ ] **Step 2: Verify**

```bash
wc -l ~/.claude/skills/llm-wiki/references/query.md
```

Expected: ~55 lines.

---

## Task 5: Write `references/lint.md`

**Files:**
- Create: `~/.claude/skills/llm-wiki/references/lint.md`

- [ ] **Step 1: Write the file**

Write the following content to `~/.claude/skills/llm-wiki/references/lint.md`:

```markdown
# Lint Procedure

WIKI_ROOT: `/Users/pei/Documents/Coding/Claude/llm-wiki`

Do not auto-fix anything. Report only, then ask the human what to address.

---

## Checks

Read all pages in `WIKI_ROOT/wiki/` before running any check.

### 1. Contradictions
Pages making conflicting claims about the same entity or concept. Look for numerical values (temperatures, properties, percentages) that differ across sources on the same topic.

### 2. Stale claims
Claims in entity/concept pages that are superseded by newer source summaries. A claim is stale if a later-ingested source explicitly updates or refutes it.

### 3. Orphan pages
Pages in `wiki/entities/` or `wiki/concepts/` that have no inbound `[[links]]` from any other wiki page. Check by searching for `[[<page-slug>]]` across all pages.

### 4. Concept stubs
Concepts mentioned by name in source summaries or entity pages that do not have their own page in `wiki/concepts/`. List each missing concept and which page mentions it.

### 5. Missing cross-references
Entity or concept names appearing as plain text in a page where a `[[link]]` should exist. For example, "MatGL" mentioned in a concept page without `[[entities/software-tools]]` or `[[sources/ko-2025-matgl]]`.

### 6. Data gaps
Important questions the wiki cannot currently answer — flag these as suggestions for new sources to ingest.

---

## Report Format

Write the lint report to `WIKI_ROOT/wiki/lint-YYYY-MM-DD.md`:

```markdown
---
title: Lint Report YYYY-MM-DD
type: lint
last_updated: YYYY-MM-DD
---

# Lint Report — YYYY-MM-DD

## Summary
- Orphans: N
- Contradictions: N
- Stubs: N
- Missing cross-references: N
- Stale claims: N
- Data gaps: N

## Contradictions
<!-- list each conflict with page references -->

## Stale Claims
<!-- list each stale claim with old page and newer source -->

## Orphan Pages
<!-- list each orphan page path -->

## Concept Stubs
<!-- list each missing concept page and where it's mentioned -->

## Missing Cross-References
<!-- list each instance: page → term that needs a [[link]] -->

## Data Gaps
<!-- list questions the wiki can't answer, suggest sources -->
```

---

## Log Entry

Append to `WIKI_ROOT/wiki/log.md`:

```
## [YYYY-MM-DD] lint
- Orphans: N | Contradictions: N | Stubs: N
- Report: [[lint-YYYY-MM-DD]]
```

---

## Commit

```bash
git -C /Users/pei/Documents/Coding/Claude/llm-wiki add wiki/lint-YYYY-MM-DD.md wiki/log.md && \
git -C /Users/pei/Documents/Coding/Claude/llm-wiki commit -m "lint: YYYY-MM-DD"
```
```

- [ ] **Step 2: Verify**

```bash
wc -l ~/.claude/skills/llm-wiki/references/lint.md
```

Expected: ~85 lines.

---

## Task 6: Write `SKILL.md`

**Files:**
- Create: `~/.claude/skills/llm-wiki/SKILL.md`

- [ ] **Step 1: Write the file**

Write the following content to `~/.claude/skills/llm-wiki/SKILL.md`:

```markdown
---
name: llm-wiki
description: Materials-science research wiki (metal AM, HEA, structural alloys). Use this skill when the user explicitly says "ingest", "query the wiki", "lint the wiki", or "lint" — and only then. Do NOT trigger on general materials-science questions unless the user specifically asks to query the wiki.
---

# LLM Wiki

**WIKI_ROOT:** `/Users/pei/Documents/Coding/Claude/llm-wiki`

This skill manages a persistent knowledge base for materials-science research. All reads and writes use the absolute WIKI_ROOT path above — this skill works from any working directory.

---

## Routing

Read the reference file for the operation the user requested:

| User says | Load | Also load |
|-----------|------|-----------|
| `"ingest [file]"` or `"ingest"` | `references/ingest.md` | `references/schema.md` |
| `"query the wiki: ..."` | `references/query.md` | `references/schema.md` only if filing a synthesis page |
| `"lint"` or `"lint the wiki"` | `references/lint.md` | — |

Always load `references/schema.md` when writing or validating wiki pages (frontmatter, cross-references, domain vocabulary).

---

## Reference Files

- `references/ingest.md` — 9-step procedure for ingesting a source from `WIKI_ROOT/raw/` into the wiki
- `references/query.md` — 6-step procedure for answering a question from wiki content
- `references/lint.md` — lint checks, report format, log format
- `references/schema.md` — page frontmatter, cross-reference syntax, conflict markup, domain vocabulary, index conventions
```

- [ ] **Step 2: Verify**

```bash
wc -l ~/.claude/skills/llm-wiki/SKILL.md
```

Expected: ~35 lines.

- [ ] **Step 3: Verify skill structure**

```bash
find ~/.claude/skills/llm-wiki -type f | sort
```

Expected:
```
/Users/pei/.claude/skills/llm-wiki/SKILL.md
/Users/pei/.claude/skills/llm-wiki/references/ingest.md
/Users/pei/.claude/skills/llm-wiki/references/lint.md
/Users/pei/.claude/skills/llm-wiki/references/query.md
/Users/pei/.claude/skills/llm-wiki/references/schema.md
```

- [ ] **Step 4: Commit the plan and skill together**

```bash
git -C /Users/pei/Documents/Coding/Claude/llm-wiki add docs/ && \
git -C /Users/pei/Documents/Coding/Claude/llm-wiki commit -m "plan: llm-wiki skill implementation"
```

---

## Task 7: Smoke test

No automated test harness — verify by manual inspection from outside the wiki directory.

- [ ] **Step 1: Confirm skill is discoverable**

From a different working directory (e.g. `~/`), open a new Claude Code session and check that `llm-wiki` appears in the available skills list.

- [ ] **Step 2: Trigger ingest with no filename**

Say: `ingest`

Expected: skill loads `references/ingest.md`, scans `WIKI_ROOT/raw/`, lists the MatGL PDF as an unprocessed file, asks which one to ingest.

- [ ] **Step 3: Trigger query**

Say: `query the wiki: what is MatGL?`

Expected: skill loads `references/query.md`, reads `WIKI_ROOT/wiki/index.md` and relevant pages, synthesizes an answer with `[[links]]`.

- [ ] **Step 4: Trigger lint**

Say: `lint the wiki`

Expected: skill loads `references/lint.md`, reads all wiki pages, produces a lint report at `WIKI_ROOT/wiki/lint-YYYY-MM-DD.md`.

- [ ] **Step 5: Confirm non-trigger**

Say: `what alloys does MatGL support?` (no "query the wiki" prefix)

Expected: skill does NOT trigger — Claude answers from its own knowledge or asks for clarification, without loading the wiki.
