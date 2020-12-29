import pygame, sys, random

pygame.init()
clock = pygame.time.Clock()

#Setting up the main window
screen_width = 1400
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pong')

class Player:
    def __init__(self, width, height):
        self.player_score = 0
        self.player = pygame.Rect(width-20-300, height/2, 1000, 140)
        self.player_speed = 0

class Opponent:
    def __init__(self, width, height):
        self.opponent_score = 0
        self.opponent = pygame.Rect(10, height/2, 10, 140)
        self.opponent_speed = 7

class Ball:
    def __init__(self, width, height):
        self.ball = pygame.Rect(width/2, height/2, 30, 30)
        self.ball_speed_x = 7
        self.ball_speed_y = 7

def Ball_Animation(ball1, player1, opponent1):
    global score_time
    ball1.ball.x += ball1.ball_speed_x
    ball1.ball.y += ball1.ball_speed_y

    # Score Update
    if ball1.ball.right >= screen_width:
        ball1.ball_speed_x *= -1
        opponent1.opponent_score += 1
        score_time = pygame.time.get_ticks()
    if ball1.ball.left <= 0:
        ball1.ball_speed_x *= -1
        player1.player_score += 1
        score_time = pygame.time.get_ticks()

    # Top and bottom wall
    if ball1.ball.bottom >= screen_height or ball1.ball.top <= 0:
        ball1.ball_speed_y *= -1

    # Ball Collission
    if ball1.ball.colliderect(player1.player) and ball1.ball_speed_x > 1:
        if abs(ball1.ball.right - player1.player.left) < 10:
            ball1.ball_speed_x *= -1.1
        elif abs(ball1.ball.top - player1.player.bottom) < 10 and ball1.ball_speed_y < 0:
            ball1.ball_speed_y *= -1
        elif abs(ball1.ball.bottom - player1.player.top) < 10 and ball1.ball_speed_y > 0:
            ball1.ball_speed_y *= -1

    if ball1.ball.colliderect(opponent1.opponent):
        ball1.ball_speed_x *= -1.1
        if abs(ball1.ball.right - opponent1.opponent.left) < 10:
            ball1.ball_speed_x *= -1.1
        elif abs(ball1.ball.top - opponent1.opponent.bottom) < 10 and ball1.ball_speed_y < 0:
            ball1.ball_speed_y *= -1
        elif abs(ball1.ball.bottom - opponent1.opponent.top) < 10 and ball1.ball_speed_y > 0:
            ball1.ball_speed_y *= -1


def player_animation(player1):
    player1.player.y += player1.player_speed

    if player1.player.top <= 0:
        player1.player.top = 0
    if player1.player.bottom >= screen_height:
        player1.player.bottom = screen_height

def opponent_animation(opponent1, ball1):
    if opponent1.opponent.top < ball1.ball.y:
        opponent1.opponent.top += opponent1.opponent_speed
    if opponent1.opponent.bottom > ball1.ball.y:
        opponent1.opponent.bottom -= opponent1.opponent_speed
    if opponent1.opponent.top <= 0:
        opponent1.opponent.top = 0
    if opponent1.opponent.bottom >= screen_height:
        opponent1.opponent.bottom = screen_height

def start(ball1):
    global score_time

    current_time = pygame.time.get_ticks()
    ball1.ball.center = (screen_width/2, screen_height/2)

    if current_time - score_time < 700:
        number_three = game_font.render("3", False, light_grey)
        screen.blit(number_three, (screen_width/2 - 10, screen_height/2 + 20))
    if 700 < current_time - score_time < 1400:
        number_three = game_font.render("2", False, light_grey)
        screen.blit(number_three, (screen_width/2 - 10, screen_height/2 + 20))
    if 1400 <current_time - score_time < 2100:
        number_three = game_font.render("1", False, light_grey)
        screen.blit(number_three, (screen_width/2 - 10, screen_height/2 + 20))

    if current_time - score_time < 2100:
        ball1.ball_speed_x, ball1.ball_speed_y = 0,0
    else:
        ball1.ball_speed_x = 7
        ball1.ball_speed_y = 7
        ball1.ball_speed_y *= random.choice((1, -1))
        ball1.ball_speed_x *= random.choice((1, -1))
        score_time = None

# Draw
ball1 = Ball(screen_width, screen_height)
player1 = Player(screen_width, screen_height)
opponent1 = Opponent(screen_width, screen_height)

# Color
bg_color = pygame.Color("grey12")
light_grey = (200, 200, 200)

# Font
game_font = pygame.font.Font("freesansbold.ttf", 32)

# Timer
score_time = True

while True:
    #Input handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                player1.player_speed += 7
            if event.key == pygame.K_UP:
                player1.player_speed -= 7
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                player1.player_speed -= 7
            if event.key == pygame.K_UP:
                player1.player_speed += 7

    Ball_Animation(ball1, player1, opponent1)
    player_animation(player1)
    opponent_animation(opponent1, ball1)

    screen.fill(bg_color)
    pygame.draw.rect(screen, light_grey, player1.player)
    pygame.draw.rect(screen, light_grey, opponent1.opponent)
    pygame.draw.ellipse(screen, light_grey, ball1.ball)
    pygame.draw.aaline(screen, light_grey, (screen_width / 2 + 10, 0), (screen_width / 2 + 10, screen_height))

    if score_time:
        start(ball1)

    player_text = game_font.render(f'{player1.player_score}', False, light_grey)
    screen.blit(player_text, (3*screen_width/4, 100))
    opponent_text = game_font.render(f'{opponent1.opponent_score}', False, light_grey)
    screen.blit(opponent_text, (1 * screen_width / 4, 100))

    #Updating the window
    pygame.display.flip()
    clock.tick(60)


