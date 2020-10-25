from flask import Flask, request
from game import Poker
app = Flask(__name__)

@app.route('/poker/<gameStyle>')
def playPoker(gameStyle):
  body = request.json
  if gameStyle == "strategy":
    poker = Poker(strategy=body.strategy)
  elif gameStyle == "desiredCards":
    poker = Poker(desiredCards=body.desiredCards)
  return poker.playPoker()