import json
from datetime import datetime

from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator
from airflow.sensors.weekday import DayOfWeekSensor
from airflow.utils.task_group import TaskGroup

hubs = ['oclc', 'loc', 'sharevde']

with DAG(
    "data_exchange_demo",
    default_args={
        "owner": "airflow",

    },
    description="PCC Data Exchange Demo",
    start_date=datetime(2021, 12, 13),
    schedule_interval=None,
    tags = ['library-of-congress', 'oclc', 'share-vde', 'sinopia'],
) as dag:
    """
    ### PCC Data Exchange
    A simple data validation and exchange pipeline for initially BIBFRAME Instance Data
    """

    weekly_download = DayOfWeekSensor(
        task_id='weekly-delta-check',
        week_day='Monday',
        use_task_execution_day=True
    )

    with TaskGroup(group_id="hub-sources-validate") as hub_sources_validate:
        hubs_plus = hubs + ["sinopia"]
        for hub in hubs_plus:
            hub_extract_task = DummyOperator(
                task_id=f"{hub}-rdf-extract"
            )
            validate_rdf_task = DummyOperator(
                task_id=f"{hub}-rdf-validate"
            )
            hub_extract_task >> validate_rdf_task
    

    construct_payload = DummyOperator(
        task_id="construct-exchange-payload"
    )

    with TaskGroup(group_id='send-payloads') as send_payloads:
        for hub in hubs:
            send_payload_task = DummyOperator(
                task_id=f"{hub}-send-payload"
            )

weekly_download >> hub_sources_validate
hub_sources_validate >> construct_payload >> send_payloads



   