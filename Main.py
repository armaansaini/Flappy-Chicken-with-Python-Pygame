import pygame
import random
import time
from Settings import *
from Sprites import *

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode([WIDTH, HEIGHT])
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.timesession = 0

        self.game_folder = path.dirname(__file__)

        self.font = pygame.font.match_font('Arial')
        self.boldfont = pygame.font.match_font('Arial Bold')

        self.font_folder = path.join(self.game_folder, 'font')
        self.Arialfont = pygame.font.Font(self.font, 25)
        self.Blocksfont = pygame.font.Font(path.join(self.font_folder,'blocks.ttf'), 100)
        self.Arialboldfont = pygame.font.Font(self.boldfont,50)

        self.credit_data = []

    # Loading Images
    def loadimages(self):
        img_folder = path.join(self.game_folder, 'img')

        # Background
        self.background = pygame.transform.scale(pygame.image.load(path.join(img_folder,'background.png')).convert(), (WIDTH,HEIGHT))

        # Walls
        self.wall_img = pygame.image.load(path.join(img_folder, 'hill.png')).convert()
        self.wall_img2 = pygame.image.load(path.join(img_folder,'hill2.png')).convert()

        # Chicken for the front page
        self.frontchicken = pygame.transform.scale(pygame.image.load(path.join(img_folder, 'frontchicken.png')).convert(), (400,400))
        self.frontchicken.set_colorkey(YELLOW)
        self.frontchicken2 = pygame.transform.scale(pygame.image.load(path.join(img_folder, 'frontchicken2.png')).convert(), (400,400))
        self.frontchicken2.set_colorkey(YELLOW)

        # Chicken for the gameplay
        self.bird_fly = []
        self.bird1 = pygame.image.load(path.join(img_folder, 'c1.png')).convert()
        self.bird2 = pygame.image.load(path.join(img_folder, 'c2.png')).convert()
        self.bird3 = pygame.image.load(path.join(img_folder, 'c3.png')).convert()
        self.bird4 = pygame.image.load(path.join(img_folder, 'c4.png')).convert()
        self.hit1 = pygame.image.load(path.join(img_folder, 'g1.png')).convert()
        self.hit2 = pygame.image.load(path.join(img_folder, 'g2.png')).convert()
        self.bird_fly.extend([self.bird1, self.bird2, self.bird3, self.bird4, self.hit1, self.hit2])

        # Clouds
        self.cloud_list = []
        self.cloud1 = pygame.image.load(path.join(img_folder, 'cloud1.png')).convert()
        self.cloud2 = pygame.image.load(path.join(img_folder, 'cloud2.png')).convert()
        self.cloud3 = pygame.image.load(path.join(img_folder, 'cloud3.png')).convert()
        self.cloud4 = pygame.image.load(path.join(img_folder, 'cloud4.png')).convert()
        self.cloud5 = pygame.image.load(path.join(img_folder, 'cloud5.png')).convert()
        self.cloud_list.extend([self.cloud1, self.cloud2, self.cloud3, self.cloud4, self.cloud5])

        # Items
        self.goldcoin = pygame.image.load(path.join(img_folder, 'gold.png')).convert()
        self.silvercoin = pygame.image.load(path.join(img_folder, 'silver.png')).convert()
        self.heart = pygame.image.load(path.join(img_folder, 'heart.png')).convert()
        self.heart.set_colorkey(BLACK)

        # Buttons
        self.greenbutton = pygame.image.load(path.join(img_folder, 'greenbutton.png')).convert()
        self.bluebutton = pygame.image.load(path.join(img_folder, 'bluebutton.png')).convert()
        self.redbutton = pygame.image.load(path.join(img_folder, 'redbutton.png')).convert()
        self.yellowbutton = pygame.image.load(path.join(img_folder, 'yellowbutton.png')).convert()
        self.greenbutton.set_colorkey(BLACK)
        self.bluebutton.set_colorkey(BLACK)
        self.redbutton.set_colorkey(BLACK)
        self.yellowbutton.set_colorkey(BLACK)

        # Numbers
        self.num0 = pygame.image.load(path.join(img_folder, 'hud_0.png')).convert_alpha()
        self.num1 = pygame.image.load(path.join(img_folder, 'hud_1.png')).convert_alpha()
        self.num2 = pygame.image.load(path.join(img_folder, 'hud_2.png')).convert_alpha()
        self.num3 = pygame.image.load(path.join(img_folder, 'hud_3.png')).convert_alpha()
        self.num4 = pygame.image.load(path.join(img_folder, 'hud_4.png')).convert_alpha()
        self.num5 = pygame.image.load(path.join(img_folder, 'hud_5.png')).convert_alpha()
        self.num6 = pygame.image.load(path.join(img_folder, 'hud_6.png')).convert_alpha()
        self.num7 = pygame.image.load(path.join(img_folder, 'hud_7.png')).convert_alpha()
        self.num8 = pygame.image.load(path.join(img_folder, 'hud_8.png')).convert_alpha()
        self.num9 = pygame.image.load(path.join(img_folder, 'hud_9.png')).convert_alpha()

    # Loading Sounds and Music
    def loadsounds(self):
        snd_folder = path.join(self.game_folder, 'snd')
        self.coin_sound = pygame.mixer.Sound(path.join(snd_folder, 'coin.wav'))
        self.coin_sound.set_volume(0.1)
        self.hurt_sound = pygame.mixer.Sound(path.join(snd_folder, 'touchwall.wav'))
        self.death_sound = pygame.mixer.Sound(path.join(snd_folder, 'death.wav'))
        self.heart_sound = pygame.mixer.Sound(path.join(snd_folder, 'gotheart.wav'))
        self.heart_sound.set_volume(0.1)
        pygame.mixer.music.load(path.join(snd_folder, 'honey-bear-loop.ogg'))
        pygame.mixer.music.set_volume(2)

    # Loading the Credits
    def loadcredits(self):
        with open(path.join(self.game_folder, 'Credits.txt'), 'rt') as f:
            for line in f:
                self.credit_data.append(line.rstrip())

    # Loading Highscore
    def loadhighscore(self):
        try:
            with open(path.join(self.game_folder, 'Highscore.txt'), 'r') as f:
                self.highscore = int(f.readline().rstrip())
        except:
            with open(path.join(self.game_folder, 'Highscore.txt'), 'w') as f:
                f.write(str(0))

    # Loading Achievements
    def loadachievement(self):
        with open(path.join(self.game_folder, 'Achievements.txt'), 'r') as f:
            print(True)
            self.ach1 = int(f.readline().rstrip())
            self.ach2 = int(f.readline().rstrip())
            self.ach3 = int(f.readline().rstrip())

    # To draw player's lives on the screen
    def drawhearts(self):
        for i in range(self.player.heart):
            self.screen.blit(self.heart, [(WIDTH-55)+(i*-55), 20])

    # To draw frames on the screen
    def drawfps(self):
        self.fpstxt = self.Arialfont.render(str(int(self.clock.get_fps())), True, BLACK)
        self.screen.blit(self.fpstxt, (10,HEIGHT-60))

    # To draw score on the screen
    def blitscore(self, score, highscore):
        scoretext = str(score)
        highscoretext = str(highscore)
        for i in range(len(scoretext)):
            if scoretext[i] == '0':
                self.screen.blit(self.num0, ((10+(i*30)),50))
            elif scoretext[i] == '1':
                self.screen.blit(self.num1, ((10+(i*30)),50))
            elif scoretext[i] == '2':
                self.screen.blit(self.num2, ((10+(i*30)),50))
            elif scoretext[i] == '3':
                self.screen.blit(self.num3, ((10+(i*30)),50))
            elif scoretext[i] == '4':
                self.screen.blit(self.num4, ((10+(i*30)),50))
            elif scoretext[i] == '5':
                self.screen.blit(self.num5, ((10+(i*30)),50))
            elif scoretext[i] == '6':
                self.screen.blit(self.num6, ((10+(i*30)),50))
            elif scoretext[i] == '7':
                self.screen.blit(self.num7, ((10+(i*30)),50))
            elif scoretext[i] == '8':
                self.screen.blit(self.num8, ((10+(i*30)),50))
            elif scoretext[i] == '9':
                self.screen.blit(self.num9, ((10+(i*30)),50))

        for i in range(len(highscoretext)):
            if highscoretext[i] == '0':
                self.screen.blit(self.num0, ((10+(i*30)),0))
            elif highscoretext[i] == '1':
                self.screen.blit(self.num1, ((10+(i*30)),0))
            elif highscoretext[i] == '2':
                self.screen.blit(self.num2, ((10+(i*30)),0))
            elif highscoretext[i] == '3':
                self.screen.blit(self.num3, ((10+(i*30)),0))
            elif highscoretext[i] == '4':
                self.screen.blit(self.num4, ((10+(i*30)),00))
            elif highscoretext[i] == '5':
                self.screen.blit(self.num5, ((10+(i*30)),0))
            elif highscoretext[i] == '6':
                self.screen.blit(self.num6, ((10+(i*30)),0))
            elif highscoretext[i] == '7':
                self.screen.blit(self.num7, ((10+(i*30)),0))
            elif highscoretext[i] == '8':
                self.screen.blit(self.num8, ((10+(i*30)),0))
            elif highscoretext[i] == '9':
                self.screen.blit(self.num9, ((10+(i*30)),0))

    # To write on the start screen
    def writestartscreen(self):
        playtext = self.Arialfont.render("PLAY", True, BLACK)
        credittext = self.Arialfont.render("CREDITS", True, BLACK)
        achievetext = self.Arialfont.render("ACHIEVEMENTS", True, BLACK)
        quittext = self.Arialfont.render("QUIT", True, BLACK)
        self.backtext = self.Arialfont.render("BACK", True, BLACK)
        flappytext = self.Blocksfont.render("FLAPPY", True, GREY)
        chickentext = self.Blocksfont.render("CHICKEN", True, DARKGREEN)

        self.screen.blit(flappytext, [50,100])
        self.screen.blit(chickentext, [500,100])

        self.screen.blit(playtext, [(WIDTH / 2)-50,308])
        self.screen.blit(achievetext, [(WIDTH / 2)-108,408])
        self.screen.blit(credittext, [(WIDTH / 2)-70,508])
        self.screen.blit(quittext, [(WIDTH / 2)-50,608])

    # Making the start screen
    def startscreen(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        click = pygame.mouse.get_pressed()
        cur = pygame.mouse.get_pos()

        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.frontchicken, (10, 300))
        self.screen.blit(self.frontchicken2, (650,300))
        self.screen.blit(self.greenbutton, ((WIDTH / 2)-120, 300))
        self.screen.blit(self.bluebutton, ((WIDTH / 2)-120, 400))
        self.screen.blit(self.yellowbutton, ((WIDTH / 2)-120, 500))
        self.screen.blit(self.redbutton, ((WIDTH / 2)-120, 600))

        self.writestartscreen()

        if click[0] == 1:
            if ((WIDTH / 2) - 120 < cur[0] < (WIDTH / 2) + 70) and (300 < cur[1] < 349):
                self.new()

            elif ((WIDTH / 2) - 120 < cur[0] < (WIDTH / 2) + 70) and (400 < cur[1] < 449):
                self.achievement()

            elif ((WIDTH / 2) - 120 < cur[0] < (WIDTH / 2) + 70) and (500 < cur[1] < 549):
                self.credits()

            elif ((WIDTH / 2) - 120 < cur[0] < (WIDTH / 2) + 70) and (600 < cur[1] < 649):
                self.running = False

        pygame.display.flip()

    # Making the credit screen
    def credits(self):
        self.showcredit = True
        while self.showcredit == True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            click = pygame.mouse.get_pressed()
            cur = pygame.mouse.get_pos()

            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.yellowbutton, (20,HEIGHT - 70))

            self.screen.blit(self.backtext, (80, HEIGHT - 62))
            for line in range(len(self.credit_data)):
                try:
                    if self.credit_data[line][0] == '#':
                        self.credit_line = self.Arialboldfont.render((self.credit_data[line]).lstrip('#'), True, BLACK)
                        self.screen.blit(self.credit_line, (250, line*25))
                    else:
                        self.credit_line = self.Arialfont.render(self.credit_data[line], True, BLACK)
                        self.screen.blit(self.credit_line, (250, line*25))
                except:
                    pass

            pygame.display.flip()

            if click[0] == 1 and 80 < cur[0] < 270 and HEIGHT - 60 < cur[1] < HEIGHT - 8:
                self.showcredit = False
                self.startscreen()

    #Making the achievement screen
    def achievement(self):
        achieve = True
        yellowbutton = pygame.transform.scale(self.yellowbutton, (500, 100))
        greenbutton = pygame.transform.scale(self.greenbutton, (500,100))

        ach1text = self.Arialboldfont.render("Score 10,000 in one game", True, BLACK)
        ach2text = self.Arialboldfont.render("Collect 50 coins in one game", True, BLACK)
        ach3text = self.Arialboldfont.render("Score 5,000 without a hit", True, BLACK)

        while achieve:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            cur = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()

            self.screen.blit(self.background, (0,0))
            self.screen.blit(self.yellowbutton, (20, HEIGHT - 70))
            self.screen.blit(self.backtext, (80, HEIGHT - 62))

            if self.ach1 == 1:
                self.screen.blit(greenbutton, (300,100))
            else:
                self.screen.blit(yellowbutton, (300,100))

            if self.ach2 == 1:
                self.screen.blit(greenbutton, (300,300))
            else:
                self.screen.blit(yellowbutton, (300,300))

            if self.ach3 == 1:
                self.screen.blit(greenbutton, (300,500))
            else:
                self.screen.blit(yellowbutton, (300,500))

            self.screen.blit(ach1text, (340, 130))
            self.screen.blit(ach2text, (320,330))
            self.screen.blit(ach3text, (340,530))
            pygame.display.update()

            if click[0] == 1 and 80 < cur[0] < 270 and HEIGHT - 60 < cur[1] < HEIGHT - 8:
                achieve = False
                self.startscreen()

    # Making the game pause
    def pause(self, counter):
        pause = True
        count = counter
        pausetext = self.Blocksfont.render('PAUSE', True, RED)
        while pause == True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pause = False
                    self.playing = False
                    self.running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        pause = False
                        return count


            self.screen.blit(pausetext, ((WIDTH / 2)-200, (HEIGHT / 2)-100))
            pygame.display.flip()

    # Initialising a New Game
    def new(self):
        self.highscore = 0
        self.loadhighscore()

        self.all_sprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.clouds = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()

        self.player = Player(self.bird_fly)
        self.all_sprites.add(self.player)

        self.WALLCOUNT = pygame.USEREVENT
        pygame.time.set_timer(self.WALLCOUNT,1000)
        self.counter = WALLCOUNTER
        self.score = 0
        self.coinscount = 0
        self.damagehitcount = 0
        self.blitscore(self.score, self.highscore)

        self.run()

    # Running the Game
    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    # Check player's collision with a wall
    def check_collision_wall(self):
        if self.player.heart == 0:
            hits = pygame.sprite.spritecollide(self.player, self.walls, False)
            if hits:
                self.damagehitcount += 1
                self.death_sound.play()
                self.tick = pygame.time.get_ticks()
                if self.highscore < self.score:
                    with open(path.join(self.game_folder,'Highscore.txt'), 'w') as f:
                        f.write(str(self.score))
                while pygame.time.get_ticks() - self.tick < 1000:
                    pass

                else:
                    Wall.dx = -10
                    Wallup.dx = -10
                    self.timesession = pygame.time.get_ticks()
                    g.new()

        else:
            hits = pygame.sprite.spritecollide(self.player, self.walls, True)
            if hits:
                self.damagehitcount += 1
                self.hurt_sound.play()
                self.player.heart -= 1

    # Check player's collision with a coin
    def check_collision_coin(self):
        hitcoin = pygame.sprite.spritecollide(self.player, self.coins, True)
        if hitcoin:
            if str(hitcoin[0])[1] == 'S':
                self.coinscount += 1
                self.score += Scoin.reward
                self.coin_sound.play()
            if str(hitcoin[0])[1] == 'G':
                self.coinscount += 1
                self.score += Gcoin.reward
                self.coin_sound.play()
            if str(hitcoin[0])[1] == 'H':
                self.player.heart += 1
                self.heart_sound.play()

    # Handle all the events happening
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.jump()

                if event.key == pygame.K_RETURN:
                    self.get_count = self.pause(self.counter)
                    self.counter = self.get_count


            if event.type == self.WALLCOUNT:
                self.counter -= 1
                if self.counter == 0:
                    self.w1 = Wall(WIDTH, self.wall_img, self)
                    self.w2 = Wallup(WIDTH, self.w1.rect.bottom, self.wall_img2, self)
                    
                    # Randomize the gold coin and giving silver otherwise
                    if self.ranthou < 10:
                        self.h = Heartup(self.w1.rect.bottom, self.heart, self)
                    elif self.ranthou < 100:
                        self.coin = Gcoin(self.goldcoin, self.w1.rect.bottom, self)
                    else:
                        self.coin = Scoin(self.silvercoin, self.w1.rect.bottom, self)
                    
                    self.score += 5
                    self.counter = 1

        # Collision with a coin or powerup
        self.check_collision_coin()

        # Collision with a wall and updating high score if accomplished
        self.check_collision_wall()

        # Random thousand
        self.ranthou = random.randrange(1000)




        # Randomize the cloud appearance
        if self.ranthou < 10 and len(self.clouds) < 2:
            self.c = Cloud(self.cloud_list)
            self.clouds.add(self.c)

    # Update all sprites
    def update(self):
        self.all_sprites.update()
        self.clouds.update()

        flag = 0
        #
        #Achievements handler
        #
        #Achievement 1 : Score 10,000 score in one game
        #Achievement 2 : Collect 50 coins in one game
        #Achievement 3 : Score 5,000 without getting hit
        #
        if self.score > 10000:
            self.ach1 = 1
            flag = 1
        if self.coinscount >= 50:
            self.ach2 = 1
            flag = 1
        if self.score > 5000 and self.damagehitcount == 0:
            self.ach3 = 1
            flag = 1
        if flag == 1:
            with open(path.join(self.game_folder, 'Achievements.txt'), 'w') as f:
                f.write(str(self.ach1) + '\n')
                f.write(str(self.ach2) + '\n')
                f.write(str(self.ach3) + '\n')
                f.flush()

    # Draw all sprites
    def draw(self):
        self.screen.blit(self.background, (0, 0))
        #self.drawfps()
        self.clouds.draw(self.screen)
        self.all_sprites.draw(self.screen)
        self.blitscore(self.score, self.highscore)
        self.drawhearts()
        pygame.display.flip()

g = Game()
g.loadimages()
g.loadcredits()
g.loadsounds()
g.loadachievement()
pygame.mixer.music.play(-1)
while g.running:
    g.startscreen()
pygame.quit()
quit()






















