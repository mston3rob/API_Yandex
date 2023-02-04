import os
import sys

import requests
from PyQt5 import uic
from PyQt5.Qt import Qt
from PyQt5.QtGui import QPixmap, QKeyEvent
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMainWindow

SCREEN_SIZE = [700, 450]

# self.keyReleaseEvent(QKeyEvent *event)

class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.getImage()
        self.initUI()

    def getImage(self, ll=()):
        if ll:
            self.current_LL = ll
        else:
            self.current_LL = ('37.530887', '55.70311')
        self.current_spn = ('0.002', '0.002')
        self.current_map_type = 'map'
        api_server = "http://static-maps.yandex.ru/1.x/"
        map_params = {
            "ll": ",".join(self.current_LL),
            "spn": ",".join(self.current_spn),
            "l": self.current_map_type
        }
        map_request = f"http://static-maps.yandex.ru/1.x/?ll={map_params['ll']}&spn={map_params['spn']}&l={map_params['l']}"
        response = requests.get(api_server, params=map_params)

        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        # Запишем полученное изображение в файл.
        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

    def initUI(self):
        super().__init__()
        uic.loadUi('map.ui', self)
        self.setWindowTitle('Отображение карты')

        # Изображение
        self.pixmap = QPixmap(self.map_file)
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(600, 450)
        self.image.setPixmap(self.pixmap)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Up:
            self.map_move('up')
        elif event.key() == Qt.Key_Down:
            self.map_move('down')
        elif event.key() == Qt.Key_Left:
            self.map_move('left')
        elif event.key() == Qt.Key_Right:
            self.map_move('right')

    def map_move(self, move):
        current_change = 1
        current_delta = None
        if move == 'up':
            current_delta = (0, 1)
        new_LL = (str(float(self.current_LL[0]) + float(current_delta[0])), str(float(self.current_LL[1]) + float(current_delta[1])))
        print(new_LL)
        self.image.setPixmap(QPixmap(self.map_file))

    def closeEvent(self, event):
        os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())