import pygame
import random

###### functions ######

# helper function to play sound
def play_sound(sound):
    return sound.play()

# generate random colored text
def get_random_text():
    i = random.randrange(0, 6)
    text = font.render('Holy sh!t it\'s cats in Space!', True, color_dictionary[i])
    return text

# function to determine if a particular object has collided with a defined boundry
def change_direction(axis, pos, boundry1, boundry2, debug):
    if axis == 'x':
        # do check to see if object has collided with defined boundries
        if pos == boundry1:
            return 'left'
        if pos == boundry2:
            return 'right'
        # no collision, direction remains the same
        else:
            return x_direction_banner

    if axis == 'y':
        if pos == boundry1:
            return 'down'
        if pos == boundry2:
            return 'up'
        else:
            return y_direction_banner

        return "ERROR how the fudge did you get here"

# function to move the banner around
def move_x(pos, direction):
    # calculate movement
    if direction == 'right':
        pos += 1
    if direction == 'left':
        pos += -1

    return pos

def move_y(pos, direction):
    # calculate movement
    if direction == 'up':
        pos += -1
    if direction == 'down':
        pos += 1

    return pos

def generate_space_cats(cat_number, x_offset_min, x_offset_max, y_offset_min, y_offset_max):
    i = 0

    while i <= cat_number:
        rand_cat = random.randrange(1,3)
        rand_pos_x = random.randrange(x_offset_min, x_offset_max)
        rand_pos_y = random.randrange(y_offset_min, y_offset_max)
        rand_cat_list[i] = { 'name': cat_dictionary[rand_cat],
            'x': rand_pos_x,
            'y': rand_pos_y,
            'direction_x': give_me_a_direction('x'),
            'direction_y': give_me_a_direction('y') }
        i += 1

def give_me_a_direction(axis):
    rand = random.randrange(0, 2)
    if axis == 'x':
        if rand == 0:
            return 'left'
        else:
            return 'right'
    if axis == 'y':
        if rand == 0:
            return 'up'
        else:
            return 'down'

    return "ERROR How the fudge did you get here"

def set_fade(alpha, direction):
    # check direction
    if direction == 'fade-out':
        if alpha == 0:
            return 'fade-in'
    if direction == 'fade-in':
        if alpha == 100:
            return 'fade-out'
    else:
        return direction

def set_fade_value(alpha, direction):
    if direction == 'fade-in':
        alpha += 1
        return alpha
    if direction == 'fade-out':
        alpha += -1
        return alpha

###### vars ######

# init stuff
pygame.init()
pygame.display.set_caption('This is how I spend my time')
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# vars
done         = False
frame        = 0
resource_dir = 'resources/'

# colors
WHITE   = (255, 255, 255)
PINK    = (255, 0, 255)
MAGENTA = (255, 51, 153)
GREEN   = (102, 255, 102)
YELLOW  = (255, 255, 0)
BLUE    = (0, 255, 255)

# movement vars
x_speed            = 0
y_speed            = 0
x_pos_player       = 400
y_pos_player       = 300
x_pos_banner       = 30
y_pos_banner       = 20
rotation_index     = 90
alpha_index        = 0
alpha_direction    = 'fade-in'
x_direction_banner = give_me_a_direction('x')
y_direction_banner = give_me_a_direction('y')

# import images
player  = pygame.image.load('resources/player.png').convert()
cat1    = pygame.image.load('resources/cat1.png').convert()
cat2    = pygame.image.load('resources/cat2.png').convert()
cat3    = pygame.image.load('resources/cat3.png').convert()
bg      = pygame.image.load('resources/bg.jpg')

# import sounds
# sound = pygame.mixer.Sound('resources/cat-meow.wav')

# import font
font = pygame.font.SysFont('comicsansms', 52)

# transform images
player  = pygame.transform.scale(player, (150,150))
bg      = pygame.transform.scale(bg, (800, 600))
cat1    = pygame.transform.scale(cat1, (200, 151))
cat2    = pygame.transform.scale(cat2, (150, 95))
cat3    = pygame.transform.scale(cat3, (125, 128))

# dictionaries
color_dictionary = { 0: WHITE, 1: PINK, 2: MAGENTA, 3: GREEN, 4: YELLOW, 5: BLUE }
cat_dictionary   = { 1: cat1, 2: cat2, 3: cat3 }

# lists
rand_cat_list = {}

# perform any functions before entering game loop
generate_space_cats(3, 10, 500, 30, 475)

###### game loop ######
while not done:
    for event in pygame.event.get():

        # press space to end the game
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            done = True

        # click to make cat noises (broken)
        if event.type == pygame.MOUSEBUTTONDOWN:
            play_sound(sound)

        # listen for key input
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x_speed = -3
            if event.key == pygame.K_RIGHT:
                x_speed = 3
            if event.key == pygame.K_UP:
                y_speed = -3
            if event.key == pygame.K_DOWN:
                y_speed = 3
            if event.key == pygame.K_p:
                generate_space_cats(5, 10, 500, 30, 475)

        # reset x_pos after input
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                x_speed = 0
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                y_speed = 0

    # move the player according to input values
    x_pos_player += x_speed
    y_pos_player += y_speed

    # get the current direction
    x_direction_banner = change_direction('x', x_pos_banner, 100, 10, 'banner')
    y_direction_banner = change_direction('y', y_pos_banner, 10, 60, 'banner')

    # move the banner accoring to magic
    x_pos_banner = move_x(x_pos_banner, x_direction_banner)
    y_pos_banner = move_y(y_pos_banner, y_direction_banner)

    # create background screen/surface
    screen.blit(bg, [0,0])

    # create player
    screen.blit(player, [x_pos_player, y_pos_player])

    # create message for all to see
    screen.blit(get_random_text(), [x_pos_banner, y_pos_banner])

    for val in rand_cat_list:

        # gather dictionary data
        name = rand_cat_list[val]['name']
        x = rand_cat_list[val]['x']
        y = rand_cat_list[val]['y']

        rand_cat_list[val]['direction_x'] = change_direction('x', x, 0, 700, 'RANDOM CAT')
        rand_cat_list[val]['direction_y'] = change_direction('y', y, 0, 500, 'RANDOM CAT')

        rand_cat_list[val]['x'] = move_x(x, rand_cat_list[val]['direction_x'])
        rand_cat_list[val]['y'] = move_y(y, rand_cat_list[val]['direction_y'])

        # transform and display new rotated image
        rotation_index += 1
        rotation_index %= 360 # reset rotation index
        img = pygame.transform.rotate(name, rotation_index)
        img.set_alpha(alpha_index)
        screen.blit(img, [rand_cat_list[val]['x'], rand_cat_list[val]['y']])

    # determine the next value for alpha
    alpha_direction = set_fade(alpha_index, alpha_direction)
    alpha_index = set_fade_value(alpha_index, alpha_direction)

    # force fps rate of 60 cause masterrace
    pygame.display.flip()
    frame += 1
    frame %= 60 # reset frame count
    clock.tick(60)
