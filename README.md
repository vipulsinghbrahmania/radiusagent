# RadiusAgent - Demo

Applink: http://13.234.112.23:8080/

The web-app is developed in Python3.6 over Django2.1 web-framework.
It follows the Model-Template-View.
The template index.html is served as the homepage.
When a link to GithHub repo is entered in the input box, it is manipulated to form a URL to make request to GitHub API.
As the API limits maximum responses to 100 per page. making the API GET/ calls in parallel.
The returned results are then calculated, as per the problem statement, in the View.
Then the output is rendered on the homepage as seperate tiles.
BULMA frontend framework is used to style the webpage.

# Usage:
In the input box, provide the link to GitHub repo(valid), and hit GO!
the real-time counts of the open issues will be populated on the homepage tiles.

# Challenges:
The results for the request are paginated by the GitHub API.
It returns only 30 results (max 100) for any request.
The API query was modified to fetch results from all pages. 

# Improvement Scope:
1. UI could be enhanced to be more responsive and as a single page app.
2. Cross Site Request Forgery could be handled by integrating the CSRF tokens, to filter invalid requests.
3. The open issue counts could be made a link which would further provide more details about the issues.
4. 404/Bad Request pages could be added to enhance the functionality, currently the app only handles valid public GitHub Repos.