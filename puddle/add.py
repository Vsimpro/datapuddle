import json, uuid, time, sqlite3
from flask import Blueprint, jsonify, request

from database import main    as sqlite
from database import queries as sqlite_queries


ENDPOINT = "/api/puddle/"
PUDDLE_ADD   = Blueprint( "puddle_add", __name__, url_prefix = ENDPOINT )


@PUDDLE_ADD.route( "/health" ) 
def health(): return jsonify( { "status" : "ok" } ), 200


#
#   Interface
#
@PUDDLE_ADD.route( "/add",  methods = [ "POST" ] )
@PUDDLE_ADD.route( "/add/", methods = [ "POST" ] )
def add_data():
    """
    Endpoint:
        POST /api/add/all      \n
        
    
    Takes a JSON object of the following format: \n
    Required:  
        "source" : <STRING> (telegram, rss, forum, ..)  \n
        "type"   : <STRING> (json, har, txt, ...)       \n
        "raw_data" : <BYTEA> (the raw data)             \n

        
    Optional: 
        "original_filename" : <STRING> (dump.sql, dump.txt, index.html) \n
        "content_type" : <STRING> (application/json, application/xml)   \n
        "timestamp" : <STRING> (2025-12-01, 1971-01-01)                 \n
        "raw_text" : <STRING> (raw data formatted into UTF-8)           \n
        "zone" : <STRING> (raw, cleaned, curated)                       \n
        "owner" : <STRING> (who gave the data, who handles the data)    \n
    """
    
    data : dict = {
        # Required:  
        #   "source" : <STRING> (telegram, rss, forum, ..) 
        #   "type"   : <STRING> (json, har, txt, ...)
        #   "raw_data" : <BYTEA> (the raw data)

        # Optional: 
        #   "original_filename" : <STRING> (dump.sql, dump.txt, index.html)
        #   "content_type"      : <STRING> (application/json, application/xml)
        #   "timestamp"         : <STRING> (2025-12-01, 1971-01-01)
        #   "raw_text"          : <STRING> (raw data formatted into UTF-8)
        #   "zone"              : <STRING> (raw, cleaned, curated)
        #   "owner"             : <STRING> (who gave the data, who handles the data)   
    }
    success : bool = False 
    data    : json = request.get_json()
    
    # Check that required fields are present
    try:
        data[ "source" ], data[ "type" ], data[ "raw_data" ]
    except KeyError:
        return jsonify( { "status" : "required fields not met" } ), 406
    
    data_id     = str(uuid.uuid4())
    ingested_at = int(time.time() * 1000)
    
    # Required fields
    source    = data[ "source" ]
    raw_data  = data[ "raw_data" ]
    data_type = data[ "type" ]
    
    # Optional fields
    zone              = None
    owner             = None
    raw_text          = None
    timestamp         = None
    content_type      = None
    original_filename = None
    
    # If data has these fields, use them
    if "zone"              in data: zone              = data[ "zone" ]
    if "owner"             in data: owner             = data[ "owner" ]
    if "raw_text"          in data: raw_text          = data[ "raw_text" ]
    if "timestamp"         in data: timestamp         = data[ "timestamp" ]
    if "content_type"      in data: content_type      = data[ "content_type" ]
    if "original_filename" in data: original_filename = data[ "original_filename" ]
    
    
    try:
        
        success = sqlite.insert_data(
            sqlite_queries.insert_into_puddle,
            (
                data_id, 
                ingested_at, 
                source, 
                data_type, 
                original_filename, 
                content_type, 
                timestamp, 
                raw_data,
                raw_text, 
                zone, 
                owner
            )
        )
        
    except sqlite3.Error as e:
        print( f"[SQLITE3] Could not insert data. Error: ", e )
        return jsonify( { "status" : "error" } ), 500
    
    # Double check for errors.
    if -1 == success:
        return jsonify( { "status" : "error" } ), 500
    
    # Data added!
    return jsonify( { "status" : "ok" } ), 201

