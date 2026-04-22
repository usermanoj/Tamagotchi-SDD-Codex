# Requirements: Persistence And Presentation Shell

## Persistence

The app must:

- save pet state to the backend after every meaningful state change
- restore pet state from the backend on page load
- compute elapsed time since the last persisted update
- handle invalid or missing persisted data by falling back to a fresh pet state safely

## Backend Contract

The backend must support at least:

- fetching the current ChuChu state
- applying a named care action
- resetting ChuChu to a fresh state
- persisting a single global ChuChu record in `SQLite`
- deriving elapsed-time decay on read before returning state to the frontend

The backend is the authority for:

- elapsed-time simulation
- action effects
- state transitions
- persistence writes

## Layout

The MVP should fit on one main screen and include:

- pet display area
- current macro state
- three vitals
- action controls
- reaction text area
- optional session summary such as elapsed care time or evolution progress

## Visual Direction

Approved direction:

- `minimal modern`
- clean cards, strong spacing, restrained color palette
- enough visual distinction to make the demo memorable without a toy-like cluttered UI

## Reset Behavior

Include one simple reset control for demo purposes.

Reset rules:

- clearly restarts ChuChu from the initial state
- asks for confirmation before wiping the current pet

## Acceptance Criteria

- refreshing the page does not reset progress unexpectedly
- the main screen is understandable without instructions
- the pet area, vitals, and actions are visually grouped
- reset is available but not easy to trigger by accident
