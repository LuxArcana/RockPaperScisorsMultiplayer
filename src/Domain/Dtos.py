import uuid


class CreateContestRequestDto:
  def __init__ (self, contestName, roundsToWin, gameType, oponentType):
    self.contestName: str = contestName
    self.roundsToWin: int = roundsToWin
    self.gameType: str = gameType
    self.oponentType: str = oponentType




class PlaceMoveResponseDto:
  def __init__(self, gameResponse, matchResponse):
    self.gameResponse: GameResponseDto = gameResponse
    self.contestResponse: ContestResponseDto = matchResponse

  def __repr__(self):
    return f'{{"gameResponse":{self.gameResponse.to_json()},"contestResponse":{self.contestResponse.to_json()}}}'

  def __str__(self):
    return self.__repr__()
  
  def to_json(self):
    return self.__repr__()




class GameResponseDto:
  def __init__(self, gameId, gameState, yourMove, opponentMove, winner):
    self.gameId: uuid = gameId
    self.gameState: str = gameState
    self.yourMove: str = yourMove
    self.opponentMove: str = opponentMove
    self.winner: str = winner
    
  def __repr__(self):
    return f'{{"gameId":"{self.gameId}","gameState":"{self.gameState}","yourMove":"{self.yourMove}","opponentMove":"{self.opponentMove}","winner":"{self.winner}"}}'

  def __str__(self):
    return self.__repr__()
  
  def to_json(self):
    return self.__repr__()
  
  def __getstate__(self):
    return self.gameId, self.gameState, self.yourMove, self.opponentMove, self.winner
  
  def __setstate__(self, state):
    self.gameId, self.gameState, self.yourMove, self.opponentMove, self.winner = state




class ContestListResponseDto:
  def __init__(self, contests):
    self.contestList = dict()
    for contestId in contests:
      self.contestList.update({contestId: ContestResponseDto(contests[contestId], None)})

  def __repr__(self) -> str:
    output: str = f'{{"contestList": ['
    delimiter: str = ''
    for contestId in self.contestList:
      output = f'{output}{delimiter}{self.contestList[contestId].to_json()},'
      delimiter = ','

    return f'{output}]}}'
  
  def __str__(self) -> str:
    return self.__repr__()
  
  def to_json(self) -> str:
    return self.__repr__()
  



class ContestResponseDto:
  def __init__(self, contest, playerId):
    self.contestId: uuid = contest.contestId
    self.contestName: str = contest.contestName
    self.contestState: str = contest.contestState
    self.roundsToWin: int = contest.roundsToWin
    self.gameType: str = contest.gameType
    self.oponentType: str = contest.oponentType
    self.winningPlayer: str = None
    
    if contest.winningPlayerId is not None:
      if contest.winningPlayerId == playerId:
        self.winningPlayer = 'YOU'
      else:
        self.winningPlayer = 'OPPONENT'
    
    self.games = dict()
    for gameId, game in contest.games.items():
      self.games.update({gameId: game.BuildResponseDto(playerId)})
    
    self.currentGameId: uuid = contest.currentGameId
    self.playerId = playerId

  #def __getstate__(self):
  #  return self.contestId, self.contestName, self.contestState, self.roundsToWin, self.gameType, self.oponentType, self.winningPlayer, self.games
  
  #def __setstate__(self, state):
  #  self.contestId, self.contestName, self.contestState, self.roundsToWin, self.gameType, self.oponentType, self.winningPlayer, self.games = state

  def __repr__(self):
    gameJson = ''
    delimiter = ''
    for gameId in self.games:
      gameJson = f'{gameJson}{delimiter}{self.games[gameId].to_json()}'
      delimiter = ','

    currentGameIdReturnValue: str = 'null'
    if self.currentGameId is not None:
      currentGameIdReturnValue = f'"{self.currentGameId}"'

    return f'{{"contestId":"{self.contestId}","contestName":"{self.contestName}","contestState":"{self.contestState}","gameType":"{self.gameType}","oponentType":"{self.oponentType}","roundsToWin":"{self.roundsToWin}","currentGameId":{currentGameIdReturnValue},"games": [{gameJson}],"winningPlayer":"{self.winningPlayer}","playerId":"{self.playerId}"}}'


  def __str__(self):
    return self.__repr__()
  
  def to_json(self):
    return self.__repr__()
