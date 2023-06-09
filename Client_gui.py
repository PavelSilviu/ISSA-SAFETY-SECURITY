import psutil as psutil
from PyQt5 import QtCore, QtGui, QtWidgets, QtTest
import socket
import rsa_library
import _pickle as cPickle
import os
import threading
import sys, time



HOST = 'localhost'
PORT = 12346
ok_client = False
airbag_on = '0xfe01'
corrupted_low = '0x5732'
corrupted_high = '0x5701'


class Ui_MainWindow(object):
    se = 0
    priv_k = 0
    pub_k = 0
    modul = 0
    ok1 = False

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(600, 500)
        MainWindow.setWindowTitle('Client')
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        MainWindow.setCentralWidget(self.centralwidget)

        self.centralwidget.setStyleSheet("background-color:white;")

        # Start client button
        self.client_start = QtWidgets.QPushButton(MainWindow)
        self.client_start.setText("Connect client")
        self.client_start.setStyleSheet("font: bold; font-size: 15px;")
        self.client_start.setGeometry(QtCore.QRect(200, 170, 200, 40))
        self.client_start.clicked.connect(self.start_client)

        self.client_label = QtWidgets.QLabel(self.centralwidget)
        self.client_label.setGeometry(QtCore.QRect(320, 170, 205, 41))
        self.client_label.setStyleSheet("font:bold;font-size: 15px;")

        # Connected label
        self.connected_label = QtWidgets.QLabel(self.centralwidget)
        self.connected_label.setGeometry(QtCore.QRect(200, 210, 200, 40))
        self.connected_label.setStyleSheet("font-size:15px;font:bold;qproperty-alignment: AlignCenter;")

        # Airbag on
        self.airbag = QtWidgets.QPushButton(MainWindow)
        self.airbag.setText("Airbag on")
        self.airbag.setStyleSheet("font: bold; font-size: 15px;")
        self.airbag.setGeometry(QtCore.QRect(70, 260, 211, 41))
        self.airbag.clicked.connect(self.send_on_data)
        self.airbag.setEnabled(False)

        # Airbag on label
        self.airbag_on_label = QtWidgets.QLabel(self.centralwidget)
        self.airbag_on_label.setGeometry(QtCore.QRect(300, 260, 200, 40))
        self.airbag_on_label.setStyleSheet("font-size:15px;font:bold;qproperty-alignment: AlignCenter;")

        # Corrupted low
        self.corrupted_low = QtWidgets.QPushButton(MainWindow)
        self.corrupted_low.setText("Corrupted low")
        self.corrupted_low.setStyleSheet("font: bold; font-size: 15px;")
        self.corrupted_low.setGeometry(QtCore.QRect(70, 330, 211, 41))
        self.corrupted_low.clicked.connect(self.send_corrupted_low)
        self.corrupted_low.setEnabled(False)

        # Corrupted low label
        self.corrupted_low_label = QtWidgets.QLabel(self.centralwidget)
        self.corrupted_low_label.setGeometry(QtCore.QRect(300, 330, 200, 40))
        self.corrupted_low_label.setStyleSheet("font-size:15px;font:bold;qproperty-alignment: AlignCenter;")

        # Corrupted high
        self.corrupted_high = QtWidgets.QPushButton(MainWindow)
        self.corrupted_high.setText("Corrupted high")
        self.corrupted_high.setStyleSheet("font: bold; font-size: 15px;")
        self.corrupted_high.setGeometry(QtCore.QRect(70, 400, 211, 41))
        self.corrupted_high.clicked.connect(self.send_corrupted_high)
        self.corrupted_high.setEnabled(False)

        # Corrupted high label
        self.corrupted_high_label = QtWidgets.QLabel(self.centralwidget)
        self.corrupted_high_label.setGeometry(QtCore.QRect(300, 400, 200, 40))
        self.corrupted_high_label.setStyleSheet("font-size:15px;font:bold;qproperty-alignment: AlignCenter;")

        # Continental image
        self.conti_label = QtWidgets.QLabel(self.centralwidget)
        self.conti_label.setGeometry(QtCore.QRect(110, 30, 400, 100))
        continental = QtGui.QImage(QtGui.QImageReader('./rsz_conti.png').read())
        self.conti_label.setPixmap(QtGui.QPixmap(continental))

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")

        MainWindow.setStatusBar(self.statusbar)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.show()

    ############################### EXERCISE 5 ###############################
    def start_client(self):
        self.corrupted_low_label.clear()
        self.airbag_on_label.clear()
        self.corrupted_high_label.clear()
        self.airbag.setEnabled(False)
        self.corrupted_high.setEnabled(False)
        self.corrupted_low.setEnabled(False)
        s = socket.socket()
        self.server_socket = s
        s.connect((HOST, PORT))

        print("connected client to server")

        # receive data from the server and decoding to get the string.
        public_key = s.recv(1024).decode()
        private_key = s.recv(1024).decode()
        modulus = s.recv(1024).decode()

        self.pub_pair = (int(public_key), int(modulus))
        self.private_pair = (int(private_key), int(modulus))

        print("received private and public keys:")
        print(self.pub_pair)
        print(self.private_pair)

        received_message = s.recv(1024).decode()
        print("received encrypted key: ", received_message)

        self.unlock_car = rsa_library.decrypt(self.private_pair, received_message)
        print("decripted key received: ", self.unlock_car)

        self.airbag.setEnabled(True)
        self.corrupted_high.setEnabled(True)
        self.corrupted_low.setEnabled(True)

        self.recv_messages()




############################### EXERCISE 8 ###############################
    def recv_messages(self):
        self.stop_event = threading.Event()
        self.c_thread = threading.Thread(target=self.recv_handler, args=(self.stop_event,))
        self.c_thread.start()


    def recv_handler(self, stop_event):
        while True:
            message = self.server_socket.recv(1024).decode()
            decrypted_message = rsa_library.decrypt(self.private_pair, message)
            print("NEW MESSAGE:", decrypted_message)
            if decrypted_message == self.unlock_car:
                self.airbag.setEnabled(True)
                self.corrupted_low.setEnabled(True)
                self.corrupted_high.setEnabled(True)
            elif decrypted_message == "0x0":
                self.corrupted_low_label.setText("Corrupted Low")
            elif decrypted_message == "0x1":
                self.corrupted_high_label.setText("Corrupted High")
            elif decrypted_message == "0x69":
                self.airbag_on_label.setText("All good")


############################### EXERCISE 9 ###############################
    def send_on_data(self):
        global airbag_on
        self.clear_messages()
        print("Airbag on")
        message = rsa_library.encrypt(self.pub_pair, airbag_on)
        print("SENDING: ", message)
        self.server_socket.send(str(message).encode())


############################### EXERCISE 10 ###############################
    def send_corrupted_low(self):
        global corrupted_low
        self.clear_messages()
        self.airbag.setEnabled(False)
        message = rsa_library.encrypt(self.pub_pair, corrupted_low)
        print("SENDING: ", message)
        self.server_socket.send(str(message).encode())


############################### EXERCISE 11 ###############################
    def send_corrupted_high(self):
        global corrupted_high
        self.clear_messages()
        self.airbag.setEnabled(False)
        message = rsa_library.encrypt(self.pub_pair, corrupted_high)
        print("SENDING: ", message)
        self.server_socket.send(str(message).encode())

    def clear_messages(self):
        self.corrupted_low_label.setText("")
        self.airbag_on_label.setText("")

    def kill_proc_tree(self, pid, including_parent=True):
         parent = psutil.Process(pid)
         if including_parent:
            parent.kill()


class MyWindow(QtWidgets.QMainWindow):
    def closeEvent(self, event):
        result = QtGui.QMessageBox.question(self,
                                            "Confirm Exit",
                                            "Are you sure you want to exit ?",
                                            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)

        if result == QtGui.QMessageBox.Yes:
            event.accept()
        elif result == QtGui.QMessageBox.No:
            event.ignore()

    def center(self):
        frameGm = self.frameGeometry()
        screen = QtWidgets.QApplication.desktop().screenNumber(QtWidgets.QApplication.desktop().cursor().pos())
        centerPoint = QtWidgets.QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MyWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.center()
    sys.exit(app.exec_())

me = os.getpid()
#kill_proc_tree(me)
