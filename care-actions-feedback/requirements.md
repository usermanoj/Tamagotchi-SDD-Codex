# Requirements: Care Actions And Feedback

## Actions

The app must expose three primary actions:

- `Feed`
- `Play`
- `Rest`

## Default Effects

Locked action effects:

- `Feed`: hunger `+30`, happiness `+6`, energy `-1`
- `Play`: happiness `+24`, hunger `-4`, energy `-8`
- `Rest`: energy `+30`, hunger `-2`, happiness `-1`

These are the locked MVP action effects and are reflected in the implementation. They are intentionally stronger so the `2`-second decay loop still allows successful care and visible progression into `Evolved`.

## Action Rules

- each action must clamp resulting stats to the legal range
- action effects must apply immediately
- each action must produce a short pet response message
- the response message should match the outcome where practical

## Feedback Rules

The interface should show:

- updated vitals immediately after the action
- a short text reaction from ChuChu
- visual emphasis on the changed state, such as a subtle animation or highlight
- clear evolution guidance, including whether ChuChu is currently in the evolution window or needs quick recovery

## Anti-Spam Rule

For MVP, avoid a heavy cooldown system unless balance demands it.

Preferred rule:

- allow quick repeated inputs
- rely on trade-offs and clamping for balance

If testing shows abuse, add a very short action lock such as `500ms` only for UX stability, not game design.

## Acceptance Criteria

- `Feed` clearly improves Hunger more than the other actions
- `Play` clearly improves Happiness and reduces Energy
- `Rest` clearly improves Energy
- action feedback appears without a page reload
- the game remains understandable after repeated action sequences
