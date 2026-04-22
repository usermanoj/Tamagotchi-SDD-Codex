# Validation: Care Actions And Feedback

## Automated Checks

Add checks for:

- each action's stat delta
- clamping after high-value recovery
- trade-off application for each action
- reaction text selection fallback

## Manual Checks

1. Use `Feed` from a low-Hunger state and confirm visible recovery.
2. Use `Play` several times and confirm Happiness rises while Energy falls.
3. Use `Rest` from a low-Energy state and confirm recovery.
4. Rapidly click actions and confirm the UI stays stable.
5. Confirm reaction text changes across at least a few different actions or conditions.

## Failure Conditions

- an action updates the wrong vital direction
- all three actions feel equivalent
- feedback appears delayed or confusing
- repeated actions create impossible values
