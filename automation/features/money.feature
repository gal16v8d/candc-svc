Feature: Money endpoint check

    Scenario Outline: AT-02 Check money endpoint calls
        Given load request data from 'features/data/AT-02/request.json'
        When  user call money endpoint as /api/money/'<path>'
        Then  response should match money validations

    Examples:
      | path       |
      | boats      |
      | infantry   |
      | planes     |
      | structures |
      | tanks      |

    Scenario Outline: AT-03 Check money endpoint calls no payload
        When  user call money endpoint as /api/money/'<path>'
        Then  response should match money validations for bad request

    Examples:
      | path       |
      | boats      |
      | infantry   |
      | planes     |
      | structures |
      | tanks      |
