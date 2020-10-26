from flask import Flask, request, jsonify
from game import Poker
app = Flask(__name__)

@app.route('/poker/<gameStyle>', methods=['GET', 'POST'])
def playPoker(gameStyle):
  body = request.json
  poker = None
  if gameStyle == "strategy":
    poker = Poker(strategy=body["strategy"])
  elif gameStyle == "desiredCards":
    poker = Poker(desiredCards=body["desiredCards"])
  res = poker.playPoker()
  return jsonify(res)