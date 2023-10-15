
from fastapi import Request

from components import *

def login_page():
	return base_html("CFA Suite | Login", f'''
		{banner(team_nav_menu())}
		{team_footer()}
	''')

def talent_page():
	return base_html("CFA Suite | Talent Engagement", f'''
		{banner(team_nav_menu())}
		{team_footer()}
	''')

def cem_page(request: Request):
	timescale_variant = request.query_params.get('timescale')
	if timescale_variant == None:
		timescale_variant = 'current_month'
	return base_html("CFA Suite | Customer Service", f'''
		{banner(team_nav_menu())}
		{cem_widget(timescale_variant)}
		{form_update_cem_score()}
		{team_footer()}
	''')

def sales_page():
	return base_html("CFA Suite | Sales & Brand Growth", f'''
		{banner(team_nav_menu())}
		{team_footer()}
	''')

def finance_page():
	return base_html("CFA Suite | Financial Stewardship", f'''
		{banner(team_nav_menu())}
		{team_footer()}
	''')