from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {"project": "I am learning DevOps"}
