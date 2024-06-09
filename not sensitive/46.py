


class VAENet(nn.Module):
  
  
    def __init__(self):
      super(VAENet, self).__init__()
      
      
      self.latent_variable_dim = 4
      self.fc1 = nn.Linear(784, 222)
 #     self.fc2 = nn.Linear(500,200)
      self.fc3mu = nn.Linear(222, self.latent_variable_dim) # used for mean
      self.fc3logvar = nn.Linear(222, self.latent_variable_dim)  #used for sd

      self.fc4 = nn.Linear(self.latent_variable_dim, 333)
      self.fc5 = nn.Linear(333, 784)

    def encode(self, x):
      x = F.relu(self.fc1(x))
 #     x = F.relu(self.fc2(x))

      return self.fc3mu(x),self.fc3logvar(x)

    def reparams(self, mu, logvar):
      if self.training:
        std = logvar.mul(0.5).exp_()
        eps = Variable(std.data.new(std.size()).normal_())
        return eps.mul(std).add_(mu)
      else:
        return mu
    
    def decode(self, lat):
      x = F.relu(self.fc4(lat))
      x = F.sigmoid(self.fc5(x))
      return x
      
    
    
    def forward(self, x):
      mu ,logvar = self.encode(x)
      lat = self.reparams(mu,logvar)
      output = self.decode(lat)

      return output, mu, logvar
      
