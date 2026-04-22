# Validation: State Progression And Personality

## Automated Checks

Add checks for:

- transition into `sick`
- recovery from `sick`
- eligibility and transition into `evolved`
- preservation of evolved state if regression is disabled
- personality trigger selection for at least a few rule-based moments

## Manual Checks

1. Let two vitals fall low enough to trigger `sick`.
2. Confirm the pet's visual state changes clearly.
3. Recover the vitals and confirm return to `normal`.
4. Maintain strong vitals and confirm `evolved` can be reached.
5. Trigger at least three special reactions and confirm they feel intentional.

## Failure Conditions

- state changes are hard to perceive
- `sick` is triggered too easily or never
- `evolved` cannot be reached through ordinary play
- personality lines appear disconnected from the pet state
