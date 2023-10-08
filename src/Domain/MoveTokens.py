

class MoveToken:
  def FromName(name):
    name = name.upper()
    if name == 'R' or name == 'ROCK':
      return RockToken()
    if name == 'P' or name == 'PAPER':
      return PaperToken()
    if name == 'S' or name == 'SCISORS':
      return ScisorsToken()
    if name == 'L' or name == 'LIZARD':
      return LizardToken()
    if name == 'K' or name == 'SPOK':
      return SpokToken()
    return None
    
  def __str__(self):
    return self.Name
    
  def __gt__(self, other):
    if self.equality(other) > 0:
      return True
    return False
    
  def __ge__(self, other):
    if self.equality(other) >= 0:
      return True
    return False
    
  def __eq__(self, other):
    if self.equality(other) == 0:
      return True
    return False
    
  def __le__(self, other):
    if self.equality(other) <= 0:
      return True
    return False
    
  def __lt__(self, other):
    if self.equality(other) < 0:
      return True
    return False



class RockToken(MoveToken):
  def __init__(self):
    self.Name = 'ROCK'
    
  def equality(self, other):
    if other.Name == 'ROCK':
      return 0
    if other.Name == 'PAPER':
      return -1
    if other.Name == 'SCISORS':
      return 1
    if other.Name == 'LIZARD':
      return 1
    if other.Name == 'SPOK':
      return -1
    return None
    
    
class PaperToken(MoveToken):
  def __init__(self):
    self.Name = 'PAPER'
  
  def equality(self, other):
    if other.Name == 'ROCK':
      return 1
    if other.Name == 'PAPER':
      return 0
    if other.Name == 'SCISORS':
      return -1
    if other.Name == 'LIZARD':
      return -1
    if other.Name == 'SPOK':
      return 1
    return None


class ScisorsToken(MoveToken):
  def __init__(self):
    self.Name = 'SCISORS'
    
  def equality(self, other):
    if other.Name == 'ROCK':
      return -1
    if other.Name == 'PAPER':
      return 1
    if other.Name == 'SCISORS':
      return 0
    if other.Name == 'LIZARD':
      return 1
    if other.Name == 'SPOK':
      return -1
    return None
    
  
class LizardToken(MoveToken):
  def __init__(self):
    self.Name = 'LIZARD'
    
  def equality(self, other):
    if other.Name == 'ROCK':
      return -1
    if other.Name == 'PAPER':
      return 1
    if other.Name == 'SCISORS':
      return -1
    if other.Name == 'LIZARD':
      return 0
    if other.Name == 'SPOK':
      return 1
    return None


class SpokToken(MoveToken):
  def __init__(self):
    self.Name = 'SPOK'
    
  def equality(self, other):
    if other.Name == 'ROCK':
      return 1
    if other.Name == 'PAPER':
      return -1
    if other.Name == 'SCISORS':
      return 1
    if other.Name == 'LIZARD':
      return -1
    if other.Name == 'SPOK':
      return 0
    return None
