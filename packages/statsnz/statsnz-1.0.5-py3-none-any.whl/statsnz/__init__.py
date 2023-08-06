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

    def __init__(self, key):
        self.key = key


    def get_odata_api(self, service, endpoint, entity, query_option, proxies):
        """
            Query the STATSNZ Odata service - example:

             service = 'https://api.stats.govt.nz/opendata/v1'
             endpoint = 'EmploymentIndicators'
             entity = 'Resources'
             query_option = "$top=10"


             proxies = {'https': 'your-proxy.co.nz:8080'}  ## proxies = {} if none
             Observations = statsnz.get_odata_api(service, endpoint, entity, query_option, proxies)

        """

        header_data = {'Ocp-Apim-Subscription-Key': self.key}

        proxies = proxies
        url = service + '/' + endpoint + '/' + entity + '?' + query_option
        top_query = "$top" in query_option
        results = pd.DataFrame()


        while url == True:

            try:
                req = requests.get(url,header_data=header_data,proxies=proxies)
                req.raise_for_status()

            # raise request errors
            except Exception as E:
                print(str(E))

                break
            #Convert to JSON
            df = pd.json_normalize(r.json()['value'])
            results = pd.concat([results,df])

            try:
                url = r.json()['@odata.nextLink']

                if top_query:
                    url = None
            except KeyError:
                url = None

            print('.', end = ' ', flush = True)

        print(len(results.index),'Obs retrieved')

        return results




    def get_tla(self, lat, long):

        """
            Uses area layer: https://datafinder.stats.govt.nz/layer/105135-territorial-authority-local-board-2021-generalised/
        """
        try:

            req = requests.get("https://datafinder.stats.govt.nz/services/query/v1/vector.json?key={}&layer=105135&x={}&y={}&max_results=3&radius=10000&geometry=true&with_field_names=true".format(self.key,long,lat)).json()
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

    def get_region(self, lat, long):

        """
            Uses area layer: https://datafinder.stats.govt.nz/layer/104254-regional-council-2020-generalised/
        """
        try:


            req = requests.get("https://datafinder.stats.govt.nz/services/query/v1/vector.json?key={}&layer=104254&x={}&y={}&max_results=3&radius=10000&geometry=true&with_field_names=true".format(self.key,long,lat)).json()
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


    def get_urban_rural(self, lat, long):

        """
            Uses area layer: https://datafinder.stats.govt.nz/layer/105158-urban-rural-2021-generalised/
        """
        try:



            req = requests.get("https://datafinder.stats.govt.nz/services/query/v1/vector.json?key={}&layer=105158&x={}&y={}&max_results=3&radius=10000&geometry=true&with_field_names=true".format(self.key,long,lat)).json()
            req = req['vectorQuery']
            req = req['layers']
            req = req['105158']
            req = req['features']
            req = req[0]
            req = req['properties']
            req = req['UR2021_V1_00_NAME']

            return req

        except Exception as e:

            req = "request_error: " + str(e)

            return req

    def get_custom_layer(self, layer_id, lat, long):
        """
            Specify an area layer for use. Response as JSON.
        """
        try:


            req = requests.get("https://datafinder.stats.govt.nz/services/query/v1/vector.json?key={}&layer={}&x={}&y={}&max_results=3&radius=10000&geometry=true&with_field_names=true".format(self.key,layer_id,long,lat)).json()


            return req

        except Exception as e:

            req = "request_error: " + str(e)

            return req
