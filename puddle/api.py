from flask import Blueprint, jsonify


ENDPOINT = "/api/puddle/"
PUDDLE   = Blueprint( "puddle" , __name__, url_prefix = ENDPOINT )


@PUDDLE.route( ENDPOINT + "health" ) 
def health(): return jsonify( { "status" : "ok" } ), 200

