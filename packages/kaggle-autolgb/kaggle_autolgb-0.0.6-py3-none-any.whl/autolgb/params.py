from logger import logger

def get_params(trial, model_config):
    params = {
        "verbosity": -1,
        "max_depth": trial.suggest_int("max_depth", 10, 1000),
        "early_stopping": trial.suggest_int("early_stopping", 100, 500),
        "n_estimators": trial.suggest_int("n_estimators", 100, 700),
        "random_state": trial.suggest_int("random_state", 42, 2042),
        "learning_rate": trial.suggest_float("learning_rate", 1e-2, 1, log=True),
        "lambda_l1": trial.suggest_float("lambda_l1", 1e-8, 10.0, log=True),
        "lambda_l2": trial.suggest_float("lambda_l2", 1e-8, 10.0, log=True),
        "num_leaves": trial.suggest_int("num_leaves", 2, 256),
        "feature_fraction": trial.suggest_float("feature_fraction", 0.4, 1.0),
        "bagging_fraction": trial.suggest_float("bagging_fraction", 0.4, 1.0),
        "min_child_samples": trial.suggest_int("min_child_samples", 5, 100),
    }
    if model_config.gpu is True:
        logger.info("enable gpu")
        params["device"] = "gpu"
        params["gpu_platform_id"] = 0
        params["gpu_device_id"] = 0
        
    return params

    