# Requirements: State Progression And Personality

## Macro States

ChuChu must support:

- `normal`
- `sick`
- `evolved`

## Sick State Rules

- ChuChu becomes `sick` when at least two vitals are `<= 25`
- ChuChu returns to `normal` after all vitals recover above `40`

When `sick`:

- the pet visual changes to show distress
- reaction text becomes more urgent
- evolution is paused until recovery

## Evolved State Rules

- ChuChu becomes `evolved` after maintaining all vitals `>= 80` for `6` consecutive live or simulated ticks
- evolution progress is evaluated on the simulation ticks, not on every button press
- a supportive care combo may temporarily dip one or more vitals below `80` between ticks without clearing progress
- evolution progress resets only if any vital drops below `70`, or if ChuChu becomes `sick`, before the next qualifying tick

When `evolved`:

- the visual presentation becomes brighter or more celebratory
- reaction text becomes proud or affectionate
- vitals may still decay, but `evolved` status does not regress during the same pet lifecycle

Approved rule:

- once evolved, ChuChu stays evolved permanently unless the player explicitly resets the pet

## Personality Rules

Include at least three personality beats, such as:

- a happy reaction when played with after a long neglect period
- a sleepy comment when Energy is low
- a special line when all vitals exceed `90`

Easter eggs should be:

- lightweight
- readable in code
- triggered by explicit rules rather than randomness alone

## Acceptance Criteria

- ChuChu visibly looks different in `normal`, `sick`, and `evolved`
- poor care can trigger `sick`
- recovery can return ChuChu to `normal`
- strong care can trigger `evolved`
- the interface clearly communicates when the evolution window is open, at risk, or complete
- at least three distinct personality reactions are discoverable
