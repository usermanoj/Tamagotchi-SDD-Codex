# Feature Plan: Care Actions And Feedback

## Goal

Turn the passive simulation into an interactive care loop that lets the player keep ChuChu healthy.

## User Story

As a player, I want a few clear actions that improve different needs so I can make meaningful care decisions instead of clicking randomly.

## In Scope

- `Feed`, `Play`, and `Rest` actions
- per-action stat effects
- reaction text or small feedback after actions
- simple balancing rules to prevent obviously broken loops

## Out Of Scope

- inventory items
- monetization or scoring systems
- large animation libraries

## Design Intent

Each action should have a benefit and at least one trade-off so the loop feels game-like:

- `Feed` restores Hunger strongly
- `Play` restores Happiness but costs Energy
- `Rest` restores Energy but should not solve every problem at once

## Definition Of Done

- all three actions produce immediate feedback
- actions update the simulation through a single rule layer
- repeated button presses cannot break stat bounds
- trade-offs are visible enough that the player can learn the system
