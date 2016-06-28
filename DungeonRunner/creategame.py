from allvillains import *
from musics import musics
from screengenerator import screengenerator
import pygame, os

def main():

    protagonist = player(getplayername())

    displaysplash()

    floor = 0
    playing = True
    while playing:

        floor += 1
        screen = s_generator.make_window()
        floorscreen, encounterscreen, controlscreen, sx, sy, floormatrix = initdetail(screen)
        playerpos = [sy, sx]

        m_player.background_play()
        updatecontrolscreen(screen, controlscreen, "Welcome, " + protagonist.name + " !")
        updatecontrolscreen(screen, controlscreen, "Use the minimap to navigate")
        updatecontrolscreen(screen, controlscreen, "to the next floor")
        navigating = True
        while navigating:

            ev = pygame.event.get()
            for event in ev:
                if event.type == pygame.QUIT:
                    playing, navigating = False, False
                    break

                if event.type == pygame.KEYDOWN: # user controlling movement
                    if event.key == pygame.K_w or event.key == pygame.K_a or event.key == pygame.K_s or event.key == pygame.K_d:

                        # move player, and update the screens
                        # if the player reaches the end, navigating will be false
                        floorscreen, coords, playerpos, floormatrix, navigating = moveplayer(pygame.key.name(event.key), floorscreen, playerpos, floormatrix)

                        # update display
                        screen.blit(floorscreen, coords)
                        pygame.display.update()

                        # check for random encounter
                        if encounter():

                            m_player.background_stop()

                            # begin battle
                            protagonist, encounterscreen, screen = battle(floor, protagonist, encounterscreen, screen, controlscreen)

                            # check results
                            if not(protagonist.alive()):
                                playing, navigating = False, False
                                break
                            else:
                                m_player.background_play()
                                screen.blit(updateencounterscreen(encounterscreen, "idle"), (25, 350))
                                pygame.display.update()

                    elif event.key == pygame.K_ESCAPE:
                        playing, navigating = False, False
                        break

        if playing == False:
            m_player.background_stop()
            gameover(screen)
            pygame.time.delay(5000)

# ------------------------------------------------ First/Last  ------------------------------------------------------ #

def getplayername():

    # create display, update display
    name = ""
    window = s_generator.make_window(image="name")
    usertext = s_generator.make_textsurface(60, name, bg=(32, 32, 64), fg=(192, 192, 0))

    window.blit(usertext, (425, 240) )
    whitebar = pygame.Surface((1000, 100))
    whitebar.fill((32, 32, 64))

    pygame.display.update()

    ready = False

    pygame.event.set_allowed(None)
    pygame.event.set_allowed(pygame.KEYDOWN)

    while(not(ready)):

            pygame.event.clear()
            event = pygame.event.wait()
            c = pygame.key.name(event.key)

            if event.key == pygame.K_RETURN:
                ready = True
            elif event.key == pygame.K_BACKSPACE:
                if len(name) >= 2:
                    name = name[0:len(name) - 1]
                else:
                    name = ""
            else:
                if len(c) == 1:
                    if pygame.key.get_mods() & pygame.KMOD_SHIFT or pygame.key.get_mods() & pygame.KMOD_CAPS:
                        name = name + c.upper()
                    else:
                        name = name + c

            #TODO: Old english text mt
            usertext = s_generator.make_textsurface(60, name, bg=(32, 32, 64), fg=(192, 192, 0))
            window.blit(whitebar, (0, 240))
            window.blit(usertext, (425, 240) )
            pygame.display.update()

    return name

def displaysplash():
    welcome = s_generator.make_window(image="splash")
    pygame.display.update()
    pygame.time.delay(7000)

def gameover(screen):

    screen = s_generator.make_window(image="gameover")
    pygame.display.update()

# ------------------------------------------------ Initialization functions ----------------------------------------- #

def initfloor(screen):

    floorplan = [[0 for x in range(60)] for x in range(30)]

    blue = (71, 71, 71)
    blueblock = pygame.Surface((10, 10))
    blueblock.fill(blue)

    red = (198, 226, 255)
    redblock = pygame.Surface((10, 10))
    redblock.fill(red)

    start = (255, 255, 0)
    startblock = pygame.Surface((10, 10))
    startblock.fill(start)

    end = (0, 0, 0)
    endblock = pygame.Surface((10, 10))
    endblock.fill(end)

    win = (255, 255, 255)
    winblock = pygame.Surface((10, 10))
    winblock.fill(win)

    sx, ex = randint(0, 59), randint(0, 59)
    sy, ey = 0, 29

    floorplan[sy][sx] = 2
    floorplan[ey][ex] = 3

    # distance is from 0 -> 29
    # vertdistance = 28
    # so, squares 1->28 need to be filled

    # likewise, horizantal difference is
    # sx - ex
    # if sx - ex < 0, then let left = true,
    # and horizantal difference *= -1

    v_d = 28
    h_d = sx - ex

    if h_d < 0:
        left = False
        h_d *= -1
    else:
        left = True

    previous = [sy, sx]

    while v_d > 0 or h_d > 0:
        if v_d == 0:
            # we only have to go right or left
            while h_d > 0:
                if left:
                    previous[1] -= 1
                    floorplan[previous[0]][previous[1]] = 1
                    h_d -= 1
                else:
                    previous[1] += 1
                    floorplan[previous[0]][previous[1]] = 1
                    h_d -= 1
        elif h_d == 0:
            # we only have to go down
            while v_d > 0:
                # fill down
                previous[0] += 1
                floorplan[previous[0]][previous[1]] = 1
                v_d -= 1
        else:
            # we're still some distance above and left/right
            coinflip = randint(0, 1)
            if coinflip == 0:
                # go down
                # previous is where we're currently at
                # to go down, we need to go to
                # previous[y + 1][x]
                previous[0] += 1
                floorplan[previous[0]][previous[1]] = 1
                v_d -= 1
            else:
                # go left/right
                # previous is where we're currently at
                # to go left/right we need to go to
                # previously[y][x+-1]
                if left:
                    previous[1] -= 1
                    floorplan[previous[0]][previous[1]] = 1
                    h_d -= 1
                else:
                    previous[1] += 1
                    floorplan[previous[0]][previous[1]] = 1
                    h_d -= 1

    for i in range(60):
        for j in range(30):
            if floorplan[j][i] == 0:
                screen.blit(blueblock, (i * 10, j * 10))
            elif floorplan[j][i] == 1:
                screen.blit(redblock, (i * 10, j * 10))
            elif floorplan[j][i] == 2:
                screen.blit(startblock, (i * 10, j * 10))
            elif floorplan[j][i] == 3:
                screen.blit(endblock, (i * 10, j * 10))


    return screen, sy, sx, floorplan

def initdetail(screen):
    floorscreen, sy, sx, floorplan = initfloor(s_generator.make_miniwindow())
    encounterscreen = updateencounterscreen(s_generator.make_miniwindow(), "idle")
    controlscreen = s_generator.make_logwindow()

    screen.blit(floorscreen, (25, 25))
    screen.blit(encounterscreen, (25, 350))
    screen.blit(controlscreen, (650, 25))

    pygame.display.update()

    return floorscreen, encounterscreen, controlscreen, sy, sx, floorplan

# ------------------------------------------------ Encounter functions ---------------------------------------------- #

def getencounterpicture(enemy):
    image = enemy + ".bmp"
    encounterimage = pygame.image.load(os.path.join("images", image)).convert_alpha()
    return encounterimage

def encounteralert(screen, subscreen):

    subscreen = updateencounterscreen(subscreen, "enc")
    screen.blit(subscreen, (25, 350))
    pygame.display.update()
    pygame.time.delay(1000)

    for i in range(7):
        black = (0, 0, 0)
        subscreen.fill(black)
        screen.blit(subscreen, (25, 350))
        pygame.display.update()
        pygame.time.delay(125)

        white = (255, 255, 255)
        subscreen.fill(white)
        screen.blit(subscreen, (25, 350))
        pygame.display.update()
        pygame.time.delay(125)

def encounter():
    if randint(1, 20) == 5:
        return True
    else:
        return False

def updateencounterscreen(subscreen, enemytype):
    battleimage = getencounterpicture(enemytype)
    subscreen.blit(battleimage, (0, 0))
    return subscreen

def fight(player1, enemy, screen, controlscreen):
    # returns the player after the engagement
    # player first, then enemy
    # perform action, check if dead, move forward
    # if either are dead, exit
    # change input to only accept one input at a time at the beginning of a player's turn
    # this is done by completely clearing the queue before the player action
    # then setting the queue to take a single command off of the queue

    # testing pygame.event.wait
    # the idea, once the fight starts, only allow keypresses, and wait for single key inputs

    fighting = True
    playerturn = True

    #added - first allow none, then add keydown to list of allowed
    pygame.event.set_allowed(None)
    pygame.event.set_allowed(pygame.KEYDOWN)
    pygame.event.clear()
    while fighting:

        while playerturn and fighting:

            # clear queue right before player turn to allow for one single command
            pygame.event.clear()
            event = pygame.event.wait()

            if event.type == pygame.KEYDOWN and (event.key == pygame.K_a or event.key == pygame.K_h or event.key == pygame.K_k):
                # user pressed attack or heal
                if event.key == pygame.K_a:
                    a = player1.attack()
                    updatecontrolscreen(screen, controlscreen, player1.name + " attacks!")
                    updatecontrolscreen(screen, controlscreen,enemy.defend(a))
                    m_player.s_play()
                    if not(enemy.alive()):
                        fighting = False
                        updatecontrolscreen(screen, controlscreen, "foe slain. player leveled up!")
                        player1.levelup()
                    else:
                        playerturn = not(playerturn)
                        updatecontrolscreen(screen, controlscreen, enemy.type() + " hp: " + str(enemy.hitpoints))

                elif event.key == pygame.K_h:
                    updatecontrolscreen(screen, controlscreen, player1.heal())
                    playerturn = not(playerturn)

                else:
                    player1.defend(99999)
                    fighting = False

        if fighting:
            updatecontrolscreen(screen, controlscreen, "-----------------------")

        while not(playerturn) and fighting:
            pygame.time.delay(1500)
            attackchoice = randint(0, 10)
            if attackchoice < 2:
                a = enemy.specialattack()
                updatecontrolscreen(screen, controlscreen, enemy.type() + " critical hit!")
                updatecontrolscreen(screen, controlscreen, player1.defend(a))
                m_player.s_play()
            else:
                a = enemy.attack()
                updatecontrolscreen(screen, controlscreen, enemy.type() + " attacks!")
                updatecontrolscreen(screen, controlscreen, player1.defend(a))
                m_player.s_play()
            updatecontrolscreen(screen, controlscreen, player1.name + " hp: " + str(player1.hitpoints))

            if not(player1.alive()):
                fighting = False
                #TODO: dead
            else:
                playerturn = not(playerturn)

        updatecontrolscreen(screen, controlscreen, "-----------------------")

    # go back to allowing all commands


    return player1

def battle(floor, player1, subscreen, screen, controlscreen):

    m_player.b_start()
    encounteralert(screen, subscreen)
    updatecontrolscreen(screen, controlscreen, "Get ready to fight!")
    updatecontrolscreen(screen, controlscreen, "---------------------------------------")

    # enemy is based on the floor that the player is on
    if floor == 1:
        enemy = pixie(randint(1, player1.level+1))
    elif floor > 1 and floor < 4:
        enemy = lizardman(randint(player1.level-1, player1.level))
    elif floor > 4:
        enemy = golem(randint(player1.level-2, player1.level))

    updatecontrolscreen(screen, controlscreen, "A " + enemy.type() + " approaches!")
    updatecontrolscreen(screen, controlscreen, enemy.type() + " hp: " + str(enemy.hitpoints))
    updatecontrolscreen(screen, controlscreen, enemy.type() + " level: " + str(enemy.level))

    updatecontrolscreen(screen, controlscreen, "---------------------------------------")
    updatecontrolscreen(screen, controlscreen, player1.name + " hp: " + str(player1.hitpoints))
    updatecontrolscreen(screen, controlscreen, player1.name + " level: " + str(player1.level))

    updatecontrolscreen(screen, controlscreen, "---------------------------------------")
    updatecontrolscreen(screen, controlscreen, "Good luck!")

    # update encounter screen based on enemy type
    subscreen = updateencounterscreen(subscreen, enemy.type())
    screen.blit(subscreen, (25, 350))
    pygame.display.update()

    # begin battle!
    player1 = fight(player1, enemy, screen, controlscreen)

    # battle over. are we still alive?
    m_player.b_stop()
    if player1.alive():
        m_player.v_play()
        subscreen = updateencounterscreen(subscreen, "victory")
        updatecontrolscreen(screen, controlscreen, "---------------------------------------")
        updatecontrolscreen(screen, controlscreen, player1.name + " hp: " + str(player1.hitpoints))
        updatecontrolscreen(screen, controlscreen, player1.name + " level: " + str(player1.level))
        updatecontrolscreen(screen, controlscreen, "---------------------------------------")


    # update with new subscreen
    screen.blit(subscreen, (25, 350))
    pygame.display.update()

    return player1, subscreen, screen

# ------------------------------------------------ Floor update functions ------------------------------------------- #

def updatefloor(screen, floorplan):
    blue = (71, 71, 71)
    blueblock = pygame.Surface((10, 10))
    blueblock.fill(blue)

    red = (198, 226, 255)
    redblock = pygame.Surface((10, 10))
    redblock.fill(red)

    start = (255, 255, 0)
    startblock = pygame.Surface((10, 10))
    startblock.fill(start)

    end = (0, 0, 0)
    endblock = pygame.Surface((10, 10))
    endblock.fill(end)

    win = (255, 255, 255)
    winblock = pygame.Surface((10, 10))
    winblock.fill(win)

    playeratend = False

    for i in range(60):
        for j in range(30):
            if floorplan[j][i] == 0:
                screen.blit(blueblock, (i * 10, j * 10))
            elif floorplan[j][i] == 1:
                screen.blit(redblock, (i * 10, j * 10))
            elif floorplan[j][i] == 2:
                screen.blit(startblock, (i * 10, j * 10))
            elif floorplan[j][i] == 3:
                screen.blit(endblock, (i * 10, j * 10))
            elif floorplan[j][i] == 5:
                screen.blit(winblock, (i * 10, j * 10))
                playeratend = True

    return screen, playeratend

def moveisallowable(floormatrix, playerpos, ch):
    # if I want to go down, then playerpos[1] + 1 == 1
    # if I want to go up, then playerpos[1] - 1 == 1
    # if I want to go left, then playerpos[0] - 1 == 1
    # if I want to go right, then playerpos[0] + 1 == 1
    if ch == "s":
        # down
        if floormatrix[playerpos[1] + 1][playerpos[0]] > 0:
            return True
        else:
            return False
    elif ch == "a":
        # left
        if floormatrix[playerpos[1]][playerpos[0] - 1 ] > 0:
            return True
        else:
            return False
    elif ch == "d":
        # right
        if floormatrix[playerpos[1]][playerpos[0] + 1] > 0:
            return True
        else:
            return False
    elif ch == "w":
        # up
        if floormatrix[playerpos[1] - 1][playerpos[0]] > 0:
            return True
        else:
            return False

def updatefloormatrix(floormatrix, playerpos, ch):

    if moveisallowable(floormatrix, playerpos, ch) == True:
        if ch == "s":
            # down
            floormatrix[playerpos[1]][playerpos[0]] = 1
            playerpos[1] += 1
        elif ch == "a":
            # left
            floormatrix[playerpos[1]][playerpos[0]] = 1
            playerpos[0] -= 1
        elif ch == "d":
            # right
            floormatrix[playerpos[1]][playerpos[0]] = 1
            playerpos[0] += 1
        elif ch == "w":
            # up
            floormatrix[playerpos[1]][playerpos[0]] = 1
            playerpos[1] -= 1

        if floormatrix[playerpos[1]][playerpos[0]] == 3:
            # we've just moved into the end block. time to generate a new floor
            floormatrix[playerpos[1]][playerpos[0]] = 5
        else:
            # we've just moved into any other valid space
            floormatrix[playerpos[1]][playerpos[0]] = 2

    return floormatrix, playerpos

def moveplayer(ch, floorscreen, playerpos, floormatrix):
    floormatrix, playerpos = updatefloormatrix(floormatrix, playerpos, ch)
    floorscreen, playeratend = updatefloor(floorscreen, floormatrix)
    print(str(playerpos))
    return [floorscreen, (25, 25), playerpos, floormatrix, not(playeratend)]

# ------------------------------------------------ status/logs functions -------------------------------------------- #

def updatecontrolscreen(screen, subscreen, message):

    # create font surface with message
    textline = s_generator.make_textsurface(message=message, stdfont=True)

    # blackbar is used to simulate messages disappearing as they go up
    blackbar = pygame.Surface((325, 25))
    blackbar.fill((0, 0, 0))

    # rectangle gets everything from the text field but the top 25 pixels
    textarea = pygame.Rect(650, 50, 325, 600)
    textsurface = screen.subsurface(textarea)
    temp = textsurface.copy()

    # then, add new line of text to bottom 25 pixels, and paste old text above
    subscreen.blit(blackbar, (0, 605))
    subscreen.blit(textline, (0, 605))
    subscreen.blit(temp, (0, 0))

    screen.blit(subscreen, (650, 25))

    pygame.display.update()

# ------------------------------------------------ END functions ---------------------------------------------------- #

if __name__ == "__main__":
    m_player = musics() # global singleton for music control at all times
    s_generator = screengenerator() # global singleton for surface generation
    pygame.init()
    main()
