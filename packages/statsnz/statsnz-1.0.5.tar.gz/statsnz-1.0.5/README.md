# statsnz

A collection of functions to enable ease of use of the various Stats NZ APIs, in python.

Installion:

  pip install statsnz



Examples:


Geocoding:


  To get the region with a set of coordinates:

    from statsnz import statsnz

    region_example = statsnz("YOUR_API_KEY").get_region(-41.242,172.323)


  Or TLA:

    region_example = statsnz("YOUR_API_KEY").get_tla(-41.242,172.323)



Odata API:




  statsnz("YOUR_API_KEY").get_region(-41.242,172.323)
  service = 'https://api.stats.govt.nz/opendata/v1'
  endpoint = 'EmploymentIndicators'
  entity = 'Resources'
  query_option = "$top=10"


  proxies = {'https': 'your-proxy.co.nz:8080'}  ## proxies = {} if none

  Observations = statsnz.get_odata_api(service, endpoint, entity, query_option, proxies)
