# Tiny Tamagotchi MVP

`ChuChu` is a standalone, spec-driven virtual pet built for the DeepLearning.AI Tiny Tamagotchi MVP challenge.

## Repository Shape

```text
tiny-tamagotchi-mvp/
  specs/
  core-simulation-loop/
  care-actions-feedback/
  state-progression-personality/
  persistence-shell/
  web/
  api/
  docs/
```

## Constitution

- [Mission](</C:/Users/Admin/OneDrive/Documents/New project/tiny-tamagotchi-mvp/specs/mission.md>)
- [Roadmap](</C:/Users/Admin/OneDrive/Documents/New project/tiny-tamagotchi-mvp/specs/roadmap.md>)
- [Tech Stack](</C:/Users/Admin/OneDrive/Documents/New project/tiny-tamagotchi-mvp/specs/tech-stack.md>)

## Feature Specs

- [Core Simulation Loop](</C:/Users/Admin/OneDrive/Documents/New project/tiny-tamagotchi-mvp/core-simulation-loop/requirements.md>)
- [Care Actions And Feedback](</C:/Users/Admin/OneDrive/Documents/New project/tiny-tamagotchi-mvp/care-actions-feedback/requirements.md>)
- [State Progression And Personality](</C:/Users/Admin/OneDrive/Documents/New project/tiny-tamagotchi-mvp/state-progression-personality/requirements.md>)
- [Persistence And Presentation Shell](</C:/Users/Admin/OneDrive/Documents/New project/tiny-tamagotchi-mvp/persistence-shell/requirements.md>)

## Implementation Summary

- Standalone `Next.js` frontend in [web](</C:/Users/Admin/OneDrive/Documents/New project/tiny-tamagotchi-mvp/web>)
- Standalone `FastAPI` backend in [api](</C:/Users/Admin/OneDrive/Documents/New project/tiny-tamagotchi-mvp/api>)
- `SQLite` persistence with a single global ChuChu save
- Deterministic backend simulation for timed decay, care actions, state transitions, and permanent evolution

## Local Run

### Backend

```powershell
cd C:\Users\Admin\OneDrive\Documents\New project\tiny-tamagotchi-mvp\api
pip install -e .[dev]
uvicorn app.main:app --reload --port 8102
```

### Frontend

```powershell
cd C:\Users\Admin\OneDrive\Documents\New project\tiny-tamagotchi-mvp\web
copy .env.example .env.local
npm install
npm run dev
```

The frontend expects the API at `http://localhost:8102/api/v1`.
