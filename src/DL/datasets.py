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
    
class PresentGameDataset(Dataset):
    def __init__(self, encoded_data, opponent_stats, strikeouts):
        self.encoded_data = encoded_data
        self.opponent_stats = opponent_stats
        self.strikeouts = strikeouts

    def __len__(self):
        return self.encoded_data.shape[0]
    
    def __getitem__(self, index) -> Any:
        return (np.concatenate([self.encoded_data[index], self.opponent_stats[index]]), self.strikeouts[index])