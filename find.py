import json
import requests

from database import main    as db
from database import queries as q


URL = "http://localhost:5000/api/puddle/regex"

def send_regex(regex_rule: str):
    payload = {
        "regex": regex_rule
    }

    response = requests.post(URL, json=payload)

    print("Status:", response.status_code)
    try:
        print("Response:", response.json())
    except ValueError:
        print("Response text:", response.text)


if __name__ == "__main__":
    db.initialize_db({
        "Datapuddle" : q.create_puddle_table,
        "Tokens"     : q.create_access_tokens
    })
    
    r = db.query_database("SELECT id, raw_bytes FROM data_puddle")
    print( "\n\n".join([str(l[0]) + " " + str(l[1]) for l in r]) )
    
    # Example regex rules
    regex_rules = [
        # vsim.xyz
        "^vsim\\.xyz$",

        # example@gmail.com
        "\\bexample@gmail\\.com\\b",

        # ends with @gmail.com
        "\\b[A-Za-z0-9._%+-]+@gmail\.com\\b",

        # database (whole word)
        "\\bdatabase\\b",

        # lorem ipsun (phrase)
        "(?i)lorem\\s+ipsun"
    ]


    for rule in regex_rules:
        print(f"\nSending regex: {rule}")
        send_regex(rule)