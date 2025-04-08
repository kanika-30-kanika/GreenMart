import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import os

from checkface import *
from speechrecog import *
from products import *
from payment_final import * 
style_sheet = """
QLabel {
    background-color: #ecf0f1; /* Light gray */
    border: 1px solid #bdc3c7; /* Gray border */
    border-radius: 5px;
    padding: 10px;
}

QLabel:hover {
    background-color: #d5dbdb; /* Slightly darker gray on hover */
    color:#000000;
}
QWidget {
    background-color: #2c3e50; /* Dark blue */
}

QPushButton {
    background-color: #3498db; /* Blue */
    color: white;
    border: 2px solid #2980b9;
    border-radius: 10px;
    padding: 12px;
    font-size: 18px;
}

QPushButton:hover {
    background-color: #2980b9;
}

QPushButton:pressed {
    background-color: #1abc9c;
}

QLabel {
    font-size: 20px;
    color: white;
}

QLineEdit {
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 5px;
    background-color: white;
    color: #2c3e50; /* Dark blue */
}

QFileDialog {
    background-color: #2c3e50; /* Dark blue */
    color: white;
}
QVBoxLayout
{
    background-color:white;
}
"""


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        Login = QPushButton('Login', self)
        Login.clicked.connect(self.ML)

        signUp = QPushButton('Sign Up', self)
        signUp.clicked.connect(self.signing)

        layout = QVBoxLayout()
        layout.addWidget(Login)
        layout.addWidget(signUp)
        self.setLayout(layout)

        self.setWindowTitle('EchoMart')
        self.setWindowIcon(QIcon('Logo.png'))
        self.width, self.height = 400, 400
        self.setGeometry(0, 0, self.width, self.height)

        self.center_on_screen()

        self.setStyleSheet(style_sheet)
        self.show()

    def center_on_screen(self):
        screen = QDesktopWidget().screenGeometry()
        x = (screen.width() - self.width) // 2
        y = (screen.height() - self.height) // 2
        self.move(x, y)

    def ML(self):
        user = identify()
        if user=="Unknown":
            print("try again")
            return
        print('login success')
        self.close()
        self.shop = shoppingInterface()
        self.shop.show()
        self.welcome = Welcome(user)
        self.welcome.show()

    def signing(self):
        self.hide()
        self.sign = newRegister(self)
        self.sign.show()


class Welcome(QDialog):
    def __init__(self, username):
        super().__init__()
        self.initUI(username)

    def initUI(self, username):
        self.setWindowTitle('EchoMart')
        self.setWindowIcon(QIcon('Logo.png'))
        self.width, self.height = 300, 200
        self.setGeometry(0, 0, self.width, self.height)

        self.center_on_screen()
        label = QLabel('Welcome ' + username, self)

        ok_button = QPushButton('OK', self)
        ok_button.clicked.connect(self.accept)

        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(ok_button)

        self.setStyleSheet(style_sheet)
        self.setLayout(layout)

    def center_on_screen(self):
        screen = QDesktopWidget().screenGeometry()
        x = (screen.width() - self.width) // 2
        y = (screen.height() - self.height) // 2
        self.move(x, y)


class newCart(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.initUI()
        self.show()

    def initUI(self):
        self.setWindowTitle('Shopping Cart')
        self.setWindowIcon(QIcon("logo.png"))
        self.width, self.height = 500, 700
        self.setGeometry(0, 0, self.width, self.height)

        self.center_on_screen()
        layout = QVBoxLayout()
        self.logo_img = QPixmap('cart.png')
        self.logo_label = QLabel(self)
        self.logo_label.setPixmap(self.logo_img.scaled(30, 30, aspectRatioMode=Qt.KeepAspectRatio))
        self.logo_label.mousePressEvent = self.labelMousePressEvent

        search_ = QHBoxLayout()
        search_.addWidget(self.logo_label,alignment=Qt.AlignTop | Qt.AlignLeft)
        self.order = QLabel("My Cart")
        search_.addWidget(self.order, alignment=Qt.AlignTop | Qt.AlignRight)
        layout.addLayout(search_)

        self.setLayout(layout)
        self.setStyleSheet(style_sheet)

    def updateGrid(self, image_paths):
        grid_layout = QGridLayout()

        row = 0
        col = 0
        for image_path in image_paths:
            Card_layout = QVBoxLayout()
            pixmap = QPixmap(image_path)
            label = QLabel()
            label.setPixmap(pixmap.scaled(200, 200, aspectRatioMode=Qt.KeepAspectRatio))
            label.setAlignment(Qt.AlignCenter)
            Card_layout.addWidget(label)
            title = QLabel(image_path)
            title.setAlignment(Qt.AlignCenter)
            Add_button = QPushButton("Buy")
            Card_layout.addWidget(title)
            Card_layout.addWidget(Add_button)
            grid_layout.addLayout(Card_layout, row, col)
            col += 1
            if col == 4:
                col = 0
                row += 1

        self.grid_widget = QWidget()
        self.grid_widget.setLayout(grid_layout)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.grid_widget)
        self.scroll_area.setWidgetResizable(True)
        self.layout.addWidget(self.scroll_area)

    def labelMousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.close()
            self.main_window.show()
        elif event.button() == Qt.RightButton:
            print("Right mouse button pressed")
        self.setStyleSheet(style_sheet)

    def center_on_screen(self):
        screen = QDesktopWidget().screenGeometry()
        x = (screen.width() - self.width) // 2
        y = (screen.height() - self.height) // 2
        self.move(x, y)



class newRegister(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.initUI()
        self.show()


    def initUI(self):
        self.setWindowTitle('Sign Up')
        self.setWindowIcon(QIcon("logo.png"))
        self.width, self.height = 500, 700
        self.setGeometry(0, 0, self.width, self.height)

        self.center_on_screen()
        layout = QVBoxLayout()

        name = QHBoxLayout()
        name.addWidget(QLabel('Name:'))
        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText('Enter Name')
        name.addWidget(self.name_input)
        layout.addLayout(name)

        address = QHBoxLayout()
        address.addWidget(QLabel('Address:'))
        self.address_input = QLineEdit(self)
        self.address_input.setPlaceholderText('Enter Address')
        address.addWidget(self.address_input)
        layout.addLayout(address)

        email = QHBoxLayout()
        email.addWidget(QLabel('Email:'))
        self.email_input = QLineEdit(self)
        self.email_input.setPlaceholderText('Enter Email-id')
        email.addWidget(self.email_input)
        layout.addLayout(email)

        phone = QHBoxLayout()
        phone.addWidget(QLabel('Phone Number:'))
        self.mobile_input = QLineEdit(self)
        self.mobile_input.setPlaceholderText('Enter Phone Number')
        phone.addWidget(self.mobile_input)
        layout.addLayout(phone)

        Image = QHBoxLayout()
        Image.addWidget(QLabel("Enter Your Image :"))
        self.file_path = QLineEdit(self)
        self.file_path.setReadOnly(True)
        Image.addWidget(self.file_path)
        file_button = QPushButton('Choose File', self)
        file_button.clicked.connect(self.choose_file)
        Image.addWidget(file_button)
        layout.addLayout(Image)

        button = QHBoxLayout()
        submit_button = QPushButton('Submit', self)
        submit_button.clicked.connect(self.on_submit)
        button.addWidget(submit_button)

        back_button = QPushButton('Go Back', self)
        back_button.clicked.connect(self.go_back)
        button.addWidget(back_button)

        layout.addLayout(button)
        self.setLayout(layout)

        self.setStyleSheet(style_sheet)

    def center_on_screen(self):
        screen = QDesktopWidget().screenGeometry()
        x = (screen.width() - self.width) // 2
        y = (screen.height() - self.height) // 2
        self.move(x, y)

    def on_submit(self):
        name = self.name_input.text()
        add = self.address_input.text()
        email = self.email_input.text()
        phone = self.mobile_input.text()
        file = self.file_name
        print('Name:', name)
        print('Address:', add)
        print('Email:', email)
        print('Phone Number:', phone)
        if self.file_name:
            print('Selected file:', file)
        self.makeProfile(name, add, email, phone, file)
        self.close()
        self.shop = shoppingInterface()
        self.shop.show()

    def makeProfile(self,name, add, email, phone, file):
        new_user = Shopper(name,email,phone,add)
        new_user.store()
        store_face_encoding(file,name)
        print("profile successfully saved to pickle")

    def choose_file(self):
        options = QFileDialog.Options()
        self.file_name, _ = QFileDialog.getOpenFileName(self, "Choose File", "", "All Files (*);;Text Files (*.txt)",options=options)
        self.file_path.setText(self.file_name)

    def go_back(self):
        self.close()
        self.main_window.show()

class shoppingInterface(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.show()

    def initUI(self, image_paths=["Product//" + i for i in os.listdir("Product")]):
        self.setWindowTitle('EchoMart')
        self.setWindowIcon(QIcon('Logo.png'))
        self.width, self.height = 1000, 800
        self.setGeometry(0, 0, self.width, self.height)

        self.center_on_screen()
        self.layout = QVBoxLayout()

        # search box -voice recognition

        self.search_box = QLineEdit(self)
        self.search_box.setPlaceholderText('Search')
        self.search_box.returnPressed.connect(self.search)

        self.mic_button = QPushButton('🎤', self)
        self.mic_button.clicked.connect(self.start_listening)
        self.logo_img = QPixmap('cart.png')
        self.logo_label = QLabel(self)
        self.logo_label.setPixmap(self.logo_img.scaled(30, 30, aspectRatioMode=Qt.KeepAspectRatio))
        self.logo_label.mousePressEvent = self.labelMousePressEvent


        search_ = QHBoxLayout()
        search_.addWidget(self.logo_label)
        search_.addWidget(self.search_box)
        search_.addWidget(self.mic_button)
        self.layout.addLayout(search_)
        # slideshow
        self.image_paths = ["img" + str(i) + ".jpg" for i in range(2, 5)]
        self.current_image_index = 0
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.change_image)
        self.timer.start(2000)
        self.change_image()
        self.layout.addWidget(self.image_label, alignment=Qt.AlignTop)

        self.updateGrid(image_paths)
        self.center_on_screen()
        self.setStyleSheet(style_sheet)
        self.setLayout(self.layout)


    def labelMousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.hide()
            self.Cart=newCart(self)
            self.Cart.show()
        elif event.button() == Qt.RightButton:
            print("Right mouse button pressed")
    def updateGrid(self, image_paths):
        grid_layout = QGridLayout()
        row = 0
        col = 0
        for image_path in image_paths:
            Card_layout = QVBoxLayout()
            pixmap = QPixmap(image_path)
            label = QLabel()
            label.setPixmap(pixmap.scaled(200, 200, aspectRatioMode=Qt.KeepAspectRatio))
            label.setAlignment(Qt.AlignCenter)
            Card_layout.addWidget(label)
            title = QLabel(image_path)
            title.setAlignment(Qt.AlignCenter)
            Add_button = QPushButton("Buy")
            Add_button.clicked.connect(lambda: self.addtocart(title.text()))
            Card_layout.addWidget(title)
            Card_layout.addWidget(Add_button)
            grid_layout.addLayout(Card_layout, row, col)
            col += 1
            if col == 4:
                col = 0
                row += 1
        self.grid_widget = QWidget()
        self.grid_widget.setLayout(grid_layout)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.grid_widget)
        self.scroll_area.setWidgetResizable(True)
        self.layout.addWidget(self.scroll_area)

    def addtocart(self,product):
        self.new_payment = RadioButtonsAlignment()
        self.new_payment.show()
        print("Hrr")

    def search(self):
        query = self.search_box.text()
        tags = set(getTags(query))
        products = ["Product\\" + i for i in ProductMatch(tags)]
        print(products)
        self.grid_widget.setParent(None)
        self.grid_widget.deleteLater()
        self.scroll_area.setParent(None)
        self.scroll_area.deleteLater()

        self.updateGrid(products)
        # print(ProductMatch(tags))

    def start_listening(self):
        print('Started listening...')  # Add functionality to start listening to audio
        self.search_box.setText(speech_to_text())
        self.search()

    def change_image(self):
        pixmap = QPixmap(self.image_paths[self.current_image_index])
        self.image_label.setPixmap(pixmap.scaled(1000, 300, aspectRatioMode=1))
        self.current_image_index = (self.current_image_index + 1) % len(self.image_paths)

    def center_on_screen(self):
        screen = QDesktopWidget().screenGeometry()
        x = (screen.width() - self.width) // 2
        y = (screen.height() - self.height) // 2
        self.move(x, y)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWidget()
    sys.exit(app.exec_())
