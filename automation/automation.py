"""Run all the defined steps to check api"""

from steps.health_step import HealthSteps
from steps.money_step import MoneySteps


if __name__ == "__main__":
    print("--- Running Health Endpoint Checks ---")
    print(HealthSteps.check_health())
    print("--- Running Money Endpoint Checks ---")
    model_types = ["boats", "infantry", "planes", "structures", "tanks"]
    for value in model_types:
        print(MoneySteps.check_money_spend_ok(value, 4, 10000))
        print(MoneySteps.check_money_spend_no_payload(value))
