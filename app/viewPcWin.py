from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget, QTableWidget, QAbstractItemView, QVBoxLayout, QTableWidgetItem
from database import SessionLocal
from services.services import ClubService


class ComputersWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.db = SessionLocal()
        self.initUI()
        self.show()


    def initUI(self):
        self.setWindowTitle("Список компьютеров")
        self.setWindowIcon(QIcon('resources/gg.ico'))
        self.resize(300, 400)
        data_service = ClubService(self.db)
        pcs = data_service.get_all_pc()
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["ID Компьютера", "Компьютер"])
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)

        layout = QVBoxLayout()
        layout.addWidget(self.table)

        self.setLayout(layout)

        self.table.setRowCount(len(pcs))
        for row_idx, pc in enumerate(pcs):
            self.table.setItem(row_idx, 0, QTableWidgetItem(str(pc.pc_id)))
            self.table.setItem(row_idx, 1, QTableWidgetItem(str(pc.pc_name)))

