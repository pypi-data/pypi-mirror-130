# from autolgb import AutoLGB

# a = AutoLGB(
#     "/media/aditta/Deep Learning files/autolgb/dataset/test.csv",
#     "/media/aditta/Deep Learning files/autolgb/dataset/test_file.csv",
#     "/media/aditta/Deep Learning files/autolgb/",
#     storage_name = "output",
#     label="Cover_Type",
#     num_folds=5,
#     direction="maximize",
#     n_trials=1
# )

# best = a.train()
# print(a.predict(best))
# import pandas as pd
# import numpy as np

# def reduce_mem_usage(df):
#     """ iterate through all the columns of a dataframe and modify the data type
#         to reduce memory usage.        
#     """
#     start_mem = df.memory_usage().sum() / 1024**2
#     print('Memory usage of dataframe is {:.2f} MB'.format(start_mem))
    
#     for col in df.columns:
#         col_type = df[col].dtype
        
#         if col_type != object:
#             c_min = df[col].min()
#             c_max = df[col].max()
#             if str(col_type)[:3] == 'int':
#                 if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max:
#                     df[col] = df[col].astype(np.int8)
#                 elif c_min > np.iinfo(np.int16).min and c_max < np.iinfo(np.int16).max:
#                     df[col] = df[col].astype(np.int16)
#                 elif c_min > np.iinfo(np.int32).min and c_max < np.iinfo(np.int32).max:
#                     df[col] = df[col].astype(np.int32)
#                 elif c_min > np.iinfo(np.int64).min and c_max < np.iinfo(np.int64).max:
#                     df[col] = df[col].astype(np.int64)  
#             else:
#                 if c_min > np.finfo(np.float16).min and c_max < np.finfo(np.float16).max:
#                     df[col] = df[col].astype(np.float16)
#                 elif c_min > np.finfo(np.float32).min and c_max < np.finfo(np.float32).max:
#                     df[col] = df[col].astype(np.float32)
#                 else:
#                     df[col] = df[col].astype(np.float64)
#         else:
#             df[col] = df[col].astype('category')

#     end_mem = df.memory_usage().sum() / 1024**2
#     print('Memory usage after optimization is: {:.2f} MB'.format(end_mem))
#     print('Decreased by {:.1f}%'.format(100 * (start_mem - end_mem) / start_mem))
    
#     return df


test_1 = pd.read_csv("/media/aditta/Deep Learning files/autolgb/dataset/multi_class_classification.csv")
print(test_1)
test_1 = reduce_mem_usage(test_1)
print(test_1)
# test_2 = test_1[:10]
# test_2.to_csv("/media/aditta/Deep Learning files/autolgb/dataset/multi_class_classification_test.csv", index=False)

# # # print(test_1.Cover_Type.value_counts())
# # # fold_names = ["Kfold", "KFOLD", "kfold"]
# # # for fold in fold_names:
# # #     if fold not in test_1.columns:
# # #         print("no")

# # # from functools import partial
# # # def f(a, b, c, x):
# # #     return 10*a + 10*b + 10*c + x

# # # g = partial(
# # #     f, 3, 1, 4
# # # )

# # # print(g(5))
# # import optuna
# # import sklearn
# # from sklearn import datasets
# # from sklearn.model_selection import train_test_split
# # import lightgbm as lgb
# # import numpy as np

# # def objective(trial):
# #     data, target = datasets.load_breast_cancer(return_X_y=True)
# #     train_x, valid_x, train_y, valid_y = train_test_split(data, target, test_size=0.25)
# #     dtrain = lgb.Dataset(train_x, label=train_y)
# #     dvalid = lgb.Dataset(valid_x, label=valid_y)

# #     param = {
# #         "objective": "binary",
# #         "metric": "auc",
# #         "verbosity": -1,
# #         "boosting_type": "gbdt",
# #         "bagging_fraction": trial.suggest_float("bagging_fraction", 0.4, 1.0),
# #         "bagging_freq": trial.suggest_int("bagging_freq", 1, 7),
# #         "min_child_samples": trial.suggest_int("min_child_samples", 5, 100),
# #     }

# #     # Add a callback for pruning.
# #     pruning_callback = optuna.integration.LightGBMPruningCallback(trial, "auc")
# #     gbm = lgb.train(
# #         param, dtrain, valid_sets=[dvalid], callbacks=[pruning_callback]
# #     )

# #     preds = gbm.predict(valid_x)
# #     pred_labels = np.rint(preds)
# #     accuracy = sklearn.metrics.accuracy_score(valid_y, pred_labels)
# #     return accuracy

# # study = optuna.create_study(
# #     direction="maximize",
# #     sampler=optuna.samplers.TPESampler(seed=42),
# #     pruner=optuna.pruners.MedianPruner(n_warmup_steps=10),
# # )
# # study.optimize(objective, n_trials=100, timeout=600)

# # import pandas as pd
# # import os

# # train_feather = pd.read_feather("/media/aditta/Deep Learning files/autolgb/output/train_fold_0.feather")
# # features = [
# #                 f for f in train_feather.columns if f not in ["target", "kfold"]
# #             ]
# # X_train = train_feather[features]

# # print(X_train)

# # from pydantic import BaseModel


# import numpy as np
# import optuna

# import lightgbm as lgb
# import sklearn.datasets
# import sklearn.metrics
# from sklearn.model_selection import train_test_split


# # FYI: Objective functions can take additional arguments
# # (https://optuna.readthedocs.io/en/stable/faq.html#objective-func-additional-args).
# def objective(trial):
#     data, target = sklearn.datasets.load_breast_cancer(return_X_y=True)
#     train_x, valid_x, train_y, valid_y = train_test_split(data, target, test_size=0.25)
#     dtrain = lgb.Dataset(train_x, label=train_y)

#     param = {
#         "objective": "binary",
#         "metric": "binary_logloss",
#         "verbosity": -1,
#         "boosting_type": "gbdt",
#         "lambda_l1": trial.suggest_float("lambda_l1", 1e-8, 10.0, log=True),
#         "lambda_l2": trial.suggest_float("lambda_l2", 1e-8, 10.0, log=True),
#         "num_leaves": trial.suggest_int("num_leaves", 2, 256),
#         "feature_fraction": trial.suggest_float("feature_fraction", 0.4, 1.0),
#         "bagging_fraction": trial.suggest_float("bagging_fraction", 0.4, 1.0),
#         "bagging_freq": trial.suggest_int("bagging_freq", 1, 7),
#         "min_child_samples": trial.suggest_int("min_child_samples", 5, 100),
#     }

#     gbm = lgb.train(param, dtrain)
#     preds = gbm.predict(valid_x)
#     pred_labels = np.rint(preds)
#     accuracy = sklearn.metrics.accuracy_score(valid_y, pred_labels)
#     return accuracy


# if __name__ == "__main__":
#     study = optuna.create_study(direction="maximize")
#     study.optimize(objective, n_trials=10)

#     # print("Number of finished trials: {}".format(len(study.trials)))

#     # print("Best trial:")
#     # trial = study.best_trial

#     # print("  Value: {}".format(trial.value))

#     print("  Params: ")
#     print(study.best_params)