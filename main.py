from fastapi import FastAPI, status

app = FastAPI()

@app.get("/")
async def root_path() -> dict:
    return {"massage": "hello world!", "status": status.HTTP_200_OK}
