import sqlite3
from flask import Blueprint, jsonify, request

from database import main    as sqlite
from database import queries as sqlite_queries


ENDPOINT    = "/api/puddle/"
PUDDLE_FETCH = Blueprint( "puddle_fetch", __name__, url_prefix = ENDPOINT )


#
#   Interface
#
@PUDDLE_FETCH.route( "/fetch/<id>",  methods = [ "GET" ] )
@PUDDLE_FETCH.route( "/fetch/<id>/", methods = [ "GET" ] )
def fetch_by_id( id : str ):
    """
    Endpoint:
        GET  /api/fetch/<id>      \n
        
            
    Returns:

    
    """

    data    : dict = { }
    success : bool = False 
    
    try:
        
        rows = sqlite.query_database(
            sqlite_queries.select_data_by_id,
            ( id, )
        )
        
        # Check that ID returned results
        if rows == []:
            return jsonify( { "status" : "error" } ), 404
        
        row = rows[0]
        
        # Map data into a dict
        ingested_at, source, datatype, original_filename, content_type, timestamp, raw_bytes, raw_text, zone, owner = \
        row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]
        
        data = { 
            "zone"              : zone,
            "owner"             : owner,
            "source"            : source,
            "datatype"          : datatype,
            "raw_text"          : raw_text,
            "raw_bytes"         : raw_bytes,
            "timestamp"         : timestamp,
            "ingested_at"       : ingested_at,
            "content_type"      : content_type,
            "original_filename" : original_filename,
        }
        
    except sqlite3.Error as e:
        print( f"[SQLITE3] Could not query data. Error: ", e, f" {sqlite_queries.select_regex_match_eveything}" )
        return jsonify( { "status" : "error" } ), 500
    
    # Data fetched!
    return jsonify( data ), 201

