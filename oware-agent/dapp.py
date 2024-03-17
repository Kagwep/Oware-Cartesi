from os import environ
import logging
import requests
from tensorflow.python.keras.models import load_model
from oware_logic import oware_moves

logging.basicConfig(level="INFO")
logger = logging.getLogger(__name__)

rollup_server = environ["ROLLUP_HTTP_SERVER_URL"]
logger.info(f"HTTP rollup_server url is {rollup_server}")

agent_moves = oware_moves.OwareMoves()

model = load_model('model/oware-100.h5')


def get_agent_move(model,game_state,player):

    agent_moves.legal_moves_generator(game_state,player)

    agent_move_selected = agent_moves.move_selector(model)

    if len(agent_move_selected) == 3:
            selected_move,new_board_state,score = agent_move_selected
    else:
         pass


def handle_advance(data,model):
    logger.info(f"Received advance request data {data}")
    return "accept"


def handle_inspect(data,model):
    logger.info(f"Received inspect request data {data}")
    return "accept"


handlers = {
    "advance_state": handle_advance,
    "inspect_state": handle_inspect,
}

finish = {"status": "accept"}

while True:
    logger.info("Sending finish")
    response = requests.post(rollup_server + "/finish", json=finish)
    logger.info(f"Received finish status {response.status_code}")
    if response.status_code == 202:
        logger.info("No pending rollup request, trying again")
    else:
        rollup_request = response.json()
        data = rollup_request["data"]
        handler = handlers[rollup_request["request_type"]]
        finish["status"] = handler(rollup_request["data"],model)
