import os

from fastapi import Request

from utility import json_read

def base_html(title, children):
	fontawesome_tag = os.getenv('FONTAWESOME_TAG')
	return f'''
		<!DOCTYPE html>
		<html lang="en">
		<head>
			<meta charset="UTF-8">	
			{fontawesome_tag}
			<script src="https://unpkg.com/htmx.org@1.9.6"></script>
			<script src="https://unpkg.com/hyperscript.org@0.9.11"></script>
		    <link rel="stylesheet" type="text/css" href="/static/output.css">
			<meta name="viewport" content="width=device-width, initial-scale=1.0">
			<title>{title}</title>
		</head>
		<body hx-boost='true' class='bg-lightgray text-darkgray'>
			{children}
			<script src='/static/bundle.js'></script>
		</body>
		</html>
	'''

def banner(menu):
	return f'''
		<div class='flex h-20 flex-row fixed top-0 w-full justify-between border-b border-lightgray bg-white'>
			<h1 class='text-lg p-6'>CFA Suite</h1>
			<div _='on click toggle .hidden on .banner-group' class='banner-group flex items-center p-6'>
				<i class='fa-solid fa-bars'></i>
			</div>
			<div _='on click toggle .hidden on .banner-group' class='banner-group hidden flex items-center p-6'>
				<i class='fa-solid fa-x'></i>
			</div>
		</div>
		<div class='h-20'></div>
		{menu}
	'''

def team_nav_menu():
	return f'''
		<nav class='banner-group hidden bg-white border-r border-lightgray fixed left-0 w-3/5 h-full'>
			<ul class='flex flex-col m-1 gap-1'>
				{nav_menu_link('Talent Engagement', "/talent")}
				{nav_menu_link('Customer Service', "/cem")}
				{nav_menu_link('Sales & Brand Growth', "/sales")}
				{nav_menu_link('Financial Stewardship', "/finance")}
			</ul>
		</nav>
	'''

def nav_menu_link(text, href):
	return f'''
		<li class='flex rounded' tux-active='{href} bg-lightgray'>
			<a href={href} class='p-6 text-xs w-full'>{text}</a>
		</li>
	'''

def widget_container(content):
	return f'''
		<div class='bg-white p-4 border-l-2 rounded border-t border-b border-gray flex m-2'>
			{content}
		</div>
	'''

def small_loading_indicator(name, href):
	return f'''
		<li class='flex flex-row justify-between items-center'>
			<p>{name}</p>
			<div class='border border-lightgray border-t-darkgray animate-spin rounded-full h-6 w-6' hx-get={href} hx-trigger='load' hx-swap='outerHTML'></div>
		</li>
	'''

def cem_widget(variant):
	current_month_path = '/cem'
	three_month_rolling_path = '/cem?timescale=three_month_rolling'
	year_to_date_path = '/cem?timescale=year_to_date'
	def get_timescale_bar(variant):
		def get_list_item(name, href, active):
			active_class = ''
			if active:
				active_class = 'underline'
			return f'''
				<li class="{active_class}">
					<a href={href}>{name}</a>
				</li>
			'''
		if variant == 'three_month_rolling':
			return f'''
				{get_list_item('Current Month', current_month_path, False)}
				{get_list_item('3 Month Rolling', three_month_rolling_path, True)}
				{get_list_item('Year To Date', year_to_date_path, False)}
			'''
		if variant == 'year_to_date':
			return f'''
				{get_list_item('Current Month', current_month_path, False)}
				{get_list_item('3 Month Rolling', three_month_rolling_path, False)}
				{get_list_item('Year To Date', year_to_date_path, True)}
			'''
		return f'''
			{get_list_item('Current Month', current_month_path, True)}
			{get_list_item('3 Month Rolling', three_month_rolling_path, False)}
			{get_list_item('Year To Date', year_to_date_path, False)}
		'''
	return widget_container(f'''
		<div class='flex w-full flex-col gap-6'>
			<div class='flex w-full justify-between'>
				<h2 class=''>CEM Scores</h2>	
				<div>
					<i class='fa-solid fa-circle-info'></i>
				</div>			 		
			</div>
			<ul class='flex flex-row gap-4 text-xs'>
				{get_timescale_bar(variant)}
			</ul>
			<ul class='text-sm flex flex-col gap-4'>
				{small_loading_indicator("OSAT", f'/components/cem_score?timescale={variant}&metric=osat')}
				{small_loading_indicator("Taste", f'/components/cem_score?timescale={variant}&metric=taste')}
				{small_loading_indicator("Speed", f'/components/cem_score?timescale={variant}&metric=speed')}
				{small_loading_indicator("Ace", f'/components/cem_score?timescale={variant}&metric=ace')}
				{small_loading_indicator("Cleanliness", f'/components/cem_score?timescale={variant}&metric=cleanliness')}
				{small_loading_indicator("Accuracy", f'/components/cem_score?timescale={variant}&metric=accuracy')}
			</ul>	 
		</div>
	''')

def cem_score(request: Request):
	cem_data_dict = json_read('./data/cem.json')
	metric = request.query_params.get('metric')
	timescale_indicator = request.query_params.get('timescale')
	score = cem_data_dict[timescale_indicator][metric]
	return f'''
		<div>{score}</div>
	'''

def form_update_cem_score(err):
	err_html = ''
	if err:
		err_html = f'''<p class='text-xs text-cfared'>{err}<p/>'''
	return widget_container(f'''
		<form method="POST" action='/action/update/cem' class='flex flex-col gap-8 w-full'>
			<div>
				<h2 class='mb-4'>Update CEM Scores</h2>
				{err_html}
			</div>
			<div class='flex flex-col gap-6'>
				<div class='flex flex-row justify-between w-full'>
					<label for='timescale' class='text-xs'>Timescale:</label>
					<select name='timescale' class='text-xs w-2/3 p-1 border border-gray'>
						<option value='current_month'>Current Month</option>
						<option value='three_month_rolling'>Three Month Rolling</option>
						<option value='year_to_date'>Year To Date</option>
					</select>
				</div>
				<div class='flex flex-row justify-between w-full gap-8 items-center'>
					<label for='osat' class='text-xs'>OSAT:</label>
					<input name='osat' type='text' class='text-xs w-2/3 p-1 rounded border border-gray' />		 
				</div>
				<div class='flex flex-row justify-between w-full gap-8 items-center'>
					<label for='taste' class='text-xs'>Taste:</label>
					<input name='taste' type='text' class='text-xs w-2/3 p-1 rounded border border-gray' />		 
				</div>
				<div class='flex flex-row justify-between w-full gap-8 items-center'>
					<label for='speed' class='text-xs'>Speed:</label>
					<input name='speed' type='text' class='text-xs w-2/3 p-1 rounded border border-gray' />		 
				</div>
				<div class='flex flex-row justify-between w-full gap-8 items-center'>
					<label for='ace' class='text-xs'>Ace:</label>
					<input name='ace' type='text' class='text-xs w-2/3 p-1 rounded border border-gray' />		 
				</div>
				<div class='flex flex-row justify-between w-full gap-8 items-center'>
					<label for='cleanliness' class='text-xs'>Cleanliness:</label>
					<input name='cleanliness' type='text' class='text-xs w-2/3 p-1 rounded border border-gray' />		 
				</div>
				<div class='flex flex-row justify-between w-full gap-8 items-center'>
					<label for='accuracy' class='text-xs'>Accuracy:</label>
					<input name='accuracy' type='text' class='text-xs w-2/3 p-1 rounded border border-gray' />		 
				</div>
				<div class='flex flex-row justify-between w-full gap-8 items-center'>
					<label for='password' class='text-xs'>Password:</label>
					<input name='password' type='text' class='text-xs w-2/3 p-1 rounded border border-gray' />		 
				</div>
				<input class='text-xs px-1 py-2 bg-black rounded text-white' type='submit'/>	 
			</div>
		</form>
	''')

def team_footer():
	return f'''
		<div class='h-16'></div>
		<footer class='fixed h-16 bottom-0 bg-white w-full bg-white border-t border-lightgray'>
			<p class='p-4 text-xs'>To have a positive influence on all who come into contact with Chick-fil-A</p>
		</footer>
	'''