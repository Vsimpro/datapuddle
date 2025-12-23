import json, uuid, time, sqlite3
from flask import Blueprint, jsonify, request

from database import main    as sqlite
from database import queries as sqlite_queries


ENDPOINT    = "/api/puddle/"
PUDDLE_FIND = Blueprint( "puddle_find", __name__, url_prefix = ENDPOINT )


#
#   Interface
#
@PUDDLE_FIND.route( "/regex",  methods = [ "GET", "POST" ] )
@PUDDLE_FIND.route( "/regex/", methods = [ "GET", "POST" ] )
def find_by_regex():
    """
    Endpoint:
        GET  /api/add/regex      \n
        POST /api/add/regex      \n
        
    
    Takes a JSON object of the following format: \n
    Required:  
        "regex" : <STRING> (regex rule)
    
    Returns:
        `json : list[ UUID ] - all the UUID's that match the regex rule
    
    """

    uuids : list = []
    data  : dict = {
        # Required:  
        #   "regex" : <STRING> (regex rule) 
    }
    regex_rule : str  = None    
    success    : bool = False 
    
    data : json = request.get_json()
    
    # Check that required fields are present
    if "regex" not in  data:
        return jsonify( { "status" : "required fields not met" } ), 406
    
    regex_rule = data[ "regex" ]
    
    try:
        
        rows = sqlite.query_database(
            sqlite_queries.select_regex_match_eveything,
            ( regex_rule, )
        )
        
        uuids = [ row[0] for row in rows ] #[(id,)] -> filter only first indexes of tuples in the list
        
    except sqlite3.Error as e:
        print( f"[SQLITE3] Could not query data. Error: ", e, f" {sqlite_queries.select_regex_match_eveything}" )
        return jsonify( { "status" : "error" } ), 500
    
    # Data fetched!
    return jsonify( uuids ), 201

