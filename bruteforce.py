from multiprocessing import Process

stdnos = {}

#read in the student numbers and append them to arrays depending on their checksum
with open("ids.txt", "r") as f:
  for line in f.readlines():
    line = line.strip()
    if line[-1] not in stdnos:
      stdnos[line[-1]] = []
    
    #if len(stdnos[line[-1]]) < 500:
    stdnos[line[-1]].append(line[0:-1])

#since there are 10 check digits, assuming its a % 10 hash function, weights would range from 0-9
#can use a base 10 number to represent the weights with each digit being a weight

def calc_checksum(id, weights):
  sum = 0
  for i in xrange(8):
    sum += int(id[i]) * int(str(weights)[i])
  
  return sum % 10

def validate(stdnos, weights):
  found_checksum_numerical_values = {}
  for check_digit in stdnos:
    numerical_checksum = calc_checksum(stdnos[check_digit][0], weights)
    if numerical_checksum in found_checksum_numerical_values:
      #different checksum_digits must have different numerical values
      return False
    else:
      found_checksum_numerical_values[numerical_checksum] = check_digit
    
    for stdno in stdnos[check_digit]:
      if numerical_checksum != calc_checksum(stdno, weights):
        return False
    
  alphabets = "ABCDEFGHJK"
  for i in xrange(10):
    if found_checksum_numerical_values[i] != alphabets[i]:
      return False
    
  return True

class Worker(Process):
  def __init__(self, lower, upper):
    super(Worker, self).__init__()
    self.lower = lower
    self.upper = upper
  def run(self):
    global stdnos
    print "Testing from range %d to %d" % (self.lower, self.upper)
    for weights in xrange(self.lower, self.upper):
      if validate(stdnos, weights):
        print "Weight: "+str(weights)

      weights += 1

if __name__ == "__main__":
  workers = {}
  for i in xrange(4):
    min = 11111111+(i*2)*11111111
    max = 11111111+((i+1)*2)*11111111
    workers[i] = Worker(min, max)
    workers[i].start()