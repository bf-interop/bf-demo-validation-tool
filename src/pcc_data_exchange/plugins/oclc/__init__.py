from airflow.plugins_manager import AirflowPlugin

from flask import Blueprint

class OCLCPlugin(AirflowPlugin):
    name = "oclc_plugin"