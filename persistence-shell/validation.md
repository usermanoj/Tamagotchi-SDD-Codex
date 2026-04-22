# Validation: Persistence And Presentation Shell

## Automated Checks

Add checks for:

- serialization and deserialization of pet state
- fallback to initial state on invalid saved data
- elapsed-time application during restore

## Manual Checks

1. Launch the app for the first time and confirm the screen is understandable.
2. Perform a few actions and refresh the page.
3. Confirm ChuChu resumes from saved state.
4. Corrupt saved data manually and confirm safe recovery.
5. Use the reset control and confirm the app returns to a fresh pet with confirmation.

## Failure Conditions

- loading from storage crashes the app
- the screen feels cluttered or unclear
- a refresh silently wipes state
- reset is destructive without warning
