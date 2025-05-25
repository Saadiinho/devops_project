from fastapi import FastAPI

app = FastAPI()

__version__ = "1.0.0"


@app.get("/healthcheck")
def root():
    return {"name": "devops_project API", "version": __version__, "status": "running"}
