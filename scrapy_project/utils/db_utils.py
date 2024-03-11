from playhouse.shortcuts import dict_to_model


def list_of_dicts_to_model(model, dicts):
    models = []
    for d in dicts:
        models.append(dict_to_model(model, d))
    return models
