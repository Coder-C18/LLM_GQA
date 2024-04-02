from PyQt6 import QtCore, QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QSizePolicy

from LLM_model.db_vector import QA_Gemini, get_list_collection_name, insert_db

from qdrant_client import QdrantClient

client = QdrantClient("localhost", port=6333)


class WorkerThread(QtCore.QThread):
    # Define a signal to communicate with the main thread
    update_signal = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()

    def run(self):
        # This is the function that will run on the background thread
        self.update_signal.emit(f"Count")


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(998, 793)

        self.tabWidget = QtWidgets.QTabWidget(parent=Dialog)
        self.tabWidget.setGeometry(QtCore.QRect(-10, 0, 1011, 801))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("Q&A")

        self.cbbox = QtWidgets.QComboBox(parent=self.tab)
        self.cbbox.setGeometry(QtCore.QRect(647, 129, 315, 36))
        self.cbbox.setObjectName("cbbox")

        self.textBrowser_2 = QtWidgets.QTextBrowser(parent=self.tab)
        self.textBrowser_2.setGeometry(QtCore.QRect(36, 66, 577, 638))
        self.textBrowser_2.setObjectName("textBrowser_2")

        self.textEdit = QtWidgets.QLineEdit(parent=self.tab)
        self.textEdit.setGeometry(QtCore.QRect(647, 251, 315, 290))
        self.textEdit.setObjectName("textEdit")
        self.textEdit.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.textEdit.setPlaceholderText(" Nhập câu hỏi tại đây ")
        self.textEdit.returnPressed.connect(self.gen_answer)
        self.textEdit.textChanged.connect(self.text_change)
        self.tabWidget.addTab(self.tab, "")


        # Inserting data into the model
        self.view_collections()


        self.pushButton = QtWidgets.QPushButton(parent=self.tab)
        self.pushButton.setGeometry(QtCore.QRect(647, 66, 137, 36))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.insert_file)
        self.pushButton.setFocusPolicy(Qt.FocusPolicy.NoFocus)


        self.pushButton_4 = QtWidgets.QPushButton(parent=self.tab)
        self.pushButton_4.setGeometry(QtCore.QRect(825, 66, 137, 36))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.senbutton = QtWidgets.QPushButton(parent=self.tab)
        self.senbutton.setGeometry(QtCore.QRect(647, 206, 315, 36))
        self.senbutton.setObjectName("senbutton")
        self.senbutton.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.senbutton.clicked.connect(self.gen_answer)

        self.senbutton.setDisabled(True)

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def view_collections(self):
        collection_names = get_list_collection_name()
        self.cbbox.addItems(collection_names)
    def text_change(self):
        text_input = self.textEdit.text()
        if text_input != '':
            self.senbutton.setDisabled(False)


    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Dialog", "Bot"))
        self.pushButton.setText(_translate("Dialog", "Insert Document"))
        self.pushButton_4.setText(_translate("Dialog", "Delete"))
        self.senbutton.setText(_translate("Dialog", "SEND QUESTION"))

    def gen_answer(self):
        text_input = self.textEdit.text()
        self.textBrowser_2.setText(self.textBrowser_2.toPlainText() + "\n" + f'User :{text_input}')
        self.textEdit.setText('')

        def gen():
            collection_name = self.cbbox.currentText()
            answer = QA_Gemini(text_input, collection_name)
            print("dang tra loi ")
            self.textBrowser_2.setText(self.textBrowser_2.toPlainText() + "\n" + f'Bot: {answer}')

        self.worker_thread = WorkerThread()
        self.worker_thread.update_signal.connect(gen)
        self.worker_thread.start()

    def insert_file(self):
        file = QtWidgets.QFileDialog.getOpenFileName(self.pushButton.parentWidget(), "Open File", 'D:',
                                                     "Documents(*.docx *.pdf)")[0]
        collection_name = file.split('/')[-1]
        insert_db(file, collection_name)
        self.view_collections()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec())
