
  
  class TwoDConvNet(nn.Module):
    def __init__(self):
        super(TwoDConvNet, self).__init__()
        self.conv1 = nn.Conv2d(1, 8, 4, 2)
        self.conv2 = nn.Conv2d(8, 16, 3, 2)
        self.conv3 = nn.Conv2d(16, 32, 2, 2)

        self.max_pool = nn.MaxPool2d(2)

        self.fc1 = nn.Linear(32 * 31, 700)
        self.fc2 = nn.Linear(700, 513)
        self.to(device)

    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        x = F.relu(self.conv3(x))
        x = self.max_pool(x)
        x = x.reshape(x.shape[0], -1)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))

        return x
        
        
