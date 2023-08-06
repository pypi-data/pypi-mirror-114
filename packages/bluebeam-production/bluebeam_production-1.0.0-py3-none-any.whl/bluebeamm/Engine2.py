# Hides "Hello from the pygame community"
from os import environ
import os

environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame
import pytmx

from bluebeamm.GlobalVars import GlobalVars
#import GlobalVars
from bluebeamm.Level import Level
from pytmx.util_pygame import load_pygame
from pygame import mixer
import time

class Game_Engine:
    def __init__(self):
        # System init
        self.SystemON = True
        pygame.init()
        pygame.font.init()
        self._get_settings()
        self.clock = pygame.time.Clock()
        self.globals = GlobalVars()
        self.game_running = False

        # Screen init
        screen_size = ((self.screen_width, self.screen_height))
        self.globals.screen_size = screen_size
        self.screen = pygame.display.set_mode(screen_size)
        pygame.display.set_caption("Blue Beam")

        # getting directory for images
        self.sourceFileDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.imageDir  = os.path.join(self.sourceFileDir, "bluebeamm/images")
        self.soundDir  = os.path.join(self.sourceFileDir, "bluebeamm/Sounds")
        self.buttonDir = os.path.join(self.imageDir, "Buttons")
        self.screenDir = os.path.join(self.imageDir, "Screens")
        #self.heart = pygame.image.load(self.imageDir, "heart.png")

        # Load HUD information

        HUDfont = pygame.font.SysFont('Arial', 30)
        self.lives_text = HUDfont.render("Life: ", False, (0, 0, 0))
        self.heart = pygame.transform.scale(pygame.image.load(os.path.join(self.imageDir, "heart.png")).convert_alpha(), (50, 50))
        self.testHUD = pygame.transform.scale(pygame.image.load(os.path.join(self.screenDir, "testHUD2.png")).convert_alpha(), (1920, 1080))
        self.HUDrect = self.testHUD.get_rect(center = (self.screen_width / 2, self.screen_height / 2))
        self.options = pygame.transform.scale(pygame.image.load(os.path.join(self.buttonDir, "pause.png")).convert_alpha(), (370, 85))
        self.optionsRect = self.options.get_rect(center = (1710, 1027))
        self.menuOn = True
        self.gameOn = True

        self.level = None
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


    # Get level
    def load_level(self, levelNum=None):
        if(levelNum):
            self.levelNum = levelNum
        elif( not(self.levelNum) ):
            print("Force loading level 1")
            self.levelNum = 1

        #if(self.level): self.level.delete()

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
            img = pygame.transform.scale(img, (80, 80))
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
            img = pygame.transform.scale(img, (80, 80))
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
            img = pygame.transform.scale(img, (80, 80))
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
        self.screen.blit(self.image, (920, 975))

    # CURRENTLY HARDCODED!!! 
    # We can modify this later - to read from another file
    def _get_settings(self):
        self.screen_width = 1920
        self.screen_height = 1080
        self.fps = 60
        self.camera_offset = pygame.math.Vector2(self.screen_width / 2 - 25, self.screen_height / 2 - 25)

    def _check_events(self):
        mouse = pygame.mouse.get_pos()
        if self.game_running:
            if self.level.player.hp > 1000:
                self.dead = True
                self.death_screen()
        
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
        '''
        if self.level.player.current_power == "yellow":
            self.yel_update()
        elif self.level.player.current_power == "blue":
            self.blue_update()
        elif self.level.player.current_power == "red":
            self.red_update()
        '''

    def _show_hud(self):
        lives = int(self.level.player.hp / 10)

        self.screen.blit(self.testHUD, self.HUDrect)
        self.screen.blit(self.options, (1525, 985))

        for i in range(lives):
            self.screen.blit(self.heart, ((285 + i * 55), 1010))


        # Ranges from 0 to 2, and can go higher
        # At 1 and higher, we want an icon to show up representing "fire speed"
        # At 2 and higher, the player unlocks the charged shot mechanic - with the corresponding charge bar
        powerup_level  = self.level.player.get_powerup_level()
        
        # Ranges from 0.0 to 1.0, representing 0% to 100% charge
        charge_percent = self.level.player.get_charge_level()
        
        if self.level.player.charge_unlocked:
            pygame.draw.rect(self.screen, (255, 0, 0, 100), pygame.rect.Rect(1120, 1020, 350, 20))
            pygame.draw.rect(self.screen, (0, 255, 0, 100), pygame.rect.Rect(1120, 1020, 350 * charge_percent, 20))
        

    def _update_screen(self):
        if not self.level.player.recently_damaged:
            #self.level.player.turn_player_green()
            not_implemented = True
        else:
            self.level.player.recently_damaged = False
        self.level.render()
        self._show_hud()
        #if self.image:
        #    self.powerup_render()
        # Does same thing as .flip(), but is more intuitive
        # self.level.player.make_player_green()
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
        mixer.music.set_volume(0.25)
        mixer.music.play(-1)

        largeText = pygame.font.SysFont("arial", 115)
        btnText = pygame.font.SysFont("arial", 40)
        TextSurf, TextRect = self.text_objects("BlueBeam", largeText)
        TextRect.center = ((self.screen_width / 2), (self.screen_height / 2) - 200)

        # Load Un-highlighted buttons
        startBtn = pygame.transform.scale(pygame.image.load(os.path.join(self.buttonDir, "StartButton.png")).convert_alpha(), (300, 125))
        optBtn  = pygame.transform.scale(pygame.image.load(os.path.join(self.buttonDir, "OptionsButton.png")).convert_alpha(), (300,125))
        helpBtn  = pygame.transform.scale(pygame.image.load(os.path.join(self.buttonDir, "HelpButton.png")).convert_alpha(), (300,125))
        quitBtn = pygame.transform.scale(pygame.image.load(os.path.join(self.buttonDir, "QuitButton.png")).convert_alpha(), (300, 125))

        # Load highlighted buttons
        startBtnRed = pygame.transform.scale(pygame.image.load(os.path.join(self.buttonDir, "StartButtonRed.png")).convert_alpha(), (300, 125))
        optBtnRed  = pygame.transform.scale(pygame.image.load(os.path.join(self.buttonDir, "OptionsButtonRed.png")).convert_alpha(), (300,125))
        helpBtnRed  = pygame.transform.scale(pygame.image.load(os.path.join(self.buttonDir, "HelpButtonRed.png")).convert_alpha(), (300,125))
        quitBtnRed = pygame.transform.scale(pygame.image.load(os.path.join(self.buttonDir, "QuitButtonRed.png")).convert_alpha(), (300, 125))

        # Load button locations        
        startRect = startBtn.get_rect(center = (self.screen_width / 2, self.screen_height / 2))
        optRect = optBtn.get_rect(center = (self.screen_width / 2, self.screen_height / 2 + 125))
        helpRect = helpBtn.get_rect(center = (self.screen_width / 2, self.screen_height / 2 + 250))
        quitRect = quitBtn.get_rect(center = (self.screen_width / 2, self.screen_height / 2 + 375))
        
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
            
            pygame.display.update()
            self.clock.tick(self.fps)


    def level_select(self):
        lvlSel = True

        level_scrn = pygame.image.load(os.path.join(self.screenDir, "LevelScreen.png"))
        
        lvl1 = pygame.image.load(os.path.join(self.buttonDir, "Level1Select.png"))
        lvl2 = pygame.image.load(os.path.join(self.buttonDir, "Level2Select.png"))
        lvl3 = pygame.image.load(os.path.join(self.buttonDir, "Level3Select.png"))
        lvl1Red = pygame.image.load(os.path.join(self.buttonDir, "Level1SelectRed.png"))
        lvl2Red = pygame.image.load(os.path.join(self.buttonDir, "Level2SelectRed.png"))
        lvl3Red = pygame.image.load(os.path.join(self.buttonDir, "Level3SelectRed.png"))

        lvl1Rect = lvl1.get_rect(center = (960, 307))
        lvl2Rect = lvl2.get_rect(center = (960, 577))
        lvl3Rect = lvl3.get_rect(center = (960, 847))
        
        while lvlSel == True and self.SystemON:
            self._check_events()
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()

            self.screen.blit(level_scrn, (0, 0))
            self.screen.blit(lvl1, lvl1Rect)
            self.screen.blit(lvl2, lvl2Rect)
            self.screen.blit(lvl3, lvl3Rect)

            if lvl1Rect.collidepoint(mouse):
                self.screen.blit(lvl1Red, lvl1Rect)
                if click[0] == 1:
                    mixer.music.stop()
                    mixer.music.unload()
                    self.menu_running = False
                    self.menuOn = False
                    lvlSel = False
                    self.load_level(1)
            if lvl2Rect.collidepoint(mouse):
                self.screen.blit(lvl2Red, lvl2Rect)
                if click[0] == 2:
                    mixer.music.stop()
                    mixer.music.unload()
                    self.menu_running = False
                    self.menuOn = False
                    lvlSel = False
                    self.load_level(2)
            if lvl3Rect.collidepoint(mouse):
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

   
    def options_screen(self):
        pauseFont = pygame.font.SysFont('verdana', 55)

        options_scrn = pygame.image.load(os.path.join(self.screenDir, "OptionsMenu.png")).convert_alpha()

        resume, resumeRect = self.text_objects("Resume", pauseFont)
        opt, optRect = self.text_objects("Options", pauseFont)
        help, helpRect = self.text_objects("Help", pauseFont)
        menu, menuRect = self.text_objects("Main Menu", pauseFont)
        end, endRect = self.text_objects("Quit", pauseFont)

        resumeRect.center = (960, 400)
        optRect.center = (960, 475)
        helpRect.center = (960, 550)
        menuRect.center = (960, 625)
        endRect.center = (960, 700)
        options = True

        
        while options == True and self.SystemON:
            mouse = pygame.mouse.get_pos()
            
            self.screen.blit(options_scrn, (0, 0))
            self.screen.blit(resume, resumeRect)


            if resumeRect.collidepoint(mouse):
                self.screen.blit(pauseFont.render("Resume", True, (255, 0, 0)), resumeRect)
            
            for event in pygame.event.get():
                            
                if event.type == pygame.MOUSEBUTTONUP:
                    if resumeRect.collidepoint(mouse):
                        options = False

            pygame.display.update()
            self.clock.tick(60)
    
    def help_screen(self):
        pauseFont = pygame.font.SysFont('verdana', 55)

        resume, resumeRect = self.text_objects("Resume", pauseFont)
        resumeRect.center = (960, 400)

        help_scrn1 = pygame.image.load(os.path.join(self.screenDir, "HelpScreen1.png")).convert_alpha()
        help_scrn2 = pygame.image.load(os.path.join(self.screenDir, "HelpScreen2.png")).convert_alpha()
        help_scrn3 = pygame.image.load(os.path.join(self.screenDir, "HelpScreen3.png")).convert_alpha()


        helpBtn = pygame.transform.scale(pygame.image.load(os.path.join(self.buttonDir, "HelpButton.png")), (300, 125))
        helpBtnRed = pygame.transform.scale(pygame.image.load(os.path.join(self.buttonDir, "HelpButtonRed.png")), (300, 125))
        helpRect = helpBtn.get_rect(center = (self.screen_width / 2 + 400, self.screen_height / 2 + 200))
        
        help = True
        scr1 = True
        scr2 = False
        scr3 = False

        
        while help and self.SystemON:
            mouse = pygame.mouse.get_pos()
            if scr1 == True:
                self.screen.blit(help_scrn1, (0, 0))
                self.screen.blit(helpBtn, helpRect)

                if helpRect.collidepoint(mouse):
                    self.screen.blit(helpBtnRed, helpRect)
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONUP:
                        if helpRect.collidepoint(mouse):
                            scr1 = False
                            scr2 = True
                pygame.display.update()
                self.clock.tick(60)
            elif scr2 == True:
                self.screen.blit(help_scrn2, (0, 0))
                self.screen.blit(helpBtn, helpRect)

                if helpRect.collidepoint(mouse):
                    self.screen.blit(helpBtnRed, helpRect)
                for event in pygame.event.get():      
                    if event.type == pygame.MOUSEBUTTONUP:
                        if helpRect.collidepoint(mouse):
                            scr2 = False
                            scr3 = True
                pygame.display.update()
                self.clock.tick(60)
            elif scr3 == True:
                self.screen.blit(help_scrn3, (0, 0))
                self.screen.blit(helpBtn, helpRect)

                if helpRect.collidepoint(mouse):
                    self.screen.blit(helpBtnRed, helpRect)
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONUP:
                        if helpRect.collidepoint(mouse):
                            scr3 = False
                            help = False
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
        pause_scrn = pygame.image.load(os.path.join(self.imageDir, "PauseMenu.png")).convert_alpha()

        pauseFont = pygame.font.SysFont('verdana', 55)

        resume, resumeRect = self.text_objects("Resume", pauseFont)
        opt, optRect = self.text_objects("Options", pauseFont)
        help, helpRect = self.text_objects("Help", pauseFont)
        menu, menuRect = self.text_objects("Main Menu", pauseFont)
        end, endRect = self.text_objects("Quit", pauseFont)

        resumeRect.center = (960, 400)
        optRect.center = (960, 475)
        helpRect.center = (960, 550)
        menuRect.center = (960, 625)
        endRect.center = (960, 700)
        

        
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
        
        restart = pygame.transform.scale(pygame.image.load(os.path.join(self.imageDir, "RestartButton.png")), (300, 125))
        restartRect = restart.get_rect(center = (self.screen_width / 2, self.screen_height / 2 - 25))

        menuBtn = pygame.transform.scale(pygame.image.load(os.path.join(self.imageDir, "MenuButton.png")), (300, 125))
        menuRect = menuBtn.get_rect(center = (self.screen_width / 2, self.screen_height / 2 + 100))

        quitBtn = pygame.transform.scale(pygame.image.load(os.path.join(self.imageDir, "QuitButton.png")), (300, 125))
        quitRect = quitBtn.get_rect(center = (self.screen_width / 2, self.screen_height / 2 + 225))

        pygame.mixer.music.stop()
        # pygame.mixer.music.load(f'Sounds/cherish.xm')
        cherish_sound_dir = os.path.join(self.soundDir, f'cherish.xm')
        #print(cherish_sound_dir)
        #pygame.mixer.music.load(cherish_sound_dir)
        #pygame.mixer.music.play(-1,0,0)
        
        while self.dead and self.SystemON:
            mouse = pygame.mouse.get_pos()

            self.screen.blit(pygame.image.load(os.path.join(self.imageDir, "DeathScreen.png")).convert_alpha(), (0, 0))
            self.screen.blit(restart, restartRect)
            self.screen.blit(menuBtn, menuRect)
            self.screen.blit(quitBtn, quitRect)

            if restartRect.collidepoint(mouse):
                self.screen.blit(pygame.transform.scale(pygame.image.load(os.path.join(self.imageDir, "RestartButtonRed.png")), (300, 125)),
                                 restartRect)
            if menuRect.collidepoint(mouse):
                self.screen.blit(pygame.transform.scale(pygame.image.load(os.path.join(self.imageDir, "MenuButtonRed.png")), (300, 125)),
                                 menuRect)
            if quitRect.collidepoint(mouse):
                self.screen.blit(pygame.transform.scale(pygame.image.load(os.path.join(self.imageDir, "QuitButtonRed.png")), (300, 125)),
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

    def exit(self):
        self.SystemON = False
        self.gameOn = False
        self.pause = False
        self.dead = False
        self.menu_running = False
        self.game_running = False

def main():
    engine = Game_Engine()
    engine.game_loop()


if __name__ == '__main__':
    main()

    # engine = Game_Engine()
    # engine.game_loop()
    #engine.run_game()
