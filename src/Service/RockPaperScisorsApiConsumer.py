import requests
import time
from Domain.Dtos import *
from Domain.MoveTokens import *




class RockPaperScisorsApiConsumer:
    def __init__(self, apiBaseUrl: str, apiKey: str):
        self.apiBaseUrl = apiBaseUrl
        self.apiKey = apiKey
        self.headers = {"Content-Type":"application/json"}
        self.headers.update({"X-APIKEY":apiKey})



    def ServerStatus(self) -> str:
        response = requests.get(f'{self.apiBaseUrl}test', headers=self.headers)
        if response.status_code != 200:
            return f'Server responded with Bad Status Code Of: {response.status_code}'
    
        return f'{response.json()["message"]}'



    def GetContestList(self) -> dict:
        response = requests.get(f'{self.apiBaseUrl}contests', headers=self.headers)
        if response.status_code != 200:
            return None #throw exception later
        return response.json()["contestList"]



    def GetContest(self, contestId: str) -> dict:
        response = requests.get(f'{self.apiBaseUrl}contest/{contestId}', headers=self.headers)
        if response.status_code != 200:
            return None #throw exception later
        return response.json()



    def GetContestAsPlayer(self, contestId: str, playerId: str) -> dict:
        response = requests.get(f'{self.apiBaseUrl}contest/{contestId}/player/{playerId}', headers=self.headers)
        if response.status_code != 200:
            return None #throw exception later
        return response.json()



    def CreateContest(self, contestName: str, roundsToWin: int, gameType: str, oponentType: str) -> dict:
        requestContent = CreateContestRequestDto(contestName, roundsToWin, gameType, oponentType)
        response = requests.post(f'{self.apiBaseUrl}contest', data = requestContent.to_json(), headers=self.headers)
        if response.status_code != 200:
            return None #throw exception later
        return response.json()
        


    def JoinContest(self, contestId: str) -> dict:
        response = requests.post(f'{self.apiBaseUrl}contest/{contestId}/join', headers=self.headers)
        if response.status_code != 200:
            return None #throw exception later
        return response.json()



    def CancelContest(self, contestId: str, playerId: str,) -> dict:
        response = requests.patch(f'{self.apiBaseUrl}contest/{contestId}/player/{playerId}/cancel', headers=self.headers)
        if response.status_code != 200:
            return None #throw exception later
        return response.json()



    def PostMove(self, contestDtoDict, moveName) -> (dict, dict):
        contestId = contestDtoDict["contestId"]
        playerId = contestDtoDict["playerId"]
        gameId = contestDtoDict["currentGameId"]

        response = requests.post(f'{self.apiBaseUrl}contest/{contestId}/game/{gameId}/player/{playerId}/{moveName}', headers=self.headers)
        responseDict = response.json()

        gameDtoDict = responseDict["gameResponse"]
        contestDtoDict = responseDict["contestResponse"]

        return (gameDtoDict, contestDtoDict)



    def WaitForContestState(self, contestDtoDict: dict, targetContestState: str, timeoutSeconds: int) -> dict:
            secondsWaited: int = 0
            while contestDtoDict["contestState"] != targetContestState:
                time.sleep(1)
                contestDtoDict = self.GetContestAsPlayer(contestDtoDict["contestId"], contestDtoDict["playerId"])
                secondsWaited += 1
                if secondsWaited >= timeoutSeconds:
                    return contestDtoDict
                
            return contestDtoDict



    def WaitForContestStateChangeFrom(self, contestDtoDict: dict, targetContestState: str, timeoutSeconds: int) -> dict:
        secondsWaited: int = 0
        while contestDtoDict["contestState"] == targetContestState:
            
            if secondsWaited >= timeoutSeconds:
                return contestDtoDict
            
            time.sleep(1)
            contestDtoDict = self.GetContestAsPlayer(contestDtoDict["contestId"], contestDtoDict["playerId"])
            secondsWaited += 1
            
            
        return contestDtoDict



    def WaitForGameState(self, contestDtoDict: dict, gameId: uuid, currentGameState: str, targetGameState: str,  timeoutSeconds: int) -> (str, dict):
        secondsWaited: int = 0
        while currentGameState != targetGameState:
            time.sleep(1)
            secondsWaited += 1

            if secondsWaited >= timeoutSeconds:
                for game in contestDtoDict["games"]:
                    if game["gameId"] == gameId:
                        return game["gameState"], contestDtoDict
                raise Exception(f'Game: {gameId} is No Longer Part Of Contest: {contestDtoDict["contestId"]}')
        
            contestDtoDict = self.GetContestAsPlayer(contestDtoDict["contestId"], contestDtoDict["playerId"])
            games = contestDtoDict["games"]
            for game in games:
                if game["gameId"] == gameId:
                    gameDtoDict = game
                    currentGameState = gameDtoDict["gameState"]
                    break

        return (currentGameState, contestDtoDict)