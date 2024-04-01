import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QListView, QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt

class AddressBook(QWidget):
    def __init__(self):
        super().__init__()
        self.contacts = {}  # 주소록을 딕셔너리로 관리합니다.
        self.init_ui()
        self.load_from_file()

    def init_ui(self):
        self.setWindowTitle('주소록 프로그램')

        self.name_label = QLabel('이름:')
        self.name_input = QLineEdit()
        self.phone_label = QLabel('전화번호:')
        self.phone_input = QLineEdit()

        self.add_button = QPushButton('추가')
        self.add_button.clicked.connect(self.add_contact)

        self.contact_list = QListView()
        self.model = QStandardItemModel()
        self.contact_list.setModel(self.model)

        layout = QVBoxLayout()
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)
        layout.addWidget(self.phone_label)
        layout.addWidget(self.phone_input)
        layout.addWidget(self.add_button)
        layout.addWidget(self.contact_list)

        self.setLayout(layout)

    def add_contact(self):
        name = self.name_input.text()
        phone = self.phone_input.text()

        if name and phone:
            self.contacts[name] = phone
            self.update_contact_list()
        else:
            QMessageBox.warning(self, '입력 오류', '이름과 전화번호를 모두 입력해주세요.', QMessageBox.Ok)

    def update_contact_list(self):
        self.model.clear()
        for name, phone in self.contacts.items():
            item = QStandardItem(f'{name}: {phone}')
            self.model.appendRow(item)

    def load_from_file(self):
        filename = 'address_book.txt'
        if filename:
            self.contacts.clear()
            with open(filename, 'r') as file:
                for line in file:
                    try:
                        name, phone = line.strip().split(',', 1)
                        self.contacts[name] = phone
                    except ValueError:
                        continue
        self.update_contact_list()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AddressBook()
    window.show()
    sys.exit(app.exec_())
