import os
import sys

import requests
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMainWindow

SCREEN_SIZE = [700, 450]


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.getImage()
        self.initUI()

    def getImage(self):
        current_LL = ('37.530887', '55.70311')
        current_spn = ('0.002', '0.002')
        current_map_type = 'map'
        api_server = "http://static-maps.yandex.ru/1.x/"
        map_params = {
            "ll": ",".join(current_LL),
            "spn": ",".join(current_spn),
            "l": current_map_type
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


    def closeEvent(self, event):
        os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())