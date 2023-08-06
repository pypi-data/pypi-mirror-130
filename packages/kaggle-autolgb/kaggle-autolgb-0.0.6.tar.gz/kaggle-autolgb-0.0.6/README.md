
## Authors

- [@Aditta-das](https://github.com/Aditta-das)


# kaggle-autolgb

kaggle autolgb is a combination of lightgbm and optuna. I tried to make kaggle monthly competition simple. Its only working with classification problem.

## Installation
```
pip install kaggle-autolgb
``` 
   
## Features

- autotune
- autotrain
- auto submission file generate
- auto prediction 


## Deployment

```
from autolgb import AutoLGB

model = AutoLGB(
    train_file = "trainning file path",
    test_file="testing file path",
    store_file= "store file path",
    storage_name = "store", # anything i.e: store/target/storage
    label="dataset label column name",
    num_folds=5, # num of num_folds
    direction="maximize", # maximize or minimize
    n_trials=2, # optuna trial
    gpu=False # gpu usage
)

best = model.train() # returns best params
model.predict(best)
model.submission_kaggle_format("kaggle submission file")
```

## License

[Apache 2.0](https://choosealicense.com/licenses/apache-2.0/)

