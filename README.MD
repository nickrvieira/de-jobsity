

## Intro

This is a simple pipeline processing tool, consisting of three core ideas:
- Loads
- Sinks
- Pipelines

**Sinks** specifies 

## Project Structure



## Mandatory Features: 
- There must be an automated process to ingest and store the data. 100%
- Trips with similar origin, destination, and time of day should be grouped together. 100%

- Develop a way to obtain the weekly average number of trips for an area, defined by a
bounding box (given by coordinates) or by a region. 100%

*Commentary*: This is ambiguous - what happens if there is only one week? Should be it averaged for a time window? Since when should we consider? Entire 2018? or max min of the dataset itself? I've decided to not left join there and simply average weeks that had at least one travel.

Also important: I've decided to do this fully on Spark - a wiser implementation would check the instances of the loading pipeline and, if is a JDBC - run the query within the Database to minimize data flow/I.O.  There should be two approaches there - one with spark (if the source is a non-jdbc) and one proper for JDBC cons.

- Develop a way to inform the user about the status of the data ingestion without using a
polling solution. 100% (NO CREDS THERE)

*Commentary*: I've create a sort of message bus - with a simple slack model there. It could be a webhook? Email? SMS? All of the previous? Simple to hook up a new adapter and set each notification for each event.

- The solution should be scalable to 100 million entries. It is encouraged to simplify the
data by a data model. Please add proof that the solution is scalable. 50%

*Commentary*:
Data models are controversial - mainly in this scenario - Indeed I could create auxiliary tables for: City and Dates, but this is non practical whenever is only a single table - this won't make the solution less or more scalable and worst: will require joins there. 

In stores such as columnar stores, data modeling in this scenario should be carefully reviewed - It may bring organization, but it adds complexity and, depending on the stack, increases the computational load for both reading (consumer/end user) and writing (pipeline processes).

- Use a SQL database. 100%

*Commentary*: Postgres.

## Running Samples

### Reading from CSV and Sinking to JDBC
``` 
python main.py --load-config '{"load_type":"GenericPySparkLoad", "options": {"path": "/home/nick/repos/test-jobsity/source_data/trips.csv", "format": "csv", "header": "true"} }' \
               --sink-config '{"sink_type": "JDBCSink", "options":{"conn_uri": "amRiYzpwb3N0Z3Jlc3FsOi8vbG9jYWxob3N0OjU0MzIvam9ic2l0eT91c2VyPW5hbml2aWFhJnBhc3N3b3JkPTEyMzQ1Ng==", "table": "lala"} }' \
               --pipeline '{"pipeline_name": "Trips", "options":{}}'
```

### Reading from JDBC and Sinking to CSV - Aggregated Pipeline
```
python main.py --load-config '{"input_path": "/home/nick/repos/test-jobsity/source_data/trips.csv", "load_type":"JDBCLoad", "options":{"conn_uri": "amRiYzpwb3N0Z3Jlc3FsOi8vbG9jYWxob3N0OjU0MzIvam9ic2l0eT91c2VyPW5hbml2aWFhJnBhc3N3b3JkPTEyMzQ1Ng==", "table": "lala"}  }' \
               --sink-config '{"sink_type": "GenericPySparkSink", "options":{"format":"json", "path":"./output_data/", "mode":"overwrite"}}' \
               --pipeline '{"pipeline_name": "TripsAggregated", "options":{}}'
```

## Scalability

## On the Cloud

## Enhancements

### Testing
I would like to introduce at very least some unit testings there - I didn't cause I've done this in pretty much one and a half day. 

Each pipeline should have each of those methods tested, while the CSV/Parquet/JSON sinks and loads could be easily tested - those in JDBC context will need `sqlalchemy` and even a docker instance for proper testing (and integrations one).
