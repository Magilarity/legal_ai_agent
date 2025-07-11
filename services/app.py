from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Welcome to Legal AI Agent backend"}


@app.get("/healthz")
def health():
    return {"status": "ok"}


@app.get("/analyze/{tender_id}")
def analyze(tender_id: str):
    # ваша логіка аналізу
    return {"tender_id": tender_id, "result": "completed"}
