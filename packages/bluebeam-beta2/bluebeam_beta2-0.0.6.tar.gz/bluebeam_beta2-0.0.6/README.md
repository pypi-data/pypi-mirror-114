# bluebeam 
~~~~~~~~~~~~~~
   The Game
~~~~~~~~~~~~~~
    Bluebeam is a run and gun exploratory sidescroller inspired by retro-games such as Contra. 
It is implemented using primarily python and pygame.

~~~~~~~~~~~~~~
 Installation
~~~~~~~~~~~~~~
1. Download the associated .tar.gz library
2. Open up the top-level directory in terminal
3. Run the shell command "cd bluebeam"
4. Run the file "Engine.py" with python. EG: "py Engine.py" or "python3 Engine.py"

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

2 ENEMIES:
 - Fish enemy, which chases down the player
 - Alien enemy, which shoots at the player and also attemts to run if he gets too close

FIRST BOSS:
 - Three-phase boss fight
 - Has lazers, explosives, and cluster bomb attacks

TILEMAP:
 - First level is loaded solely from the .tmx file (created in tiled)
 - A tilemap background is implemented, allowing for large maps without a performance penalty

MAIN MENU & PAUSE SCREEN:
 - Main menu and pause screen are implemented almost entirely
 - The only missing menu is a "options" setting, which will contain parameters to adjust sound

SOUNDS:
 - Game music
 - Audio effects for various in-game events
 - Audio effects for when the player gets damaged

~~~~~~~~~~~~~~~~~~
   Future Goals
~~~~~~~~~~~~~~~~~~
1. An additional 1-2 levels, depending on how much time we have
2. An additional 2-4 enemies
3. An additional 1-2 bosses
4. Performance improvements using a "chunking" system for collision checking
5. More haptic feedback for when the player gets damaged
6. An additional 1-2 powerup types for the player
7. A victory screen, along with a level select system
8. A options menu including sound settings