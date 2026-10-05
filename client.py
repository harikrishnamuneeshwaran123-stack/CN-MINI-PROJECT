import socket
import json
import pygame

# -----------------------------
# SERVER SETTINGS
# -----------------------------

SERVER_IP = "127.0.0.1"
SERVER_PORT = 5555

# -----------------------------
# GAME SETTINGS
# -----------------------------

WIDTH = 800
HEIGHT = 600

# -----------------------------
# UDP SOCKET
# -----------------------------

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setblocking(False)

# -----------------------------
# PYGAME
# -----------------------------

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("UDP Multiplayer Game")

clock = pygame.time.Clock()

font = pygame.font.Font(None, 30)

running = True

# -----------------------------
# GAME LOOP
# -----------------------------

while running:

    dx = 0
    dy = 0

    # Events
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

    # Keyboard
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        dx = -5

    if keys[pygame.K_RIGHT]:
        dx = 5

    if keys[pygame.K_UP]:
        dy = -5

    if keys[pygame.K_DOWN]:
        dy = 5

    # -------------------------
    # SEND MOVEMENT TO SERVER
    # -------------------------

    message = {
        "type": "move",
        "dx": dx,
        "dy": dy
    }

    try:

        sock.sendto(
            json.dumps(message).encode(),
            (SERVER_IP, SERVER_PORT)
        )

    except Exception:
        pass

    # -------------------------
    # RECEIVE GAME STATE
    # -------------------------

    try:

        data, server_address = sock.recvfrom(4096)

        game_state = json.loads(data.decode())

        # Background
        screen.fill((20, 25, 40))

        # ---------------------
        # DRAW COIN
        # ---------------------

        coin = game_state["coin"]

        pygame.draw.circle(
            screen,
            (255, 215, 0),
            (coin["x"], coin["y"]),
            12
        )

        # ---------------------
        # DRAW PLAYERS
        # ---------------------

        colors = [
            (0, 200, 255),
            (255, 80, 80),
            (80, 255, 100),
            (255, 150, 50)
        ]

        for index, player in enumerate(game_state["players"]):

            color = colors[index % len(colors)]

            pygame.draw.circle(
                screen,
                color,
                (player["x"], player["y"]),
                20
            )

            # Player ID
            text = font.render(
                "P" + str(player["id"]),
                True,
                (255, 255, 255)
            )

            screen.blit(
                text,
                (
                    player["x"] - 10,
                    player["y"] - 45
                )
            )

            # Score
            score_text = font.render(
                "Score: " + str(player["score"]),
                True,
                (255, 255, 255)
            )

            screen.blit(
                score_text,
                (10, 10 + index * 30)
            )

        pygame.display.flip()

    except BlockingIOError:
        pass

    except Exception:
        pass

    # 30 FPS
    clock.tick(30)

# -----------------------------
# EXIT
# -----------------------------

sock.close()
pygame.quit()
