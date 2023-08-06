#!/usr/bin/env python3
import sys
sys.path.insert(0, 'path/to/utils.py')
sys.path.insert(0, 'path/to/schemas.py')
from dataclasses import dataclass
import logging
from sklearn import model_selection
import pandas as pd
from logger import logger
# import utils
from .utils import reduce_memory_usage, obj_to_cat, apply_binary_classification, apply_multilabel_classification, model_training, predict_test
import os
import json
from .schemas import Configuration

'''
model = AutoLGB()
model.train()

function design:
    _create_folds()
    _data_preprocess()
        if label data type is object
        --> apply_binary_classification()
        --> apply_multilabel_classification()
    _data_spliting()
    _optimizer() optuna train and get the best params
    train()
    predict()
'''

@dataclass
class AutoLGB:
    train_file: str = None
    test_file: str = None
    store_file: str = None
    storage_name: str = "storage"
    num_folds: int = 5
    shuffle: bool = True
    seed: int = 42
    label: str = None
    gpu: bool = False
    n_trials: int = 1
    direction: str = "minimize"

    '''
    StratifiedKFold : split data
    '''
    def _create_folds(self, train_data):
        train_data["kfold"] = -1
        y = train_data[self.label].values
        kf = model_selection.StratifiedKFold(
            n_splits=self.num_folds, 
            shuffle=self.shuffle, 
            random_state=self.seed
        )
        for _fold, (train_, valid_) in enumerate(kf.split(X=train_data, y=y)):
            train_data.loc[valid_, "kfold"] = _fold


    '''
    apply fold and create fold columns
    store in folder as feather
    apply label encoder
    drop useless columns
    split data
    '''

    def _make_folder(self):
        directory = os.path.join(self.store_file, self.storage_name)
        if not os.path.exists(directory):
            logger.info(f"Create folder name : {self.storage_name} folder")
            os.mkdir(directory)
        else:
            logger.info("Folder already exists")

    def _data_preprocess(self):
        self._make_folder()
        
        train_data = pd.read_csv(self.train_file)
        train_data = reduce_memory_usage(train_data)
        train_data = obj_to_cat(train_data, self.label)
        fold_names = ["Kfold", "KFOLD", "kfold"]
        logger.info("Using 'kfold' for train data")
        model_config = {}
        model_config["test_file"] = self.test_file
        model_config["num_folds"] = self.num_folds
        model_config["store_file"] = self.store_file
        model_config["storage_name"] = self.storage_name
        model_config["label"] = self.label
        model_config["gpu"]= self.gpu
        model_config["n_trials"] = self.n_trials
        model_config["gpu_platform_id"] = 0
        model_config["gpu_device_id"] = 0
        model_config["direction"] = self.direction
        self.model_config = Configuration(**model_config)

        for fold_name in fold_names:
            if fold_name not in train_data.columns:
                self._create_folds(train_data)
        logger.info("'kfold' done...")
        if len(train_data[self.label].unique()) > 2:
            logger.info('Multiclass Classification')
            train_data = apply_multilabel_classification(train_data, self.label)
        else:
            logger.info('Binary Classification')
            train_data = apply_binary_classification(train_data, self.label)

        for fold in range(self.num_folds):
            train_fold = train_data[train_data.kfold != fold].reset_index(drop=True)
            test_fold = train_data[train_data.kfold == fold].reset_index(drop=True)
            
            
            logger.info(f"Saving Train and Valid Fold: {fold}")
            train_fold.to_feather(os.path.join(self.store_file, f"{self.storage_name}/train_fold_{fold}.feather"))
            test_fold.to_feather(os.path.join(self.store_file, f"{self.storage_name}/valid_fold_{fold}.feather"))
  

    def train(self):
        '''
        model.fit(X_train, y_train) add eval_set
        '''
        self._data_preprocess()
        logging.info("Model Training and try to get the best params")
        best_params = model_training(self.model_config)
        logging.info("Train Finished")
        params_dir = os.path.join(self.store_file, f"{self.storage_name}/best_params.json")
        with open(params_dir, "w") as f:
            json.dump(best_params, f) 
        print(self.predict(best_params))
        return best_params
    
    def predict(self, best_params):
        # test_ = pd.read_csv(self.test_file)
        pred = predict_test(self.model_config, best_params)
        sub = pd.DataFrame(pred, columns=[self.label]).to_csv(os.path.join(self.store_file, f"{self.storage_name}/sub.csv"), index=False)
        return sub

    def submission_kaggle_format(self, path):
        submission = pd.read_csv(path)
        pre_test_csv = pd.read_csv(os.path.join(self.store_file, f"{self.storage_name}/sub.csv"))
        submission[self.label] = pre_test_csv[self.label]
        submission.to_csv(os.path.join(self.store_file, f"{self.storage_name}/kaggle_submission.csv"), index=False)
        logger.info("Submission file ready")


# if __name__ == "__main__":
#     a = AutoLGB(
#         train_file = "/media/aditta/Deep Learning files/autolgb/dataset/test.csv",
#         test_file="/media/aditta/Deep Learning files/autolgb/dataset/test_file.csv",
#         store_file= "/media/aditta/Deep Learning files/autolgb/",
#         storage_name = "output",
#         label="Cover_Type",
#         num_folds=5,
#         direction="maximize",
#         n_trials=1
#     )
#     best = a.train()
#     print(a.predict(best))
#     a.submission_kaggle_format("/media/aditta/Deep Learning files/autolgb/dataset/test_file.csv")