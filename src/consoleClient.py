from Service.RockPaperScisorsConsoleUI import *



API_BASE_URL: str = 'http://172.17.0.1:8080/rps/api/v1/'
API_KEY: str = 'X'
MAX_ROUNDS_TO_WIN: int = 9


rockPaperScisorsConsole: RockpaperScisorsConsoleUI = RockpaperScisorsConsoleUI(API_BASE_URL, API_KEY, MAX_ROUNDS_TO_WIN)

rockPaperScisorsConsole.Play()
