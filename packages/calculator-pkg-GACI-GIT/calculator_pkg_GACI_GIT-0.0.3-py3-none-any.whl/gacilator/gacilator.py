class calculator:

  memory = 0

  def addition (self, x):
    self.memory = self.memory + x
    return self.memory

  def subtraction(self, x):
    self.memory = self.memory - x
    return self.memory

  def multiplication(self, x):
    self.memory = self.memory * x
    return self.memory

  def division(self, x):
    self.memory = self.memory / x
    return self.memory

  def nroot(self, x):
    self.memory = x**(1/float(self.memory))
    return self.memory

  def reset(self):
    self.memory = 0
    return 'Memory cleared'