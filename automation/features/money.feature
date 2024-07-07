Feature: Money endpoint check

    Scenario Outline: AT-02 Check money endpoint calls
        Given load request data from features/data/AT-02/request.json
        When  user call money endpoint as /api/money/<path>
        Then  response should match money validations

    Examples:
      | path       |
      | boats      |
      | infantry   |
      | planes     |
      | structures |
      | tanks      |

    Scenario Outline: AT-03 Check money endpoint calls no payload
        When  user call money endpoint as /api/money/<path>
        Then  user get error from api with code 415
        And   user get error from api and msg is Did not attempt to load JSON data because the request Content-Type was not 'application/json'.

    Examples:
      | path       |
      | boats      |
      | infantry   |
      | planes     |
      | structures |
      | tanks      |

    Scenario Outline: AT-04 Check money endpoint calls empty payload
        Given load request data from features/data/AT-04/request.json
        When  user call money endpoint as /api/money/<path>
        Then  user get error from api with code 400

    Examples:
      | path       |
      | boats      |
      | infantry   |
      | planes     |
      | structures |
      | tanks      |
