# statsnz

A collection of functions to enable ease of use of the various Stats NZ APIs

Installion:

  pip install statsnz

Examples:

  To get the region with a set of coordinates:

    from statsnz import statsnz

    region_example = statsnz("YOUR_API_KEY",-41.242,172.323).get_region()


  Or TLA:

    region_example = statsnz("YOUR_API_KEY",-41.242,172.323).get_region()
