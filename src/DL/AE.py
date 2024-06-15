import torch
import torch.nn as nn

class Encoder(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers):
        super(Encoder, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)

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
        self.lstm = nn.LSTM(hidden_size, hidden_size, num_layers, batch_first=True)
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
    
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
input_size = 10  # Dimensionality of input features
hidden_size = 25  # Dimensionality of LSTM hidden states
num_layers = 2  # Number of LSTM layers
num_epochs = 1000
learning_rate = 0.001

# Model, Loss, Optimizer
model = LSTMAutoencoder(input_size, hidden_size, num_layers).to(device)
criterion = nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

# Dummy data (replace with actual data)
input_sequence = torch.randn(32, 10, input_size).to(device)  # Batch size of 32, sequence length of 10

# Training loop
for epoch in range(num_epochs):
    model.train()
    optimizer.zero_grad()

    # Forward pass
    output_sequence = model(input_sequence)
    
    # Calculate loss
    loss = criterion(output_sequence, input_sequence)
    
    # Backward pass and optimize
    loss.backward()
    optimizer.step()
    
    if (epoch+1) % 10 == 0:
        print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}')