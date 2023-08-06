# Hides "Hello from the pygame community"
from os import environ
import os

environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame
import pytmx
from bluebeam.objects import Block
from bluebeam.objects import PhysObject, Player, YellowPower
from bluebeam.GlobalVars import GlobalVars
from bluebeam.Level import Level
from pytmx.util_pygame import load_pygame
from pygame import mixer
import math
import time

class Game_Engine:
    def __init__(self, width, height):
        # getting directory for images
        self.sourceFileDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.saveDir   = os.path.join(self.sourceFileDir, "bluebeam")
        self.imageDir  = os.path.join(self.sourceFileDir, "bluebeam/images")
        self.soundDir  = os.path.join(self.sourceFileDir, "bluebeam/Sounds")
        self.buttonDir = os.path.join(self.imageDir, "Buttons")
        self.screenDir = os.path.join(self.imageDir, "Screens")
        self.savefile = open(os.path.join(self.saveDir, "savefile.txt"), 'r')

        self.game_init(width, height)

    def game_init(self, width, height):
        # System init
        self.SystemON = True
        pygame.init()
        pygame.font.init()

        self._set_resolution(width, height)

        self.clock = pygame.time.Clock()
        self.globals = GlobalVars()
        self.game_running = False

        # Screen init
        screen_size = ((self.screen_width, self.screen_height))
        self.globals.screen_size = screen_size
        self.screen = pygame.display.set_mode(screen_size, pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE)
        #self.screen = pygame.Surface((1920, 1080))
        pygame.display.set_caption("Blue Beam")

        
        

        # Load HUD information
        self.xscale = self.screen_width / 1920
        self.yscale = self.screen_height / 1080
        #self.xscale = 1
        #self.yscale = 1
        HUDfont = pygame.font.SysFont('Arial', 30)
        self.lives_text = HUDfont.render("Life: ", False, (0, 0, 0))
        self.heart = pygame.transform.scale(pygame.image.load(os.path.join(self.imageDir, "heart.png")).convert_alpha(), (int(50 * self.xscale), int(50 * self.yscale)))
        self.testHUD = pygame.transform.scale(pygame.image.load(os.path.join(self.screenDir, "testHUD2.png")).convert_alpha(), (self.screen_width, self.screen_height))
        self.HUDrect = self.testHUD.get_rect(center = (self.screen_width / 2, self.screen_height / 2))
        self.options = pygame.transform.scale(pygame.image.load(os.path.join(self.buttonDir, "pause.png")).convert_alpha(), (int(370 * self.xscale), int(85 * self.yscale)))
        self.optionsRect = self.options.get_rect(center = (int(1710 * self.xscale), int(1027 * self.yscale)))
        self.menuOn = True
        self.gameOn = True

        self.level = None
        self.levelNum = None
        self.image = None

        self.pause = False
        self.dead = False
        self.restart = False
        #Load mixer/sounds
        pygame.mixer.pre_init(44100, -16, 2, 512)
        mixer.init()

        self.images = []
        self.index = 0
        self.animation_counter = 0

        self.x_scroll1 = self.screen_width / 2 - int(85 * self.xscale)
        self.x_scroll2 = self.screen_width / 2 - int(85 * self.xscale)
        self.globals.set_music_vol(5)
        self.globals.set_FX_vol(5)

        self.game_loop()
    
    def reset(self):
        # Get Level
        self.level = Level(self.globals, self.screen, self.camera_offset)

    # Get level
    def load_level(self, levelNum=None):
        if(levelNum):
            self.levelNum = levelNum
        elif( not(self.levelNum) ):
            print("Force loading level 1")
            self.levelNum = 1

        #if(self.level): self.level.delete()

        levelname = None

        if(self.levelNum == 1):
            levelname = "TestMap.tmx"
        elif(self.levelNum == 2):
            levelname = "MapLevel2.tmx"
        elif(self.levelNum == 3):
            levelname = "MapLevel3.tmx"
        self.level = Level(self.globals, self.screen, self.camera_offset, levelname)
            
    def yel_update(self):
        self.images = []
        for frame in range(1,6):
            img = pygame.image.load(os.path.join(self.imageDir, f'Yellow/frame{frame}.png'))

            #img = pygame.image.load(f'images/Yellow/frame{frame}.png')
            img = pygame.transform.scale(img, (int(80 * self.xscale), int(80 * self.yscale)))
            self.images.append(img)
        self.image = self.images[self.index]
        
        self.animation_counter += 1
        if self.animation_counter >= 10:
            self.image = self.images[self.index]
            self.index += 1
            self.animation_counter = 0
            if self.index >= 5:
                self.index = 0

    def blue_update(self):
        self.images = []
        for frame in range(1,6):
            img = pygame.image.load(os.path.join(self.imageDir, f'Blue/frame {frame}.png'))

            #img = pygame.image.load(f'images/Blue/frame {frame}.png')
            img = pygame.transform.scale(img, (int(80 * self.xscale), int(80 * self.yscale)))
            self.images.append(img)
        self.image = self.images[self.index]
        
        self.animation_counter += 1
        if self.animation_counter >= 10:
            self.image = self.images[self.index]
            self.index += 1
            self.animation_counter = 0
            if self.index >= 5:
                self.index = 0

    def red_update(self):
        self.images = []
        for frame in range(1,6):
            img = pygame.image.load(os.path.join(self.imageDir, f'Red/frame {frame}.png'))


            #img = pygame.image.load(f'images/Red/frame {frame}.png')
            img = pygame.transform.scale(img, (int(80 * self.xscale), int(80 * self.yscale)))
            self.images.append(img)
        self.image = self.images[self.index]
        
        self.animation_counter += 1
        if self.animation_counter >= 10:
            self.image = self.images[self.index]
            self.index += 1
            self.animation_counter = 0
            if self.index >= 5:
                self.index = 0

    
    def powerup_render(self):
        self.screen.blit(self.image, (int(920 * self.xscale), int(975 * self.yscale)))


    # CURRENTLY HARDCODED!!! 
    # We can modify this later - to read from another file
    def _get_settings(self):
        #self.screen_width = 1920
        #self.screen_height = 1080
        #xscale = self.screen_width / 1920
        #yscale = self.screen_height / 1080
        #self.fps = 60
        #self.camera_offset = pygame.math.Vector2(self.screen_width / 2 - int(25 * xscale), self.screen_height / 2 - int(25 * yscale))
        pass
        
    def _set_resolution(self, width, height):
        self.screen_width = width
        self.screen_height = height
        screen_size = ((self.screen_width, self.screen_height))
        self.screen = pygame.display.set_mode(screen_size)
        
        xscale = self.screen_width / 1920
        yscale = self.screen_height / 1080
        #xscale = 1
        #yscale = 1
        self.xscale = self.screen_width / 1920
        self.yscale = self.screen_height / 1080
        #self.xscale = 1
        #self.yscale = 1
        self.heart = pygame.transform.scale(pygame.image.load(os.path.join(self.imageDir, "heart.png")).convert_alpha(), (int(50 * self.xscale), int(50 * self.yscale)))
        self.testHUD = pygame.transform.scale(pygame.image.load(os.path.join(self.screenDir, "testHUD2.png")).convert_alpha(), (self.screen_width, self.screen_height))
        self.HUDrect = self.testHUD.get_rect(center = (self.screen_width / 2, self.screen_height / 2))
        self.options = pygame.transform.scale(pygame.image.load(os.path.join(self.buttonDir, "pause.png")).convert_alpha(), (int(370 * self.xscale), int(85 * self.yscale)))
        self.optionsRect = self.options.get_rect(center = (int(1710 * self.xscale), int(1027 * self.yscale)))
        self.fps = 60
        self.camera_offset = pygame.math.Vector2(self.screen_width / 2 - int(25 * xscale), self.screen_height / 2 - int(25 * yscale))

    def _check_events(self):
        mouse = pygame.mouse.get_pos()
        if self.game_running:
            if self.level.player.hp <= 0:
                self.dead = True
                self.death_screen()
            if self.level.bossDeathState == 1:
                self.victory_screen()
                self.game_running = False
                self.menuOn = True
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit()
            elif event.type == pygame.KEYDOWN:
                if self.game_running and (event.key == pygame.K_p or event.key == pygame.K_ESCAPE):
                    self.pause = True
                    self.paused()
            elif event.type == pygame.MOUSEBUTTONUP:
                    if mouse[0] in range(self.optionsRect.left, self.optionsRect.right) and mouse[1] in range(self.optionsRect.top, self.optionsRect.bottom):
                        self.pause = True
                        self.paused()

    def _object_updates(self):
        self.level.update()
        #'''
        if self.level.player.current_power == "yellow":
            self.yel_update()
        elif self.level.player.current_power == "blue":
            self.blue_update()
        elif self.level.player.current_power == "red":
            self.red_update()
        #'''

    def _show_hud(self):
        lives = int(self.level.player.hp / 10)

        self.screen.blit(self.testHUD, self.HUDrect)
        self.screen.blit(self.options, (int(1525 * self.xscale), int(985 * self.yscale)))

        for i in range(lives):
            self.screen.blit(self.heart, (int((285 + i * 55) * self.xscale), int(1010 * self.yscale)))


        # Ranges from 0 to 2, and can go higher
        # At 1 and higher, we want an icon to show up representing "fire speed"
        # At 2 and higher, the player unlocks the charged shot mechanic - with the corresponding charge bar
        powerup_level  = self.level.player.get_powerup_level()
        
        # Ranges from 0.0 to 1.0, representing 0% to 100% charge
        charge_percent = self.level.player.get_charge_level()
        
        if self.level.player.charge_unlocked:
            pygame.draw.rect(self.screen, (255, 0, 0, 100), pygame.rect.Rect(int(1120 * self.xscale), int(1020 * self.yscale), int(350 * self.xscale), int(20 * self.yscale)))
            pygame.draw.rect(self.screen, (0, 255, 0, 100), pygame.rect.Rect(int(1120 * self.xscale), int(1020 * self.yscale), int(350 * self.xscale) * charge_percent, int(20 * self.yscale)))
        

    def _update_screen(self):
        self.level.render()
        self._show_hud()
        if self.image:
            self.powerup_render()
        # Does same thing as .flip(), but is more intuitive
        pygame.display.update()

    def text_objects(self, text, font):
        textSurface = font.render(text, True, (255, 255, 255))
        return textSurface, textSurface.get_rect()

    def _update_dt(self):
        if self.clock.get_fps() == 0:
            dt = 0
        else:
            dt = 1. / self.clock.get_fps()
        self.globals.delta_time = dt

    def _cam_pos(self):
        return self.level.player.pos - self.camera_offset

    def main_menu(self):
        self.menu_running = True
        #mixer.music.load("sounds/Dangerous Dungeon.wav")
        mixer.music.load(os.path.join(self.soundDir, "Dangerous Dungeon.wav"))
        mixer.music.set_volume(0.3 * (self.globals.get_music_vol() / 100))
        mixer.music.play(-1)

        largeText = pygame.font.SysFont("arial", int(115 * self.yscale))
        btnText = pygame.font.SysFont("arial", int(40 * self.yscale))
        TextSurf, TextRect = self.text_objects("BlueBeam", largeText)
        TextRect.center = ((self.screen_width / 2), (self.screen_height / 2) - int(200 * self.yscale))

        # Load Un-highlighted buttons
        startBtn = pygame.transform.scale(pygame.image.load(os.path.join(self.buttonDir, "StartButton.png")).convert_alpha(), (int(300 * self.xscale), int(125 * self.yscale)))
        optBtn  = pygame.transform.scale(pygame.image.load(os.path.join(self.buttonDir, "OptionsButton.png")).convert_alpha(), (int(300 * self.xscale), int(125 * self.yscale)))
        helpBtn  = pygame.transform.scale(pygame.image.load(os.path.join(self.buttonDir, "HelpButton.png")).convert_alpha(), (int(300 * self.xscale), int(125 * self.yscale)))
        quitBtn = pygame.transform.scale(pygame.image.load(os.path.join(self.buttonDir, "QuitButton.png")).convert_alpha(), (int(300 * self.xscale), int(125 * self.yscale)))

        # Load highlighted buttons
        startBtnRed = pygame.transform.scale(pygame.image.load(os.path.join(self.buttonDir, "StartButtonRed.png")).convert_alpha(), (int(300 * self.xscale), int(125 * self.yscale)))
        optBtnRed  = pygame.transform.scale(pygame.image.load(os.path.join(self.buttonDir, "OptionsButtonRed.png")).convert_alpha(), (int(300 * self.xscale), int(125 * self.yscale)))
        helpBtnRed  = pygame.transform.scale(pygame.image.load(os.path.join(self.buttonDir, "HelpButtonRed.png")).convert_alpha(), (int(300 * self.xscale), int(125 * self.yscale)))
        quitBtnRed = pygame.transform.scale(pygame.image.load(os.path.join(self.buttonDir, "QuitButtonRed.png")).convert_alpha(), (int(300 * self.xscale), int(125 * self.yscale)))

        # Load button locations        
        startRect = startBtn.get_rect(center = (self.screen_width / 2, self.screen_height / 2))
        optRect = optBtn.get_rect(center = (self.screen_width / 2, self.screen_height / 2 + int(125 * self.yscale)))
        helpRect = helpBtn.get_rect(center = (self.screen_width / 2, self.screen_height / 2 + int(250 * self.yscale)))
        quitRect = quitBtn.get_rect(center = (self.screen_width / 2, self.screen_height / 2 + int(375 * self.yscale)))
        
        while self.menu_running and self.SystemON:
            self._check_events()

            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()

            self.screen.fill((0, 0, 0))
            self.screen.blit(TextSurf, TextRect)
            
            # Blit all buttons
            self.screen.blit(startBtn, startRect)
            self.screen.blit(optBtn, optRect)
            self.screen.blit(quitBtn, quitRect)
            self.screen.blit(helpBtn, helpRect)

            # Check if any button is hovered over / pressed
            if startRect.collidepoint(mouse):
                self.screen.blit(startBtnRed, startRect)
                if click[0] == 1:
                    self.level_select()
                    return
            if optRect.collidepoint(mouse):
                self.screen.blit(optBtnRed,  optRect)
                if click[0] == 1:
                    self.screen.fill((0, 0, 0))
                    self.options_screen()
            if helpRect.collidepoint(mouse):
                self.screen.blit(helpBtnRed, helpRect)
                if click[0] == 1:
                    self.help_screen()
            if quitRect.collidepoint(mouse):
                self.screen.blit(quitBtnRed, quitRect)
                if click[0] == 1:
                    self.exit()
                    break
            
            for event in pygame.event.get():
                if event.type == pygame.VIDEORESIZE:
                    self.screen = pygame.display.set_mode(event.size, pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE)

            #self.display_screen.blit(pygame.transform.scale(self.screen, (1080, 720)), (0, 0))
            pygame.display.update()
            self.clock.tick(self.fps)

    def level_select(self):
        time.sleep(0.5)
        lvlSel = True
        
        self.savefile = open(os.path.join(self.saveDir, "savefile.txt"), 'r')
        self.savefile.seek(0)
        savelines = self.savefile.readlines()
        lvl2unlocked = savelines[0].strip()
        lvl3unlocked = savelines[1].strip()

        level_scrn = pygame.transform.scale(pygame.image.load(os.path.join(self.screenDir, "LevelScreen.png")),  (self.screen_width, self.screen_height))

        backBtn = pygame.transform.scale(pygame.image.load(os.path.join(self.buttonDir, "BackButton.png")), (int(300 * self.xscale), int(125 * self.yscale)))
        backBtnRed = pygame.transform.scale(pygame.image.load(os.path.join(self.buttonDir, "BackButtonRed.png")), (int(300 * self.xscale), int(125 * self.yscale)))
        backRect = backBtn.get_rect(center = (int(175 * self.xscale), int(100 * self.yscale)))
        
        lvl1 = pygame.transform.scale(pygame.image.load(os.path.join(self.buttonDir, "Level1Select.png")), (int(1671 * self.xscale), int(237 * self.yscale)))
        lvl2 = pygame.transform.scale(pygame.image.load(os.path.join(self.buttonDir, "Level2Select.png")), (int(1671 * self.xscale), int(237 * self.yscale)))
        lvl3 = pygame.transform.scale(pygame.image.load(os.path.join(self.buttonDir, "Level3Select.png")), (int(1671 * self.xscale), int(237 * self.yscale)))
        lvl1Red = pygame.transform.scale(pygame.image.load(os.path.join(self.buttonDir, "Level1SelectRed.png")), (int(1671 * self.xscale), int(237 * self.yscale)))
        lvl2Red = pygame.transform.scale(pygame.image.load(os.path.join(self.buttonDir, "Level2SelectRed.png")), (int(1671 * self.xscale), int(237 * self.yscale)))
        lvl3Red = pygame.transform.scale(pygame.image.load(os.path.join(self.buttonDir, "Level3SelectRed.png")), (int(1671 * self.xscale), int(237 * self.yscale)))
        lvl2locked = pygame.transform.scale(pygame.image.load(os.path.join(self.buttonDir, "Level2SelectLocked.png")), (int(1671 * self.xscale), int(237 * self.yscale)))
        lvl3locked = pygame.transform.scale(pygame.image.load(os.path.join(self.buttonDir, "Level3SelectLocked.png")), (int(1671 * self.xscale), int(237 * self.yscale)))

        lvl1Rect = lvl1.get_rect(center = (self.screen_width / 2, int(307 * self.yscale)))
        lvl2Rect = lvl2.get_rect(center = (self.screen_width / 2, int(577 * self.yscale)))
        lvl3Rect = lvl3.get_rect(center = (self.screen_width / 2, int(847 * self.yscale)))
        
        while lvlSel == True and self.SystemON:
            self._check_events()
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()

            self.screen.blit(level_scrn, (0, 0))
            self.screen.blit(backBtn, backRect)
            self.screen.blit(lvl1, lvl1Rect)
            if lvl2unlocked == "1":
                self.screen.blit(lvl2, lvl2Rect)
            else:
                self.screen.blit(lvl2locked, lvl2Rect)
            if lvl3unlocked == "1":
                self.screen.blit(lvl3, lvl3Rect)
            else:
                self.screen.blit(lvl3locked, lvl3Rect)

            if backRect.collidepoint(mouse):
                self.screen.blit(backBtnRed, backRect)
                if click[0] == 1:
                    lvlSel == False
                    return
            if lvl1Rect.collidepoint(mouse):
                self.screen.blit(lvl1Red, lvl1Rect)
                if click[0] == 1:
                    mixer.music.stop()
                    mixer.music.unload()
                    self.menu_running = False
                    self.menuOn = False
                    lvlSel = False
                    self.load_level(1)
            if lvl2Rect.collidepoint(mouse) and lvl2unlocked == "1":
                self.screen.blit(lvl2Red, lvl2Rect)
                if click[0] == 1:
                    mixer.music.stop()
                    mixer.music.unload()
                    self.menu_running = False
                    self.menuOn = False
                    lvlSel = False
                    self.load_level(2)
            if lvl3Rect.collidepoint(mouse) and lvl3unlocked == "1":
                self.screen.blit(lvl3Red, lvl3Rect)
                if click[0] == 1:
                    mixer.music.stop()
                    mixer.music.unload()
                    self.menu_running = False
                    self.menuOn = False
                    lvlSel = False
                    self.load_level(3)

            pygame.display.update()
            self.clock.tick(self.fps)

    def button(self, x, y, width, height, color, action = None):
        global pen_color, pen_size
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x + width > mouse[0] > x and y + height + 12 > mouse[1] > y - 12:
            pygame.draw.rect(self.screen, color, (x, y, width, height))
            if click[0] == 1 and action != None:
                if action == "scroll1":
                    self.x_scroll1 = mouse[0]
                if action == "scroll2":
                    self.x_scroll2 = mouse[0]
        else:
            pygame.draw.rect(self.screen, color, (x, y, width, height))
    
    
    def options_screen(self):
        pauseFont = pygame.font.SysFont('verdana', int(55 * self.yscale))

        back, backRect = self.text_objects("Back", pauseFont)
        backRect.center = (self.screen_width / 2, int(400 * self.yscale))

        arrowLeft = pygame.transform.scale(pygame.image.load(os.path.join(self.buttonDir, "ArrowLeft.png")).convert_alpha(), (int(75 * self.xscale), int(75 * self.yscale)))
        arrowRight = pygame.transform.scale(pygame.image.load(os.path.join(self.buttonDir, "ArrowRight.png")).convert_alpha(), (int(75 * self.xscale), int(75 * self.yscale)))
        arrowLeftRect = arrowLeft.get_rect(center = (int(800 * self.xscale), int(683 * self.yscale)))
        arrowRightRect = arrowRight.get_rect(center = (int(1230 * self.xscale), int(683 * self.yscale)))

        options = True
        if self.screen_width == 1080:
            resOpt1 = True
            resOpt2 = False
        elif self.screen_width == 1920:
            resOpt1 = False
            resOpt2 = True

        
        while options == True and self.SystemON:
            mouse = pygame.mouse.get_pos()
            
            self.screen.blit(pygame.transform.scale(pygame.image.load(os.path.join(self.screenDir, "OptionsMenu.png")).convert_alpha(), (self.screen_width, self.screen_height)), (0, 0))
            self.screen.blit(back, backRect)

            self.button(self.screen_width / 2 - int(100 * self.xscale), self.screen_height / 2 - int(50 * self.yscale), int(275 * self.xscale), int(4 * self.yscale), (255, 255, 255), "scroll1")
            pygame.draw.rect(self.screen, (255, 0, 0), (self.x_scroll1 - int(5 * self.xscale), self.screen_height / 2 - int(65 * self.yscale), int(10 * self.xscale), int(30 * self.yscale)))
            self.globals.set_music_vol(math.trunc((self.x_scroll1 - (self.screen_width / 2 - int(100 * self.xscale))) / int(275 * self.xscale) * 100))
            if self.globals.get_music_vol() == 98 or self.globals.get_music_vol() == 99:
                self.globals.set_music_vol(100)
            mixer.music.set_volume(0.3 * (self.globals.get_music_vol() / 100))

            self.button(self.screen_width / 2 - int(100 * self.xscale), self.screen_height / 2 + int(45 * self.yscale), int(275 * self.xscale), int(4 * self.yscale), (255, 255, 255), "scroll2")
            pygame.draw.rect(self.screen, (255, 0, 0), (self.x_scroll2 - int(5 * self.xscale), self.screen_height / 2 + int(30 * self.yscale), int(10 * self.xscale), int(30 * self.yscale)))
            self.globals.set_FX_vol(math.trunc((self.x_scroll2 - (self.screen_width / 2 - int(100 * self.xscale))) / int(275 * self.xscale) * 100))
            if self.globals.get_FX_vol() == 98 or self.globals.get_FX_vol() == 99:
                self.globals.set_FX_vol(100)

            volume, volumeRect = self.text_objects("Music Volume", pauseFont)
            (volumeRect.top, volumeRect.left) = (self.screen_height / 2 - int(85 * self.yscale), int(325 * self.xscale))

            sound, soundRect = self.text_objects(str(self.globals.get_music_vol()), pauseFont)
            soundRect.center = (int(1200 * self.xscale), self.screen_height / 2 - int(50 * self.yscale))

            fx, fxRect = self.text_objects("Effects Volume", pauseFont)
            (fxRect.top, fxRect.left) = (self.screen_height / 2 + int(10 * self.xscale), int(325 * self.xscale))

            fxsound, fxsoundRect = self.text_objects(str(self.globals.get_FX_vol()), pauseFont)
            fxsoundRect.center = (int(1200 * self.xscale), self.screen_height / 2 + int(45 * self.yscale))

            res, resRect = self.text_objects("Resolution", pauseFont)
            (resRect.top, resRect.left) = (self.screen_height / 2 + int(105 * self.yscale), int(325 * self.xscale))

            self.screen.blit(volume, volumeRect)
            self.screen.blit(sound, soundRect)
            self.screen.blit(fx, fxRect)
            self.screen.blit(fxsound, fxsoundRect)
            
            """ if not self.game_running:
                self.screen.blit(res, resRect)
                self.screen.blit(arrowLeft, arrowLeftRect)
                self.screen.blit(arrowRight, arrowRightRect)

                
                if resOpt1:
                    resText, resTextRect = self.text_objects("1080x720", pauseFont)
                    (resTextRect.top, resTextRect.left) = (self.screen_height / 2 + int(105 * self.yscale), int(875 * self.xscale))
                    self.screen.blit(resText, resTextRect)
                elif resOpt2:
                    resText, resTextRect = self.text_objects("1920x1080", pauseFont)
                    (resTextRect.top, resTextRect.left) = (self.screen_height / 2 + int(105 * self.yscale), int(860 * self.xscale))
                    self.screen.blit(resText, resTextRect) """

            if backRect.collidepoint(mouse):
                self.screen.blit(pauseFont.render("Back", True, (255, 0, 0)), backRect)
            
            for event in pygame.event.get():
                            
                if event.type == pygame.MOUSEBUTTONUP:
                    if backRect.collidepoint(mouse):
                        if not self.game_running:    
                            if resOpt1 and not self.screen_width == 1080:
                                pygame.quit()
                                self.game_init(1080, 720)
                            elif resOpt2 and not self.screen_width == 1920:
                                pygame.quit()
                                self.game_init(1920, 1080)
                        options = False
                    if not self.game_running:    
                        if arrowLeftRect.collidepoint(mouse) or arrowRightRect.collidepoint(mouse):
                            resOpt1 = not resOpt1
                            resOpt2 = not resOpt2

            pygame.display.update()
            self.clock.tick(60)
    
    def help_screen(self):
        pauseFont = pygame.font.SysFont('verdana', int(55 * self.yscale))

        resume, resumeRect = self.text_objects("Resume", pauseFont)
        resumeRect.center = (self.screen_width / 2, int(400 * self.yscale))

        help_scrn1 = pygame.transform.scale(pygame.image.load(os.path.join(self.screenDir, "HelpScreen1.png")).convert_alpha(), (self.screen_width, self.screen_height))
        help_scrn2 = pygame.transform.scale(pygame.image.load(os.path.join(self.screenDir, "HelpScreen2.png")).convert_alpha(), (self.screen_width, self.screen_height))
        help_scrn3 = pygame.transform.scale(pygame.image.load(os.path.join(self.screenDir, "HelpScreen3.png")).convert_alpha(), (self.screen_width, self.screen_height))


        exitBtn = pygame.transform.scale(pygame.image.load(os.path.join(self.buttonDir, "ExitButton.png")), (int(300 * self.xscale), int(125 * self.yscale)))
        exitBtnRed = pygame.transform.scale(pygame.image.load(os.path.join(self.buttonDir, "ExitButtonRed.png")), (int(300 * self.xscale), int(125 * self.yscale)))
        exitRect = exitBtn.get_rect(center = (self.screen_width / 2 + int(700 * self.xscale), self.screen_height / 2 + int(425 * self.yscale)))

        #helpBtn = pygame.transform.scale(pygame.image.load(os.path.join(self.buttonDir, "HelpButton.png")), (300, 125))
        #helpBtnRed = pygame.transform.scale(pygame.image.load(os.path.join(self.buttonDir, "HelpButtonRed.png")), (300, 125))
        #helpRect = helpBtn.get_rect(center = (self.screen_width / 2 + 400, self.screen_height / 2 + 200))
        
        help = True
        scr1 = True
        scr2 = False
        scr3 = False

        
        while help and self.SystemON:
            mouse = pygame.mouse.get_pos()
            if scr1 == True:
                self.screen.blit(help_scrn1, (0, 0))
                self.screen.blit(exitBtn, exitRect)

                if exitRect.collidepoint(mouse):
                    self.screen.blit(exitBtnRed, exitRect)
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONUP:
                        if exitRect.collidepoint(mouse):
                            scr1 = False
                            scr2 = True
                pygame.display.update()
                self.clock.tick(60)
            elif scr2 == True:
                self.screen.blit(help_scrn2, (0, 0))
                self.screen.blit(exitBtn, exitRect)

                if exitRect.collidepoint(mouse):
                    self.screen.blit(exitBtnRed, exitRect)
                for event in pygame.event.get():      
                    if event.type == pygame.MOUSEBUTTONUP:
                        if exitRect.collidepoint(mouse):
                            scr2 = False
                            scr3 = True
                pygame.display.update()
                self.clock.tick(60)
            elif scr3 == True:
                self.screen.blit(help_scrn3, (0, 0))
                self.screen.blit(exitBtn, exitRect)

                if exitRect.collidepoint(mouse):
                    self.screen.blit(exitBtnRed, exitRect)
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONUP:
                        if exitRect.collidepoint(mouse):
                            scr3 = False
                            help = False
                            self.screen.fill((0, 0, 0))
                pygame.display.update()
                self.clock.tick(60)

    def game_loop(self):
        while self.gameOn and self.SystemON:
            if self.menuOn:
                self.main_menu()
            elif self.restart:
                self.restart = False
                self.load_level()
                self.run_game()
            else:
                self.run_game()

    def run_game(self):
        #print(self.sourceFileDir)
        self.game_running = True
        # Get Level
        while self.game_running and self.SystemON:   
            if self.pause == False and self.dead == False and self.restart == False:
                self._update_dt()
                self._check_events()
                self._object_updates()
            self._update_screen()
            self.clock.tick(self.fps) # Performs a time.sleep, at an interval ensuring the game runs at (fps)
        self.level.delete()

    
    def paused(self):
        pause_scrn = pygame.transform.scale(pygame.image.load(os.path.join(self.imageDir, "PauseMenu.png")).convert_alpha(), (self.screen_width, self.screen_height))

        pauseFont = pygame.font.SysFont('verdana', int(55 * self.yscale))

        resume, resumeRect = self.text_objects("Resume", pauseFont)
        opt, optRect = self.text_objects("Options", pauseFont)
        help, helpRect = self.text_objects("Help", pauseFont)
        menu, menuRect = self.text_objects("Main Menu", pauseFont)
        end, endRect = self.text_objects("Quit", pauseFont)

        resumeRect.center = (self.screen_width / 2, int(400 * self.yscale))
        optRect.center = (self.screen_width / 2, int(475 * self.yscale))
        helpRect.center = (self.screen_width / 2, int(550 * self.yscale))
        menuRect.center = (self.screen_width / 2, int(625 * self.yscale))
        endRect.center = (self.screen_width / 2, int(700 * self.yscale))
        

        
        while self.pause == True and self.SystemON:
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()

            self.screen.blit(pause_scrn, (0, 0))
            self.screen.blit(resume, resumeRect)
            self.screen.blit(opt, optRect)
            self.screen.blit(help, helpRect)
            self.screen.blit(menu, menuRect)
            self.screen.blit(end, endRect)


            if resumeRect.collidepoint(mouse):
                self.screen.blit(pauseFont.render("Resume", True, (255, 0, 0)), resumeRect)
            if optRect.collidepoint(mouse):
                self.screen.blit(pauseFont.render("Options", True, (255, 0, 0)), optRect)
            if helpRect.collidepoint(mouse):
                self.screen.blit(pauseFont.render("Help", True, (255, 0, 0)), helpRect)
            if menuRect.collidepoint(mouse):
                self.screen.blit(pauseFont.render("Main Menu", True, (255, 0, 0)), menuRect)
            if endRect.collidepoint(mouse):
                self.screen.blit(pauseFont.render("Quit", True, (255, 0, 0)), endRect)
            
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.pause = False
                            
                elif event.type == pygame.MOUSEBUTTONUP:
                    if resumeRect.collidepoint(mouse):
                        self.pause = False
                    if optRect.collidepoint(mouse):
                        self.options_screen()
                    if helpRect.collidepoint(mouse):
                        self.help_screen()
                    if menuRect.collidepoint(mouse):
                        self.game_running = False
                        self.pause = False
                        self.menuOn = True
                    if endRect.collidepoint(mouse):
                        self.exit()

            pygame.display.update()
            self.clock.tick(60)
            

    def death_screen(self):
        
        restart = pygame.transform.scale(pygame.image.load(os.path.join(self.imageDir, "RestartButton.png")), (int(300 * self.xscale), int(125 * self.yscale)))
        restartRect = restart.get_rect(center = (self.screen_width / 2, self.screen_height / 2 - int(25 * self.yscale)))

        menuBtn = pygame.transform.scale(pygame.image.load(os.path.join(self.imageDir, "MenuButton.png")), (int(300 * self.xscale), int(125 * self.yscale)))
        menuRect = menuBtn.get_rect(center = (self.screen_width / 2, self.screen_height / 2 + int(100 * self.yscale)))

        quitBtn = pygame.transform.scale(pygame.image.load(os.path.join(self.imageDir, "QuitButton.png")), (int(300 * self.xscale), int(125 * self.yscale)))
        quitRect = quitBtn.get_rect(center = (self.screen_width / 2, self.screen_height / 2 + int(225 * self.yscale)))

        pygame.mixer.music.stop()
        # pygame.mixer.music.load(f'Sounds/cherish.xm')
        cherish_sound_dir = os.path.join(self.soundDir, f'cherish.xm')
        pygame.mixer.music.load(cherish_sound_dir)
        pygame.mixer.music.play(-1,0,0)

        deathscreen = pygame.image.load(os.path.join(self.imageDir, "DeathScreen.png")).convert_alpha()
        deathscreen = pygame.transform.scale(deathscreen, (self.screen_width, self.screen_height))
        
        while self.dead and self.SystemON:
            mouse = pygame.mouse.get_pos()

            self.screen.blit(deathscreen, (0, 0))
            self.screen.blit(restart, restartRect)
            self.screen.blit(menuBtn, menuRect)
            self.screen.blit(quitBtn, quitRect)

            if restartRect.collidepoint(mouse):
                self.screen.blit(pygame.transform.scale(pygame.image.load(os.path.join(self.imageDir, "RestartButtonRed.png")), (int(300 * self.xscale), int(125 * self.yscale))),
                                 restartRect)
            if menuRect.collidepoint(mouse):
                self.screen.blit(pygame.transform.scale(pygame.image.load(os.path.join(self.imageDir, "MenuButtonRed.png")), (int(300 * self.xscale), int(125 * self.yscale))),
                                 menuRect)
            if quitRect.collidepoint(mouse):
                self.screen.blit(pygame.transform.scale(pygame.image.load(os.path.join(self.imageDir, "QuitButtonRed.png")), (int(300 * self.xscale), int(125 * self.yscale))),
                                 quitRect)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    if mouse[0] in range(restartRect.left, restartRect.right) and mouse[1] in range(restartRect.top, restartRect.bottom):
                        self.game_running = False
                        self.dead = False
                        self.restart = True
                    if mouse[0] in range(menuRect.left, menuRect.right) and mouse[1] in range(menuRect.top, menuRect.bottom):
                        self.game_running = False
                        self.dead = False
                        self.menuOn = True
                    if mouse[0] in range(quitRect.left, quitRect.right) and mouse[1] in range(quitRect.top, quitRect.bottom):
                        self.exit()

            pygame.display.update()
            self.clock.tick(60)

    def victory_screen(self):
        if self.levelNum == 1:
            self.savefile.seek(0)
            savelines = self.savefile.readlines()
            lvl2unlocked = savelines[0].strip()
            lvl3unlocked = savelines[1].strip()
            self.savefile = open(os.path.join(self.saveDir, "savefile.txt"), 'w')
            self.savefile.writelines(["1\n", lvl3unlocked])
        if self.levelNum == 2:
            self.savefile.seek(0)
            self.savefile = open(os.path.join(self.saveDir, "savefile.txt"), 'w')
            self.savefile.writelines(["1\n", "1"])



        victFont = pygame.font.SysFont('Verdana', int(120 * self.yscale))
        start = time.time()

        while time.time() - start < 5:
            if int(time.time() - start) % 2 == 0:
                self.screen.blit(victFont.render("LEVEL CLEAR", True, (255, 0, 0)), (self.screen_width / 2 - int(400 * self.xscale), self.screen_height / 2 - int(300 * self.yscale)))
            else:
                self.screen.blit(victFont.render("LEVEL CLEAR", True, (0, 255, 0)), (self.screen_width / 2 - int(400 * self.xscale), self.screen_height / 2 - int(300 * self.yscale)))
            pygame.display.update()
            self.clock.tick(self.fps)
        self.level.bossDeathState = 0

    def exit(self):
        self.SystemON = False
        self.gameOn = False
        self.pause = False
        self.dead = False
        self.menu_running = False
        self.game_running = False
        #pygame.quit()

def main():
    engine = Game_Engine(1920, 1080)
    #engine.game_loop()


if __name__ == '__main__':
    main()

    # engine = Game_Engine()
    # engine.game_loop()
    #engine.run_game()
