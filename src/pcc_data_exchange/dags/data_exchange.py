import json
from datetime import datetime

from airflow.decorators import dag, task

@dag(schedule_interval=None, start_date=datetime(2021, 12, 13), catchup=False, tags = ['library-of-congress', 'oclc', 'share-vde', 'sinopia'])
def data_exchange_taskflow_dag():
    """
    ### PCC Data Exchange
    A simple data validation and exchange pipeline for initially BIBFRAME Instance Data
    """
    @task()
    def extract_bf_source():
        """
        #### Extracts BIBFRAME RDF from Source
        """
        return "complete"

    @task()
    def validate_bf(bf_instance: str):
        """
        #### Validates BIBFRAME RDF Instance
        """
        return True

    @task()
    def construct_payload(bf_instance: str):
        """
        #### Constructs Interchange Payload
        """
        payload = { "uri": bf_instance }
        return payload

    @task()
    def send_payload(targets: list, payload: dict):
        """
        #### Sends Payloads to Hubs
        """
        for target in targets:
            print(f"{target} with {payload}")
        return True

    bibframe_source = extract_bf_source()
    validate_bibframe = validate_bf(bibframe_source)
    payload = construct_payload(validate_bibframe)
    send_to_hubs = send_payload(['oclc','loc', 'share-vde'], payload)

pcc_data_exchange = data_exchange_taskflow_dag()
