
def view_rules(args, prediction_db):
    from src.mtool.util.sqlite import sqlite_prediction
    from src.mtool.display import display_prediction
    from src.mtool.predictions.rules_engine import rules

    if hasattr(args, "name"):
        name = args.name
    else:
        name = args

       
    name = rules.get_ruleset_by_ordinal(name, prediction_db)

    ruleset_db = sqlite_prediction.get_ruleset_path(prediction_db, name)

    rules_list = sqlite_prediction.list_rules_in_ruleset(ruleset_db)
    display_prediction.display_rule_list(name, rules_list)