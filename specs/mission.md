# Tiny Tamagotchi MVP Mission

## Project Goal

Build a small web-based virtual pet named `ChuChu` using a spec-driven workflow so the specification is clear enough that implementation can follow it with minimal ambiguity.

This project is being shaped for the DeepLearning.AI Tiny Tamagotchi MVP challenge, where the primary artifact is the quality of the spec and the implementation is proof that the spec is actionable.

## Problem Statement

Many tiny demos show isolated UI interactions but do not feel alive. `ChuChu` should feel like a living companion through a simple, readable loop:

- vitals decay over time
- the player responds with care actions
- the pet visibly reacts to good or poor care
- the system stays understandable enough for a reviewer to trace behavior from spec to code

## Target User

The primary user is a casual player who wants a short, charming interaction that can be understood in seconds without onboarding.

The secondary audience is a reviewer evaluating whether:

- the product scope is disciplined
- the behavior rules are explicit
- the implementation follows the documented intent

## Product Promise

Within one short session, the player should be able to:

1. understand ChuChu's needs at a glance
2. take meaningful actions to improve those needs
3. observe state changes caused by time and care quality
4. discover at least a few personality moments that make ChuChu memorable

## Core User Flow

The intended MVP user flow is:

1. open the app and see ChuChu's current vitals and macro state
2. notice whether ChuChu needs attention through bars, status, and reaction text
3. choose `Feed`, `Play`, or `Rest` based on the visible need
4. observe immediate stat changes and reaction feedback
5. return later and see backend-persisted progress, including elapsed-time decay
6. continue caring until ChuChu either recovers from neglect or permanently evolves

## Success Criteria

The MVP is successful when all of the following are true:

- `ChuChu` exposes three core vitals: Hunger, Happiness, and Energy.
- Vitals automatically change over time without requiring page refresh.
- The player can use `Feed`, `Play`, and `Rest` to influence the vitals.
- The pet clearly communicates at least three macro states: `Normal`, `Sick`, and `Evolved`.
- The app feels coherent as a single playable loop rather than a set of disconnected buttons.
- The repository contains constitution and feature-level specs aligned with implementation and validation artifacts.

## Non-Goals For MVP

The first release does not need:

- multiplayer or social mechanics
- authentication or user accounts
- cloud sync
- complex inventory systems
- breeding, death, or irreversible punishment loops
- a large content library of animations or mini-games

## Edge Cases And Failure Handling

The MVP must handle these cases safely:

- first launch when no persisted pet record exists
- refresh or reopen after elapsed time has passed
- repeated rapid action clicks without breaking stat bounds
- invalid or corrupted persisted pet data
- explicit user reset of the single global ChuChu save

## Product Principles

- `Readable over clever`: behavior should be easy to explain from the spec.
- `Small but alive`: limited scope is acceptable if the pet has personality.
- `Immediate feedback`: each action should trigger a visible or textual response.
- `Forgiving loop`: the MVP should encourage recovery instead of punishing mistakes too harshly.
- `Spec is source of truth`: if code and spec disagree, the spec wins until deliberately updated.

## Approved Experience Direction

The approved direction for the first implementation pass is:

- one screen experience
- `minimal modern` visual language
- short response text from ChuChu
- evolution earned through consistently good care rather than elapsed wall-clock time
- permanent evolution once achieved

## Confirmed Product Decisions

- Tiny Tamagotchi will live as a `standalone app`
- persistence will be `backend-backed`
- the design style is `minimal modern`
- evolution is triggered by `good care only`
- evolution is `permanent`

## Remaining Decisions Before Implementation

The remaining implementation decisions were resolved by proceeding with the recommended defaults:

- backend persistence layer: `SQLite`
- save model: `single global ChuChu save`
- pet presentation: `stylized UI avatar system`
- offline decay: `capped at 8 hours`
