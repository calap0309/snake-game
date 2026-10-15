import asyncio
import random

import pygame

# --- config ---
COLS, ROWS = 21, 21
CELL = 20
WIDTH, HEIGHT = COLS * CELL, ROWS * CELL
HUD_H = 44

BG = (15, 17, 21)
GRID = (35, 39, 51)
SNAKE = (74, 222, 128)
HEAD = (34, 197, 94)
FOOD = (248, 113, 113)
TEXT = (229, 231, 235)
DIM = (120, 128, 145)


def draw_text(surf, font, text, center, color=TEXT):
    img = font.render(text, True, color)
    surf.blit(img, img.get_rect(center=center))


async def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT + HUD_H))
    pygame.display.set_caption("Snake")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("monospace", 18, bold=True)
    big = pygame.font.SysFont("monospace", 30, bold=True)

    play = pygame.Rect(0, HUD_H, WIDTH, HEIGHT)

    def reset():
        snap = [(10, 10), (9, 10), (8, 10)]
        d = (1, 0)
        return snap, d, d, 0, 130, 0.0, "ready"

    snake, direction, nxt, score, tick, acc, state = reset()
    best = 0

    def place_food():
        occupied = set(snake)
        free = [(x, y) for y in range(ROWS) for x in range(COLS) if (x, y) not in occupied]
        return random.choice(free) if free else (0, 0)

    food = place_food()

    def start():
        nonlocal snake, direction, nxt, score, tick, acc, state, food
        snake, direction, nxt, score, tick, acc, state = reset()
        food = place_food()

    running = True
    while running:
        dt = clock.tick(60) / 1000.0

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            elif e.type == pygame.KEYDOWN:
                if e.key in (pygame.K_p, pygame.K_SPACE):
                    if state == "playing":
                        state = "paused"
                    elif state == "paused":
                        state = "playing"
                    elif state in ("ready", "over"):
                        start()
                        state = "playing"
                elif e.key == pygame.K_r:
                    start()
                    state = "playing"
                elif state in ("ready", "over"):
                    start()
                    state = "playing"
                elif state == "playing":
                    if e.key in (pygame.K_UP, pygame.K_w) and direction != (0, 1):
                        nxt = (0, -1)
                    elif e.key in (pygame.K_DOWN, pygame.K_s) and direction != (0, -1):
                        nxt = (0, 1)
                    elif e.key in (pygame.K_LEFT, pygame.K_a) and direction != (1, 0):
                        nxt = (-1, 0)
                    elif e.key in (pygame.K_RIGHT, pygame.K_d) and direction != (-1, 0):
                        nxt = (1, 0)

        if state == "playing":
            acc += dt
            step = tick / 1000.0
            while acc >= step:
                acc -= step
                direction = nxt
                hx, hy = snake[0]
                head = (hx + direction[0], hy + direction[1])
                if not (0 <= head[0] < COLS and 0 <= head[1] < ROWS) or head in snake[:-1]:
                    state = "over"
                    best = max(best, score)
                    break
                snake.insert(0, head)
                if head == food:
                    score += 1
                    food = place_food()
                    if score % 5 == 0 and tick > 60:
                        tick -= 8
                else:
                    snake.pop()

        # --- draw ---
        screen.fill(BG)
        for y in range(ROWS):
            for x in range(COLS):
                pygame.draw.circle(screen, GRID, (x * CELL + CELL // 2, play.y + y * CELL + CELL // 2), 1)
        for i, (x, y) in enumerate(snake):
            pad = 2
            rect = pygame.Rect(x * CELL + pad, play.y + y * CELL + pad, CELL - 2 * pad, CELL - 2 * pad)
            pygame.draw.rect(screen, HEAD if i == 0 else SNAKE, rect, border_radius=4)
        pygame.draw.circle(screen, FOOD, (food[0] * CELL + CELL // 2, play.y + food[1] * CELL + CELL // 2), CELL // 2 - 3)

        draw_text(screen, font, f"Score {score}", (WIDTH // 4, HUD_H // 2))
        draw_text(screen, font, f"Best {best}", (3 * WIDTH // 4, HUD_H // 2), DIM)

        if state == "ready":
            draw_text(screen, big, "SNAKE", (WIDTH // 2, HEIGHT // 2), HEAD)
            draw_text(screen, font, "Arrows / WASD to start", (WIDTH // 2, HEIGHT // 2 + 40), DIM)
        elif state == "paused":
            draw_text(screen, big, "PAUSED", (WIDTH // 2, HEIGHT // 2), TEXT)
        elif state == "over":
            draw_text(screen, big, "GAME OVER", (WIDTH // 2, HEIGHT // 2 - 10), FOOD)
            draw_text(screen, font, f"Score {score}  -  press R / SPACE", (WIDTH // 2, HEIGHT // 2 + 34), DIM)

        pygame.display.flip()
        await asyncio.sleep(0)  # hand control back to the browser

    pygame.quit()


asyncio.run(main())
