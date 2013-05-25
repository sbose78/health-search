The health case reports' similarity prediction
================================================


WHAT this service aims to accomplish
--------------------------------------------

This REST-styled webservice will be used for 
- training the system 
- Prediction of similiar health case reports.


WHY
----

For assisting care-givers by letting them take a look at previously discussed similar/related documented health issues.


HOW - The interface
---------------

Add a new health case report to the search index:

	POST http://<server-host>/index

	Request Parameters :
	- URL 
	- Title
	- Description

	Response format :

	content-type : application/json
	body :
	{
		status : "OK"	
	}



Find out similar health cases ( or case reports or health issues) :

	POST http://<server-host>/similarity

	Request Parameters:
	-Description 

The objective of having a webservice is to make sure the system can be extended as in, 

- A simple interface to allow adding of more case reports one-by-one or as a batch process.
- An embeddable solution where any website or healthcare platform would be able to display similar case reports on their own website.

Storage
---------

The case reports are stored in documents in a MongoDB database ( plumbing done by Mongohq.org ).
To make sure performance doesn't fall due to opening of new connections, the application checks
if there's an alive connection , failure of which makes the application instantiate a new 
database connection.

Initially, I had decided to save case reports in serialized documents ( using Pickle ) but threw away what I built realising that it became too inconvenient to deploy the application executable without 
moving the data around.

The  MongoDB database uses 2 collections :

- case_reports : In this collection, each document stores the URL , title and description of the case 				   report.
- indices : In this collection, each document stores a unique medical term and its corresponding Set (			 list of unique members ) of document IDs of case reports which feature that medical term.


Web framework 
---------------

I used Django on Openshift to write my application in Python.
Use of Django meant easy harnessing of its out-of-the-box REST-style URL mapping.


URL
----

http://journal.sbose.in


Technologies used for building
-------------------------------

- Server-side scripting : Python ,
- Web framework :  Django ,
- Application hosting:  Openshift Django
- Database : MongoDB hosted on www.MongoHQ.org

Developer tools:

- Sublime Text

Installation
--------------

- Clone the repository
- The Openshift-deployable app can be found at web/health-search/...
  Add a file named "credentials.properties" under wsgi/openshift/
- To a "python manage.py runserver " at wsgi/openshift in the commandline
- The 