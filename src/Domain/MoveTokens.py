

class MoveToken:
  def __init__(self):
    self.Name: str = 'INVALID'
    
  def __str__(self) -> str:
    return 'INVALID'

  def equality(self, other) -> int:
    return None
  


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



class RockMoveToken(MoveToken):
  def __init__(self):
    self.Name: str = 'ROCK'

  def __str__(self) -> str:
    return self.Name
    
  def equality(self, other) -> int:
    match other.Name:
      case 'ROCK':
        return 0
      case 'PAPER':
        return -1
      case 'SCISORS':
        return 1
      case 'LIZARD':
        return 1
      case 'SPOK':
        return -1
      case _:
        return None
  
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



class PaperMoveToken(MoveToken):
  def __init__(self):
    self.Name: str = 'PAPER'

  def __str__(self) -> str:
    return self.Name
  
  def equality(self, other) -> int:
    match other.Name:
      case 'ROCK':
        return 1
      case 'PAPER':
        return 0
      case 'SCISORS':
        return -1
      case 'LIZARD':
        return -1
      case 'SPOK':
        return 1
      case _:
        return None
  
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
  


class ScisorsMoveToken(MoveToken):
  def __init__(self):
    self.Name: str = 'SCISORS'

  def __str__(self):
    return self.Name
  
  
  def equality(self, other):
    match other.Name:
      case 'ROCK':
        return -1
      case 'PAPER':
        return 1
      case 'SCISORS':
        return 0
      case 'LIZARD':
        return 1
      case 'SPOK':
        return -1
      case _:
        return None
  
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
  
  

class LizardMoveToken(MoveToken):
  def __init__(self):
    self.Name: str = 'LIZARD'

  def __str__(self):
    return self.Name
  
  def equality(self, other):
    match other.Name:
      case 'ROCK':
        return -1
      case 'PAPER':
        return 1
      case 'SCISORS':
        return -1
      case 'LIZARD':
        return 0
      case 'SPOK':
        return 1
      case _:
        return None
  
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

    
    
class SpokMoveToken(MoveToken):
  def __init__(self):
    self.Name: str = 'SPOK'
  
  def __str__(self):
    return self.Name
  
  def equality(self, other):
    match other.Name:
      case 'ROCK':
        return 1
      case 'PAPER':
        return -1
      case 'SCISORS':
        return 1
      case 'LIZARD':
        return -1
      case 'SPOK':
        return 0
      case _:
        return None
  

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
    




    
class MoveTokenBuilder:
  def FromName(stringName) -> MoveToken:
    match stringName.upper():
      case 'ROCK':
       return RockMoveToken()
      case 'R':
        return RockMoveToken()
      case 'PAPER':
        return PaperMoveToken()
      case 'P':
        return PaperMoveToken()
      case 'SCISORS':
        return ScisorsMoveToken()
      case 'S':
        return ScisorsMoveToken()
      case 'LIZARD':
        return LizardMoveToken()
      case 'L':
        return LizardMoveToken()
      case 'SPOK':
        return SpokMoveToken()
      case 'K':
        return SpokMoveToken()
      case _:
        return None