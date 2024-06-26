Feature: Model endpoint check

    Scenario Outline: AT-04 Check model endpoint calls (GET) all
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

    Scenario Outline: AT-05 Check model endpoint calls (GET) by id
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

    Scenario Outline: AT-06 Check model endpoint calls (GET) by id - not found
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

    Scenario Outline: AT-07 Check model endpoint calls (POST) missing req data
        Given load request data from features/data/AT-07/<request>
        When  user call model POST endpoint as /api/<path>
        Then  user get error from api with code 400

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