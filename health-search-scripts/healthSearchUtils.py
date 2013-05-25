from xml.dom import minidom
import pickle
import time
from pymongo.connection import Connection
from bson.objectid import ObjectId
import re
import credentials

collection_indices = "indices"
collection_case_reports = "case_reports"
MY_DB_CONNECTION_STRING = credentials.DB_CONNECTION_STRING
#test
connection = None # Connection('mongodb://sbose78:ECDW=19YRS@staff.mongohq.com:10068/BOSE')
def generate_case_report_file():	
	xmldoc = minidom.parse('downloaded.xml')
	#print str(xmldoc)
	itemlist = xmldoc.getElementsByTagName('oai_dc:dc')
	print len( itemlist)
	for health_issue in itemlist :
		 title = health_issue.getElementsByTagName('dc:title')
		 title = title[0].childNodes[0].data 
		 print title

		 date = health_issue.getElementsByTagName('dc:date')
		 date = date[0].childNodes[0].data 
		 print date
		 #print my_issue[0].childNodes[0].data

		 url = health_issue.getElementsByTagName("dc:identifier")
		 url = url[0].childNodes[0].data
		 print url

		 health_issue_id = url.split('/')
		 health_issue_id = health_issue_id[len(health_issue_id)-1]
		 print health_issue_id

		 description = health_issue.getElementsByTagName("dc:description")
		 if len(description) > 0:
		 	description = description[0].childNodes[0].data
		 	if len(description)>0:
		 		print description
		 	else: 
		 		description = "NULL"
		 else:
		 	description = "NULL"

		 health_issue_json = { 
		 "title" : title , "date" : date , "description" :description , 
		 "url" : url
		 }
		 #file_name = "case_reports_bmj/"+title+str(time.time())+".htxt"
		 #pickle.dump(health_issue_json , open(file_name,"wb"))

		 insert_into_db(health_issue_json)

		 # testing if the file has been written by 
		 # reading it back and printing to console.
		 #read_health_issue = pickle.load(open(file_name,"rb"))
		 #read_health_issue = read_health_issue['description']
		 #read_health_issue1 =read_health_issue.encode('utf-8')# read_health_issue.encode('utf-8')

		 #print read_health_issue,"************************"

def getFileList():
	import glob
	return glob.glob("case_reports_bmj/*.htxt")

def updateIndex():
	all_files = getFileList()
	for case_report in all_files :
		full_file_path = case_report
		case_report_file = open(full_file_path,"rb")
		print pickle.load(case_report_file)
	#print all_files

def getConnection():
	global connection
	if connection != None and connection.alive() == False :
		connection = Connection(MY_DB_CONNECTION_STRING)
	elif connection == None:
		connection = Connection(MY_DB_CONNECTION_STRING)
	else:
		pass
	return connection['BOSE']

def insert_into_db(health_issue_json):	
	getConnection()	
	db=connection['BOSE']
	collection = db['case_reports']
	collection.insert(health_issue_json)

# case reports queried by arbitrary condition 
def get_case_report_by_condition(condition):
	db=getConnection()
	collection=db[collection_case_reports]
	case_reports = collection.find(condition)
	return case_reports

# case reports queried by ID
def get_case_report_by_id(case_report_id):
	case_reports = get_case_report_by_condition({"_id": ObjectId(case_report_id)})
	for report in case_reports:
		return report
	return None


def retreive_all_case_reports():
	db=getConnection()
	collection = db[collection_case_reports]
	all_case_reports=collection.find({})
	for a in all_case_reports:
		print a['_id'] , ":" , a['description']
		report_id = a['_id']
		report_id = (str(report_id))
		update_index_by_case_report(a['description'], report_id )


# This function breaks the case report into 
# individual words that could be used for indexing the
# document
def get_tokens_from_case_report(case_report):
	case_report = case_report.strip()
	case_report = case_report.upper()
	tokens = re.split('[;,\'\\)^. (=-]',case_report)
	unique_set = set()
	for token in tokens :
		if len(token) >2 :
			unique_set.add(token)
		else:
			pass
	return tokens

# the full case report is passed to 
# this function. This function updates the
# indices accordingly.
def update_index_by_case_report(case_report,case_report_id):
	case_report = case_report.upper()
	tokens = get_tokens_from_case_report(case_report)
	for token in tokens:
		update_index_by_word(token,case_report_id)
'''
def index_case_report():
	db=getConnection()
	collection = db['test']

	indexes= ["1101","1124"]	
	bio_term = { "name":"heart" , "index":indexes}
	collection.insert(bio_term)
'''

def update_index():
	db=getConnection()
	collection=db['test']
	all_case_reports = collection.find({"name":"heart"})
	for case_report in all_case_reports:
		indexes = case_report['index']
		indexes.append("5555")
		collection.update({"name":"heart"}, {"$set": {"index":indexes}})

def update_index_by_word(word,index):
	db=getConnection()
	collection=db[collection_indices]
	collection.update({"name":word},{"$push" : {"index":index}})

# The word is added to the index
def add_new_word(word):
	db=getConnection()
	collection=db[collection_indices]
	my_index=[]
	collection.insert({"name":word.upper(),	"index": my_index})
#add_new_word('leg')

# This function adds all the health issues 
# into the mongodb.
def create_index():
	unique_set = set()
	count = 0
	f=open("word_list.txt","r")
	#full_text = 
	for line in f:
		#print line
		medical_terms = is_medical_term(line)
		#print line
		if medical_terms != None :
			for term in medical_terms :
				
				term = term.strip()
				if(len(term)==0):
					continue
				else:
					term = term.upper()
					count=count+1
					print count, ":",term
					unique_set.add(term)
		else:
			pass
	print len(unique_set)
	print unique_set

	for medical_term  in unique_set :
		add_new_word(medical_term)

# this function checks whether a specific word should
# be present in the index
def is_medical_term(line_from_text):
	line_from_text = line_from_text.strip()
	tokens = re.split('[;,\'\\)^. (=-]',line_from_text)
	filtered_tokens=set()
	for word in tokens :
		#print word
		if word.isupper()==True and len(word)>3:
			filtered_tokens.add(word)
		elif len(word)>3: 
			filtered_tokens.add(word)
		else:
			pass
	return filtered_tokens

def rank_case_reports(search_key):
	indices_map_by_health_term = get_indices_of_health_terms_from_search_key(search_key)
	case_vs_count_map={}
	case_vs_count_map_ranked={}

	# Iterate all the mappings by key-value where 
	# keys are the biological terms in the search key

	for index in indices_map_by_health_term:
		index_set = indices_map_by_health_term[index]
		#print index_set 

		for case in index_set:
			case = str(case)

			# the if-else could be replaced by
			# case_vs_count_map[case]+=1  ?

			if case_vs_count_map.get(case) == None :
				case_vs_count_map[case]=1
			else : 
				count = case_vs_count_map[case]
				count = count +1
				del case_vs_count_map[case]
				case_vs_count_map[case]=count
	print case_vs_count_map
	ranks =[]

	# get the order of the dictionary by value
	for w in sorted(case_vs_count_map, key=case_vs_count_map.get, reverse=True):
  		print w, case_vs_count_map[w]
  		#case_vs_count_map_ranked[w]  = case_vs_count_map[w]
  		ranks.append(w)

  	# add the "order" information to make the ranking make sense
  	case_vs_count_map_ranked['order']=ranks
  	case_vs_count_map_ranked['cases']= case_vs_count_map
  	print case_vs_count_map_ranked
  	return case_vs_count_map_ranked
	



#controller function
def get_indices_of_health_terms_from_search_key(search_key):
	tokens = get_tokens_from_case_report(search_key)
	map_of_health_term_to_index={}
	for token in tokens :
		index_set = get_indices_by_health_term(token)
		if len(index_set) != 0:
			map_of_health_term_to_index[token]= index_set
		else: 
			pass
	print map_of_health_term_to_index
	return map_of_health_term_to_index

# this function fetches the case reports 
# which contains the specific health term

def get_indices_by_health_term(medical_term):
	db=getConnection()
	collection = db[collection_indices]
	my_indices=collection.find({"name":medical_term})
	for my_index in my_indices:
		return my_index['index']
	return []

def get_search_results(case_report_description):
	similar_cases= rank_case_reports(case_report_description)
	case_IDs_sorted_by_relevance = similar_cases['order']
	case_details_sorted_by_relevance = []

	for case_id in case_IDs_sorted_by_relevance :
		case_details  = get_case_report_by_id(case_id)
		case_details_sorted_by_relevance.append(case_details)

	return case_details_sorted_by_relevance
def format_search_results(case_details_sorted_by_relevance):
	for result in case_details_sorted_by_relevance:
		print "TITLE :  ", result['title']
		print "URL :  ", result['url']
		print "\n\n\n"


def main():
	#update_index_by_case_report("fever aaaaa nose")
	#retreive_all_case_reports()
	#create_index()
	#print get_indices_by_health_term("PULMONARY")
	#get_indices_of_health_terms_from_search_key("She presented with ,diarrhoea and rectal bleeding and was found to have multiple pleomorphic ulcers with a patchy cobblestone mucosa on sigmoidoscopy")
	#rank_case_reports("She presented with ,diarrhoea and rectal bleeding and was found to have multiple pleomorphic ulcers with a patchy cobblestone mucosa on sigmoidoscopy")	
	#generate_case_report_file()	
	#print get_case_report_by_id('519efbbe3324f21e47fe526f')
	format_search_results(get_search_results("A young man was brought for mental retardation, frequent non-bloody diarrhoea"))
	#get_search_results("Two months back while physical activity, I was hurt at my waist which I came to understand the next day, pain started after 3 days and gradually got worse. I cannot walk without support and at present I have immense pain in my waist and knee")

main()