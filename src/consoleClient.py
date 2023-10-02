from Service.RockPaperScisorsConsoleUI import *



API_BASE_URL: str = 'http://127.0.0.1:88/rps/api/v1/'
API_KEY: str = 'X'
MAX_ROUNDS_TO_WIN: int = 9


rockPaperScisorsConsole: RockpaperScisorsConsoleUI = RockpaperScisorsConsoleUI(API_BASE_URL, API_KEY, MAX_ROUNDS_TO_WIN)

rockPaperScisorsConsole.Play()
