from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root_url():
    return {"message":"hello world"}