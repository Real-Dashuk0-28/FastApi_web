from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("index.html", 'r', encoding='utf-8') as f:
        html_c = f.read()

    return HTMLResponse(content=html_c)
