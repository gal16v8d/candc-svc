Feature: Model endpoint check

    Scenario Outline: AT-04 Check model endpoint calls (GET) all
        When  user call model endpoint as /api/'<path>'
        Then  response should match model validations

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
