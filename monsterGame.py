from IPython.display import clear_output
import random

# this function prints grid and all instances of objects
def makeGrid(rows, cols, monsters, player, egg, door):
    for y in range(rows):
        print(' ---'*cols)
        for x in range(cols):
            monster_created = False
            for monster in monsters:
                if monster.coords == [x, y] and x == cols - 1 and monster_created == False:
                    print('| m |', end='')
                    monster_created = True
                elif monster.coords == [x, y] and monster_created == False:
                    print('| m ', end='')
                    monster_created = True
            if player.coords == [x, y] and x == cols - 1 and monster_created == False:
                print('| p |', end='')
            elif player.coords == [x, y] and monster_created == False:
                print('| p ', end='')
            elif egg.coords == [x, y] and x == cols - 1 and monster_created == False:
                print('| e |', end='')
            elif egg.coords == [x, y] and monster_created == False:
                print('| e ', end='')
            elif door.coords == [x, y] and x == cols - 1 and monster_created == False:
                print('| d |', end='')
            elif door.coords == [x, y] and monster_created == False:
                print('| d ', end='')
            elif x == cols - 1 and monster_created == False:
                print('|   |', end='')
            elif monster_created == False:
                print('|   ', end='')
        print()
        if y == rows - 1:
            print(' ---'*cols)

class Monster():
    def __init__(self, coords):
        self.coords = coords

    def initCoords(self, rows, cols):
        self.coords = [random.randint(0, cols-1), random.randint(0, rows-1)]

    def moveMonster(self, ans, rows, cols):
        if ans == 'up':
            if self.coords[1] + 1 >= rows -1:
                self.coords = [self.coords[0], 0]
            else:
                self.coords = [self.coords[0], self.coords[1] + 2]
        elif ans == 'down':
            if self.coords[1] - 1 <= 0:
                self.coords = [self.coords[0], rows -1]
            else:
                self.coords = [self.coords[0], self.coords[1] - 2]
        elif ans == 'left':
            if self.coords[0] - 1 <= 0:
                self.coords = [cols -1, self.coords[1]]
            else:
                self.coords = [self.coords[0] - 2, self.coords[1]]
        elif ans == 'right':
            if self.coords[0] + 1 >= cols -1:
                self.coords = [0, self.coords[1]]
            else:
                self.coords = [self.coords[0] + 2, self.coords[1]]

class Player():
    def __init__(self, coords, eggs_collected=0):
        self.coords = coords
        self.eggs_collected = eggs_collected

    def initCoords(self, rows, cols, monsters):
        # initialize first coords
        self.coords = [random.randint(0, cols-1), random.randint(0, rows-1)]
        # check and loop until coords are not same as monster
        for monster in monsters:
            while monster.coords == self.coords:
                self.coords = [random.randint(0, cols-1), random.randint(0, rows-1)]

    def movePlayer(self, monsters, rows, cols):
        ans = input('Where would you like to move? ')

        if ans == 'up':
            if self.coords[1] - 1 < 0:
                self.coords = [self.coords[0], rows -1]
            else:
                self.coords = [self.coords[0], self.coords[1] - 1]

        elif ans == 'down':
            if self.coords[1] + 1 > rows - 1:
                self.coords = [self.coords[0], 0]
            else:
                self.coords = [self.coords[0], self.coords[1] + 1]

        elif ans == 'left':
            if self.coords[0] - 1 < 0:
                self.coords = [cols -1, self.coords[1]]
            else:
                self.coords = [self.coords[0] - 1, self.coords[1]]

        elif ans == 'right':
            if self.coords[0] + 1 > cols -1:
                self.coords = [0, self.coords[1]]
            else:
                self.coords = [self.coords[0] + 1, self.coords[1]]
        for monster in monsters:
            monster.moveMonster(ans, rows, cols)


    def checkEgg(self, egg):
        if self.coords == egg.coords:
            self.eggs_collected += 1
            egg.coords = [-1, -1]

class Egg():
    def __init__(self, coords):
        self.coords = coords

    def initCoords(self, rows, cols):
        self.coords = [random.randint(0, cols-1), random.randint(0, rows-1)]

class Door():
    def __init__(self, coords):
        self.coords = coords

    def initCoords(self, rows, cols):
        self.coords = [random.randint(0, cols-1), random.randint(0, rows-1)]

# create a game over function
def game_over(player, monsters, door, num_eggs):
    for monster in monsters:
        if player.coords == monster.coords:
            return 1
    if player.coords == door.coords and num_eggs == player.eggs_collected:
        return 2
    return False

# initialize game over flag
flag = False

level = 0

# main outer initializing loop
while True:
    # size of grid
    rows = 10
    cols = 10
    level += 1

    # objects for game
    monsters = [Monster([0, 0]) for i in range(level)]
    player = Player([1, 1])
    egg = Egg([2, 2])
    door = Door([3, 3])

    # randomly initiating coordinates for start
    for monster in monsters:
        monster.initCoords(rows, cols)
    player.initCoords(rows, cols, monsters)
    egg.initCoords(rows, cols)
    door.initCoords(rows, cols)


    # main game loop
    while True:
        clear_output()
        # show grid
        makeGrid(rows, cols, monsters, player, egg, door)
        # move player and monster
        player.movePlayer(monsters, rows, cols)
#         monster.moveMonster()
        player.checkEgg(egg)

        # check game_over
        flag = game_over(player, monsters, door, 1)

        if flag == 1:
            print('You were eaten by the monster!')
            level -= 1
            break
        elif flag == 2:
            print('Congrats you beat this level!')
            break

    ans = input('Would you like to play again? ')
    if ans == 'no':
        break
