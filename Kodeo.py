import urllib, json
from pprint import pprint
from datetime import datetime
import time
from flask import Flask,request,jsonify
import os

app = Flask(__name__)

@app.route('/')
def firstPage():
	return "Hello World"

@app.route('/getpointsForUser')
def api_hello():
	points = 0
	client_id = "39c9aaea6e3c93cc9247"
	client_secret = "01203f23db09a26aa448511f9c0ddd68a2f7ad43"
	user = request.args['user']
	date2Str = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%dT%H:%M:%SZ')
	currentDate = datetime.strptime(date2Str,'%Y-%m-%dT%H:%M:%SZ')

	for i in range(0,10):
		url = "https://api.github.com/users/" + user + "/events?page=" + str(i) + "&client_id=" + client_id + "&client_secret=" + client_secret
		print url
		response = urllib.urlopen(url)
		data = json.loads(response.read())
		print len(data)

		dateStr = data[0]["created_at"]
		commitDate = datetime.strptime(dateStr,'%Y-%m-%dT%H:%M:%SZ')
		if abs(currentDate - commitDate).days >= 10:
			break	
		
		for commit in data:
			payload = commit["payload"]
			commitType = commit["type"]
			print commitType
			if commitType == "PushEvent":
				points += 3
			elif commitType == "PullRequestEvent":
				points += 4
			elif commitType == "CommentEvent":
				points += 1
			elif commitType == "IssueEvent":
				points += 2
	return "points: " + str(points)

if __name__ == '__main__':
    app.run()