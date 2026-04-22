# Tiny Tamagotchi API

Backend service for the `ChuChu` Tiny Tamagotchi MVP.

## Local Run

```powershell
pip install -e .[dev]
uvicorn app.main:app --reload --port 8102
```

## API

- `GET /api/v1/pet`
- `POST /api/v1/pet/actions`
- `POST /api/v1/pet/reset`
