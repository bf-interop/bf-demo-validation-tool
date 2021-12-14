from airflow.plugins_manager import AirflowPlugin

from flask import Blueprint

class ShareVDEPlugin(AirflowPlugin):
    name = "sharevde_plugin"