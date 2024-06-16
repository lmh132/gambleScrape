import numpy as np
import json
from collections import OrderedDict
import pprint
from typing import Any
from torch.utils.data import Dataset


class GameHistoryDataset(Dataset):
    def __init__(self, arr):
        self.arr = arr

    def __len__(self):
        return self.arr.shape[0]
    
    def __getitem__(self, index) -> Any:
        return self.arr[index]