from pydantic import BaseModel


class Configuration(BaseModel):
    train_file: str = None
    test_file: str = None
    store_file: str = None
    storage_name: str = "storage"
    shuffle: bool = True
    seed: int = 42
    label: str = None
    gpu: bool = False
    n_trials: int = 100
    gpu: bool = False
    num_folds: int = 5
    direction: str = "minimize"
