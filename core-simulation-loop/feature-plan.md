# Feature Plan: Core Simulation Loop

## Goal

Define the living systems that make ChuChu feel alive even before polish and personality layers are added.

## User Story

As a player, I want to glance at ChuChu and understand whether care is needed so I can respond before the pet declines.

## In Scope

- three vitals: Hunger, Happiness, Energy
- stat ranges and clamping rules
- automatic tick-based updates while the app is open
- threshold logic for risk conditions
- derived summary state inputs used by later features

## Out Of Scope

- action buttons and their UI polish
- persistent storage details
- elaborate animation systems
- evolution visuals

## Functional Summary

The system should maintain a pet state object with:

- current vitals
- current macro state
- last updated timestamp
- last reaction text
- derived flags such as `needsAttention`

The loop should apply periodic decay so that:

- Hunger trends downward over time
- Happiness trends downward over time
- Energy trends downward over time, but usually more slowly than active play costs

## Dependencies

- approved stat ranges
- approved decay rates
- approved interpretation of low-stat thresholds

## Risks

- decay that is too aggressive will make the game stressful
- decay that is too weak will make the pet feel static
- mixing UI timing with rules could make testing brittle

## Definition Of Done

- the simulation loop can run independently of the UI styling
- stat decay is deterministic and documented
- low-stat thresholds are explicit
- the game state can be inspected and reasoned about from code and spec
