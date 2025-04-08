import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

style_sheet = """
QLabel {
    background-color: #ecf0f1; /* Light gray */
    border: 1px solid #bdc3c7; /* Gray border */
    border-radius: 5px;
    padding: 10px;
}

QLabel:hover {
    background-color: #d5dbdb; /* Slightly darker gray on hover */
    color: #000000;
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

QVBoxLayout {
    background-color: white;
}

QRadioButton {
    color: white;
    font-weight: bold;
}

QRadioButton::indicator:checked {
    background-color: #3498db; /* Blue when checked */
    border: 2px solid #2980b9;
    border-radius: 5px;
}
"""


class SuccessfulPage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Shopping Cart')
        self.setWindowIcon(QIcon("logo.png"))
        self.width, self.height = 500, 300
        self.setGeometry(0, 0, self.width, self.height)

        self.center_on_screen()
        
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        label_success = QLabel("Order Placed\nThank You\nPayment Successful", self)
        label_success.setAlignment(Qt.AlignCenter)
        layout.addWidget(label_success)

        ok_button = QPushButton("OK", self)
        ok_button.clicked.connect(self.close)
        layout.addWidget(ok_button)
        self.setStyleSheet(style_sheet)
    
    def center_on_screen(self):
        screen = QDesktopWidget().screenGeometry()
        x = (screen.width() - self.width) // 2
        y = (screen.height() - self.height) // 2
        self.move(x, y)


class PaymentPage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Shopping Cart')
        self.setWindowIcon(QIcon("logo.png"))
        self.width, self.height = 500, 300
        self.setGeometry(0, 0, self.width, self.height)

        self.center_on_screen()
        
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.label_payment_method = QLabel("Select Payment method:", self)
        self.radio_button_upi = QRadioButton("UPI")
        self.radio_button_cod = QRadioButton("Cash on Delivery")
        self.radio_button_net_banking = QRadioButton("Net Banking")
        self.radio_button_credit_card = QRadioButton("Credit Card")

        layout.addWidget(self.label_payment_method,alignment=Qt.AlignTop)
        layout.addWidget(self.radio_button_upi)
        layout.addWidget(self.radio_button_cod)
        layout.addWidget(self.radio_button_net_banking)
        layout.addWidget(self.radio_button_credit_card)

        self.radio_button_upi.setChecked(True)

        self.radio_button_upi.toggled.connect(self.show_upi_verification)
        self.radio_button_net_banking.toggled.connect(self.show_net_banking_dropdown)
        self.radio_button_credit_card.toggled.connect(self.show_credit_card_fields)

        self.textbox_upi = QLineEdit(self)
        self.textbox_upi.setPlaceholderText("Enter UPI ID")
        self.textbox_upi.hide()

        self.verify_button = QPushButton("Verify", self)
        self.verify_button.clicked.connect(self.verify_upi)
        self.verify_button.hide()

        layout.addWidget(self.textbox_upi)
        layout.addWidget(self.verify_button)

        self.pay_button = QPushButton("Pay", self)
        self.pay_button.clicked.connect(self.process_payment)
        layout.addWidget(self.pay_button)

        self.net_banking_dropdown = QComboBox(self)
        self.net_banking_dropdown.addItems(["Bank A", "Bank B", "Bank C"])
        self.net_banking_dropdown.hide()

        layout.addWidget(self.net_banking_dropdown)

        self.credit_card_name = QLineEdit(self)
        self.credit_card_name.setPlaceholderText("Cardholder Name")
        self.credit_card_name.hide()

        self.credit_card_number = QLineEdit(self)
        self.credit_card_number.setPlaceholderText("Card Number")
        self.credit_card_number.hide()

        self.cvv = QLineEdit(self)
        self.cvv.setPlaceholderText("CVV")
        self.cvv.setEchoMode(QLineEdit.Password)
        self.cvv.hide()

        expiry_dates = ["01/22", "02/22", "03/22", "04/22"]
        self.expiry_dropdown = QComboBox(self)
        self.expiry_dropdown.addItems(expiry_dates)
        self.expiry_dropdown.hide()

        layout.addWidget(self.credit_card_name)
        layout.addWidget(self.credit_card_number)
        layout.addWidget(self.cvv)
        layout.addWidget(self.expiry_dropdown)

        self.cancel_button = QPushButton("Cancel", self)
        self.cancel_button.clicked.connect(self.close)
        layout.addWidget(self.cancel_button)

        self.select_button = QPushButton("Select", self)
        self.select_button.clicked.connect(self.select_payment_method)
        layout.addWidget(self.select_button)

        layout.setSpacing(5)
        self.setStyleSheet(style_sheet)


    def show_upi_verification(self, checked):
        if checked:
            self.textbox_upi.show()
            self.verify_button.show()
        else:
            self.textbox_upi.hide()
            self.verify_button.hide()

    def verify_upi(self):
        upi_id = self.textbox_upi.text()
        if upi_id:
            print(f"Verifying UPI: {upi_id}")
            self.show_verification_message()
        else:
            QMessageBox.warning(self, "Error", "Please enter UPI ID.")

    def show_net_banking_dropdown(self, checked):
        if checked:
            self.hide_pay_fields()
            self.net_banking_dropdown.show()
        else:
            self.net_banking_dropdown.hide()

    def show_credit_card_fields(self, checked):
        if checked:
            self.hide_pay_fields()

            self.credit_card_name.show()
            self.credit_card_number.show()
            self.cvv.show()
            self.expiry_dropdown.show()

    def hide_pay_fields(self):
        self.net_banking_dropdown.hide()
        self.credit_card_name.hide()
        self.credit_card_number.hide()
        self.cvv.hide()
        self.expiry_dropdown.hide()

    def process_payment(self):
        if self.get_checked_payment_method():
            checked_button = self.get_checked_payment_method()

            if checked_button == self.radio_button_upi:
                self.show_successful_page()
            elif checked_button == self.radio_button_credit_card:
                if self.validate_credit_card():
                    self.show_successful_page()
            else:
                self.show_successful_page()
        else:
            QMessageBox.warning(self, "Error", "Please select a payment method.")

    def get_checked_payment_method(self):
        if self.radio_button_upi.isChecked():
            return self.radio_button_upi
        elif self.radio_button_net_banking.isChecked():
            return self.radio_button_net_banking
        elif self.radio_button_credit_card.isChecked():
            return self.radio_button_credit_card
        return None

    def validate_credit_card(self):
        card_name = self.credit_card_name.text()
        card_number = self.credit_card_number.text()
        cvv = self.cvv.text()

        if card_name and card_number and cvv:
            return True
        else:
            QMessageBox.warning(self, "Error", "Please fill all Credit Card fields.")
            return False

    def show_verification_message(self):
        QMessageBox.information(self, "Verification", "UPI Verified! Proceed to payment.")

    def show_successful_page(self):
        self.successful_page = SuccessfulPage()
        self.successful_page.show()
        self.close()

    def select_payment_method(self):
        selected_button = self.get_checked_payment_method()

        if selected_button:
            self.disable_radio_buttons(selected_button)
            self.enable_additional_elements(selected_button)
        else:
            QMessageBox.warning(self, "Error", "Please select a payment method.")

    def disable_radio_buttons(self, selected_button):
        all_radio_buttons = [
            self.radio_button_upi,
            self.radio_button_cod,
            self.radio_button_net_banking,
            self.radio_button_credit_card
        ]

        for button in all_radio_buttons:
            if button != selected_button:
                button.setEnabled(False)
    def center_on_screen(self):
        screen = QDesktopWidget().screenGeometry()
        x = (screen.width() - self.width) // 2
        y = (screen.height() - self.height) // 2
        self.move(x, y)

    def enable_additional_elements(self, selected_button):
        if selected_button == self.radio_button_upi:
            self.show_upi_verification(True)
        elif selected_button == self.radio_button_net_banking:
            self.show_net_banking_dropdown(True)
        elif selected_button == self.radio_button_credit_card:
            self.show_credit_card_fields(True)
  
class RadioButtonsAlignment(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Payment')
        self.setWindowIcon(QIcon("logo.png"))
        self.width, self.height = 500, 300
        self.setGeometry(0, 0, self.width, self.height)

        self.center_on_screen()
        
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.label_address = QLabel("Address:", self)
        self.radio_button_1 = QRadioButton("Address 1")
        self.radio_button_2 = QRadioButton("Address 2")
        self.radio_button_3 = QRadioButton("Address 3")
        # self.radio_button_1.setChecked(True)

        layout.addWidget(self.label_address,alignment=Qt.AlignTop)
        layout.addWidget(self.radio_button_1)
        layout.addWidget(self.radio_button_2)
        layout.addWidget(self.radio_button_3)

        button_layout = QHBoxLayout()
        proceed_button = QPushButton("Proceed")
        cancel_button = QPushButton("Cancel")

        button_layout.addWidget(proceed_button)
        button_layout.addWidget(cancel_button)

        layout.addLayout(button_layout)

        cancel_button.clicked.connect(QApplication.quit)
        proceed_button.clicked.connect(self.open_payment_page)
        self.setStyleSheet(style_sheet)

    def center_on_screen(self):
        screen = QDesktopWidget().screenGeometry()
        x = (screen.width() - self.width) // 2
        y = (screen.height() - self.height) // 2
        self.move(x, y)

    def open_payment_page(self):
        self.payment_page = PaymentPage()
        self.payment_page.show()
        self.close()

