from os import environ
import logging
import requests
from tensorflow.python.keras.models import load_model
from oware_logic import oware_moves,player,houses,state
import json
import binascii


logging.basicConfig(level="INFO")
logger = logging.getLogger(__name__)

rollup_server = environ["ROLLUP_HTTP_SERVER_URL"]
logger.info(f"HTTP rollup_server url is {rollup_server}")

agent_player = player.Player()

agent_moves = oware_moves.OwareMoves()

model = load_model('model/oware-100.h5')

game_houses =  houses.Houses()

agent_oware_moves = []


def get_agent_move(model,current_board_state_string,player_name):


    name = player_name
    player_houses = game_houses.houses_order[::-1][6:12] if name.lower() =='agent' else game_houses.houses_order[::-1][0:6] 
    captured = 0

    agent = player.Player(name,player_houses,captured)

    name = "opponent"
    player_houses =  game_houses.houses_order[::-1][0:6] if name.lower() =='agent' else game_houses.houses_order[::-1][6:12]
    captured = 0

    player_one = player.Player(name,player_houses,captured)

    opponent_won = False

    board = json.loads(current_board_state_string)

    player_two = agent
    

    game_state = state.State(True,player_one,player_two,agent.name,board)

    agent_moves.legal_moves_generator(game_state,agent)

    agent_move_selected = agent_moves.move_selector(model)

    if len(agent_move_selected) == 3:
            selected_move,new_board_state,score = agent_move_selected
    else:
        opponent_won = False

    return selected_move,opponent_won,score


def handle_advance(data,model):
    logger.info(f"Received advance request data {data}")

    JSON_payload = {}

    try:
        # Assuming data['payload'] is a hexadecimal string
        payload_bytes = bytes.fromhex(data['payload'][2:])  # Remove the '0x' prefix
        payload_str = payload_bytes.decode('utf-8')
        JSON_payload = json.loads(payload_str)


    except Exception as e:
        logger.error(f"Error parsing JSON payload: {str(e)}")
        logger.info(f"Adding a report with binary payload {data['payload']}")
        
        # Assuming rollup_server is defined elsewhere
        response = requests.post(rollup_server + "/report", json={"payload": data['payload']})

        if response.status_code == 200:
            logger.info("Report successfully added")
        else:
            logger.error(f"Failed to add report. Status code: {response.status_code}")

    url = rollup_server + "/report"
    hex_result = ""

    try:
        if JSON_payload.get("method") == "prime":
            name = int(JSON_payload["args"]["name"])
            board_state_string = int(JSON_payload["args"]["board_state"])

            agent_oware_move = get_agent_move(model,board_state_string,name)
            
            agent_oware_moves.extend(agent_oware_move)

            logger.info("The agents move is: %s", agent_oware_move)

            url = rollup_server + "/notice"
            hex_result = binascii.hexlify(json.dumps({"moves": [agent_oware_move]}).encode()).decode()

        else:
            logger.info("Method is undefined")
            hex_result = binascii.hexlify(json.dumps({"error": "Method Undefined"}).encode()).decode()
            
    except Exception as e:
        logger.error("Error: %s", e)
        hex_result = binascii.hexlify(json.dumps({"Error": str(e)}).encode()).decode()

    # Post the result
    try:
        response = requests.post(url, json={"payload": hex_result})
        if response.status_code == 200:
            logger.info("Report successfully added")
        else:
            logger.error("Failed to add report. Status code: %s", response.status_code)
    except Exception as e:
        logger.error("Error posting result: %s", e)


    return "accept"


def handle_inspect(data,model):
    logger.info(f"Received inspect request data {data}")

    hex_result = ""

    try:
        payload_str = binascii.unhexlify(data['payload']).decode()
        
        if payload_str == "primes":
            hex_result = binascii.hexlify(json.dumps({"moves": agent_oware_moves}).encode()).decode()
        else:
            hex_result = binascii.hexlify("This is a simple cartesi Dapp to find primes between two integers".encode()).decode()

    except Exception as e:
        logger.error("Error: %s", e)
        hex_result = binascii.hexlify(json.dumps({"error": str(e)}).encode()).decode()

    # Post the result
    try:
        response = requests.post(rollup_server + "/report", json={"payload": hex_result})
        if response.status_code == 200:
            logger.info("Report successfully added")
        else:
            logger.error("Failed to add report. Status code: %s", response.status_code)
    except Exception as e:
        logger.error("Error posting result: %s", e)

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
