import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from datasets import PresentGameDataset
import pickle

class NN(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(NN, self).__init__()
        self.nn = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.ReLU(),
            nn.Dropout(0.25),
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),
            nn.Dropout(0.25),
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),
            nn.Dropout(0.25),
            nn.Linear(hidden_size, output_size)
        )

    def forward(self, x):
        return self.nn(x)
    
def validate_model(model, dataloader, criterion):
    model.eval()
    total_loss = 0
    with torch.no_grad():
        for batch, labels in dataloader:
            batch = batch.to(device)
            output = model(batch).squeeze()
            loss = criterion(output, labels)
            total_loss += loss.item()
    return total_loss / len(dataloader)
    
f = open("data/traindatapickles/PROC.pkl", "rb")
games = pickle.load(f)

f = open("data/traindatapickles/OPP.pkl", "rb")
opp = pickle.load(f)

f = open("data/traindatapickles/SO.pkl", "rb")
so = pickle.load(f)

traindataset = PresentGameDataset(games[:12500], opp[:12500], so[:12500])
traindataloader = DataLoader(dataset=traindataset, batch_size=32, shuffle=True)

testdataset = PresentGameDataset(games[:12500], opp[:12500], so[:12500])
testdataloader = DataLoader(dataset=testdataset, batch_size=32, shuffle=True)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
input_size = 9  # Dimensionality of input features
hidden_size = 128  # Dimensionality of hidden states
fc_output_size = 1 #num of output features on fc layer
num_epochs = 100
learning_rate = 0.001

# Model, Loss, Optimizer
model = NN(input_size, hidden_size, fc_output_size).to(device)
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=learning_rate)

if __name__ == "__main__":
    for epoch in range(num_epochs):
        model.train()
        for batch, labels in traindataloader:
            batch = batch.to(device)

            out = model(batch).squeeze()

            loss = criterion(out, labels)

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
    torch.save(model.state_dict(), 'models/NN_state.pth')

    # Alternatively, save the entire model
    torch.save(model, 'models/NN.pth')