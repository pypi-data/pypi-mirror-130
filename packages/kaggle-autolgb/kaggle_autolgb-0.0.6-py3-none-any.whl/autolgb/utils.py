from logging import log
import sys
from lightgbm.callback import early_stopping
from logger import logger
sys.path.insert(0, 'path/to/params.py')
from sklearn import preprocessing
import lightgbm as lgb
from .params import get_params
from functools import partial
import optuna
import os
import json
import numpy as np
import pandas as pd
from sklearn import metrics

optuna.logging.set_verbosity(optuna.logging.INFO)

def reduce_memory_usage(df):
    start_mem = df.memory_usage().sum() / 1024**2
    logger.info(f'Memory usage of dataframe is {start_mem} MB')
    for col in df.columns:
        col_type = df[col].dtype
        if col_type != object:
            c_min = df[col].min()
            c_max = df[col].max()
            if str(col_type)[:3] == 'int':
                if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max:
                    df[col] = df[col].astype(np.int8)
                elif c_min > np.iinfo(np.int16).min and c_max < np.iinfo(np.int16).max:
                    df[col] = df[col].astype(np.int16)
                elif c_min > np.iinfo(np.int32).min and c_max < np.iinfo(np.int32).max:
                    df[col] = df[col].astype(np.int32)
                elif c_min > np.iinfo(np.int64).min and c_max < np.iinfo(np.int64).max:
                    df[col] = df[col].astype(np.int64)  
            else:
                if c_min > np.finfo(np.float16).min and c_max < np.finfo(np.float16).max:
                    df[col] = df[col].astype(np.float16)
                elif c_min > np.finfo(np.float32).min and c_max < np.finfo(np.float32).max:
                    df[col] = df[col].astype(np.float32)
                else:
                    df[col] = df[col].astype(np.float64)
        else:
            df[col] = df[col].astype('category')

    end_mem = df.memory_usage().sum() / 1024**2
    logger.info('Memory usage after optimization is: {:.2f} MB'.format(end_mem))
    logger.info('Decreased by {:.1f}%'.format(100 * (start_mem - end_mem) / start_mem))
    
    return df

def obj_to_cat(data, label):
    categorical = []
    ignore_fields = [label]
    # drop_fields = ["id", "ID", "Id"]
    # useless_col = []

    for col in data.columns:
        # if col in drop_fields:
        #     useless_col.append(col)
        if data[col].dtype == "object" and col not in ignore_fields:
            categorical.append(col)
    if len(categorical) > 0:
        ord_encoder = preprocessing.OrdinalEncoder()
        data[categorical] = ord_encoder.fit_transform(data[categorical].values)
    # data.drop(useless_col, axis=1, inplace=True)
    # logger.info("Drop id column")
    return data

def apply_binary_classification(data_type, label):
    lb = preprocessing.LabelBinarizer()
    data_type[label] = lb.fit_transform(data_type[label].values)
    return data_type

def apply_multilabel_classification(data_type, label):
    le = preprocessing.LabelEncoder()
    data_type[label] = le.fit_transform(data_type[label].values)    
    return data_type

def model_lgb(**param):
    model = lgb.LGBMClassifier(**param)
    return model

def optimize(trial, model_config):
    param = get_params(trial, model_config)

    early_stopping_rounds = param["early_stopping"]
    del param["early_stopping"]

    for fold in range(model_config.num_folds):
        # /media/aditta/Deep Learning files/autolgb/output/train_fold_0.feather
        # /media/aditta/Deep Learning files/autolgb/output/
        train_feather = pd.read_feather(os.path.join(model_config.store_file, f"{model_config.storage_name}/train_fold_{fold}.feather"))
        valid_feather = pd.read_feather(os.path.join(model_config.store_file, f"{model_config.storage_name}/valid_fold_{fold}.feather"))
        features = [
            f for f in train_feather.columns if f not in [model_config.label, "kfold"]
        ]
        X_train = train_feather[features]
        X_valid = valid_feather[features]

        y_train = train_feather[model_config.label].values
        y_valid = valid_feather[model_config.label].values
        model = model_lgb(**param)
        model.fit(X_train, y_train, eval_set=[(X_valid, y_valid)], callbacks=[early_stopping(early_stopping_rounds)])
        pred = model.predict(X_valid)
        acc = metrics.accuracy_score(pred, y_valid)
        return acc

def model_training(model_config):
    optimize_func = partial(
        optimize,
        model_config=model_config
    )
    study = optuna.create_study(
        study_name="1",
        direction=model_config.direction,
        load_if_exists=True,
        storage=os.path.join(f"sqlite:///{model_config.store_file}", f"{model_config.storage_name}/hyperparams.db")
    )
    study.optimize(
        optimize_func, 
        n_trials=model_config.n_trials
    )
    return study.best_params

def param_load(model_config):
    with open(os.path.join(model_config.store_file, f"{model_config.storage_name}/best_params.json"), "r") as f:
        best_params = json.load(f)
    return best_params

def predict_test(model_config, best_params):

    early_stopping_rounds = best_params["early_stopping"]
    # del best_params["early_stopping"]
    
    if model_config.gpu is True:
        best_params["device"] = "gpu"
        best_params["gpu_platform_id"] = 0
        best_params["gpu_device_id"] = 0

    test_ = pd.read_csv(model_config.test_file)
    best_params = param_load(model_config)
    final_test_pred = []
    for fold in range(model_config.num_folds):
        train_feather = pd.read_feather(os.path.join(model_config.store_file, f"{model_config.storage_name}/train_fold_{fold}.feather"))
        valid_feather = pd.read_feather(os.path.join(model_config.store_file, f"{model_config.storage_name}/valid_fold_{fold}.feather"))
        features = [
            f for f in train_feather.columns if f not in [model_config.label, "kfold"]
        ]
        X_train = train_feather[features]
        X_valid = valid_feather[features]
        y_train = train_feather[model_config.label].values
        y_valid = valid_feather[model_config.label].values
        model = model_lgb(**best_params)
        model.fit(X_train, y_train, eval_set=[(X_valid, y_valid)], callbacks=[early_stopping(early_stopping_rounds)])
        pred = model.predict(test_)
        return pred

# def prediction_test(model_config):
#     predict = partial(
#         predict_test,
#         model_config=model_config
#     )
#     print(predict)
    # test_file = predict_test(test_file_path)
    # best_params = param_load(model_config)
    # train_feather = pd.read_feather(os.path.join(model_config.store_file, f"{model_config.storage_name}/train_fold_{fold}.feather"))
    # valid_feather = pd.read_feather(os.path.join(model_config.store_file, f"{model_config.storage_name}/valid_fold_{fold}.feather"))
    # features = [
    #     f for f in train_feather.columns if f not in [model_config.label, "kfold"]
    # ]
    # X_train = train_feather[features]
    # X_valid = valid_feather[features]
    # y_train = train_feather[model_config.label].values
    # y_valid = valid_feather[model_config.label].values
    # model = _model(**best_params)
    # model.fit(X_train, y_train, eval_set=[(X_valid, y_valid)])
    # pred = model.predict(test_file)
    # return features