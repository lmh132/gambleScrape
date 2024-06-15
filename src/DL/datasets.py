import numpy as np
import json
from collections import OrderedDict
import pprint
from typing import Any
from torch.utils.data import Dataset


class BaseballDataset(Dataset):
    def __init__(self, datadict):
        self.datadict = datadict

    def __len__(self):
        return len(self.datadict["strikeouts"])
    
    def __getitem__(self, index) -> Any:
        prevgamestats = self.datadict["prevgames"][index]
        oppstats = self.datadict["oppstats"][index]
        strikeouts = self.datadict["strikeouts"][index]

        return (prevgamestats, oppstats), strikeouts