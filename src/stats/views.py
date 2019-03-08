import requests
from datetime import datetime
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name='dispatch') # csrf bypassed.
def home(request):

	last_24 = 0 
	seven_24 = 0
	more_7 = 0
	count = 1
	total = 0
	
	query = request.POST.get('query')
	if query:
		while True:
			# results limited by API to 100 per page.
			url = 'https://api.github.com/repos/' + query[19:] + '/issues?page=' + str(count) + '&per_page=100'
			res = requests.get(url).json()
			
			if len(res) == 0: # break when no more pages.
				break

			else:
				count += 1
				total += len(res) # count of total issues.
				for i in res:
					x = datetime.strptime(i['created_at'], '%Y-%m-%dT%H:%M:%SZ') # creation time of the issue.
					y = datetime.strptime(str(datetime.now()), '%Y-%m-%d %H:%M:%S.%f') # now time.
					z = (y-x).total_seconds()
					
					if z < 86400: # last 24 hours.
						last_24 += 1
					
					elif z > 86400 and z < 604800: # more than 24 hours and less than a week.
						seven_24 += 1
					
					else: # more than a week.
						more_7 += 1

	result = {
		'total': total,
		'last_24': last_24,
		'seven_24': seven_24,
		'more_7': more_7
	}

	context = {
		'result': result
	}

	return render(request, 'stats/index.html', context)
