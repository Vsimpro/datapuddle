# DataPuddle
Datapuddle is like a datalake, but smaller, and inside SQLite3. It's meant to store un-constructed data with relevant metadata, to be found later.

## What is databuddle?
The puddle is a deliberately small and simple version of a lake. It stores raw, unstructured data together with metadata. (time, source, type, filename, etc)

Instead of being a cloud storage dump, it uses a SQLite3 instance (maybe PSQL in the future) to keep everything stored and easy to reason about.

## How to use:
Build with:
```sh
# in the project root
docker-compose up

# once the containers are up, create a new token
python3 admin.py --new-token
```
Now you're ready to push data into the lake. Find `push.py` for ready made functions to use in your project.


## API Documentation
TODO:

## Database documentation
Read the database/queries.py. The comments will explain everything briefly.


## Why is datapuddle?
DataPuddle is a small project to help _me_ understand how DataLakes _could_ work. I don't think it will scale. Changes will arrive!

I will try to write extensive comments as notes to show my thought process.