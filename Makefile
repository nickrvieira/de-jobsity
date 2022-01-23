
.PHONY: download_csv prepare_dirs run_ingestion run_aggregation cleanup

prepare_dirs:
	mkdir -p ./application_data/input/
	mkdir -p ./application_data/output/

download_csv:prepare_dirs
	wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=14JcOSJAWqKOUNyadVZDPm7FplA7XYhrU' -O ./application_data/input/sample.csv

run_ingestion:download_csv
# You might need Root privileges for building image locally
	docker-compose run application --load-config '{"load_type":"GenericPySparkLoad", "options": {"path": "/app/input/sample.csv", "format": "csv", "header": "true"} }'  --sink-config '{"sink_type": "JDBCSink", "options":{"conn_uri": "amRiYzpwb3N0Z3Jlc3FsOi8vcG9zdGdyZXM6NTQzMi9qb2JzaXR5P3VzZXI9bmFuaXZpYWEmcGFzc3dvcmQ9MTIzNDU2", "table": "trips"} }' --pipeline '{"pipeline_name": "Trips", "options":{}}'


run_aggregation:
# You might need Root privileges for building image locally
	docker-compose run application --load-config '{"load_type":"JDBCLoad", "options":{"conn_uri": "amRiYzpwb3N0Z3Jlc3FsOi8vcG9zdGdyZXM6NTQzMi9qb2JzaXR5P3VzZXI9bmFuaXZpYWEmcGFzc3dvcmQ9MTIzNDU2", "table": "trips"}  }' --sink-config '{"sink_type": "GenericPySparkSink", "options":{"format":"json", "path":"/app/output/aggregated", "mode":"overwrite"}}' --pipeline '{"pipeline_name": "TripsAggregated", "options":{"region":"Turin", "p1":[7.54, 44], "p2":[7.70, 46]}}'

cleanup:
	docker-compose down
	sudo rm -rf ./application_data /opt/naniviaa/psqldata
