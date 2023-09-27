import requests
import time
from os import system
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



    def PostMove(self, contestDtoDict, moveName) -> (dict, dict):
        contestId = contestDtoDict["contestId"]
        playerId = contestDtoDict["playerId"]
        gameId = contestDtoDict["currentGameId"]

        response = requests.post(f'{self.apiBaseUrl}contest/{contestId}/game/{gameId}/player/{playerId}/{moveName}', headers=self.headers)
        responseDict = response.json()

        gameDtoDict = responseDict["gameResponse"]
        contestDtoDict = responseDict["contestResponse"]

        return (gameDtoDict, contestDtoDict)






def GetMenuDisplayTextFromContestDict(contest: dict) -> str:
    return f'Name: {contest["contestName"]}\tType: {contest["gameType"]}\tOponent: {contest["oponentType"]}\tStatus: {contest["contestState"]}'




def Menu_GetMove(gameType: str) -> str:
    abrvMoves: str = 'R,P,S'
    menuHeader: str = '\n\nMove Menu\n---------'
    moveName: str = None

    while moveName is None:
        #system('cls')
        print(menuHeader)
        print('R)\tRock')
        print('P)\tPaper')
        print('S)\tScisors')
        if gameType == 'ROCK_PAPER_SCISORS_LIZARD_SPOK':
            abrvMoves = 'R,P,S,L,K'
            print('L)\tLizard')
            print('K)\tspoK')

        rawInput = input(f'Enter A Move ({abrvMoves}): ')
        move = MoveTokenBuilder.FromName(rawInput)
        if move is not None and move.Name != 'INVALID':
            moveName = move.Name
        else:
            menuHeader = '\n\n-----------------\nINVALID SELECTION\nTry Again\nMove Menu\n-----------------'

    return moveName



def Menu_Main(menuItems: dict) -> uuid:
    actionGuid: uuid = None
    #system('cls')
    menuHeader: str = '\n\n-----------------------\nMain Menu\n-----------------------'

    while actionGuid is None:
        print(menuHeader)
        for menuItem in menuItems:
            menuText: str = menuItems[menuItem][0]
            print(f'{menuItem})\t{menuText}')
        
        menuSelection: str = input('\nChoose An Option: ').upper()

        if menuSelection in menuItems:
            actionGuid = menuItems[menuSelection][1]
        else:
            menuHeader = '\n\n-----------------------\nINVALID SELECTION\nMain Menu\n-----------------------'
            
    return actionGuid




def BuildMainMenuItems(contestList: dict, createContestGuid: uuid, refreshListGuid: uuid, exitGameGuid: uuid) -> dict:
    menuItems: dict = dict()
    menuIndex: int = 1

    for contestDict in contestList:
        menuText: str = GetMenuDisplayTextFromContestDict(contestDict)
        menuItems.update({str(menuIndex): (menuText, contestDict["contestId"])})
        menuIndex += 1

    menuItems.update({"C":("Create New Contest", createContestGuid)})
    menuItems.update({"R":("Refresh Contests", refreshListGuid)})
    menuItems.update({"X":("Exit Game", exitGameGuid)})
    return menuItems





def PlayContest(apiConsumer: RockPaperScisorsApiConsumer, contestDtoDict: dict):
    
    if contestDtoDict["contestState"] == "WAIT_FOR_PLAYER_JOIN":
        print('Waiting For Player To Join')
    while contestDtoDict["contestState"] == "WAIT_FOR_PLAYER_JOIN":
        time.sleep(1)
        contestDtoDict = apiConsumer.GetContestAsPlayer(contestDtoDict["contestId"], contestDtoDict["playerId"])
        print('.', end='')

    keepPlaying = True
    while keepPlaying:
        (gameDtoDict, contestDtoDict) = apiConsumer.PostMove(contestDtoDict, Menu_GetMove(contestDtoDict["gameType"]))
        print(f'{gameDtoDict}\n')

        gameState: str = gameDtoDict["gameState"]
        gameId: str = gameDtoDict["gameId"]
        if gameState != "COMPLETE":
            print("Waiting For Oponent")
        while gameState != "COMPLETE":
            contestDtoDict = apiConsumer.GetContestAsPlayer(contestDtoDict["contestId"], contestDtoDict["playerId"])
            games = contestDtoDict["games"]
            for game in games:
                if game["gameId"] == gameId:
                    gameDtoDict = game
                    gameState = gameDtoDict["gameState"]
                    break
            print('.',end='')
            time.sleep(1)
        print(f'\n{gameDtoDict}\n')

        
        if contestDtoDict["contestState"] != 'PLAYING':
            keepPlaying = False
            


    print(contestDtoDict)
    input('Press Enter To Continue')



def Menu_GameType() -> str:
    return 'ROCK_PAPER_SCISORS'

def Menu_OponentType() -> str:
    return 'PVE'

def Menu_RoundsToWin() -> int:
    return 3

def Menu_ContestName() -> str:
    return 'Test Client'




apiConsumer: RockPaperScisorsApiConsumer = RockPaperScisorsApiConsumer("http://127.0.0.1:88/rpsapi/api/v1/", "x")


createContestGuid: uuid = uuid.uuid4()
refreshListGuid: uuid = uuid.uuid4()
exitGameGuid: uuid = uuid.uuid4()

keepPlaying: bool = True

while keepPlaying:
    contestDtoDict: dict = None

    contestList = apiConsumer.GetContestList()
    actionGuid: uuid = Menu_Main(BuildMainMenuItems(contestList, createContestGuid, refreshListGuid, exitGameGuid))
    if actionGuid == createContestGuid:
        contestDtoDict = apiConsumer.CreateContest(Menu_ContestName(), Menu_RoundsToWin() , Menu_GameType(), Menu_OponentType())
    elif actionGuid == exitGameGuid:
        keepPlaying = False
    elif actionGuid == refreshListGuid or actionGuid is None:
        pass #do nothing and redraw menu
    else: #look for a contest
        for contestDto in contestList:
            if contestDto["contestId"] == actionGuid:
                contestDtoDict = contestDto
                break
    
    if contestDtoDict is not None:
        PlayContest(apiConsumer, contestDtoDict)

print('\n================================\n--Goodbye, Thanks For Playing\n================================\n\n')
exit(0)