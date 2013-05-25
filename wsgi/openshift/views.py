import os
from django.shortcuts import render_to_response
from django.http import HttpResponse
import json
import urllib2
import pymongo
from bson import BSON
from bson import json_util
#import simplejson as sjson
import healthSearchUtils


def home(request):
    return render_to_response('home/index.html')

def get_search_results(request):
	report = request.POST["report"]
	print report
	search_results = healthSearchUtils.get_search_results(report)
	#search_results = healthSearchUtils.makeJSONSerializable(search_results)
	
	return HttpResponse(json.dumps(search_results, sort_keys=True, indent=4, default=json_util.default),mimetype="application/json")
def add_new_report(request):
	title = request.POST["title"]
	url = request.POST["url"]
	description = request.POST["description"]

	health_issue_json = {
		"title":title,
		"url":url,
		"description":description
	}

	object_id=healthSearchUtils.insert_into_db(health_issue_json)

	generated_response={
		"ID":str(object_id) ,
		"title":title,
		"URL":url,
		"Description":description
	}

	return HttpResponse(json.dumps(generated_response, sort_keys=True, indent=4, default=json_util.default),mimetype="application/json")
