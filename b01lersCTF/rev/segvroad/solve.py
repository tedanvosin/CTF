from enum import Enum
from pwn import *


# Constants
class shift(Enum):
    RIGHT_SHIFT = 0x1
    FILL_ROW = 0x2
    LEFT_SHIFT = 0x0


# Global vars
level = 0
magic_no = 0x13523
shift_array: list[int] = [0 for _ in range(10)]
map: list[list[int]] = [[0 for _ in range(10)] for _ in range(10)]
move_count: int = 0
coordinates: list[int, int] = [0, 0]


def initialize_row1(y: int, userid: int) -> int:
    random_number: int = 0
    x_mod_3: int = y % 3

    if x_mod_3:
        if x_mod_3 == 1:
            random_number = ((userid + level + y) * magic_no) & 0x3FF ^ 0xFFFFFDDD
        else:
            random_number = 0x288
    else:
        random_number = ((userid + level + y) * magic_no) & 0x3FF ^ 0x2AA

    for x in range(0, 10):
        map[y][x] = (random_number >> x) & 1

    shift_array[y] = 1
    return y


def initialize_row2(x: int, userid: int) -> int:
    random_number: int = 0
    x_mod_3: int = x % 3

    if x_mod_3:
        if x_mod_3 == 1:
            random_number = ~(((userid + level + x) * magic_no) & 0x3FF)
        else:
            random_number = 0xFFFFFFCF
    else:
        random_number = ((userid + level + x) * magic_no) & 0x3FF

    for y in range(0, 10):
        map[x][y] = (random_number >> y) & 1

    shift_array[x] = 0
    return x


def fill_row(idx: int) -> None:
    shift_array[idx] = shift.FILL_ROW.value

    return idx


def initialize_map(userid: int) -> int:
    idx: int = 0
    y: int = 1
    rand: int = 0

    shift_array[0] = 3
    shift_array[-1] = 3

    while y:
        idx = y

        if y > 8:
            break

        rand = (((userid + level + y) * magic_no) >> (2 * y)) & 3

        if rand == 2:
            initialize_row1(y, userid)
            y += 1
            continue
        elif rand == 3:
            fill_row(y)
        else:
            if rand or y > 0 and not shift_array[y - 1]:
                initialize_row1(y, userid)
                y += 1
                continue

            initialize_row2(y, userid)

        y += 1

    return idx


def right_shift_row(y: int) -> list[int]:
    tmp: int = map[y][-1]

    for x in range(9, 0, -1):
        map[y][x] = map[y][x - 1]

    map[y][0] = tmp
    return map[y]


def left_shift_row(y: int) -> int:
    tmp: int = map[y][0]

    for x in range(0, 9):
        map[y][x] = map[y][x + 1]

    map[y][9] = tmp
    return map[y]


def maze_shift() -> None:
    for y in range(0, 10):
        if shift_array[y] != 1 or (y & 1) != 0:
            if shift_array[y] == shift.RIGHT_SHIFT.value:
                right_shift_row(y)
            elif shift_array[y] == shift.FILL_ROW.value and move_count % 7 == 3:
                for i in range(0, 10):
                    map[y][i] = 1
            elif shift_array[y] == shift.FILL_ROW.value:
                for x in range(0, 10):
                    map[y][x] = 0
        else:
            left_shift_row(y)


def print_map(map, player=False):
    print("+" * 12)
    for ya in range(10):
        print("+", end="")
        for xa in range(10):
            if player and xa == coordinates[0] and ya == coordinates[1]:
                print("@", end="")
                continue
            if map[ya][xa] == 0:
                print(" ", end="")
            else:
                print("#", end="")
        print("+")
    print("+" * 12)


def move(direction):
    if direction == "w" and coordinates[1] > 0:
        coordinates[1] -= 1
    elif direction == "s" and coordinates[1] < 9:
        coordinates[1] += 1
    elif direction == "a" and coordinates[0] > 0:
        coordinates[0] -= 1
    elif direction == "d" and coordinates[0] < 9:
        coordinates[0] += 1


def reset(userid: int) -> int:
    global map, level, coordinates

    level += 1
    map = [[0 for _ in range(10)] for _ in range(10)]
    coordinates = [0, 0]
    return initialize_map(userid)


if __name__ == "__main__":
    p = remote("segvroad.atreides.b01lersc.tf", 8443, ssl=True)
    p.recvuntil(b"userid: ")
    userid: int = int(p.recvline().strip())
    print(f"userid: {userid}")
    initialize_map(userid)
    while 1:
        print("Current Maze:")
        print_map(map, player=True)
        print(
            "x: %d | y: %d | block: %d"
            % (coordinates[0], coordinates[1], (move_count + 1) % 7 == 3)
        )
        maze_shift()
        print("Next Maze:")
        print_map(map, player=True)

        direction = input("> ")
        move_count += 1
        move(direction)

        if direction == "w":
            direction = "s"
        if direction == "s":
            direction = "w"
        p.sendlineafter(b"> ", direction.encode())

        if map[coordinates[1]][coordinates[0]] == 1:
            print("You hit a wall!")
            p.interactive()
            exit(1)

        if coordinates[1] == 9 and coordinates[0] == 9:
            line = p.recvline().strip()
            if b"Leveled up" in line:
                print('Levelled UP!!!')
                reset(userid)
                
    p.interactive()
