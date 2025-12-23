"""
*   Datapuddle!
*   -Vs1m, 12/2025
"""
import os, dotenv; dotenv.load_dotenv()
from flask import Flask, Blueprint, abort
from flask_cors import CORS

from puddle.add  import PUDDLE_ADD
from puddle.find import PUDDLE_FIND

from database import main    as sqlite
from database import queries as sql_queries


PORT  = os.getenv( "PORT" )
HOST  = os.getenv( "HOST" )
DEBUG = os.getenv( "DEBUG" )


app = Flask(__name__)
app.register_blueprint( PUDDLE_ADD )
app.register_blueprint( PUDDLE_FIND )

# I'm lazy, let's allow everything! This _cant_ backfire.
CORS(app)


@app.before_request
def check_authentication():
    # While testing, we don't need the authentication tokens.
    #abort(401)
    
    return 


@app.route("/health")
def health_check(): return "200", 200


if __name__ == "__main__":
    # Initialize the database
    sqlite.initialize_db({
        "Datapuddle" : sql_queries.create_puddle_table,
        "Tokens"     : sql_queries.create_access_tokens
    })
    
    app.run( host=HOST, port=PORT, debug=DEBUG )
    