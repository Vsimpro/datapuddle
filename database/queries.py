"""
NOTES: Mass storage queries. 

For the storage to be efficient, certain metadata is needed:
- time
- source
- type
- content type
- original file name

And of course the data:
- raw_data (raw)
- raw_text (utf-8, if possible)

Nice to haves:
- zone (raw / cleaned / curated)
- owner
"""


#
#   Main data puddle table
#
create_puddle_table = """
CREATE TABLE IF NOT EXISTS data_puddle (
    id                UUID      PRIMARY KEY,
    ingested_at       TIMESTAMP NOT NULL,   -- timestamp of the data being logged into the system
    source            TEXT      NOT NULL,   -- where the data came from (telegram, scraper, rss)
    type              TEXT      NOT NULL,   -- type of the data, (json, har, txt) 
    original_filename TEXT,                 -- if available, store the original filename
    content_type      TEXT,                 -- the mimetype of the content
    timestamp         TEXT,                 -- if know, the original timestamp of the data (LinkedIn dump from 2012)

    raw_bytes         BYTEA     NOT NULL,   -- raw bytes of the data. 
    raw_text          TEXT,                 -- raw bytes turned into text, if possible.

    zone              TEXT DEFAULT 'raw',   -- is data RAW, CLEANED, or CURATED.  
    owner             TEXT                  -- Who owns the data (vs1m, Vsimpro, Ville)
);
"""


select_regex_match_eveything = """
SELECT id FROM data_puddle WHERE raw_text ~* ?
"""
"""SELCT id .. WHERE <REGEX> """


#
#   Access tokens
#
create_access_tokens = """
CREATE TABLE IF NOT EXISTS access_tokens (
    id     UUID PRIMARY KEY,
    name   TEXT NOT NULL,
    active INTEGER
);
"""