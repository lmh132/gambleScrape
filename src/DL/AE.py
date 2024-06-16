import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from datasets import GameHistoryDataset
import pickle

class Encoder(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers):
        super(Encoder, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True, dropout = 0.25)

    def forward(self, x):
        # Initialize hidden state and cell state
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
        
        # Forward propagate LSTM
        out, (hn, cn) = self.lstm(x, (h0, c0))
        return hn, cn
    
class Decoder(nn.Module):
    def __init__(self, hidden_size, output_size, num_layers):
        super(Decoder, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.lstm = nn.LSTM(hidden_size, hidden_size, num_layers, batch_first=True, dropout = 0.25)
        self.fc = nn.Linear(hidden_size, output_size)

    def forward(self, x, hn, cn):
        # Forward propagate LSTM
        out, (hn, cn) = self.lstm(x, (hn, cn))
        # Decode hidden state of last time step
        out = self.fc(out)
        return out
    
class LSTMAutoencoder(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers):
        super(LSTMAutoencoder, self).__init__()
        self.encoder = Encoder(input_size, hidden_size, num_layers)
        self.decoder = Decoder(hidden_size, input_size, num_layers)

    def forward(self, x):
        # Encoder
        hn, cn = self.encoder(x)
        
        # Decoder
        # Prepare the initial input for the decoder (typically zeros or the last input frame)
        decoder_input = torch.zeros(x.size(0), x.size(1), self.encoder.hidden_size).to(x.device)
        out = self.decoder(decoder_input, hn, cn)
        
        return out
    
def validate_model(model, dataloader, criterion):
    model.eval()
    total_loss = 0
    with torch.no_grad():
        for batch in dataloader:
            batch = batch.to(device)
            output = model(batch)
            loss = criterion(output, batch)
            total_loss += loss.item()
    return total_loss / len(dataloader)
    
f = open("data/traindatapickles/PREV.pkl", "rb")
gamehistory = pickle.load(f)

traindataset = GameHistoryDataset(gamehistory[:5000])
traindataloader = DataLoader(dataset=traindataset, batch_size=32, shuffle=True)

testdataset = GameHistoryDataset(gamehistory[5000:10000])
testdataloader = DataLoader(dataset=traindataset, batch_size=32, shuffle=True)

    
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
input_size = 8  # Dimensionality of input features
hidden_size = 32  # Dimensionality of LSTM hidden states
num_layers = 2  # Number of LSTM layers
num_epochs = 100
learning_rate = 0.001

# Model, Loss, Optimizer
model = LSTMAutoencoder(input_size, hidden_size, num_layers).to(device)
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=learning_rate)

# Training loop
for epoch in range(num_epochs):
    model.train()
    for batch in traindataloader:
        batch = batch.to(device)

        out = model(batch)

        loss = criterion(out, batch)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        val_loss = validate_model(model, testdataloader, criterion)

    if (epoch + 1) % 10 == 0:
        print(f'Epoch [{epoch + 1}/{num_epochs}], Train Loss: {loss.item():.4f}, Val Loss: {val_loss:.4f}')

# Final validation
final_val_loss = validate_model(model, testdataloader, criterion)
print(f'Final Validation Loss: {final_val_loss:.4f}')

# Save the model's state dictionary
torch.save(model.state_dict(), 'model_state_dict.pth')

# Alternatively, save the entire model
torch.save(model, 'entire_model.pth')