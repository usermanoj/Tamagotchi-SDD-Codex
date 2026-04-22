# Tiny Tamagotchi MVP Tech Stack

## Decision Framing

The challenge does not require a complex stack. The best technical choice is the one that keeps the implementation small, testable, and directly traceable to the spec.

## Proposed Stack Based On Approved Decisions

- Frontend: standalone `Next.js 16` app with `React 19` and `TypeScript`
- Backend: standalone `FastAPI` service in Python
- App shape: single-screen web app backed by a lightweight HTTP API
- State management: React UI state plus a deterministic backend game engine module
- Persistence: backend database, not browser-only storage
- Styling: purpose-built `minimal modern` CSS for a clean challenge-ready presentation
- Validation: targeted unit tests for game rules plus manual QA checklist for interaction flow

## Why This Is The Current Recommendation

- the repo already contains working `Next.js` and `FastAPI` examples we can reuse conceptually
- a standalone app keeps the submission cleaner than mixing it into the unrelated `BoardBrief` product
- backend persistence matches the approved product direction
- a small deterministic game engine keeps gameplay logic testable and easy to trace from the spec

## Recommended Architecture

### UI Layer

- renders ChuChu, vitals, current state, action buttons, and short reaction text
- triggers actions through a narrow interface instead of mutating raw state everywhere

### Game Engine Layer

- owns stat boundaries, tick decay, state transitions, and action effects
- exposes pure functions where possible so the rules are easy to test

### API Layer

- exposes endpoints to fetch pet state, apply care actions, and reset the pet
- applies authoritative simulation updates before persisting results
- returns normalized state objects to the frontend

### Persistence Layer

- stores pet state in a backend database
- restores pet state on load
- accounts for elapsed real time between requests so ChuChu still changes while the app is closed

## Placement In This Repo

Approved direction:

- build Tiny Tamagotchi as a new standalone project inside `tiny-tamagotchi-mvp/`

Suggested layout:

```text
tiny-tamagotchi-mvp/
  specs/
  web/
  api/
  core-simulation-loop/
  care-actions-feedback/
  state-progression-personality/
  persistence-shell/
```

## Recommended Validation Tooling

- logic tests for stat decay, action effects, threshold handling, and evolution rules
- manual scenario checks for first launch, reload recovery, and visible state changes

If lightweight browser tests are easy to add later, they are a bonus but not required for MVP spec quality.

## Technical Constraints

- backend is required for persistence, but gameplay rules should still be deterministic and locally testable
- core rules should not depend on animation timing
- stat values should be clamped to a fixed range
- elapsed-time recovery logic must be deterministic and documented
- UI feedback should not be the only source of truth for game state

## Final Technical Decisions

All technical decisions for the MVP are resolved:

- persistence store: `SQLite`
- frontend-backend contract: `single global pet API`
- offline elapsed time: `capped at 8 hours`

## Locked Implementation Choices

- standalone `Next.js` frontend plus standalone `FastAPI` backend
- `SQLite` for MVP persistence
- single-pet API with explicit reset endpoint
- capped offline decay window of 8 hours to prevent extreme punishment
