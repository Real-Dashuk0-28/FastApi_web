from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get('/')
def read_root():
    return 'Hello'


@app.get("/calculate")
def calculate(num1: float, num2: float):
    result = num1 + num2
    return {"result": result}


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True, host='127.0.0.1', port=8000)
