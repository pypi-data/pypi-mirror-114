# -*- coding: utf-8 -*-
"""
Created on Tue May 11 12:18:36 2021

@author: flynn

"""
import os
import json
import pandas as pd
import requests




class statsnz:

    """
    Base class. Initialise your API key, and pass the coordinates

    """
    
    def __init__(self, key, lat, long):
        self.key = key
        self.lat = lat
        self.long = long

    def get_tla(self):

        """
            Uses area layer: https://datafinder.stats.govt.nz/layer/105135-territorial-authority-local-board-2021-generalised/
        """
        try:

            req = requests.get("https://datafinder.stats.govt.nz/services/query/v1/vector.json?key={}&layer=105135&x={}&y={}&max_results=3&radius=10000&geometry=true&with_field_names=true".format(self.key,self.long,self.lat)).json()
            req = req['vectorQuery']
            req = req['layers']
            req = req['105135']
            req = req['features']
            req = req[0]
            req = req['properties']
            req = req['TALB2021_V1_00_NAME']
            return req

        except Exception as e:

            req = "request_error: " + str(e)

            return req

    def get_region(self):

        """
            Uses area layer: https://datafinder.stats.govt.nz/layer/104254-regional-council-2020-generalised/
        """
        try:


            req = requests.get("https://datafinder.stats.govt.nz/services/query/v1/vector.json?key={}&layer=104254&x={}&y={}&max_results=3&radius=10000&geometry=true&with_field_names=true".format(self.key,self.long,self.lat)).json()
            req = req['vectorQuery']
            req = req['layers']
            req = req['104254']
            req = req['features']
            req = req[0]
            req = req['properties']
            req = req['REGC2020_V1_00_NAME']

            return req

        except Exception as e:

            req = "request_error: " + str(e)

            return req


    def get_urban_rural(self):

        """
            Uses area layer: https://datafinder.stats.govt.nz/layer/105158-urban-rural-2021-generalised/
        """
        try:


            req = requests.get("https://datafinder.stats.govt.nz/services/query/v1/vector.json?key={}&layer=105158&x={}&y={}&max_results=3&radius=10000&geometry=true&with_field_names=true".format(self.key,self.long,self.lat)).json()
            req = req['vectorQuery']
            req = req['layers']
            req = req['105158']
            req = req['features']
            req = req[0]
            req = req['properties']
            req = req['REGC2020_V1_00_NAME']

            return req

        except Exception as e:

            req = "request_error: " + str(e)

            return req
