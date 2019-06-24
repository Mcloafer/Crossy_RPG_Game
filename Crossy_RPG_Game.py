#Pygame development 1
#Start the basic game set up
#Set up the display

#Gain access to the pygame library
import pygame

#Size of the screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SCREEN_TITLE = 'Crossy RPG'
#Colors according to RGB codes
WHITE_COLOR = (255, 255, 255)
BLACK_COLOR = (0, 0, 0)

#Pygame development 2
#Set up the game loop
#Use game loop to render graphics

#Clock used to update game events and frames
clock = pygame.time.Clock()
pygame.font.init()
font = pygame.font.SysFont('comicsans',75)

class Game:

    #Typical rate of 60 for low end games, equivalent to FPS
    TICK_RATE = 60
    
    #Initializer for the game class to set up width, height, and title
    def __init__(self, image_path, title, width, height):
        self.title = title
        self.width = width
        self.height = height

        #Create the window of specified size in white to display the game
        self.game_screen = pygame.display.set_mode((width,height))
        #Set the game window color to white
        self.game_screen.fill(WHITE_COLOR)
        pygame.display.set_caption(title)

        background_image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(background_image, (width, height))

    def run_game_loop(self, level_speed):
        is_game_over = False
        did_win = False
        direction = 0

        #Import character images and their starting positions/dimensions/scales
        player_character = PlayerCharacter('Player Character.png', 375, 700, 50, 50)
        enemy_0 = NonPlayerCharacter('Enemy Character.png', 20, 600, 40, 40)
        #Speed increased as we advance in difficulty
        enemy_0.SPEED *= level_speed

        #Creating another enemy
        enemy_1 = NonPlayerCharacter('Enemy Character.png', self.width -40, 400, 40, 40)
        enemy_1.SPEED *= level_speed

        #Creating a third enemy
        enemy_2 = NonPlayerCharacter('Enemy Character.png', 20, 200, 40, 40)
        enemy_2.SPEED *= level_speed

        treasure = GameObject('Treasure.png', 375, 50, 50, 50)

        #Main game loop, used to update all gameplay such as movement, checks, and graphics
        #Runs until is_game_over = True
        while not is_game_over:

            #A loop to get all of the events occuring at any given time
            #Events are most often mouse movement, mouse and button clicks, or exit events
            for event in pygame.event.get():
                #If we have a quit type event (exit out) then exit out of the game loop
                if event.type == pygame.QUIT:
                    is_game_over = True
                #Detect when key is pressed down
                elif event.type == pygame.KEYDOWN:
                    #Move up if up key is pressed
                    if event.key == pygame.K_UP:
                        direction = 1
                    #Move down if down key pressed
                    elif event.key == pygame.K_DOWN:
                        direction = -1
                #Detect when key is released
                elif event.type == pygame.KEYUP:
                    #Stop movement when key no longer pressed
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        direction = 0

                print(event)
                
            #Redraw the screen to be a white blank window
            self.game_screen.fill(WHITE_COLOR)
            self.game_screen.blit(self.image, (0,0))

            #Draw the treasure
            treasure.draw(self.game_screen)
            
            #Update the player position
            player_character.move(direction, self.height)
            #Draw the player at the new position
            player_character.draw(self.game_screen)

            #Move and draw the enemy character
            enemy_0.move(self.width)
            enemy_0.draw(self.game_screen)

            #New enemies will appear as higher levels are reached
            if level_speed > 1.75:
                enemy_1.move(self.width)
                enemy_1.draw(self.game_screen)
            if level_speed > 2.75:
                enemy_2.move(self.width)
                enemy_2.draw(self.game_screen)

            #End game is collision between enemy and treasure
            if player_character.detect_collision(enemy_0):
                is_game_over = True
                did_win = False
                text = font.render('You lost! :T', True, BLACK_COLOR)
                self.game_screen.blit(text, (300, 350))
                pygame.display.update()
                clock.tick(1)
                break
            elif player_character.detect_collision(enemy_1):
                is_game_over = True
                did_win = False
                text = font.render('You lost! :T', True, BLACK_COLOR)
                self.game_screen.blit(text, (300, 350))
                pygame.display.update()
                clock.tick(1)
                break
            elif player_character.detect_collision(enemy_2):
                is_game_over = True
                did_win = False
                text = font.render('You lost! :T', True, BLACK_COLOR)
                self.game_screen.blit(text, (300, 350))
                pygame.display.update()
                clock.tick(1)
                break
            
            elif player_character.detect_collision(treasure):
                    is_game_over = True
                    did_win = True
                    text = font.render('Keep going!', True, BLACK_COLOR)
                    self.game_screen.blit(text, (290, 350))
                    pygame.display.update()
                    clock.tick(1)
                    break
            
            while level_speed == 1:
                if player_character.detect_collision(treasure):
                    is_game_over = True
                    did_win = False
                    text = font.render('Congratulations, you have won!', True, BLACK_COLOR)
                    self.game_screen.blit(text, (15, 350))
                    pygame.display.update()
                    clock.tick(1)
                    break
            #Update all game graphics
            pygame.display.update()
            #Tick the clock to update everything within the game
            clock.tick(self.TICK_RATE)

        #Keeps the game going and increases speed if level won, otherwise kill the program if loss
        if did_win:
            self.run_game_loop(level_speed + 0.25)
        else:
            return

class GameObject:

    def __init__(self, image_path, x, y, width, height):
        object_image = pygame.image.load(image_path)
        #Scale the image up
        self.image = pygame.transform.scale(object_image, (width, height))
        
        self.x_pos = x
        self.y_pos = y

        self.width = width
        self.height = height

    def draw(self, background):
        background.blit(self.image, (self.x_pos, self.y_pos))

#Class to represent the character controlled by the player
class PlayerCharacter(GameObject):

    #GLOBAL: How many tiles the character moves per second
    SPEED = 5

    def __init__(self, image_path, x, y, width, height):
        super().__init__(image_path, x, y, width, height)

    #Move function will move character up if direction > 0, down if < 0
    def move(self, direction, max_height):
        if direction > 0:
            self.y_pos -= self.SPEED
        elif direction < 0:
            self.y_pos += self.SPEED

        if self.y_pos >= max_height - 40:
            self.y_pos = max_height - 40
    #Definition that will detect collision when there is overlap in the game objects w/ player character
    def detect_collision(self, other_body):
        if self.y_pos > other_body.y_pos + other_body.height:
            return False
        elif self.y_pos + self.height < other_body.y_pos:
            return False
        
        if self.x_pos > other_body.x_pos + other_body.width:
            return False
        elif self.x_pos + self.width < other_body.x_pos:
            return False
        
        return True

#Class to represent the character controlled by the player
class NonPlayerCharacter(GameObject):

    #GLOBAL: How many tiles the character moves per second
    SPEED = 5

    def __init__(self, image_path, x, y, width, height):
        super().__init__(image_path, x, y, width, height)

    #Move function will move character up if direction > 0, down if < 0
    def move(self, max_width):
        if self.x_pos <= 20:
            self.SPEED = abs(self.SPEED)
        elif self.x_pos >= max_width - 40:
            self.SPEED = -abs(self.SPEED)
        self.x_pos += self.SPEED

#initializer
pygame.init()

new_game = Game('Background.png', SCREEN_TITLE, SCREEN_WIDTH, SCREEN_HEIGHT)
new_game.run_game_loop(1)

#Quit pygame and the program
pygame.quit()
quit()

#Pygame Development 3
#Draw object to the screen
#Load images into object

#Pygame development 4
#Focus on making code object oriented
#Introduce classes and object into our code

#Pygame Development 5
#Implement game classes
#Implement generic game object class

#Pygame Development 6
#Implement Game Classes
#Implement Player Character Class and Movement

#Pygame development 7
#Implement game classes
#Implement enemy character class and bounds checking

#Pygame Development 8
#Implement collision detection
#Detect collisions with treasure and enemies

#Pygame Development 9
#Add true end game conditions
#Implement specific win and lose conditions

#Pygame development 10
#Make the game more interesting
#Add More enemies