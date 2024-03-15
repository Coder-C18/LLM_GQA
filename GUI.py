import time
from PyQt6 import QtCore,QtWidgets
from db_vector import QA_Gemini
from langchain_community.document_loaders import Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from qdrant_client import QdrantClient
import google.generativeai as gemini_client
from qdrant_client.http.models import Distance, PointStruct, VectorParams

GEMINI_API_KEY = "AIzaSyCieu0Mua9b0gjo-RbIGi-bTJGYlwzVN1U"  # add your key here
client = QdrantClient("localhost", port=6333)
gemini_client.configure(api_key=GEMINI_API_KEY)


class WorkerThread(QtCore.QThread):
    # Define a signal to communicate with the main thread
    update_signal = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()

    def run(self):
        # This is the function that will run on the background thread
        self.update_signal.emit(f"Count")
from PyQt6.QtCore import Qt
class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            return self._data[index.row()][index.column()]

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._data[0])



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
        self.cbbox.setGeometry(QtCore.QRect(20, 10,200, 20))
        self.cbbox.setObjectName("cbbox")



        self.textBrowser_2 = QtWidgets.QTextBrowser(parent=self.tab)
        self.textBrowser_2.setGeometry(QtCore.QRect(20, 60, 941, 500))
        self.textBrowser_2.setObjectName("textBrowser_2")

        self.textEdit = QtWidgets.QLineEdit(parent=self.tab)
        self.textEdit.setGeometry(QtCore.QRect(20, 630, 941, 41))
        self.textEdit.setObjectName("textEdit")
        self.textEdit.returnPressed.connect(self.gen_answer)
        self.tabWidget.addTab(self.tab, "")

        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("Document Manager")

        self.tableView = QtWidgets.QTableView(parent=self.tab_2)
        self.tableView.setGeometry(QtCore.QRect(20, 240, 971, 491))
        self.tableView.setObjectName("tableView")



        # Inserting data into the model
        self.view_collections()


        self.frame = QtWidgets.QFrame(parent=self.tab_2)
        self.frame.setGeometry(QtCore.QRect(10, 0, 981, 171))
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")

        self.progressBar = QtWidgets.QProgressBar(parent=self.frame)
        self.progressBar.setGeometry(QtCore.QRect(10, 130, 791, 23))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.progressBar.hide()

        self.pushButton = QtWidgets.QPushButton(parent=self.frame)
        self.pushButton.setGeometry(QtCore.QRect(10, 70, 131, 41))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.insert_file)

        self.pushButton_3 = QtWidgets.QPushButton(parent=self.frame)
        self.pushButton_3.setGeometry(QtCore.QRect(160, 70, 151, 41))
        self.pushButton_3.setObjectName("pushButton_3")

        self.textBrowser = QtWidgets.QTextBrowser(parent=self.frame)
        self.textBrowser.setGeometry(QtCore.QRect(10, 20, 641, 31))
        self.textBrowser.setObjectName("textBrowser")

        self.pushButton_2 = QtWidgets.QPushButton(parent=self.frame)
        self.pushButton_2.setGeometry(QtCore.QRect(650, 20, 111, 31))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.select_file)

        self.pushButton_4 = QtWidgets.QPushButton(parent=self.tab_2)
        self.pushButton_4.setGeometry(QtCore.QRect(20, 180, 151, 41))
        self.pushButton_4.setObjectName("pushButton_4")

        self.tabWidget.addTab(self.tab_2, "")

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(Dialog)


    def view_collections(self):

        x = client.get_collections()
        self.cbbox.addItems([i.name for i in x.collections])
        x = [[i.name] for i in x.collections]
        self.tableView.setModel(TableModel(x))


    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Dialog", "Tab 1"))
        self.pushButton.setText(_translate("Dialog", "Insert Document"))
        self.pushButton_3.setText(_translate("Dialog", "Cancel insert"))
        self.pushButton_2.setText(_translate("Dialog", "Browser"))
        self.pushButton_4.setText(_translate("Dialog", "Delete"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Dialog", "Tab 2"))


    def gen_answer(self):
        text_input = self.textEdit.text()
        self.textBrowser_2.setText(self.textBrowser_2.toPlainText() + "\n" + f'User :{text_input}')
        self.textEdit.setText('')

        def gen():
            collection_name = self.cbbox.currentText()
            answer = QA_Gemini(text_input,collection_name)
            print("dang tra loi ")
            self.textBrowser_2.setText(self.textBrowser_2.toPlainText() + "\n" + f'Bot: {answer}')

        self.worker_thread = WorkerThread()
        self.worker_thread.update_signal.connect(gen)
        self.worker_thread.start()


    def select_file(self):
        file = QtWidgets.QFileDialog.getOpenFileName(self.pushButton.parentWidget(), "Open File", 'D:',
                                                     "Documents(*.docx *.pdf)")
        self.textBrowser.setText(file[0])

    def insert_file(self):
        file_path = self.textBrowser.toPlainText()
        collection_name = file_path.split('/')[-1]
        print(file_path)
        print(collection_name)

        loader = Docx2txtLoader(file_path)
        pages = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=2048, chunk_overlap=512)

        docs = text_splitter.split_documents(pages)

        document_chunks = [chunk.page_content for chunk in docs]

        results = []
        t = 1
        self.progressBar.show()
        for index in range(len(document_chunks)):
            print(index)

            emb = gemini_client.embed_content(
                model="models/embedding-001",
                content=document_chunks[index],
                task_type="retrieval_document",
                title="Qdrant x Gemini",
            )['embedding']
            results.append(emb)
            if t % 60 == 0:
                time.sleep(60)
            t += 1
            self.progressBar.setProperty('value', round(((index + 1) / len(document_chunks)) * 100))

        points = [
            PointStruct(
                id=idx,
                vector=response,
                payload={"text": text},
            )
            for idx, (response, text) in enumerate(zip(results, document_chunks))
        ]
        client.create_collection(collection_name, vectors_config=
        VectorParams(
            size=768,
            distance=Distance.COSINE,
        )
                                )
        client.upsert(collection_name, points)
        self.view_collections()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec())
