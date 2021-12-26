from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from static.responses import HTMLContent

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
async def root():
    return HTMLContent.hello()
