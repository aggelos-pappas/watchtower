from fastapi import FastAPI

app = FastAPI(title="Watchtower")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
