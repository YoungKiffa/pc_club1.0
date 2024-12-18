from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QComboBox, QLineEdit, QMessageBox, QLabel

from app.viewPcWin import ComputersWindow
from database import SessionLocal
from services.services import ClubService

class AddDataWin(QWidget):
    def __init__(self, data=None):
        super().__init__()
        self.data = data
        self.db = SessionLocal()
        self.initUI()
        if data:
            self.upload_editable_data()
        self.show()

    def initUI(self):
        self.setWindowIcon(QIcon('resources/gg.ico'))
        self.setWindowTitle("Добавить нового пользователя")
        self.setGeometry(100, 100, 400, 300)

        self.name_surname_label = QLabel("Имя Фамилия:")
        self.name_surname_input = QLineEdit()


        self.id_pc_label = QLabel("Компьютер:")
        self.id_pc_input = QComboBox()
        self.load_id_pc()

        self.time_label = QLabel("Время:")
        self.time_input = QLineEdit()

        self.info = QPushButton("Список компьютеров")
        self.add_button = QPushButton("Добавить пользователя")
        self.cls_1 = QPushButton("Выйти")

        self.info.clicked.connect(self.info_pc)
        self.add_button.clicked.connect(self.add_user)
        self.cls_1.clicked.connect(self.close)

        layout = QVBoxLayout()
        layout.addWidget(self.name_surname_label)
        layout.addWidget(self.name_surname_input)
        layout.addWidget(self.id_pc_label)
        layout.addWidget(self.id_pc_input)
        layout.addWidget(self.time_label)
        layout.addWidget(self.time_input)
        layout.addWidget(self.info)
        layout.addWidget(self.add_button)
        layout.addWidget(self.cls_1)
        self.setLayout(layout)

    def info_pc(self):
        self.win_add = ComputersWindow()
        self.win_add.show()

    def load_id_pc(self):
        pc_types = ClubService(db=self.db).get_all_pc()
        self.id_pc_input.addItems([str(Pcs.pc_id) for Pcs in pc_types])

    def upload_editable_data(self):
        self.user_id = int(self.data[0])
        self.name_surname_input.setText(self.data[1])
        self.id_pc_input.setCurrentText(self.data[2])
        self.time_input.setText(self.data[3])


    def add_user(self):
        if self.data is None:
            ClubService(db=self.db).add_user(self.name_surname_input.text(),
                                             self.id_pc_input.currentText(),
                                             self.time_input.text()
                                             )
            print(ClubService(db=self.db).get_all_users())
            QMessageBox.information(self, "Информация", "Пользователь добавлен успешно!")
            self.close()
        else:
            ClubService(db=self.db).update_data(self.user_id,
                                                self.name_surname_input.text(),
                                                self.id_pc_input.currentText(),
                                                self.time_input.text())

            QMessageBox.information(self, "Информация", "Пользователь изменен успешно!")
            self.close()
