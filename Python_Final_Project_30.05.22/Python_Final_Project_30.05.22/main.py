#----------------------KÜTÜPHANE----------------------#
#-----------------------------------------------------#
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from AnasayfaUI import *
#----------------------UYGULAMA OLUŞTURMA----------------------#
#--------------------------------------------------------------#
Uygulama=QApplication(sys.argv)
penAna=QMainWindow()
ui=Ui_MainWindow()
ui.setupUi(penAna)
penAna.show()
#----------------------VERİTABANI OLUŞTURMA----------------------#
#--------------------------------------------------------------#
import sqlite3
global curs
global conn
conn=sqlite3.connect('veritabani.db')
curs=conn.cursor()
sorguCreTblKayitform=("CREATE TABLE IF NOT EXISTS Tablo (                      \
                      ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,       \
                      TCNO INTEGER NOT NULL UNIQUE,                      \
                      İSİM TEXT NOT NULL,                                  \
                      SOYİSİM TEXT NOT NULL,                               \
                      DOGUM_TARİHİ TEXT NOT NULL,                            \
                      CİNSİYET TEXT NOT NULL,                                        \
                      MEDENİ_HAL TEXT NOT NULL,                                       \
                      ASKERLİK TEXT NOT NULL,                                \
                      EHLİYET TEXT NOT NULL,                                \
                      EĞİTİM TEXT NOT NULL,                                \
                      DEPARTMAN TEXT NOT NULL,                             \
                      CALISMA_SAATİ TEXT NOT NULL,                      \
                      MAAS TEXT NOT NULL,                          \
                      EPOSTA TEXT NOT NULL,                                 \
                      TEL TEXT NOT NULL,                                   \
                      ADRES TEXT NOT NULL)")
curs.execute(sorguCreTblKayitform)
conn.commit()

#----------------------------KAYDET--------------------------#
#------------------------------------------------------------#

def EKLE():
    _kimlik = ui.txt_Kimlik.text()
    _isim =ui.txt_Isim.text()
    _soyisim = ui.txt_Soyisim.text()
    _dogumtarihi=ui.cmb_Gun.currentText()+ui.cmb_Ay.currentText()+ui.cmb_Yil.currentText()
    if ui.rb_Erkek.isChecked() == True:
        _cinsiyet = "Erkek"
    else:
        _cinsiyet = "Kadın"
    if ui.rb_Bekar.isChecked() == True:
        _medenihal = "Bekar"
    else:
        _medenihal = "Evli"
    if ui.rb_Askerlik_yapildi.isChecked() == True:
        _askerlik = "Yapıldı"
    elif ui.rb_Askerlik_Tecilli.isChecked() == True:
        _askerlik = "Yapılmadı"
    else :
        _askerlik = "Muaf"
    if ui.cb_Ehliyet.isChecked() == True:
        _ehliyet = "Ehliyeti var"
    else:
        _ehliyet = "Ehliyeti yok"
    _ogrenim = ui.cmb_Egitim.currentText()
    _departman = ui.cmb_Departman.currentText()
    _calismasaat = ui.txt_Calisma_Saatleri.text()
    _maas = ui.txt_Maas_Bilgisi.text()
    _eposta = ui.txt_Posta.text()
    _telno = ui.txt_Tel.text()
    _adres = ui.txt_Adres.text()

    curs.execute("INSERT INTO Tablo     \
                         (TCNO,İSİM,SOYİSİM,DOGUM_TARİHİ,CİNSİYET,MEDENİ_HAL,ASKERLİK,EHLİYET,EĞİTİM,DEPARTMAN,CALISMA_SAATİ,MAAS,EPOSTA,TEL,ADRES)  \
                         VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", \
                         (_kimlik,_isim,_soyisim,_dogumtarihi,_cinsiyet,_medenihal,_askerlik,_ehliyet,_ogrenim,_departman,_calismasaat,_maas,_eposta,_telno,_adres))
    conn.commit()
    LİSTELE()
#----------------------------LİSTELE--------------------------#
#------------------------------------------------------------#
def LİSTELE():
    ui.Tablo.clear()
    ui.Tablo.setHorizontalHeaderLabels(('ID','TC NO','İSİM','SOYİSİM','DOĞUM TARİHİ','CİNSİYET','MEDENİ HAL','ASKERLİK','EHLİYET','EĞİTİM','DEPARTMAN','ÇALIŞMA SAATİ','MAAŞ','E_POSTA','TEL','ADRES'    ))
    ui.Tablo.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    curs.execute("SELECT* FROM Tablo")
    for satirIndeks,satirVeri in enumerate(curs):
        for sutunIndeks,sutunVeri in enumerate(satirVeri):
            ui.Tablo.setItem(satirIndeks,sutunIndeks,QTableWidgetItem(str(sutunVeri)))
    ui.txt_Kimlik.clear()
    ui.txt_Isim.clear()
    ui.txt_Soyisim.clear()
    ui.txt_Adres.clear()
    ui.txt_Tel.clear()
    ui.txt_Posta.clear()
    ui.txt_Maas_Bilgisi.clear()
    ui.txt_Calisma_Saatleri.clear()
    curs.execute("SELECT COUNT (*) FROM Tablo")
    kayitSayisi = curs.fetchone()
    ui.label_Adet.setText(str(kayitSayisi[0]))





LİSTELE()

#----------------------------ÇIKIŞ--------------------------#
#------------------------------------------------------------#
def CIKIS():
    cevap=QMessageBox.question(penAna,"ÇIKIŞ","Programdan çıkmak istediğinize emin misiniz?",\
                         QMessageBox.Yes |QMessageBox.No)
    if cevap==QMessageBox.Yes:
        conn.close()
        sys.exit(Uygulama.exec_())
    else:
        penAna.show()

#---------------------------SİL------------------------------#
#------------------------------------------------------------#
def SIL():
    cevap=QMessageBox.question(penAna,"KAYIT SİL","Kaydı silmek istediğinize emin misiniz ?",\
                         QMessageBox.Yes |QMessageBox.No)
    if cevap == QMessageBox.Yes:
        secili = ui.Tablo.selectedItems()
        silinecek = secili[1].text()
        try:
            curs.execute("DELETE FROM Tablo WHERE TCNO='%s'"%(silinecek))
            conn.commit()
            LİSTELE()
            ui.statusbar.showMessage("Kayıt silme işlemi başarılı.",10000)
        except Exception as Hata:
            ui.statusbar.showMessage("Şöyle bir hata ile karşılaşıldı : "+ str(Hata))
    else:
        ui.statusbar.showMessage("Silme işlemi iptal edildi ...",10000)

#---------------------------ARAMA------------------------------#
#------------------------------------------------------------#

def ARA():
    aranan1=ui.txt_Kimlik.text()
    aranan2=ui.txt_Isim.text()
    aranan3=ui.txt_Soyisim.text()
    aranan4=ui.txt_Id.text()
    curs.execute("SELECT * FROM Tablo WHERE TCNO=?  OR İSİM=? OR SOYİSİM=? OR (İSİM=? AND SOYİSİM=?)OR ID=?", \
                 (aranan1,aranan2,aranan3,aranan2,aranan3,aranan4))
    conn.commit()
    ui.Tablo.clear()
    for satirIndeks,satirVeri in enumerate(curs):
        for sutunIndeks,sutunVeri in enumerate(satirVeri):
            ui.Tablo.setItem(satirIndeks,sutunIndeks,QTableWidgetItem(str(sutunVeri)))

    secili = ui.Tablo.selectedItems()
    ui.txt_Kimlik.text





#---------------------------Bilgi Doldurma------------------------------#
#------------------------------------------------------------#

#---------------------------GUNCELLE------------------------------#
#------------------------------------------------------------#
def GUNCELLE():
    cevap = QMessageBox.question(penAna,"KAYIT GÜNCELLE","Kaydı güncellemek istediğinize emin misniz ?",
                                        QMessageBox.Yes | QMessageBox.No)
    if cevap==QMessageBox.Yes:
        try:
            secili=ui.Tablo.selectedItems()
            _Id = int(secili[0].text())
            _kimlik = ui.txt_Kimlik.text()
            _isim = ui.txt_Isim.text()
            _soyisim = ui.txt_Soyisim.text()
            _dogumtarihi = ui.cmb_Gun.currentText() + ui.cmb_Ay.currentText() + ui.cmb_Yil.currentText()
            if ui.rb_Erkek.isChecked() == True:
                _cinsiyet = "Erkek"
            else:
                _cinsiyet = "Kadın"
            if ui.rb_Bekar.isChecked() == True:
                _medenihal = "Bekar"
            else:
                _medenihal = "Evli"
            if ui.rb_Askerlik_yapildi.isChecked() == True:
                _askerlik = "Yapıldı"
            elif ui.rb_Askerlik_Tecilli.isChecked() == True:
                _askerlik = "Yapılmadı"
            else:
                _askerlik = "Muaf"
            if ui.cb_Ehliyet.isChecked() == True:
                _ehliyet = "Ehliyeti var"
            else:
                _ehliyet = "Ehliyeti yok"
            _ogrenim = ui.cmb_Egitim.currentText()
            _departman = ui.cmb_Departman.currentText()
            _calismasaat = ui.txt_Calisma_Saatleri.text()
            _maas = ui.txt_Maas_Bilgisi.text()
            _eposta = ui.txt_Posta.text()
            _telno = ui.txt_Tel.text()
            _adres = ui.txt_Adres.text()
            curs.execute("UPDATE Tablo SET TCNO=?,İSİM=?,SOYİSİM=?,DOGUM_TARİHİ=?,CİNSİYET=?,\
                         MEDENİ_HAL=?,ASKERLİK=?,EHLİYET=?,EĞİTİM=?,DEPARTMAN=?,CALISMA_SAATİ=?,MAAS=?,EPOSTA=?,TEL=?,ADRES=? WHERE ID=?", \
                         (_kimlik,_isim,_soyisim,_dogumtarihi,_cinsiyet,_medenihal,_askerlik,_ehliyet,_ogrenim,_departman,_calismasaat,_maas,_eposta,_telno,_adres,_Id))
            conn.commit()

            LİSTELE()

        except Exception as Hata:
            ui.statusbar.showMessage("Şöyle bir hata meydana geldi "+str(Hata))
    else:
        ui.statusbar.showMessage("Güncelleme iptal edildi",10000)


#----------------------------SİNYAL-SLOT--------------------------#
#------------------------------------------------------------#
ui.btn_Kayit_Ekle.clicked.connect(EKLE)
ui.btn_Kayit_Listele.clicked.connect(LİSTELE)
ui.btn_Cikis.clicked.connect(CIKIS)
ui.btn_Kayit_Sil.clicked.connect(SIL)
ui.btn_Kayit_Ara.clicked.connect(ARA)
ui.btn_Guncelle.clicked.connect(GUNCELLE)



sys.exit(Uygulama.exec_())
