import requests
import asyncio
from aiohttp import ClientSession
from datetime import datetime
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


@method_decorator(csrf_exempt, name='dispatch') # csrf bypassed.
def home(request):

	# client and token for the API.
	pay_load = {
	    'client_id': '0c712f8006e232840971',
	    'client_secret': '96416c842ee5944c4fe52bef536f00a74f4a2573',
	}

	headers = { 
	    'content-type': 'application/json' 
	}

	# query the API to get total issues.
	def get_count(query):
	    url = 'https://api.github.com/repos/' + query
	    result = requests.get(url, params=pay_load, headers=headers).json()
	    
	    # per page 100 responses. find the count to loop.
	    # math.ceil implement
	    count = int((result['open_issues_count'] / 100) + ((result['open_issues_count'] % 100) != 0))
	    return count

	async def fetch(url, session): # async method, for each response page
		last_24, seven_24, more_7, total = 0, 0, 0, 0
		async with session.get(url, params=pay_load, headers=headers) as response: # async GET/ call to API
			res = await response.json()
			for i in res:
				if not 'pull_request' in i: # filter pull requests
					total += 1
					x = datetime.strptime(i['created_at'], '%Y-%m-%dT%H:%M:%SZ') # issue create time
					y = datetime.strptime(str(datetime.now()), '%Y-%m-%d %H:%M:%S.%f') # now time
					z = (y-x).total_seconds() # diff time in seconds
					if z < 86400: # less than 24 Hrs
						last_24 += 1
					elif z > 86400 and z < 604800: # more than 24 Hrs, less than a week
						seven_24 += 1
					elif z > 604800: # more than a week
						more_7 += 1
			return [total, last_24, seven_24, more_7] # output for a single response page

	async def run(query, count): # function to create threaded tasks.
	    url = 'https://api.github.com/repos/' + query + '/issues?page={}&per_page=100'
	    tasks = []
	    async with ClientSession() as session: # using user session
	        for i in range(count):
	            task = asyncio.ensure_future(fetch(url.format(i+1), session))
	            tasks.append(task)

	        responses = await asyncio.gather(*tasks) # combining output from all pages
	        return responses
	
	# driver code
	query = request.POST.get('query') # fetch from UI input
	result = None
	
	if query: # non-empty input case
		loop = asyncio.new_event_loop()
		asyncio.set_event_loop(loop)
		count = get_count(query[19:])
		future = asyncio.ensure_future(run(query[19:], count)) # call to run method
		
		x = loop.run_until_complete(future) # complete output as list of lists
		
		keys = ['total', 'last_24', 'seven_24', 'more_7'] # keys for the output dict
		vals = [sum(col) for col in zip(*x)] # values for the output dict
		result = dict(zip(keys, vals)) # forming the output dict		

	# passed to the front-end
	context = {
		'result': result
	}
	
	# render page on request, pass the variables to display
	return render(request, 'stats/index.html', context)
