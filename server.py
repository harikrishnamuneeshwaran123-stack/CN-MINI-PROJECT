import socket
import json
import random

HOST = "0.0.0.0"
PORT = 5555

WIDTH = 800
HEIGHT = 600

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((HOST, PORT))

players = {}

coin = {
    "x": random.randint(50, WIDTH - 50),
    "y": random.randint(50, HEIGHT - 50)
}

print("=" * 40)
print("UDP MULTIPLAYER GAME SERVER")
print("=" * 40)
print(f"Server running on port {PORT}")
print("Waiting for players...")
print()

while True:

    try:
        data, address = server.recvfrom(4096)

        message = json.loads(data.decode())

        # New player
        if address not in players:

            player_id = len(players) + 1

            players[address] = {
                "id": player_id,
                "x": random.randint(50, WIDTH - 50),
                "y": random.randint(50, HEIGHT - 50),
                "score": 0
            }

            print(f"Player {player_id} connected: {address}")

        player = players[address]

        # Player movement
        if message["type"] == "move":

            player["x"] += message.get("dx", 0)
            player["y"] += message.get("dy", 0)

            # Keep player inside game area
            player["x"] = max(20, min(WIDTH - 20, player["x"]))
            player["y"] = max(20, min(HEIGHT - 20, player["y"]))

            # Check coin collision
            distance_x = abs(player["x"] - coin["x"])
            distance_y = abs(player["y"] - coin["y"])

            if distance_x < 25 and distance_y < 25:

                player["score"] += 1

                coin = {
                    "x": random.randint(50, WIDTH - 50),
                    "y": random.randint(50, HEIGHT - 50)
                }

                print(
                    f"Player {player['id']} "
                    f"collected coin! "
                    f"Score: {player['score']}"
                )

        # Create game state
        game_state = {
            "players": list(players.values()),
            "coin": coin
        }

        packet = json.dumps(game_state).encode()

        # Broadcast to all players
        for client_address in players:
            server.sendto(packet, client_address)

    except Exception as e:
        print("Error:", e)
