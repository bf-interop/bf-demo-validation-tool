from airflow.plugins_manager import AirflowPlugin

from flask import Blueprint

class SinopiaPlugin(AirflowPlugin):
    name = "sinopia_plugin"