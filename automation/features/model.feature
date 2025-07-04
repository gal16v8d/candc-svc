Feature: Model endpoint check

    Scenario Outline: AT-05 Check model endpoint calls (GET) all
        When  user call model GET endpoint as /api/<path>
        Then  response should match model list validations

    Examples:
      | path               |
      | boats              |
      | boatxfactions      |
      | factions           |
      | games              |
      | infantry           |
      | infantryxfactions  |
      | planes             |
      | planexfactions     |
      | structures         |
      | structurexfactions |
      | tanks              |
      | tankxfactions      |

    Scenario Outline: AT-06 Check model endpoint calls (GET) all with args
        When  user call model GET endpoint as /api/<path>
        Then  response should match model list validations

    Examples:
      | path                            |
      | boats?can_go_ground=true        |
      | boatxfactions?faction_id=1      |
      | factions?game_id=1              |
      | games?active=true               |
      | infantry?can_swim=true          |
      | infantryxfactions?faction_id=1  |
      | planes?base_cost=1200           |
      | planexfactions?faction_id=1     |
      | structures?name=Dugout          |
      | structurexfactions?faction_id=1 |
      | tanks?is_special=true           |
      | tankxfactions?faction_id=1      |

    Scenario Outline: AT-07 Check model endpoint calls (GET) all no matches
        When  user call model GET endpoint as /api/<path>
        Then  user get error from api with code 404

    Examples:
      | path                                        |
      | boats?name=IFV                              |
      | boatxfactions?faction_id=999                |
      | factions?faction_id=999                     |
      | games?name=Command and Conquer Tiberian Sun |
      | infantry?name=IFV                           | 
      | infantryxfactions?faction_id=999            |
      | planes?name=IFV                             |
      | planexfactions?faction_id=999               |
      | structures?name=Defender                    |
      | structurexfactions?faction_id=999           |
      | tanks?name=Boomer                           |
      | tankxfactions?faction_id=999                |

    Scenario Outline: AT-08 Check model endpoint calls (GET) all with bad args
        When  user call model GET endpoint as /api/<path>
        Then  user get error from api with code 400

    Examples:
      | path                                       |
      | boats?non_existing_field=true              |
      | boatxfactions?non_existing_field=true      |
      | factions?non_existing_field=true           |
      | games?non_existing_field=true              |
      | infantry?non_existing_field=true           |
      | infantryxfactions?non_existing_field=true  |
      | planes?non_existing_field=true             |
      | planexfactions?non_existing_field=true     |
      | structures?non_existing_field=true         |
      | structurexfactions?non_existing_field=true |
      | tanks?non_existing_field=true              |
      | tankxfactions?non_existing_field=true      |

    Scenario Outline: AT-09 Check model endpoint calls (GET) by id
        When  user call model GET by Id endpoint as /api/<path>/<model_id>
        Then  response should match model element validations

    Examples:
      | path               | model_id |
      | boats              | 1        |
      | boatxfactions      | 1        |
      | factions           | 1        |
      | games              | 1        |
      | infantry           | 1        |
      | infantryxfactions  | 1        |
      | planes             | 1        |
      | planexfactions     | 1        |
      | structures         | 1        |
      | structurexfactions | 1        |
      | tanks              | 1        |
      | tankxfactions      | 1        |

    Scenario Outline: AT-10 Check model endpoint calls (GET) by id - not found
        When  user call model GET by Id endpoint as /api/<path>/<model_id>
        Then  user get error from api with code 404

    Examples:
      | path               | model_id |
      | boats              | 999      |
      | boatxfactions      | 999      |
      | factions           | 999      |
      | games              | 999      |
      | infantry           | 999      |
      | infantryxfactions  | 999      |
      | planes             | 999      |
      | planexfactions     | 999      |
      | structures         | 999      |
      | structurexfactions | 999      |
      | tanks              | 999      |
      | tankxfactions      | 999      |

    Scenario Outline: AT-11 Check model endpoint calls (POST) missing req data
        Given load request data from features/data/AT-11/<request>
        When  user call model POST endpoint as /api/<path>
        Then  user get error from api with code 400
        And   request data is cleared out

    Examples:
      | request                | path               |
      | boat.json              | boats              |
      | boatxfaction.json      | boatxfactions      |
      | faction.json           | factions           |
      | game.json              | games              |
      | infantry.json          | infantry           |
      | infantryxfaction.json  | infantryxfactions  |
      | plane.json             | planes             |
      | planexfaction.json     | planexfactions     |
      | structure.json         | structures         |
      | structurexfaction.json | structurexfactions |
      | tank.json              | tanks              |
      | tankxfaction.json      | tankxfactions      |
    
    Scenario Outline: AT-12 Check model endpoint calls (PATCH) by id - no payload
        When  user call model PATCH endpoint as /api/<path>/<model_id>
        Then  user get error from api with code 415
        And   user get error from api and msg is Did not attempt to load JSON data because the request Content-Type was not 'application/json'.

    Examples:
      | path               | model_id |
      | boats              | 999      |
      | boatxfactions      | 999      |
      | factions           | 999      |
      | games              | 999      |
      | infantry           | 999      |
      | infantryxfactions  | 999      |
      | planes             | 999      |
      | planexfactions     | 999      |
      | structures         | 999      |
      | structurexfactions | 999      |
      | tanks              | 999      |
      | tankxfactions      | 999      |

    Scenario Outline: AT-13 Check model endpoint calls (PATCH) by id - not found
        Given load request data from features/data/AT-13/request.json
        When  user call model PATCH endpoint as /api/<path>/<model_id>
        Then  user get error from api with code 404

    Examples:
      | path               | model_id |
      | boats              | 999      |
      | boatxfactions      | 999      |
      | factions           | 999      |
      | games              | 999      |
      | infantry           | 999      |
      | infantryxfactions  | 999      |
      | planes             | 999      |
      | planexfactions     | 999      |
      | structures         | 999      |
      | structurexfactions | 999      |
      | tanks              | 999      |
      | tankxfactions      | 999      |

    Scenario Outline: AT-14 Check model endpoint calls (PATCH) by id - not updatable
        Given load request data from features/data/AT-14/<request>
        When  user call model PATCH endpoint as /api/<path>/<model_id>
        Then  user get error from api with code 400

    Examples:
      | path               | model_id | request              |
      | boats              | 1        | request-created.json |
      | boatxfactions      | 1        | request-created.json |
      | factions           | 1        | request-created.json |
      | games              | 1        | request-created.json |
      | infantry           | 1        | request-created.json |
      | infantryxfactions  | 1        | request-created.json |
      | planes             | 1        | request-created.json |
      | planexfactions     | 1        | request-created.json |
      | structures         | 1        | request-created.json |
      | structurexfactions | 1        | request-created.json |
      | tanks              | 1        | request-created.json |
      | tankxfactions      | 1        | request-created.json |
      | boats              | 1        | request-updated.json |
      | boatxfactions      | 1        | request-updated.json |
      | factions           | 1        | request-updated.json |
      | games              | 1        | request-updated.json |
      | infantry           | 1        | request-updated.json |
      | infantryxfactions  | 1        | request-updated.json |
      | planes             | 1        | request-updated.json |
      | planexfactions     | 1        | request-updated.json |
      | structures         | 1        | request-updated.json |
      | structurexfactions | 1        | request-updated.json |
      | tanks              | 1        | request-updated.json |
      | tankxfactions      | 1        | request-updated.json |

    Scenario Outline: AT-15 Check model endpoint calls (PATCH) by id - invalid field
        Given load request data from features/data/AT-15/request.json
        When  user call model PATCH endpoint as /api/<path>/<model_id>
        Then  user get error from api with code 400

    Examples:
      | path               | model_id |
      | boats              | 1        |
      | boatxfactions      | 1        |
      | factions           | 1        |
      | games              | 1        |
      | infantry           | 1        |
      | infantryxfactions  | 1        |
      | planes             | 1        |
      | planexfactions     | 1        |
      | structures         | 1        |
      | structurexfactions | 1        |
      | tanks              | 1        |
      | tankxfactions      | 1        |

    Scenario Outline: AT-16 Check model endpoint calls (DELETE) by id - not found
        When  user call model DELETE endpoint as /api/<path>/<model_id>
        Then  user get error from api with code 404

    Examples:
      | path               | model_id |
      | boats              | 999      |
      | boatxfactions      | 999      |
      | factions           | 999      |
      | games              | 999      |
      | infantry           | 999      |
      | infantryxfactions  | 999      |
      | planes             | 999      |
      | planexfactions     | 999      |
      | structures         | 999      |
      | structurexfactions | 999      |
      | tanks              | 999      |
      | tankxfactions      | 999      |