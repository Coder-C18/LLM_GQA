from PyQt6 import QtCore, QtGui, QtWidgets
from db_vector import QA_Gemini
import time
from langchain_community.document_loaders import Docx2txtLoader
from langchain.text_splitter import  RecursiveCharacterTextSplitter
from qdrant_client import QdrantClient
import google.generativeai as gemini_client
from qdrant_client.http.models import Distance, PointStruct, VectorParams

GEMINI_API_KEY = "AIzaSyCieu0Mua9b0gjo-RbIGi-bTJGYlwzVN1U"  # add your key here
client = QdrantClient("localhost", port=6333)
gemini_client.configure(api_key=GEMINI_API_KEY)






class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setEnabled(True)
        Dialog.resize(1086, 761)

        self.dialog_upload = QtWidgets.QDialog(parent=Dialog)


        self.lineEdit = QtWidgets.QLineEdit(parent=Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(10, 680, 811, 31))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.returnPressed.connect(self.on_line_text_press)
        self.lineEdit.editingFinished.connect(self.off)

        self.messbox = QtWidgets.QMessageBox(parent=Dialog)
        self.messbox.setGeometry(QtCore.QRect(830, 130, 241, 23))



        self.textBrowser = QtWidgets.QTextBrowser(parent=Dialog)
        self.textBrowser.setGeometry(QtCore.QRect(10, 10, 811, 661))
        self.textBrowser.setObjectName("textBrowser")


        self.progressBar = QtWidgets.QProgressBar(parent=self.messbox)
        self.progressBar.setGeometry(QtCore.QRect(830, 130, 241, 23))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")


        self.pushButton = QtWidgets.QPushButton(parent=Dialog)
        self.pushButton.setGeometry(QtCore.QRect(830, 90, 241, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.oki)


        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButton.setText(_translate("Dialog", "UpLoad Documnet"))


    def oki(self):
        file  = QtWidgets.QFileDialog.getOpenFileName(self.pushButton.parentWidget(),"Open File",'D:\code\LLM_GQA',("Documents(*.docx *.pdf)"))

        loader = Docx2txtLoader(file[0])
        pages = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=2048, chunk_overlap=512)

        docs = text_splitter.split_documents(pages)

        document_chunks = [chunk.page_content for chunk in docs]

        results = []
        t = 1
        print(len(document_chunks))
        self.messbox.show()
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
            self.progressBar.setProperty('value', round(((index+1)/len(document_chunks))*100))

        points = [
            PointStruct(
                id=idx,
                vector=response,
                payload={"text": text},
            )
            for idx, (response, text) in enumerate(zip(results, document_chunks))
        ]
        # client.create_collection('docxaa88', vectors_config=
        # VectorParams(
        #     size=768,
        #     distance=Distance.COSINE,
        # )
        #                         )
        client.upsert('docx', points)



    def on_line_text_press(self):
        text_input = self.lineEdit.text()
        self.textBrowser.setText(self.textBrowser.toPlainText() + "\n" + text_input)

        answer = QA_Gemini(text_input)
        self.textBrowser.setText(self.textBrowser.toPlainText() + "\n" + answer)
    def off(self):
        self.lineEdit.setText('')


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec())
