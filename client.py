import pygame
from network import Network

pygame.font.init()

WIN_SIZE = 500, 600
SYMBOLS_DICT = {0: 'X', 1: 'O', -1: ''}
win = pygame.display.set_mode(WIN_SIZE)
pygame.display.set_caption("Client")


class Button:
    def __init__(self, id, text, x, y):
        self.id = id
        self.text = text
        self.x = x
        self.y = y
        self.color = (0,0,0)
        self.width = 130
        self.height = 130

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("comicsans", 150)
        text = font.render(self.text, 1, (255, 255, 255))
        win.blit(text, (self.x + round(self.width / 2) - round(text.get_width() / 2),
                        self.y + round(self.height / 2) - round(text.get_height() / 2)))

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False


def redrawWindow(win, game, p):
    win.fill((128, 128, 128))

    if not (game.connected()):
        font = pygame.font.SysFont("comicsans", 70)
        text = font.render("Waiting for Player...", 1, (255, 0, 0), True)
        win.blit(text,
                 (WIN_SIZE[0] / 2 - text.get_width() / 2, WIN_SIZE[1] / 2 - text.get_height() / 2))
    else:
        font = pygame.font.SysFont("comicsans", 60)
        if not game.empty_cells() or not game.win_game() == -1:
            text = font.render("Round finished", 1, (0, 255, 255))
        elif (game.moves and not p) or (not game.moves and p):
            text = font.render("Opponent's move", 1, (0, 255, 255))
        else: # game.moves and p or not game.moves and not p:
            text = font.render("Your move", 1, (0, 255, 255))
        win.blit(text, (WIN_SIZE[0] / 2 - text.get_width() / 2, 35))

        font = pygame.font.SysFont("comicsans", 50)
        text = font.render(f"You are playing for  '{SYMBOLS_DICT[p]}'", 1, (0, 255, 255))
        win.blit(text, (WIN_SIZE[0] / 2 - text.get_width() / 2, WIN_SIZE[1] - 35 - text.get_height()))

        for idx, cell_value in enumerate(game.cells_values):
            btns[idx].text = SYMBOLS_DICT[cell_value]

        for btn in btns:
            btn.draw(win)

    pygame.display.update()


btns = [Button(x_idx - 1 + (y_idx - 1) * 3, "", 131 * x_idx - 77, 131 * y_idx - 20)
                                                                for y_idx in [1,2,3]
                                                                for x_idx in [1,2,3]]


def main():
    run = True
    clock = pygame.time.Clock()
    n = Network("192.168.1.203", 5555)
    player = n.get_player_conn()
    print(f"You are player: {player}")

    while run:
        clock.tick(60)
        try:
            game = n.send("get")
        except Exception as error:
            run = False
            print(f"Couldn't get game: {error}")
            break

        if not game.empty_cells() or not game.win_game() == -1:
            redrawWindow(win, game, player)
            pygame.time.delay(500)

            font = pygame.font.SysFont("comicsans", 140)
            if game.win_game() == player:
                text = font.render("You Won!", 1, (255, 0, 0))
            elif game.win_game() == -1:
                text = font.render("Tie Game", 1, (255, 0, 0))
            else:
                text = font.render("You Lost...", 1, (255, 0, 0))
            win.blit(text,
                     (WIN_SIZE[0] / 2 - text.get_width() / 2, WIN_SIZE[1] / 2 - text.get_height() / 2))
            pygame.display.update()
            pygame.time.delay(3000)

            try:
                game = n.send("reset")
            except Exception as error:
                run = False
                print(f"Couldn't get game: {error}")
                break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in btns:
                    if btn.click(pos) and game.connected() and game.cells_values[btn.id] == -1:
                        if not player and not game.moves or player and game.moves:
                            n.send(btn.id)

        redrawWindow(win, game, player)


def menu_screen():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        win.fill((128, 128, 128))
        font = pygame.font.SysFont("comicsans", 80)
        text = font.render("Click to Play!", 1, (255, 0, 0))
        win.blit(text,
                 (WIN_SIZE[0] / 2 - text.get_width() / 2, WIN_SIZE[1] / 2 - text.get_height() / 2))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False

    main()


while True:
    menu_screen()
