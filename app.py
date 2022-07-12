from flask import Flask, jsonify
import database as db

app = Flask(__name__)

counter = 0

@app.route("/api/v1/counter") # http://localhost:5000/api/v1/counter
def hello_world():
    global counter
    counter += 1
    
    return str(counter)

@app.route("/api/v1/scrape") # http://localhost:5000/api/v1/scrape
def scrape():
    
    thing = {"message": "Scrape successful"}
    return jsonify(thing)

@app.route("/api/v1/getLastGames/<int:num>/<string:team>") # http://localhost:5000/api/v1/getLastGames/<int:num>/<string:team>
def getLastGames(num, team):
    teamsRegon = ''
    return jsonify(teamsRegon)

@app.route("/api/v1/getTeam/<string:team>") # http://localhost:5000/api/v1/getTeam/<string:team>
def getTeam(team):
    return db.getTeamLast5Games('team').to_json(orient='records')

if __name__ == "__main__":
    app.run(debug=True)
