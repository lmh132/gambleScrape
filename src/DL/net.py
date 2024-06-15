import torch
import torch.nn as nn
import torchvision
import torchvision.transforms as transforms

#device config
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

#hyper params
input_size = 7
sequence_length = 3
num_layers = 2
hidden_size = 128
output_size = 1
num_epochs = 5
batch_size = 64
learning_rate = 0.001

class RNN(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers, output_size):
        super(RNN, self).__init__()
        self.num_layers = num_layers

        self.hidden_size = hidden_size

        self.rnn = nn.RNN(input_size, hidden_size, num_layers, batch_first=True)

model = RNN(input_size, hidden_size, num_layers, output_size)