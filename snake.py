import pygame
import random

pygame.init()
pygame.mixer.init()
pygame.mixer.music.set_volume(0.7)
#colors
black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)
red = (255, 0, 0)
green = (0, 255, 0)
brown=(173, 138, 101)
done = False

size = [400, 600]
screen = pygame.display.set_mode(size)

#Images
target_image = pygame.image.load("assets/mouse.png").convert()
snake_head = pygame.image.load("assets/snake_head.png").convert()
snake_head = pygame.transform.scale(snake_head, (20,20))
snake_body = pygame.image.load("assets/snake_body.png").convert()
life_image = pygame.transform.rotate(snake_head,90)
new_game = pygame.image.load("assets/new_game.jpeg").convert()
Icon = pygame.image.load('assets/icon.png')
#icon
pygame.display.set_icon(Icon)

#Block class
class Block(pygame.sprite.Sprite):
    def __init__(self,color,width,height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width,height])
        self.image.fill(color)
        self.rect = self.image.get_rect()

#Player class
class Player(Block):
    #Game Constants
    x_speed = 20
    y_speed = 0
    direction = 0
    fps = 0
    score = 0
    start = False
    collision = False
    rotation = 0
    snake_list = []
    lives = 4
      
#Update snake position    
def update(length):
    i = length-1
    if i < 0:
        player.rect.x+=player.x_speed
        player.rect.y+=player.y_speed
    else:
        holding_x = player.rect.x
        holding_y = player.rect.y
        player.rect.x+=player.x_speed
        player.rect.y+=player.y_speed
        while i >= 1:
            player.snake_list[i].rect.x = player.snake_list[i-1].rect.x
            player.snake_list[i].rect.y = player.snake_list[i-1].rect.y
            i -=1
        player.snake_list[0].rect.x = holding_x
        player.snake_list[0].rect.y = holding_y
    
        
#Check for collisions
def checkCollisions():
    hit_yourself = pygame.sprite.spritecollide(player,snake_blocks,False)
    if len(hit_yourself)>0:
        pygame.mixer.music.load("assets/crash.mp3")
        pygame.mixer.music.play()
        player.collision = True
    got_target = pygame.sprite.spritecollide(player,target_block,False)
    if len(got_target)>0:
        pygame.mixer.music.load("assets/eat.mp3")
        pygame.mixer.music.play()
        block.rect.x = random.randrange(0,385)
        block.rect.y = random.randrange(20,585)
        new_block = Block(blue,20,20)
        new_block.image = snake_body
        new_block.image.set_colorkey(white)
        new_block.rect.x = -20
        new_block.rect.y = -20
        snake_blocks.add(new_block)
        player.snake_list.append(new_block)
        player.fps+=0.5
        player.score+=1
    new_block = pygame.sprite.spritecollide(block,snake_blocks,False)
    if len(new_block)>0:
        block.rect.x = random.randrange(0,385)
        block.rect.y = random.randrange(20,585)
    if player.rect.x > size[0]-19 or player.rect.x < 0 or player.rect.y > size[1]-19 or player.rect.y < 20:
        pygame.mixer.music.load("assets/crash.mp3")
        pygame.mixer.music.play()
        player.collision = True
    

#Calculate the degree of rotation for the snake head
def rotate(current_direction, intended_direction):
    x = intended_direction - current_direction
    return x

#Reset the game
def reset():
    player.x_speed = 20
    player.y_speed = 0
    player.fps = 5
    player.rotation = rotate(player.direction,360)
    player.image = pygame.transform.rotate(player.image,player.rotation)
    player.direction = 0
    player.rect.x = 200
    player.rect.y = 200
    for i in snake_blocks:
        i.kill()
    player.snake_list = []
    player.lives-=1

def displayLives(screen):
    x = 320
    y = 0
    for i in range(player.lives):
        screen.blit(life_image,[x+20,y])

        x+=20

def displayMenu(screen):
    font = pygame.font.Font(None, 60)
    title = font.render('SNAKE GAME', 1,brown)
    screen.fill(white)
    screen.blit(Icon,[100,0])
    screen.blit(title,[55,230])
    font = pygame.font.Font(None, 30)
    click = font.render('Click Below To Start Game', 1,brown)
    screen.blit(click,[65,320])
    screen.blit(new_game,[15,350])
    
player_block = pygame.sprite.RenderPlain()
snake_blocks = pygame.sprite.RenderPlain()
player = Player(red,20,20)
player.image = snake_head
player.image.set_colorkey(white)
player.rect.x = 200
player.rect.y = 200
player_block.add(player)

target_block = pygame.sprite.RenderPlain()
block = Block(black,15,15)
block.image = target_image
block.image.set_colorkey(white)
block.rect.x = random.randrange(0,size[0]-15)
block.rect.y = random.randrange(20,size[1]-15)
target_block.add(block)
font = pygame.font.Font(None,25)

pygame.display.set_caption("Snake Game By Rahul Choudhary")
clock = pygame.time.Clock()

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and (player.y_speed!=20 or player.score<2):
                player.x_speed = 0
                player.y_speed = -20
                player.rotation = rotate(player.direction, 90)
                player.image = pygame.transform.rotate(player.image,player.rotation)
                player.direction = 90
            if event.key == pygame.K_DOWN and (player.y_speed!=-20 or player.score<2):
                player.x_speed = 0
                player.y_speed = 20
                player.rotation = rotate(player.direction, 270)
                player.image = pygame.transform.rotate(player.image,player.rotation)
                player.direction = 270
            if event.key == pygame.K_LEFT and (player.x_speed!=20 or player.score<2):
                player.x_speed = -20
                player.y_speed = 0
                player.rotation = rotate(player.direction, 180)
                player.image = pygame.transform.rotate(player.image,player.rotation)
                player.direction = 180
            if event.key == pygame.K_RIGHT and (player.x_speed!=-20 or player.score<2):
                player.x_speed = 20
                player.y_speed = 0
                player.rotation = rotate(player.direction, 360)
                player.image = pygame.transform.rotate(player.image,player.rotation)
                player.direction = 0
    while player.start == False:
        displayMenu(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                player.start = True
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if mouse[0] > 15 and mouse[0] < 350:
                    if mouse[1] > 350 and mouse[1] < 447:
                        reset()
                        player.start = True
        pygame.display.flip()
        clock.tick(20)

    update(len(player.snake_list))
    checkCollisions()
    if player.collision == True:
        screen.fill(white)
        displayLives(screen)
        score_text = font.render("Score: "+str(player.score),True,black)
        life_text = font.render("Lives: ",True,black)
        screen.blit(score_text,[5,5])
        screen.blit(life_text,[285,5])
        pygame.display.flip()
        pygame.time.wait(400)
        reset()
        player.collision = False
    if player.lives < 1:
        screen.fill(brown)
        font = pygame.font.Font(None, 70)
        title = font.render('GAME OVER', 1,white)
        font = pygame.font.Font(None,25)
        screen.blit(title,[55,265])
        pygame.display.flip()
        pygame.time.wait(800)
        player.score = 0
        player.lives = 4
        player.start = False
    screen.fill(white)
    pygame.draw.rect(screen,red, [0, 23, 400,577],3)
    target_block.draw(screen)
    player_block.draw(screen)
    snake_blocks.draw(screen)
    score_text = font.render("Score: "+str(player.score),True,black)
    life_text = font.render("Lives: ",True,black)
    screen.blit(score_text,[5,5])
    screen.blit(life_text,[285,5])
    displayLives(screen)
    pygame.display.flip()
    clock.tick(player.fps)
pygame.quit()
