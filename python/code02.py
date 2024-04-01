import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QListWidgetItem, QMessageBox, QDialog
from PyQt5.uic import loadUi
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QMenu, QAction, QLineEdit, QPushButton, QVBoxLayout, QLabel, QDialogButtonBox

from PyQt5.QtCore import Qt

from addBookMySQL import *

class EditContactDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("주소록 수정")
        layout = QVBoxLayout()
        #DB 객체 생성 앞으로 self.db 라는 객체로 불리게 됨
        self.db = mysqlDB()
        self.name_edit = QLineEdit()
        self.phone_edit = QLineEdit()
        layout.addWidget(QLabel("이름:"))
        layout.addWidget(self.name_edit)
        layout.addWidget(QLabel("전화번호:"))
        layout.addWidget(self.phone_edit)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

        self.setLayout(layout)

    def get_contact_info(self):
        return self.name_edit.text(), self.phone_edit.text()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # UI 파일을 로드합니다.
        loadUi('ui01.ui', self)
        self.setWindowTitle('내가 만드는 주소록 Ver 0.1')

        # 이미지 파일의 경로를 저장하는 변수를 초기화합니다.
        self.image_paths = []

        # 빈 이미지를 생성합니다.
        self.empty_pixmap = QPixmap()
        self.default_pixmap = QPixmap('./res/unknown.png')  # 디폴트 이미지 경로

        # 실행시 주소록 읽어 오기
        self.load_address_book()

        # pushButton이 클릭되었을 때의 동작을 연결합니다.
        self.pushButton.clicked.connect(self.open_image_dialog)
        # pushButton_3이 클릭되었을 때의 동작을 연결합니다.
        self.pushButton_3.clicked.connect(self.save_address_book)
        # lineEdit에 대한 returnPressed 시그널을 연결합니다.
        self.lineEdit.returnPressed.connect(self.add_to_address_book)
        # pushButton_4이 클릭되었을 때의 동작을 연결합니다.
        self.pushButton_4.clicked.connect(self.add_to_address_book)
        # listWidget에 컨텍스트 메뉴 삭제 및 수정을 추가합니다.
        self.listWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.listWidget.customContextMenuRequested.connect(self.show_context_menu)
        # listWidget에 item이 더블클릭되었을 때의 동작을 연결합니다.
        self.listWidget.itemDoubleClicked.connect(self.show_image)

        # 검색창에서 텍스트를 입력할 때마다 주소록을 검색하여 결과를 표시합니다.
        self.lineEdit_search.textChanged.connect(self.search_address_book)

    def show_context_menu(self, pos):
        # 컨텍스트 메뉴를 생성합니다.
        context_menu = QMenu()
        delete_action = QAction("삭제", self)
        delete_action.triggered.connect(self.delete_item)
        edit_action = QAction("수정", self)
        edit_action.triggered.connect(self.edit_item)
        context_menu.addAction(delete_action)
        context_menu.addAction(edit_action)

        # 컨텍스트 메뉴를 보여줍니다.
        context_menu.exec_(self.listWidget.mapToGlobal(pos))

    def delete_item(self):
        # 선택된 아이템을 삭제합니다.
        selected_items = self.listWidget.selectedItems()
        for item in selected_items:
            row = self.listWidget.row(item)
            self.listWidget.takeItem(row)

    def load_address_book(self):
        # 파일 다이얼로그를 엽니다.
        filename = 'addbook2.txt'

        # 만약 사용자가 파일을 선택했다면
        if filename:
            # 파일을 읽어서 listWidget에 표시합니다.
            with open(filename, 'r') as file:
                for line in file:
                    # 데이터를 분리합니다.
                    data = line.strip().split(',')
                    name, phone, photo_path = data

                    # QListWidgetItem을 생성합니다.
                    item = QListWidgetItem(name + ' - ' + phone)

                    # 이미지 파일의 경로를 저장합니다.
                    self.image_paths.append(photo_path if photo_path.lower() != 'none' else '')

                    # 사진이 있는 경우에는 사진을 표시하고, 없는 경우에는 빈 이미지를 표시합니다.
                    if photo_path.strip().lower() != 'none':
                        pixmap = QPixmap(photo_path)
                    else:
                        pixmap = self.default_pixmap

                    # QListWidgetItem에 아이콘을 설정합니다.
                    icon = QIcon(pixmap)
                    item.setIcon(icon)

                    # QListWidget에 item을 추가합니다.
                    self.listWidget.addItem(item)

    def search_address_book(self):
        # 검색어를 가져옵니다.
        search_text = self.lineEdit_search.text().strip().lower()

        # 검색어가 비어있다면 모든 항목을 표시합니다.
        if not search_text:
            self.load_address_book()
            return

        # 검색어를 포함하는 주소록 항목을 찾습니다.
        found_items = []  # 변경된 부분: 검색 결과를 저장할 리스트 정의
        for index, path in enumerate(self.image_paths):
            item = self.listWidget.item(index)
            if item is not None:  # item이 None이 아닌 경우에만 처리
                name, _ = item.text().split(' - ')
                if search_text in name.lower():
                    new_item = QListWidgetItem(item.text())  # 새로운 QListWidgetItem 생성
                    pixmap = QPixmap(path)
                    new_item.setIcon(QIcon(pixmap))
                    found_items.append(new_item)  # 변경된 부분: 검색 결과를 리스트에 추가

        # 검색 결과를 표시합니다.
        self.listWidget.clear()
        for item in found_items:
            self.listWidget.addItem(item)

    def save_address_book(self):
        # 파일 다이얼로그를 엽니다.
        filename = 'addbook2.txt'

        # 만약 사용자가 파일을 선택했다면
        if filename:
            # listWidget의 아이템을 파일에 저장합니다.
            with open(filename, 'w') as file:
                for index in range(self.listWidget.count()):
                    item = self.listWidget.item(index)
                    # 아이템에서 이름과 전화번호를 가져옵니다.
                    name, phone = item.text().split(' - ')                    
                    # 아이콘의 파일 경로를 가져옵니다.                    
                    photo_path = self.image_paths[index]  # 해당 아이템의 이미지 파일 경로를 가져옵니다.
                    # 이름, 전화번호, 이미지 파일 경로를 파일에 씁니다.
                    file.write(name + ',' + phone + ',' + photo_path + '\n')
            # 주소록을 저장했다는 메시지를 표시합니다.
            QMessageBox.information(self, '주소록 저장', '주소록이 성공적으로 저장되었습니다.')

    def add_to_address_book(self):
        # lineEdit에 입력된 텍스트를 가져옵니다.
        name = self.lineEdit.text().strip()
        phone = self.lineEdit_2.text().strip()
        photo_path = self.label_4.text().strip()

        # 가져온 데이터가 비어있지 않은 경우에만 주소록에 추가합니다.
        if name and phone:
            # QListWidgetItem을 생성합니다.
            item = QListWidgetItem(name + ' - ' + phone)

            # 사진이 있는 경우에는 해당 사진을 표시하고, 없는 경우에는 빈 이미지를 표시합니다.
            if photo_path.strip().lower() != 'none':
                pixmap = QPixmap(photo_path)
            else:
                pixmap = self.empty_pixmap

            # QListWidgetItem에 아이콘을 설정합니다.
            item.setIcon(QIcon(pixmap))

            # QListWidget에 item을 추가합니다.
            self.listWidget.addItem(item)
            
            # 이미지 파일의 경로를 저장합니다.
            self.image_paths.append(photo_path)
            
            result = self.db.insert(name,phone, photo_path)
            print("Insert test:", result)

            # lineEdit을 초기화합니다.
            self.lineEdit.clear()
            self.lineEdit_2.clear()

    def open_image_dialog(self):
        # 파일 다이얼로그를 엽니다.
        filename, _ = QFileDialog.getOpenFileName(self, '이미지 파일 선택', '', '이미지 파일 (*.png *.jpg *.jpeg *.bmp *.gif)')

        # 만약 사용자가 파일을 선택했다면
        if filename:
            # 선택한 이미지 파일을 label_3에 표시합니다.
            pixmap = QPixmap(filename)
            self.label_3.setPixmap(pixmap)
            self.label_3.setScaledContents(True)
            self.label_4.setText(filename)

    def show_image(self, item):
    # 선택된 아이템의 사진을 표시합니다.
        row = self.listWidget.row(item)
        photo_path = self.image_paths[row]
        pixmap = QPixmap(photo_path)
        self.label_3.setPixmap(pixmap)
        self.label_3.setScaledContents(True)

    def edit_item(self):
        selected_items = self.listWidget.selectedItems()
        if not selected_items:
            return

        selected_item = selected_items[0]
        row = self.listWidget.row(selected_item)
        name, phone = selected_item.text().split(' - ')

        edit_dialog = EditContactDialog()
        edit_dialog.name_edit.setText(name)
        edit_dialog.phone_edit.setText(phone)

        if edit_dialog.exec_():
            new_name, new_phone = edit_dialog.get_contact_info()
            self.listWidget.item(row).setText(f"{new_name} - {new_phone}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())