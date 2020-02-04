import random
import sys
import time

def print_usage():
    print("################################################")
    print("Usage:")
    print(" python3 board.py [-help] | [M] [N] | [-p] [path]")
    print("Example:\n python3 board.py 70 70")
    print("Where is:")
    print(" [-help] - print usage")
    print(" [M]     - Board hight (M >= 1)")
    print(" [N]     - Board width (N >= 1)")
    print(" [-p]    - flag for using path instead random generated board")
    print(" [path]  - path of 'board' file  (example  python3 board.py -p test.txt)")
    print(" Ctrl+C  - exit")
    print("################################################")
    exit()


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

def generate_board(m, n, flag_p, path):
    '''
    Функция либо генерирует доску(board[M]][N]) и заполняет рандомно 0-ем или 1-ей,
    либо считывает из файла и помещает в массив board.
    Также проводится проверка валидности файла
    '''
    board = []
    if flag_p == True:
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
            print_usage()
    else:
        for j in range(m):
            board.append([random.randint(0, 1) for i in range(n)])
        return board, m, n
    

def summ_connections(board, y, x, m, n):
    '''
    y и x настоящее положение клетки
    m и n размеры доски
    функция провераяет сколько соседей живых,
    если он станет равным 4 можно выходить из функции(следует из задания)
    '''
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
    '''
    Обновляем статус каждой клетки на борде
    Если изменений состояния(changes) на доске не произошло,
    то выводится последнее состояние, программа завершается.
    '''
    changes = False
    status_cell = [0, 0]

    for i in range(m):
        for j in range(n):
            summ_conn = summ_connections(board, i, j, m, n)
            prev = board[i][j]
            board[i][j] = change_status(summ_conn, board[i][j])
            if prev != board[i][j]:
                changes = True
            if board[i][j] == 1:
                status_cell[0] += 1
            else:
                status_cell[1] += 1
    return board, changes, status_cell


def print_board(board, cases, status_cell):
    for i in board:
        print(*i)
    if cases == 1:
        print("\n")
    elif cases == 2:
        print("Cell alive = {}\nCell died = {}".format(status_cell[0], status_cell[1]))
    elif cases == 3:
        print("No more changes on board")


def programm(board_size, flag_p, path):
    '''
    Функция отвечает за состояние доски и вывод ее в консоль каждую секунду.
    В случае, когда изменений нет, завершается программа.
    '''
    m = board_size[0]
    n = board_size[1]
    board, m, n = generate_board(m, n, flag_p, path)
    changes = True
    print_board(board, 1, None)
    check_time = time.time()
    key = 0
    try:
        while changes:
            board, changes, status_cell = check_board(board, m, n)
            if time.time() - check_time >= 1:
                check_time = time.time()
                print_board(board, 2, status_cell)     
    except KeyboardInterrupt:
        print_board(board, 0, None)
        exit()
    print_board(board, 3, None)   


def check_arg(arg):
    '''
    Проверка, что в аргументе только число
    Пример: 
    python3 board.py 10 20s  - вызовет Usage
    '''
    try:
        for i in arg:
            if not i.isdigit():
                raise Exception
            if int(arg) <= 1:
                raise Exception
    except:
        print_usage()
    return True


def main():
    '''
    Проверка аргументов sys.args
    От этого зависит нужно генерировать доску или считывать из файла
    Так же если даны M и N и включен флаг -p, вызывается ошибка(Usage в консоль)
    Пример:
    python3 board.py 10 20 ./Desctop/example.txt
    '''
    board_size = [0, 0]
    count = 0
    flag_p = False
    flag_no_path = False
    path = ""
    for i in range(1, len(sys.argv)):
        if count > 1:
            print_usage()
        elif i == "-help":
            print_usage()
        elif sys.argv[i] == "-p":
            if flag_no_path == True:
                print_usage()
            elif i + 1 == len(sys.argv) - 1:
                flag_p = True
                path = sys.argv[i + 1]
                break
            else:
                print_usage()
        elif check_arg(sys.argv[i]):
            if flag_p == True:
                print_usage()
            flag_no_path = True
            board_size[count] = int(sys.argv[i])
            count += 1
        else:
            print_usage()
    programm(board_size, flag_p, path)

if __name__ == '__main__':
    main()
    