
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

from components import *
from pages import *
from utility import *

load_dotenv()
app = FastAPI()
app.mount("/static", StaticFiles(directory="../static"), name="static")

@app.get("/")
async def get_login_page_html(request: Request):
    return HTMLResponse(content=login_page())

@app.get("/talent")
async def get_talent_page_html(request: Request):
    return HTMLResponse(content=talent_page())

@app.get("/cem")
async def get_cem_page_html(request: Request):
    return HTMLResponse(content=cem_page(request))

@app.get("/sales")
async def get_sales_page_html(request: Request):
    return HTMLResponse(content=sales_page())

@app.get("/finance")
async def get_finance_page_html(request: Request):
    return HTMLResponse(content=finance_page())

@app.get('/components/cem_score')
async def get_cem_score_html(request: Request):
	return HTMLResponse(content=cem_score(request))

@app.post('/action/update/cem')
async def update_cem_scores(request: Request, timescale: str = Form(...), osat: str = Form(...), taste: str = Form(...), speed: str = Form(...), ace: str = Form(...), cleanliness: str = Form(...), accuracy: str = Form(...), password: str = Form(...)):
    real_timescale = ['current_month', 'three_month_rolling', 'year_to_date']
    if timescale not in real_timescale:
        return RedirectResponse(f'/cem', status_code=303)
    cem_data = json_read('./data/cem.json')
    filtered_by_timescale = cem_data[timescale]
    filtered_by_timescale['osat'] = osat
    filtered_by_timescale['taste'] = taste
    filtered_by_timescale['speed'] = speed
    filtered_by_timescale['ace'] = ace
    filtered_by_timescale['cleanliness'] = cleanliness
    filtered_by_timescale['accuracy'] = accuracy
    json_write(cem_data, './data/cem.json')
    return RedirectResponse(f'/cem?timescale={timescale}', status_code=303)
