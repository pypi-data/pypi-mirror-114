# bluebeam 
~~~~~~~~~~~~~~
   The Game
~~~~~~~~~~~~~~
    Bluebeam is a run and gun exploratory sidescroller inspired by retro-games such as Contra. 
It is implemented using primarily python and pygame.

~~~~~~~~~~~~~~~~~
 Pip Installation
~~~~~~~~~~~~~~~~~~
1. Download the associated .tar.gz library
2. Open up the top-level directory in terminal
3. pip install the zipped file or alternatively pip install from pypi
   pip install bluebeam-release
4. Run the game from any directory with play_bluebeam

~~~~~~~~~~~~~~
Windows Installer
~~~~~~~~~~~~~~
1. Navigate to the .msi file in Explorer
2. Double-click to install anywhere using the wizard
3. When installation finishes a shortcut named Blue Beam will appear double click to run
4. ALTERNATIVELY: run python setup_cx.py bdist_msi
5. THen navigate to dist double click the msi

~~~~~~~~~~~~~~
  Repository
~~~~~~~~~~~~~~
https://github.com/josephmbarron/bluebeam

~~~~~~~~~~~~~~~~~~
 Current Features
~~~~~~~~~~~~~~~~~~

PLAYER CHARACTER CONTROLS:
 - WASD and SPACE for character movement
 - ARROW KEYS for shooting
 - RSHIFT to charge up your charged shot, when unlocked

3 COLLECTABLE POWERUPS:
 - BLUE - unlocks the CHARGED SHOT
 - YELLOW - boosts the player's attack speed for the rest of the level
 - RED - heals the player for 1 heart

4 ENEMIES:
 - Fish enemy, which chases down the player
 - Alien enemy, which shoots at the player and also attemts to run if he gets too close
 - Green alien enemy, which will invert your controls if you get to close. (Kill from a distance)
 - Big alien moves toward you and tries to whip the player with his tentacles

FIRST BOSS:
 - Three-phase boss fight
 - Has lazers, explosives, and cluster bomb attacks
 - Turrets are destructible entities
 - Weak point: blue cores

SECOND BOSS:
 - Three-phase fight against a small-scale rising assault tower
 - Boss can fire projectiles in patterns, launch rockets, charge, call in lasers, and use special accelerating bullets
 - Weak point: blue diamond

FINAL BOSS:
 - Three-phase fight against a large machine
 - Uses one of five random attacks: punching, radial bullets, lasers, background rockets, and wave bombs
 - When starting a new phase, uses a super attack
 - Weak point: blue core, exposed after performing a set amount of attacks 

SECOND BOSS:

THIRD BOSS

TILEMAP:
 - First level is loaded solely from the .tmx file (created in tiled)
 - A tilemap background is implemented, allowing for large maps without a performance penalty

MAIN MENU & PAUSE SCREEN:
 - Main menu and pause screen are implemented almost entirely
 - You can adjust volume
 - You can press help and see basic controls for the game and see what the powerups do

SOUNDS:
 - Game music
 - Audio effects for various in-game events
 - Audio effects for when the player gets damaged
