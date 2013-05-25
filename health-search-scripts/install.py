'''
 pre-requisite
 --------------

 Add a "credentials.py" file in this same directory and the database connection string
 in this format

 DB_CONNECTION_STRING = "mongodb://USERNAME:PASSWORD@HOST:PORT/DATABASE"

 Example,

 DB_CONNECTION_STRING = "mongodb://sbose78:my_password@staff.mongohq.com:10068/BOSE"


 Also, make sure the following files are present in the same directory:

 sample-case-reports.xml 
 word_list.txt 

'''
import healthSearchUtils

# Add all the sample case reports to the MongoDB database
healthSearchUtils.generate_case_report_repository()

# Add all the medical keywords to the MongoDB database
healthSearchUtils.create_index()


# Test with a sample search-key
result = healthSearchUtils.get_search_results("A young man was brought for mental retardation, frequent non-bloody diarrhoea")
healthSearchUtils.format_search_results(result)