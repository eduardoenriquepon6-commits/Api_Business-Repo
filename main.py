import uvicorn 
from fastapi import FastAPI
from routes.usuarios import router as router_usuarios

app = FastAPI()

app.include_router(router_usuarios)

@app.get("/")
def read_root():
    return {"Hello": "Customer!"}



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")