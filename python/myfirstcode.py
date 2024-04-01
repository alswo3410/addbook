import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QGridLayout, QListWidget, QMessageBox
from PyQt5.QtGui import QIcon
import os

class AddressBookApp(QWidget):
    def __init__(self):
        super().__init__()

        self.address_book = {}
        self.filtered_address_book = {}
        self.file_path = os.path.join(os.path.expanduser("~"), "address_book.txt")

        if not os.path.exists(self.file_path):
            with open(self.file_path, "w"):
                pass

        self.init_ui()

    def init_ui(self):
        self.name_label = QLabel("이름:")
        self.name_entry = QLineEdit()

        self.phone_label = QLabel("전화번호:")
        self.phone_entry = QLineEdit()

        self.add_button = QPushButton(QIcon("add.png"), "추가")
        self.delete_button = QPushButton(QIcon("delete.png"), "삭제")
        self.save_button = QPushButton(QIcon("save.png"), "저장")
        self.load_button = QPushButton(QIcon("load.png"), "불러오기")

        self.search_label = QLabel("검색:")
        self.search_entry = QLineEdit()

        self.contact_list_label = QLabel("저장된 주소:")
        self.contact_list = QListWidget()

        grid_layout = QGridLayout()
        grid_layout.addWidget(self.name_label, 0, 0)
        grid_layout.addWidget(self.name_entry, 0, 1)
        grid_layout.addWidget(self.phone_label, 1, 0)
        grid_layout.addWidget(self.phone_entry, 1, 1)
        grid_layout.addWidget(self.add_button, 2, 0)
        grid_layout.addWidget(self.delete_button, 2, 1)
        grid_layout.addWidget(self.save_button, 3, 0)
        grid_layout.addWidget(self.load_button, 3, 1)
        grid_layout.addWidget(self.search_label, 4, 0)
        grid_layout.addWidget(self.search_entry, 4, 1)

        main_layout = QVBoxLayout()
        main_layout.addLayout(grid_layout)
        main_layout.addWidget(self.contact_list_label)
        main_layout.addWidget(self.contact_list)

        self.setLayout(main_layout)

        self.add_button.clicked.connect(self.add_contact)
        self.delete_button.clicked.connect(self.delete_contact)
        self.save_button.clicked.connect(self.save_address_book)
        self.load_button.clicked.connect(self.load_address_book)
        self.search_entry.textChanged.connect(self.search_contacts)

        self.setGeometry(100, 100, 500, 400)
        self.setWindowTitle('주소록')
        self.show()

    def add_contact(self):
        name = self.name_entry.text()
        phone = self.phone_entry.text()

        if name and phone:
            self.address_book[name] = {"phone": phone}
            self.contact_list.addItem(f"{name}: {phone}")
            self.name_entry.clear()
            self.phone_entry.clear()
        else:
            self.show_warning("경고", "이름과 전화번호를 모두 입력하세요.")

    def delete_contact(self):
        selected_item = self.contact_list.currentItem()

        if selected_item:
            name = selected_item.text().split(":")[0]
            del self.address_book[name]
            self.contact_list.takeItem(self.contact_list.row(selected_item))
        else:
            self.show_warning("경고", "삭제할 연락처를 선택하세요.")

    def save_address_book(self):
        try:
            with open(self.file_path, "w") as file:
                for name, data in self.address_book.items():
                    file.write(f"{name}:{data['phone']}\n")

            self.show_info("저장 완료", "주소록이 성공적으로 저장되었습니다.")
        except Exception as e:
            self.show_warning("에러", f"저장 중 오류가 발생했습니다: {str(e)}")

    def load_address_book(self):
        try:
            with open(self.file_path, "r") as file:
                lines = file.readlines()

            self.address_book.clear()
            self.contact_list.clear()

            for line in lines:
                name, phone = line.strip().split(":")
                self.address_book[name] = {"phone": phone}
                self.contact_list.addItem(f"{name}: {phone}")

            self.show_info("불러오기 완료", "주소록이 성공적으로 불러와졌습니다.")
        except FileNotFoundError:
            self.show_warning("경고", "저장된 주소록 파일을 찾을 수 없습니다.")
        except Exception as e:
            self.show_warning("에러", f"불러오기 중 오류가 발생했습니다: {str(e)}")

    def search_contacts(self):
        query = self.search_entry.text().lower()
        self.filtered_address_book = {name: data for name, data in self.address_book.items() if query in name.lower() or query in data['phone']}
        self.update_contact_list()

    def update_contact_list(self):
        self.contact_list.clear()
        for name, data in self.filtered_address_book.istems():
            self.contact_list.addItem(f"{name}: {data['phone']}")

    def show_warning(self, title, message):
        QMessageBox.warning(self, title, message)

    def show_info(self, title, message):
        QMessageBox.information(self, title, message)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = AddressBookApp()
    sys.exit(app.exec_())
