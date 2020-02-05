import random
import sys
import time
from threading import Thread

USAGE = """
#######################################################################
Usage:
 python3 board.py [-help] | [M] [N] | [-p] [path]
Example:\n python3 board.py 70 70
Where is:
 [-help] - print usage
 [M]     - Board hight (M >= 1)
 [N]     - Board width (N >= 1)
 [-p]    - flag for using path instead random generated board
 [path]  - path of 'board' file  (example  python3 board.py -p test.txt)
 Ctrl+C  - exit
########################################################################
"""

class Changes():
    """
    Класс предназначен для отслеживания состояния доски
    есть изменения состояния или нет
    Нужно для выхода из потоков
    """
    def __init__(self):
        self.ch = True

def print_usage(num): 
    print(USAGE)
    if num == 1:
        print("Wrong numbers in args")
    elif num == 2:
        print("Too many arguments")
    elif num == 3:
        print("Error in file")
    elif num == 4:
        print("M and N ")
    exit(1)


def check_massive(mass):
    for i in mass:
        if i > 1 or i < 0:
            return True
    return False


def check_size_mass(mass):
    len_et = len(mass[0])
    for i in mass:
        if len_et != len(i):
            return True
    return False


def generate_board(m, n):
    board = []
    for j in range(m):
            board.append([random.randint(0, 1) for i in range(n)])
    return board, m, n


def create_from_path(path):
    board = []
    try:
        with open(path, "r") as f:
            loop = True
            while loop:
                s = list(map(int, f.readline().split()))
                if check_massive(s):
                    raise Exception
                if s == []:
                    loop = False
                else:
                    board.append(s)
            if check_size_mass(board):
                raise Exception
            return board, len(board), len(board[0])
    except:
        print_usage(3)


def summ_connections(board, y, x, m, n):
    """
    Функция подсчитывает кол-во живых соседей и выходит
    при количестве > 3
    """
    res = 0
    if y > 0 and x > 0:
        res += board[y - 1][x - 1]
    if y > 0:
        res += board[y - 1][x]
    if y > 0 and x < n - 1:
        res += board[y - 1][x + 1]
    if x > 0:
        res += board[y][x - 1]
    if res < 4 and x < n - 1:
        res += board[y][x + 1]
    if res < 4 and y < m - 1 and x > 0:
        res += board[y + 1][x - 1]
    if res < 4 and y < m - 1:
        res += board[y + 1][x]
    if res < 4 and y < m - 1 and x < n - 1:
        res += board[y + 1][x + 1]
    return res


def change_status(summ_conn, status):
    if status == 1:
        if summ_conn == 2 or summ_conn == 3:
            return 1
        else:
            return 0
    else:
        if summ_conn == 3:
            return 1
        else:
            return 0


def check_board(board, m, n):
    changes = False
    for i in range(m):
        for j in range(n):
            summ_conn = summ_connections(board, i, j, m, n)
            prev = board[i][j]
            board[i][j] = change_status(summ_conn, board[i][j])
            if prev != board[i][j]:
                changes = True
    return board, changes


def print_status_cell(board):
    """
    Функция подсчитывает количество живых клеток
    """
    status_cell = [0, 0]
    for i in board:
        for j in i:
            if j == 1:
                status_cell[0] += 1
            else:
                status_cell[1] += 1
    print("Cell alive = {}\nCell died = {}".format(status_cell[0], status_cell[1]))


def print_board(board, cases):
    mass = []
    for j, i in enumerate(board):
        mass.append(i)
        print(*mass[j])
    print_status_cell(mass)
    if cases == 1:
        print("No more changes on board")
    if cases == 2:
        print("Programm ended")


def thread_1(board, m, n, changes):
    """
    Поток-1 постоянно изменяет состояние доски
    """
    while changes.ch:
            board, changes.ch = check_board(board, m, n)
    

def thread_2(board, changes):
    """
    Поток-2 спит 1 секунду, затем выводит доску и кол-во живых клеток
    """
    while changes.ch:
            time.sleep(1)
            print_board(board, 0)
    print_board(board, 1)


def programm(board_size, flag_p, path):
    """
    Основная функция
    Распределение потоков:
        thread1 - изменяет состояние доски(board[])
        thread2 - выводит состояние доски каждую секунду(board[])
    Выход из потоков осуществляет при отсутствии изменений состояний доски
    в ином случае посредством CTRL+C
    """
    if not flag_p:
        board, m, n = generate_board(board_size[0], board_size[1])
    else:
        board, m, n = create_from_path(path)
    status_cell = [0, 0]
    print_board(board, 0)
    changes = Changes()
    thread1 = Thread(target=thread_2, args=(board, changes), daemon=True)
    thread2 = Thread(target=thread_1, args=(board, m, n, changes), daemon=True)
    try:
        thread1.start()
        thread2.start()
        thread1.join()
        thread2.join()
    except KeyboardInterrupt:
        print_board(board, 2)


def check_arg(arg):
    try:
        if int(arg) < 1:
            raise Exception
        for i in arg:
            if not i.isdigit():
                raise Exception
    except:
        print_usage(1)
    return True


def validating():
    """
    Проверка входящих аргументов(кол-во, конфликты флагов)
    """
    board_size = [0, 0]
    count = 0
    flag_p, flag_no_path, count, path = False, False, 0, ""
    if len(sys.argv) < 3:
        print("No arguments")
        exit(1)
    for i in range(1, len(sys.argv)):
        if count > 1:
            print_usage(2)
        elif i == "-help":
            print_usage(0)
        elif sys.argv[i] == "-p":
            if flag_no_path == True:
                print_usage(4)
            elif i + 1 == len(sys.argv) - 1:
                flag_p = True
                path = sys.argv[i + 1]
                break
            else:
                print_usage(0)
        elif check_arg(sys.argv[i]):
            if flag_p == True:
                print_usage(4)
            flag_no_path = True
            board_size[count] = int(sys.argv[i])
            count += 1
        else:
            print_usage(0)
    return board_size, flag_p, path

def main():
    board_size, flag_p, path = validating()
    programm(board_size, flag_p, path)


if __name__ == '__main__':
    main()
