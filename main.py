import pgzrun
import random

WIDTH = 600
HEIGHT = 450
TITLE = "Super racing F1"

ship = Actor("coche12", (300, 400))
menu = Actor("menu12", (300, 200))
boton = Actor("boton12", (300, 100))
ganar = Actor("ganar12", (300, 200))
space = Actor("pista12", (300, 225))
gameover = Actor("gameover12", (300, 225))

mode = "menu"
ganarpuntos = 50
count = 0
highscore = 0
enemies = []
moneya = []
NUM_ENEMIES = 5
NUM_COINS = 4

def create_enemies():
    global enemies
    enemies = []
    for i in range(NUM_ENEMIES):
        x = random.randint(50, WIDTH - 50)
        y = random.randint(-450 * (i + 1) // NUM_ENEMIES, -50 * (i + 1))
        enemy = Actor("enemigo12", (x, y))
        enemy.speed = random.randint(3, 8)
        enemies.append(enemy)

def spawn_money():
    global moneya
    moneya = []
    for _ in range(NUM_COINS):
        x = random.randint(50, WIDTH - 50)
        y = random.randint(80, HEIGHT - 120)
        moneda = Actor("moneda12", (x, y))
        moneya.append(moneda)

create_enemies()
spawn_money()

def draw():
    screen.clear()
    space.draw()

    if mode == "menu":
        menu.draw()
        boton.draw()
        screen.draw.text("Haz clic en el botón para jugar", center=(300, 400), fontsize=30, color="white")
        return

    if mode == "game":
        ship.draw()
        for enemy in enemies:
            enemy.draw()
        for moneda in moneya:
            moneda.draw()
        screen.draw.text(str(count), topleft=(WIDTH / 10, HEIGHT / 15), color="white", fontsize=35)

    elif mode == "end":
        gameover.draw()
        screen.draw.text("Tu puntaje: " + str(count), center=(WIDTH / 2, HEIGHT / 2 + 120), color="white", fontsize=40)
        screen.draw.text("Récord: " + str(highscore), center=(WIDTH / 2, HEIGHT / 2 + 170), color="yellow", fontsize=35)
        screen.draw.text("Presiona ENTER para reiniciar", center=(WIDTH / 2, HEIGHT / 2 + 220), color="yellow", fontsize=30)

    elif mode == "win":
        ganar.draw()
        screen.draw.text("¡Ganaste con " + str(count) + " puntos!", center=(WIDTH / 2, HEIGHT / 2 + 120), color="white", fontsize=40)
        screen.draw.text("Record: " + str(highscore), center=(WIDTH / 2, HEIGHT / 2 + 170), color="yellow", fontsize=35)
        screen.draw.text("Presiona ENTER para reiniciar", center=(WIDTH / 2, HEIGHT / 2 + 220), color="yellow", fontsize=30)

def on_mouse_down(pos):
    global mode
    if mode == "menu" and boton.collidepoint(pos):
        mode = "game"

def on_mouse_move(pos):
    if mode == "game":
        x, y = pos
        x = max(50, min(WIDTH - 50, x))
        y = max(50, min(HEIGHT - 50, y))
        ship.pos = (x, y)

def on_key_down(key):
    global mode
    if (mode == "end" or mode == "win") and key == keys.RETURN:
        reset_game()

def new_enemy():
    x = random.randint(50, WIDTH - 50)
    y = random.randint(-450, -50)
    enemy = Actor("enemigo12", (x, y))
    enemy.speed = random.randint(3, 10)
    enemies.append(enemy)

def move_enemies():
    global count
    for enemy in enemies[:]:
        enemy.y += enemy.speed
        if enemy.y > HEIGHT + 100:
            count += 1
            enemies.remove(enemy)
            new_enemy()

def collisions():
    global mode, highscore
    for enemy in enemies:
        if ship.colliderect(enemy):
            if count > highscore:
                highscore = count
            mode = "end"

def reposition_coin(moneda):
    moneda.x = random.randint(50, WIDTH - 50)
    moneda.y = random.randint(80, HEIGHT - 120)

def collisions_money():
    global count, mode, highscore, ganarpuntos
    for moneda in moneya:
        if ship.colliderect(moneda):
            count += 5
            reposition_coin(moneda)
            if count >= ganarpuntos:
                if count > highscore:
                    highscore = count
                ganarpuntos += 20
                mode = "win"

def reset_game():
    global count, mode, ganarpuntos
    count = 0
    ganarpuntos = 50
    ship.pos = (300, 400)
    create_enemies()
    spawn_money()
    mode = "game"

def update():
    if mode == "game":
        move_enemies()
        collisions()
        collisions_money()

pgzrun.go()