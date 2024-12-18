from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QTableWidget, QTableWidgetItem, \
    QMessageBox, QHBoxLayout
from PyQt6.QtGui import QIcon

from app.addDataWin import AddDataWin
from database import SessionLocal, init_db
from services.services import ClubService

class ViewDataWin(QWidget):
    def __init__(self):
        super().__init__()
        self.db = SessionLocal()
        self.initUI()
        self.load_data()

    def initUI(self):
        self.setWindowTitle("База Данных")
        self.setWindowIcon(QIcon('resources/gg.ico'))
        self.setGeometry(100, 100, 1000, 500)
        self.table = QTableWidget()
        self.back_button = QPushButton("Выйти")
        self.del_entry = QPushButton("Удалить")
        self.edit_entry = QPushButton("Изменить")
        main_l = QVBoxLayout()
        h_l1 = QHBoxLayout()
        main_l.addWidget(self.table)
        h_l1.addWidget(self.edit_entry)
        h_l1.addWidget(self.del_entry)
        h_l1.addWidget(self.back_button)
        main_l.addLayout(h_l1)
        self.setLayout(main_l)
        self.back_button.clicked.connect(self.back)
        self.edit_entry.clicked.connect(self.edit_order)
        self.del_entry.clicked.connect(self.delete_order)

    def load_data(self):
        data_service = ClubService(self.db)
        users = data_service.get_all_users()

        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['ID Пользователя', 'Имя Фамилия', 'ПК', 'Время'])
        self.table.setRowCount(len(users))
        for row_idx, user in enumerate(users):
            self.table.setItem(row_idx, 0, QTableWidgetItem(str(user.user_id)))
            self.table.setItem(row_idx, 1, QTableWidgetItem(str(user.user_name_surname)))
            self.table.setItem(row_idx, 2, QTableWidgetItem(str(user.pc_name)))
            self.table.setItem(row_idx, 3, QTableWidgetItem(str(user.user_time)))



    def delete_order(self):
        if self.table.selectedItems():
            selected_row = self.table.currentRow()
            user_id = int(self.table.item(selected_row, 0).text())
            confirmation_dialog = QMessageBox()

            confirmation_dialog.setWindowTitle("Подтверждение удаления")
            confirmation_dialog.setText(
                f"Вы уверены, что хотите удалить пользователя с ID: "
                f"{self.table.item(self.table.currentRow(), 0).text()}?")
            confirmation_dialog.setIcon(QMessageBox.Icon.Warning)
            confirmation_dialog.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            confirmation_dialog.setDefaultButton(QMessageBox.StandardButton.No)
            user_response = confirmation_dialog.exec()
            if user_response == QMessageBox.StandardButton.Yes:
                db = SessionLocal()
                init_db()
                user_servise = ClubService(db)
                user_servise.delete_user(user_id)
                self.table.removeRow(selected_row)
                QMessageBox.information(self, "Информация", "Пользователь удален успешно!")
            else:
                QMessageBox.information(self, "Информация", "Отмена удаления")


    def back(self):
        self.close()

    def edit_order(self):
        self.win_edit = AddDataWin(
            [self.table.item(self.table.selectedItems()[0].row(),
                             col).text() for col in range(self.table.columnCount())]
        )
        self.win_edit.show()

