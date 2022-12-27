import os.path
import sys
import time
import sqlite3

from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication,QDialog,QWidget,QStackedWidget,QFileDialog
from PyQt5.QtGui import QIcon
from pytube import YouTube

class ana(QDialog):
    def __init__(self):
        super(QDialog,self).__init__()
        loadUi(r"C:\Users\bugra\OneDrive\Masaüstü\mp3 dönüştürücü\mp3converter.ui",self)

        self.pushButton_3.clicked.connect(self.ara)
        self.pushButton.clicked.connect(self.sec)
        self.pushButton_2.clicked.connect(self.indir)
        self.pushButton_2.clicked.connect(self.ekle)

        self.liste = []
        self.baglan()
        self.son_indirilenler()

    def baglan(self):
        self.con = sqlite3.connect(r"C:\Users\bugra\OneDrive\Masaüstü\mp3 dönüştürücü\sarkılar.db")
        self.cursor = self.con.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS sarkılar(isim TEXT)")
    def ara(self):
        try:
            url = self.lineEdit.text()
            self.yt = YouTube(url)
            self.label_8.setText(self.yt.title)
            dk = self.yt.length//60
            sn = self.yt.length%60
            self.label_9.setText("{} dk {} sn".format(dk,sn))
        except:
            self.label_8.setText("GEÇERSİZ URL (https://www.youtube.com/...)")

    def sec(self):
        self.label_10.setText("----------------")
        self.path = str(QFileDialog.getExistingDirectory(self, "Select Directory"))     #varolanı seçtirir

    def indir(self):
        a = list(os.walk(self.path))
        for x,y,z in a:
            for i in z:
                if i.endswith(".mp3"):
                    self.liste.append(i)
        (self.yt.title + ".mp3").strip("#")
        if (self.yt.title+".mp3") in self.liste:
            self.label_10.setText("Bu şarkı zaten belirtilen klosörde bulunuyor")
            print("hata")
        else:
            mp3 = self.yt.streams.filter(only_audio=True).first()
            out_file = mp3.download(output_path=self.path)

            base,ext = os.path.splitext(out_file)
            new_file = base+".mp3"
            os.rename(out_file,new_file)

            self.label_10.setText("İNDİRME BAŞARILI")

    def ekle(self):
        self.cursor.execute("Insert into sarkılar values(?)", (self.yt.title,))
        self.con.commit()

    def son_indirilenler(self):
        self.cursor.execute("select * from sarkılar")
        list = self.cursor.fetchall()
        a = len(list)
        try:
            self.label_5.setText("{}".format(list[a-1][0]))
            self.label_6.setText("{}".format(list[a-2][0]))
            self.label_7.setText("{}".format(list[a-3][0]))
        except:
            pass
app = QApplication(sys.argv)
ana1 = ana()
widget = QStackedWidget()
widget.addWidget(ana1)
widget.setWindowTitle("Mp3 Dönüştürücü")
widget.setWindowIcon(QIcon(r"C:\Users\bugra\OneDrive\Masaüstü\mp3 dönüştürücü\icon.png"))
widget.setFixedHeight(800)
widget.setFixedWidth(1200)
widget.show()
try:
    sys.exit(app.exec_())
except:
    print("çıkılıyor")