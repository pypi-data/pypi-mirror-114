# statsnz

A collection of functions to enable ease of use of the various Stats NZ APIs, in python.

Installion:

  pip install statsnz

Examples:

  To get the region with a set of coordinates:

    from statsnz import statsnz

    region_example = statsnz("YOUR_API_KEY").get_region(-41.242,172.323)


  Or TLA:

    region_example = statsnz("YOUR_API_KEY").get_tla(-41.242,172.323)
