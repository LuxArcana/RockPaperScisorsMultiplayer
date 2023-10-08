import os
from flask import Flask, render_template
from Service.RockPaperScisorsApiConsumer import *


API_BASE_URL: str = 'http://rps_api_gunicorn_flask:5000/api/v1/'
API_BASE_URL_PUBLIC: str = 'http://127.0.0.1:8080/rps/api/v1/'
API_KEY: str = 'X'
MAX_ROUNDS_TO_WIN: int = 9


template_dir = os.path.abspath('./webClientResources/templates')
static_dir = os.path.abspath('./webClientResources/static')
app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)



rpsApi: RockPaperScisorsApiConsumer = RockPaperScisorsApiConsumer(API_BASE_URL, API_KEY)

#test route to check health of frontend
@app.route('/healthz', methods=['GET'])
def test():
    try:
        message = rpsApi.ServerStatus()
    except Exception as e:
        message = e.args[0]
    
    return render_template('healthz.html', message=message)



    
@app.route('/', methods=['GET'])
def mainEndpoint():
    try:
        return render_template('index.html', contests=rpsApi.GetContestList())
    except Exception as e:
        return render_template('error.html', message=e.args[0])



#start the web service manually if this was launched directly instead of from WSGI
if __name__ == '__main__':
    print('Starting From Main Not WSGI')
    app.run(debug=True)