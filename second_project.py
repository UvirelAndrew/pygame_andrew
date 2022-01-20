from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import pygame
from random import *
import sys
import os.path
import math

black = (0, 0, 0)
white = (255, 255, 255)
gray_yellow = (255, 196, 155)
beige = (255, 167, 108)
deep_purple = (103, 58, 183)
blue = (33, 150, 243)
light_yellow = (255, 255, 74)
light_red = (255, 57, 57)
red = (255, 0, 0)
light_orange = (255, 133, 51)
pink = (255, 87, 45)
grey = (150, 150, 150)
light_grey = (192, 192, 192)
yellow = (255, 255, 128)
dark_yellow = (204, 204, 0)
orange = (251, 82, 0)
brown = (193, 63, 0)


color_dict = {
    0: light_grey,
    2: white,
    4: gray_yellow,
    8: beige,
    16: light_orange,
    32: pink,
    64: light_red,
    128: light_yellow,
    256: dark_yellow,
    512: orange,
    1024: yellow,
    2048: brown,
    4096: red,
}


def get_color(i):
    if i in color_dict:
        return color_dict[i]
    else:
        return red


points = 0
board_size = 4
matrix = [
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0]
]
last_matrix = []


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('2048.ui', self)
        self.pushButton_rules.clicked.connect(self.open_rules)
        self.pushButton_info.clicked.connect(self.open_info)
        self.pushButton_game.clicked.connect(self.open_game)
        MainWindow.setFixedSize(self, 500, 400)
        self.setWindowIcon(QIcon('icon_menu.png'))

    def open_info(self):
        self.info_window = InfoWindow()
        self.info_window.show()

    def open_rules(self):
        self.rules_window = RulesWindow()
        self.rules_window.show()

    def open_game(self):
        game()


class InfoWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('info.ui', self)
        self.setWindowIcon(QIcon('icon_info.png'))
        InfoWindow.setFixedSize(self, 650, 340)


class RulesWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('rules.ui', self)
        self.setWindowIcon(QIcon('icon_rules.png'))
        RulesWindow.setFixedSize(self, 800, 560)


def game():  # после нажатия кнопки выводим окно игры
    pygame.init()
    surface = pygame.display.set_mode((600, 700), 0, 0)
    pygame.display.set_caption('Игра 2048')
    counts = pygame.font.SysFont('Times New Roman', 32)
    points_t = pygame.font.SysFont('Times New Roman', 30)

    def main(from_loaded=False):
        if not from_loaded:
            random_element()
            random_element()
        print_matrix()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if check_go():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT or event.key == pygame.K_UP \
                                or event.key == pygame.K_DOWN or event.key == pygame.K_RIGHT:
                            rotations = count_of_rotations(event.key)
                            last_matrix.append(list_board())
                            for i in range(0, rotations):
                                rotate()
                            if check_move():
                                move()
                                connection()
                                random_element()
                            for j in range(0, (4 - rotations) % 4):
                                rotate()
                            print_matrix()
                else:
                    game_over()

                if event.type == pygame.KEYDOWN:
                    global board_size
                    global points
                    global matrix

                    if event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL:
                        points = 0
                        surface.fill(white)
                        matrix = [[0 for i in range(0, board_size)] for j in range(0, board_size)]
                        main()
                    elif 50 < event.key < 57 and event.key != 55:
                        board_size = event.key - 48
                        points = 0
                        surface.fill(white)
                        matrix = [[0 for i in range(0, board_size)] for j in range(0, board_size)]
                        main()
                    elif event.key == pygame.K_PAGEUP:
                        save_game()
                    elif event.key == pygame.K_PAGEDOWN:
                        load_game()
                    elif event.key == pygame.K_BACKSPACE:
                        undo()
            pygame.display.update()

    def print_matrix():  # выводим поле
        surface.fill(white)
        global board_size
        global points
        for i in range(0, board_size):
            for j in range(0, board_size):
                pygame.draw.rect(surface, get_color(matrix[i][j]),
                                 (i * (600 / board_size), j * (600 / board_size) + 100, 600 / board_size,
                                  600 / board_size))

                label = counts.render(str(matrix[i][j]), True, black)
                label2 = points_t.render('Очки: ' + str(points), True, black)
                if matrix[i][j] < 10:  # смещение надписи на элементе для визуальной красоты
                    offset = -10
                elif matrix[i][j] < 100:
                    offset = -15
                elif matrix[i][j] < 1000:
                    offset = -20
                else:
                    offset = -25
                if matrix[i][j] > 0:
                    surface.blit(label, (i * (600 / board_size) + (300 / board_size) + offset,
                                         j * (600 / board_size) + 100 + 300 / board_size - 15))
                surface.blit(label2, (10, 10))
        for i in range(board_size + 1):
            pygame.draw.line(surface, grey, (0, i * (600 / board_size) + 100), (600, i * (600 / board_size) + 100),
                             48 // board_size)
            pygame.draw.line(surface, grey, (i * (600 / board_size), 100), (i * (600 / board_size), 700),
                             48 // board_size)
        for i in range(0, board_size):
            for j in range(0, board_size):
                if matrix[i][j] == 2048:
                    label0 = points_t.render('Вы дошли до 2048!', True, black)
                    surface.blit(label0, (10, 50))

    def random_element():  # добавление на поле в случайное место числа 2
        n = math.floor(random() * board_size ** 2)
        while matrix[math.floor(n / board_size)][n % board_size] != 0:
            n = math.floor(random() * board_size * board_size)
        matrix[math.floor(n / board_size)][n % board_size] = 2

    def move():  # движение ячеек вверх
        for i in range(0, board_size):
            for j in range(0, board_size - 1):
                while matrix[i][j] == 0 and sum(matrix[i][j:]) > 0:
                    for n in range(j, board_size - 1):
                        matrix[i][n] = matrix[i][n + 1]
                    matrix[i][board_size - 1] = 0

    def check_go():
        for i in range(0, board_size ** 2):
            if matrix[math.floor(i / board_size)][i % board_size] == 0:
                return True
        for i in range(0, board_size):
            for j in range(0, board_size - 1):
                if matrix[i][j] == matrix[i][j + 1]:
                    return True
                elif matrix[j][i] == matrix[j + 1][i]:
                    return True
        return False

    def check_move():  # можно ли двигать
        for i in range(0, board_size):
            for j in range(1, board_size):
                if matrix[i][j - 1] == 0 and matrix[i][j] > 0:
                    return True
                elif (matrix[i][j - 1] == matrix[i][j]) and matrix[i][j - 1] != 0:
                    return True
        return False

    def connection():  # сложение ячеек
        global points
        for i in range(0, board_size):
            for j in range(0, board_size - 1):
                if matrix[i][j] == matrix[i][j + 1] and matrix[i][j] != 0:
                    matrix[i][j] = matrix[i][j] * 2
                    matrix[i][j + 1] = 0
                    points += matrix[i][j]
                    move()

    def save_game():  # сохранение игры
        f = open('game', 'w')
        elements = ' '.join([str(matrix[math.floor(x / board_size)][x % board_size])
                             for x in range(0, board_size ** 2)])
        f.write(str(board_size) + '\n')
        f.write(elements + '\n')
        f.write(str(points))
        f.close()

    def load_game():  # загрузка игры
        if os.path.isfile('game'):
            global points
            global board_size
            global matrix
            f = open('game', 'r')
            board_size = int(f.readline())
            mat = (f.readline()).split(' ', board_size ** 2)
            points = int(f.readline())
            matrix = [[0 for i in range(0, board_size)] for j in range(0, board_size)]
            for i in range(0, board_size ** 2):
                matrix[math.floor(i / board_size)][i % board_size] = int(mat[i])
            f.close()
            main(True)

    def rotate():  # переход на следующий ход
        global matrix
        matrix = [list(reversed(col)) for col in zip(*matrix)]

    def count_of_rotations(k):  # сколько раз повернуть
        if k == pygame.K_UP:
            return 0
        elif k == pygame.K_RIGHT:
            return 1
        elif k == pygame.K_DOWN:
            return 2
        elif k == pygame.K_LEFT:
            return 3

    def list_board():  # матрица списком
        mat = []
        for i in range(0, board_size ** 2):
            mat.append(matrix[math.floor(i / board_size)][i % board_size])
        mat.append(points)
        return mat

    def game_over():  # выводим экран после окончания игры
        global points
        surface.fill(black)
        label1 = points_t.render('Игра окончена!', True, white)
        label2 = points_t.render('Очки: ' + str(points), True, white)
        label3 = points_t.render('Нажмите клавишу Ctrl', True, white)
        label4 = points_t.render('для перезапуска игры', True, white)
        label5 = points_t.render('Для отмены хода', True, white)
        label6 = points_t.render('нажмите Backspace', True, white)
        surface.blit(label1, (200, 100))
        surface.blit(label2, (250, 300))
        surface.blit(label3, (152, 500))
        surface.blit(label4, (160, 540))
        surface.blit(label5, (182, 370))
        surface.blit(label6, (170, 410))

    def undo():  # отмена хода
        if len(last_matrix) > 0:
            mat = last_matrix.pop()
            for i in range(0, board_size ** 2):
                matrix[math.floor(i / board_size)][i % board_size] = mat[i]
            global points
            points = mat[board_size ** 2]
            print_matrix()

    main()


def except_hook(cls, exception, traceback):  # обрабатываем исключения
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())