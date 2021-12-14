from airflow.plugins_manager import AirflowPlugin

from flask import Blueprint

class PCCPlugin(AirflowPlugin):
    name = "pcc_plugin"