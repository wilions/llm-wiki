# llm-wiki Skill — Design Spec

**Date:** 2026-04-17  
**Status:** Approved

---

## Goal

Convert the llm-wiki knowledge base into a Claude Code skill so that:

1. The ingest / query / lint operations trigger automatically when the user says the right keywords — from **any working directory**, not just inside `llm-wiki/`
2. The skill is self-contained and portable, carrying all procedures internally

---

## Non-Goals

- Bundling wiki content into the skill (wiki files stay in the repo)
- A `search` command or other new operations
- Making the skill generic / shareable (this is a personal, materials-science-specific skill, separate from the existing `research-wiki` skill)

---

## File Structure

```
~/.claude/skills/llm-wiki/
├── SKILL.md                   ← lean: path config, routing, operation pointers (~100 lines)
└── references/
    ├── ingest.md              ← full 9-step ingest procedure
    ├── query.md               ← full 6-step query procedure
    ├── lint.md                ← lint procedure + report format
    └── schema.md              ← page frontmatter, conventions, domain vocabulary
```

---

## Path Configuration

A single constant near the top of `SKILL.md`:

```
WIKI_ROOT: /Users/pei/Documents/Coding/Claude/llm-wiki
```

All file reads and writes in all three operations use this absolute path. This is the only place the path is declared.

---

## Trigger Mechanism

The `description` frontmatter field:

> Materials-science research wiki (metal AM, HEA, structural alloys). Use this skill when the user explicitly says "ingest", "query the wiki", "lint the wiki", or "lint" — and only then. Do NOT trigger on general materials-science questions unless the user specifically asks to query the wiki.

**Triggers:**
- `"ingest [file]"` — file ingestion
- `"ingest"` (no filename) — scan `WIKI_ROOT/raw/` for unprocessed files
- `"query the wiki: ..."` — wiki query
- `"lint"` / `"lint the wiki"` — wiki lint

**Does not trigger:**
- General materials-science questions without explicit wiki reference

---

## Operations

### Ingest (`references/ingest.md`)

Mirrors the 9-step procedure from `WIKI_ROOT/CLAUDE.md`, with two additions:
- All paths use `WIKI_ROOT` absolute prefix
- If user says "ingest" with no filename: scan `WIKI_ROOT/raw/` and list files that have no matching slug in `WIKI_ROOT/wiki/sources/`, ask user to pick one

Steps (from CLAUDE.md):
1. Read source file from `WIKI_ROOT/raw/`
2. Discuss key takeaways (2–3 questions max)
3. Write summary to `WIKI_ROOT/wiki/sources/<slug>.md`
4. Update `WIKI_ROOT/wiki/index.md`
5. Update/create entity pages in `WIKI_ROOT/wiki/entities/`
6. Update/create concept pages in `WIKI_ROOT/wiki/concepts/`
7. Update `WIKI_ROOT/wiki/overview.md`
8. Append to `WIKI_ROOT/wiki/log.md`
9. Commit: `git -C WIKI_ROOT add wiki/ && git commit -m "ingest: <title>"`

### Query (`references/query.md`)

Mirrors the 6-step query procedure from CLAUDE.md, paths adapted.

### Lint (`references/lint.md`)

Mirrors the lint procedure from CLAUDE.md. Output: `WIKI_ROOT/wiki/lint-YYYY-MM-DD.md`.

### Schema (`references/schema.md`)

Loaded when any operation needs to write or validate wiki pages. Contains:
- Page frontmatter format
- Cross-reference (`[[page]]`) conventions
- Conflict markup format (`⚠️ **Conflict:**`)
- Domain vocabulary: alloy systems, AM processes, key properties, key concepts
- Index conventions

---

## Routing Logic in SKILL.md

```
if user says "ingest":
    load references/ingest.md
    load references/schema.md (for writing pages)
    
if user says "query the wiki":
    load references/query.md
    load references/schema.md (if filing answer as synthesis)
    
if user says "lint" or "lint the wiki":
    load references/lint.md
```

---

## What Stays in the Repo

The existing `WIKI_ROOT/CLAUDE.md` remains the authoritative schema for anyone working directly inside the `llm-wiki/` repo. The skill is additive — it makes the same procedures available from any directory. If the schema evolves, both files need updating (this is intentional; the skill is a copy, not a live reference).

---

## Out of Scope

- Eval / test harness for the skill (operations are deterministic, human-reviewed)
- Description optimization loop (can be done after first use if triggering is unreliable)
