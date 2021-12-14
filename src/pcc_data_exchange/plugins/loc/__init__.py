from airflow.plugins_manager import AirflowPlugin

from flask import Blueprint

class LibraryOfCongressPlugin(AirflowPlugin):
    name = "loc_plugin"