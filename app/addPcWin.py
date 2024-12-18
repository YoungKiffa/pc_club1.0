from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLineEdit, QMessageBox, QLabel

from database import SessionLocal
from services.services import ClubService


class AddPcWin(QWidget):
    def __init__(self):
        super().__init__()
        self.db = SessionLocal()
        self.initUI()
        self.show()

    def initUI(self):
        self.setWindowIcon(QIcon('resources/gg.ico'))
        self.setWindowTitle("Добавить новый компьютер")
        self.setGeometry(100, 100, 300, 100)

        self.name_pc_label = QLabel("Имя компьютера:")
        self.name_pc_input = QLineEdit()

        self.add_button = QPushButton("Добавить компьютер")
        self.cls_1 = QPushButton("Выйти")

        self.add_button.clicked.connect(self.add_pc)
        self.cls_1.clicked.connect(self.close)

        layout = QVBoxLayout()
        layout.addWidget(self.name_pc_label)
        layout.addWidget(self.name_pc_input)
        layout.addWidget(self.add_button)
        layout.addWidget(self.cls_1)
        self.setLayout(layout)

    def upload_editable_data(self):
        if self.db:
            self.name_pc_input.setText(self.db[0])

    def add_pc(self):
        ClubService(db=self.db).add_pc(self.name_pc_input.text())
        print(ClubService(db=self.db).get_all_pc())

        QMessageBox.information(self, "Информация", "Компьютер добавлен успешно!")
        self.close()

