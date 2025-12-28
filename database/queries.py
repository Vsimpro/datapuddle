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
    ingested_at       TIMESTAMP NOT NULL,   -- timestamp of the data being logged into the system, in UNIX timestamp and millisecodns
    source            TEXT      NOT NULL,   -- where the data came from (http://t.me/..., http://forum.onion...,)
    type              TEXT      NOT NULL,   -- type of the data, (json, har, txt) 
    original_filename TEXT,                 -- if available, store the original filename
    content_type      TEXT,                 -- the mimetype of the content
    timestamp         INTEGER,              -- if know, the original timestamp of the data (LinkedIn dump from 2012)

    raw_bytes         BYTEA     NOT NULL,   -- raw bytes of the data. 
    raw_text          TEXT,                 -- raw bytes turned into text, if possible.

    zone              TEXT DEFAULT 'raw',   -- is data RAW, CLEANED, or CURATED.  
    owner             TEXT                  -- What owns the data (Telegram Listener, Forum Scraper, RSS Listener)
);
"""


select_regex_match_eveything = """
SELECT id 
FROM  data_puddle 
WHERE raw_text REGEXP ?
    AND
      (? IS NULL OR ingested_at >= ?)
    AND
      (? IS NULL OR ingested_at <= ?);
"""
"""SELCT id .. WHERE <REGEX> AND <TIMESTAMPS>"""

select_data_by_id = """
SELECT ingested_at, source, type, original_filename, content_type, timestamp, raw_bytes, raw_text, zone, owner
FROM   data_puddle
WHERE  id = ?;
"""
"""ingested_at, source, type, original_filename, content_type, timestamp, raw_bytes, raw_text, zone, owner"""

insert_into_puddle = """
INSERT INTO data_puddle (
    id,
    ingested_at, 
    source, 
    type, 
    original_filename, 
    content_type, 
    timestamp, 
    raw_bytes, 
    raw_text, 
    zone, 
    owner
) VALUES ( ?,?,?,?,?,?,?,?,?,?,? );
"""
"""
id, ingested_at, source, type, original_filename, content_type, timestamp, raw_bytes, raw_text, zone, owner
"""

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