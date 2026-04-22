# Tiny Tamagotchi MVP Roadmap

## Roadmap Intent

This roadmap is intentionally small. The challenge values a clear, implementation-ready spec more than a large feature count.

## Phase 0: Constitution

Artifacts:

- `specs/mission.md`
- `specs/tech-stack.md`
- `specs/roadmap.md`

Exit criteria:

- project goal is explicit
- scope and non-goals are documented
- core technical approach is chosen
- milestones requiring user approval are identified

## Phase 1: Core Simulation Loop

Feature folder:

- `core-simulation-loop/`

Scope:

- define ChuChu's vitals
- define timed stat decay
- define low-stat thresholds and system rules
- expose a live status panel

Why first:

- this is the heart of the game
- every later feature depends on reliable simulation behavior

## Phase 2: Care Actions And Feedback

Feature folder:

- `care-actions-feedback/`

Scope:

- implement `Feed`, `Play`, and `Rest`
- define stat changes for each action
- add cooldown or balance rules only if needed for MVP clarity
- show clear action feedback after each interaction

Why second:

- the simulation needs a player response loop to be meaningful

## Phase 3: State Progression And Personality

Feature folder:

- `state-progression-personality/`

Scope:

- define `Normal`, `Sick`, and `Evolved`
- connect states to simulation thresholds and recovery logic
- add small personality reactions or easter eggs
- make the pet visually distinct across states

Why third:

- visible state change is the strongest proof that the system feels alive

## Phase 4: Persistence And Presentation Shell

Feature folder:

- `persistence-shell/`

Scope:

- preserve ChuChu between reloads
- persist ChuChu on the backend instead of browser-only storage
- shape the final single-screen layout
- polish empty, first-load, and resumed-session behavior

Why fourth:

- persistence makes the game feel like a companion instead of a toy reset every refresh

## Phase 5: Validation And Submission Prep

Scope:

- run implementation checks against each feature validation spec
- capture proof that implementation follows the spec
- prepare a short demo flow for the final video

Deliverables:

- passing validation notes
- stable playable app
- documentation folder ready for reviewer inspection

## Replanning Checkpoints

Pause for review after:

1. constitution approval
2. core simulation implementation
3. state progression implementation
4. full MVP validation

At each checkpoint we should ask:

- did any assumption prove wrong?
- is the roadmap still small enough for a polished MVP?
- does the implementation still match the written rules?

## Recommended Delivery Sequence

1. approve constitution and high-level product direction
2. approve technical approach and app location in repo
3. implement the core simulation and care loop
4. add state progression and personality
5. add persistence and polish
6. validate against the written specs
