class calculator:

  memory = 0

  def addtion (x):
    calculator.memory = calculator.memory + x
    return calculator.memory

  def subtraction(x):
    calculator.memory = calculator.memory - x
    return calculator.memory

  def multiplication(x):
    calculator.memory = calculator.memory * x
    return calculator.memory

  def division (x):
    calculator.memory = calculator.memory / x
    return calculator.memory

  def nroot(x):
    calculator.memory = calculator.memory**(1/float(x))
    return calculator.memory

  def reset():
    calculator.memory = 0
    return 'Memory cleared'