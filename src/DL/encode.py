import torch
import pickle
import pprint
from AE import Autoencoder
import numpy as np
from alive_progress import alive_bar

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

input_size = 8  # Dimensionality of input features
hidden_size = 32  # Dimensionality of LSTM hidden states
fc_output_size = 5
num_layers = 2  # Number of LSTM layers
num_epochs = 100
learning_rate = 0.001
dropout = 0.25

# Instantiate and load the encoder part of the model
encoder_model = Autoencoder(input_size, hidden_size, fc_output_size, num_layers)
encoder_model.load_state_dict(torch.load("models/AE_state.pth"))  # Load the encoder part
encoder_model.to(device)
encoder_model.eval()

# Function to extract features
def extract_features(model, data):
    data = torch.from_numpy(data).unsqueeze(dim = 0)
    model.eval()
    with torch.no_grad():
        data = data.to(device)
        features = model(data)
    return features

f = open("data/traindatapickles/PREV.pkl", "rb")
gamehistory = pickle.load(f)

PROC = []

if __name__ == "__main__":
    print("processing over 15,000 game sequences...")
    with alive_bar(len(gamehistory)) as bar:
        for new_data in gamehistory:
            _, encoded_features = extract_features(encoder_model, new_data)
            PROC.append(encoded_features)
            bar()
    PROC = np.array(PROC, dtype=np.float32).reshape(-1, 5)
    print("final output shape: {}".format(PROC.shape))
    with open("data/traindatapickles/PROC.pkl", "wb") as f:
        pickle.dump(PROC, f)
        f.close()