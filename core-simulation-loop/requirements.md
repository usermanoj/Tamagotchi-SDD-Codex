# Requirements: Core Simulation Loop

## Data Model

The pet state must include:

- `name`: fixed to `ChuChu`
- `hunger`: integer from `0` to `100`
- `happiness`: integer from `0` to `100`
- `energy`: integer from `0` to `100`
- `status`: one of `normal`, `sick`, `evolved`
- `lastUpdatedAt`: timestamp
- `lastReaction`: short text string
- `daysSurvived` or equivalent progression counter

## Initial State

On a fresh start:

- all vitals begin in a healthy range
- implementation default is `92` for all vitals to make the evolution loop realistically reachable in ordinary play
- status begins as `normal`
- reaction text welcomes the player

## Tick Rules

While the app is open, the system must update on a fixed cadence.

Locked rule:

- one simulation tick every `2` seconds

Per tick default decay:

- hunger: `-3` every tick
- happiness: `-3` every tick
- energy: `-3` every tick

These values are the locked MVP decay rates and are reflected in the implementation. They create a much faster, more arcade-like loop where care decisions need to happen quickly.

## Clamping Rules

- no vital may fall below `0`
- no vital may rise above `100`
- every state update must clamp values before derived logic runs

## Threshold Rules

- if any one vital is `<= 25`, ChuChu is `at risk`
- if any two vitals are `<= 25`, ChuChu becomes eligible for `sick`
- if all vitals are `>= 80` for a sustained period defined in the state progression spec, ChuChu becomes eligible for `evolved`
- if an evolution run is already active, quick recovery actions may preserve that run between ticks as long as all vitals stay `>= 70`

## Derived Indicators

The simulation should expose at least:

- `needsAttention`
- `criticalVitals`
- `evolutionProgress`

These are helper signals for rendering and messaging and must be derived from the source vitals, not stored independently.

## Elapsed Time Handling

When the app resumes after inactivity:

- the system must compute elapsed time from `lastUpdatedAt`
- the same rule set used for live ticks should be applied in bulk
- offline decay should be capped to avoid wiping out the pet from one long absence

Locked cap:

- maximum simulated offline decay window: `8` hours

## Acceptance Criteria

- a fresh session shows healthy vitals for ChuChu
- waiting without interaction causes visible stat decline
- vitals never exceed bounds
- reopening the app after time has passed reflects elapsed decay
- the simulation rules can be tested without rendering the full UI
