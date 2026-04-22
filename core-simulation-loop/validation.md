# Validation: Core Simulation Loop

## Automated Checks

Add logic-level checks for:

- default pet state creation
- one-tick decay application
- multiple-tick bulk decay application
- lower and upper clamping
- threshold flag derivation

## Manual Checks

1. Launch the app and confirm ChuChu begins with healthy vitals.
2. Leave the app untouched long enough for at least two visible updates.
3. Confirm vitals visibly decrease without user action.
4. Refresh the page and confirm the pet resumes from stored state rather than resetting.
5. Simulate longer elapsed time and confirm offline decay respects the cap.

## Failure Conditions

- stats drift outside `0-100`
- the pet resets unexpectedly on refresh
- decay depends on frame rate or animation timing
- threshold flags disagree with visible values
