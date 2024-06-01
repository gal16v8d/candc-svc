"""Run all the defined steps to check api"""

from steps.health_step import HealthSteps
from steps.model_step import MODELS, ModelSteps
from steps.money_step import MODEL_TYPES, MoneySteps


if __name__ == "__main__":
    print("--- Running Health Endpoint Checks ---")
    print(HealthSteps.check_health())
    print("--- Running Money Endpoint Checks ---")
    for value in MODEL_TYPES:
        print(MoneySteps.check_money_spend_ok(value, 4, 10000))
        print(MoneySteps.check_money_spend_no_payload(value))
    print("--- Running Crud Endpoint Checks ---")
    for value in MODELS:
        print(ModelSteps.check_get_all(value.name, value.data_args))
