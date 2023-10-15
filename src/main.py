
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, PlainTextResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError

from components import *
from pages import *
from utility import *
from data import *

load_dotenv()
app = FastAPI()
app.mount("/static", StaticFiles(directory="../static"), name="static")
create_cem_json()

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
async def update_cem_scores(request: Request):
    form = await request.form()
    timescale = form.get('timescale')
    osat = form.get('osat')
    taste = form.get('taste')
    speed = form.get('speed')
    ace = form.get('ace')
    cleanliness = form.get('cleanliness')
    accuracy = form.get('accuracy')
    password = form.get('password')
    if password != os.getenv('CEM_PASSWORD'):
        return RedirectResponse(f'/cem?form_update_cem_err=wrong password', status_code=303)
    if osat == '' or taste == '' or speed == '' or ace == '' or cleanliness == '' or accuracy == '':
        return RedirectResponse(f'/cem?form_update_cem_err=please fill out all the form fields', status_code=303)
    try:
        int(osat)
        int(taste)
        int(speed)
        int(ace)
        int(cleanliness)
        int(accuracy)
    except:
        return RedirectResponse(f'/cem?form_update_cem_err=fields must contain numbers only', status_code=303)
    real_timescale = ['current_month', 'three_month_rolling', 'year_to_date']
    if timescale not in real_timescale:
        return RedirectResponse(f'/cem?form_update_cem_err=umm.. whatcha doin?', status_code=303)
    password = password.lower()
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
