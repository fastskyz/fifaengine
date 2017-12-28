# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainGUI.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import fut
import time
import random


#============================================================================================================================
# Variables

mail = ""
pswd = ""
SQ = ""
platform = ""
players = []
Bins = []
SellMins = []
SellMaxs = []

#============================================================================================================================
# Fucntions







#------------------------------------------------

def SendUnassignedToTradepile( items ):
    for item in items:
        bot.sendToTradepile(item['id'])
        print("player added to tradepile!")

def SellInstantly( Bid, BIN):
    BoughtPlayer = bot.unassigned()
    idItem = BoughtPlayer['id']
    bot.sendToTradepile(-1, idItem)
    print( "Listing..." )
    bot.sell(idItem, SellMin, SellMax, 3600)
                        
def UpdatePrice( ID , BIN , SellMin , SellMax , RPM , Min ):
    items = bot.searchAuctions(ctype="player", assetId=ID ,  max_buy=BIN )
    if items[0]['buyNowPrice'] <= BIN:
        if items[1]['buyNowPrice'] <= BIN:
            print("Price Update needed")
            while (BIN + ( items[0]['buyNowPrice']/20 ) ) >= items[0]['buyNowPrice']:
                if BIN > 10000:
                    BIN = BIN - 250
                else:
                    BIN = BIN - 100

    SnipeNow( ID , BIN , SellMin , SellMax , RPM , ((Min*60)-(150*RPM/60))/60 )


def SnipeNow( ID , BIN , SellMin , SellMax , RPM , Min ):
        print("Searching for: {}, Coins: {} , RPM: {}" .format(BIN, bot.credits , RPM ))
        timeout = time.time() + 60*Min
        count = 1
        while True:
            if count == 150:
                UpdatePrice( ID , BIN , SellMin , SellMax , RPM , Min )
                break;
            count = count + 1
            test = 0
            coins = bot.credits
            if coins < 1000 or test == 5 or time.time() > timeout:
                break; 
            test = test - 1
            items = bot.searchAuctions(ctype="player", assetId=ID ,  max_buy=BIN)
            for item in items:
                if coins > item['buyNowPrice']:
                    try:
                        bot.bid(item['tradeId'], item['buyNowPrice'])
                        print ("Found: {} for {}, Maxtime: {}" .format(item['tradeId'], item['buyNowPrice'], item['expires']))
                        if SellMin > 0:
                            SellInstantly( SellMin , SellMax )
                    except RuntimeError:
                        print('player already gone!')

                else:
                    print( "Not enough coins, coins needed: {}" .format(item['buyNowPrice']))

            RandomHumanNum = random.randint( 1 , 3 ) / 10
            time.sleep( 60 / RPM + RandomHumanNum )


    
def sendLoginRequest(mail , pswd , SQ , platform, TwoStep ):
    sms=TwoStep
    print("Logging in using: {} , platform: {} , 2 Step verification: {}" .format(mail , platform , sms ))
    global bot
    bot = fut.Core(mail , pswd , SQ , platform )
    time.sleep(2)
    coins = bot.credits
    print("Coins = {}".format(str(coins)))
    items = bot.unassigned()
    SendUnassignedToTradepile(items)





def logmeout():
    bot.logout()
    print("Logged out!")


#============================================================================================================================
# UI


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(800, 579)
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 431, 111))
        self.groupBox.setSizeIncrement(QtCore.QSize(0, 0))
        self.groupBox.setBaseSize(QtCore.QSize(0, 0))
        self.groupBox.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.groupBox.setObjectName("groupBox")
        self.LoginBTN = QtWidgets.QPushButton(self.groupBox)
        self.LoginBTN.setGeometry(QtCore.QRect(300, 80, 121, 23))
        self.LoginBTN.setCheckable(False)
        self.LoginBTN.setObjectName("LoginBTN")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(10, 50, 47, 13))
        self.label_2.setTextFormat(QtCore.Qt.PlainText)
        self.label_2.setObjectName("label_2")
        self.MailTXT = QtWidgets.QLineEdit(self.groupBox)
        self.MailTXT.setGeometry(QtCore.QRect(100, 20, 191, 20))
        self.MailTXT.setObjectName("MailTXT")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(10, 80, 81, 16))
        self.label_3.setTextFormat(QtCore.Qt.PlainText)
        self.label_3.setObjectName("label_3")
        self.Check2Step = QtWidgets.QCheckBox(self.groupBox)
        self.Check2Step.setGeometry(QtCore.QRect(300, 20, 121, 21))
        self.Check2Step.setObjectName("Check2Step")
        self.PswdTXT = QtWidgets.QLineEdit(self.groupBox)
        self.PswdTXT.setGeometry(QtCore.QRect(100, 50, 191, 20))
        self.PswdTXT.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedKingdom))
        self.PswdTXT.setText("")
        self.PswdTXT.setEchoMode(QtWidgets.QLineEdit.Password)
        self.PswdTXT.setObjectName("PswdTXT")
        self.PlatformSelect = QtWidgets.QComboBox(self.groupBox)
        self.PlatformSelect.setGeometry(QtCore.QRect(300, 50, 121, 22))
        self.PlatformSelect.setObjectName("PlatformSelect")
        self.PlatformSelect.addItem("")
        self.PlatformSelect.addItem("")
        self.PlatformSelect.addItem("")
        self.PlatformSelect.addItem("")
        self.PlatformSelect.addItem("")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(10, 20, 47, 13))
        self.label.setTextFormat(QtCore.Qt.PlainText)
        self.label.setObjectName("label")
        self.SQTXT = QtWidgets.QLineEdit(self.groupBox)
        self.SQTXT.setGeometry(QtCore.QRect(100, 80, 191, 20))
        self.SQTXT.setObjectName("SQTXT")
        self.groupBox_3 = QtWidgets.QGroupBox(Dialog)
        self.groupBox_3.setGeometry(QtCore.QRect(450, 10, 341, 561))
        self.groupBox_3.setObjectName("groupBox_3")
        self.PlayerID = QtWidgets.QLineEdit(self.groupBox_3)
        self.PlayerID.setGeometry(QtCore.QRect(92, 20, 231, 20))
        self.PlayerID.setObjectName("PlayerID")
        self.label_5 = QtWidgets.QLabel(self.groupBox_3)
        self.label_5.setGeometry(QtCore.QRect(20, 20, 47, 16))
        self.label_5.setObjectName("label_5")
        self.label_4 = QtWidgets.QLabel(self.groupBox_3)
        self.label_4.setGeometry(QtCore.QRect(290, 200, 41, 16))
        self.label_4.setObjectName("label_4")
        self.RPM = QtWidgets.QSlider(self.groupBox_3)
        self.RPM.setGeometry(QtCore.QRect(290, 230, 31, 261))
        self.RPM.setMaximum(30)
        self.RPM.setProperty("value", 12)
        self.RPM.setOrientation(QtCore.Qt.Vertical)
        self.RPM.setObjectName("RPM")
        self.BuyBIN = QtWidgets.QSpinBox(self.groupBox_3)
        self.BuyBIN.setGeometry(QtCore.QRect(70, 50, 91, 16))
        self.BuyBIN.setMinimum(200)
        self.BuyBIN.setMaximum(15000000)
        self.BuyBIN.setSingleStep(100)
        self.BuyBIN.setObjectName("BuyBIN")
        self.label_6 = QtWidgets.QLabel(self.groupBox_3)
        self.label_6.setGeometry(QtCore.QRect(20, 50, 41, 16))
        self.label_6.setObjectName("label_6")
        self.SellBIN = QtWidgets.QSpinBox(self.groupBox_3)
        self.SellBIN.setGeometry(QtCore.QRect(230, 70, 91, 16))
        self.SellBIN.setMinimum(200)
        self.SellBIN.setMaximum(15000000)
        self.SellBIN.setSingleStep(100)
        self.SellBIN.setObjectName("SellBIN")
        self.Label_Selel = QtWidgets.QLabel(self.groupBox_3)
        self.Label_Selel.setGeometry(QtCore.QRect(170, 70, 41, 16))
        self.Label_Selel.setObjectName("Label_Selel")
        self.SellBid = QtWidgets.QSpinBox(self.groupBox_3)
        self.SellBid.setGeometry(QtCore.QRect(70, 70, 91, 16))
        self.SellBid.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
        self.SellBid.setMinimum(150)
        self.SellBid.setMaximum(15000000)
        self.SellBid.setSingleStep(100)
        self.SellBid.setObjectName("SellBid")
        self.Label_Selel_2 = QtWidgets.QLabel(self.groupBox_3)
        self.Label_Selel_2.setGeometry(QtCore.QRect(20, 70, 41, 16))
        self.Label_Selel_2.setObjectName("Label_Selel_2")
        self.SellInstant = QtWidgets.QCheckBox(self.groupBox_3)
        self.SellInstant.setGeometry(QtCore.QRect(250, 50, 81, 17))
        self.SellInstant.setObjectName("SellInstant")
        self.AutoUpdate = QtWidgets.QCheckBox(self.groupBox_3)
        self.AutoUpdate.setGeometry(QtCore.QRect(170, 50, 81, 17))
        self.AutoUpdate.setObjectName("AutoUpdate")
        self.groupBox_4 = QtWidgets.QGroupBox(self.groupBox_3)
        self.groupBox_4.setGeometry(QtCore.QRect(10, 100, 321, 81))
        self.groupBox_4.setObjectName("groupBox_4")
        self.SnipeMin = QtWidgets.QSpinBox(self.groupBox_4)
        self.SnipeMin.setGeometry(QtCore.QRect(80, 20, 42, 16))
        self.SnipeMin.setAlignment(QtCore.Qt.AlignCenter)
        self.SnipeMin.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.SnipeMin.setObjectName("SnipeMin")
        self.label_7 = QtWidgets.QLabel(self.groupBox_4)
        self.label_7.setGeometry(QtCore.QRect(30, 20, 47, 13))
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.groupBox_4)
        self.label_8.setGeometry(QtCore.QRect(130, 20, 41, 16))
        self.label_8.setObjectName("label_8")
        self.StopMin = QtWidgets.QSpinBox(self.groupBox_4)
        self.StopMin.setGeometry(QtCore.QRect(80, 40, 42, 16))
        self.StopMin.setAlignment(QtCore.Qt.AlignCenter)
        self.StopMin.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.StopMin.setObjectName("StopMin")
        self.label_10 = QtWidgets.QLabel(self.groupBox_4)
        self.label_10.setGeometry(QtCore.QRect(130, 40, 41, 16))
        self.label_10.setObjectName("label_10")
        self.StartMin = QtWidgets.QSpinBox(self.groupBox_4)
        self.StartMin.setGeometry(QtCore.QRect(80, 60, 42, 16))
        self.StartMin.setAlignment(QtCore.Qt.AlignCenter)
        self.StartMin.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.StartMin.setObjectName("StartMin")
        self.label_12 = QtWidgets.QLabel(self.groupBox_4)
        self.label_12.setGeometry(QtCore.QRect(130, 60, 41, 16))
        self.label_12.setObjectName("label_12")
        self.StartSnipeCheck = QtWidgets.QCheckBox(self.groupBox_4)
        self.StartSnipeCheck.setGeometry(QtCore.QRect(10, 60, 70, 17))
        self.StartSnipeCheck.setObjectName("StartSnipeCheck")
        self.StopSnipeCheck = QtWidgets.QCheckBox(self.groupBox_4)
        self.StopSnipeCheck.setGeometry(QtCore.QRect(10, 40, 70, 17))
        self.StopSnipeCheck.setObjectName("StopSnipeCheck")
        self.label_9 = QtWidgets.QLabel(self.groupBox_4)
        self.label_9.setGeometry(QtCore.QRect(220, 10, 47, 13))
        self.label_9.setObjectName("label_9")
        self.RadioErrorStop = QtWidgets.QRadioButton(self.groupBox_4)
        self.RadioErrorStop.setGeometry(QtCore.QRect(200, 30, 82, 17))
        self.RadioErrorStop.setObjectName("RadioErrorStop")
        self.RadioErrorPause = QtWidgets.QRadioButton(self.groupBox_4)
        self.RadioErrorPause.setGeometry(QtCore.QRect(200, 50, 82, 17))
        self.RadioErrorPause.setObjectName("RadioErrorPause")
        self.groupBox_5 = QtWidgets.QGroupBox(self.groupBox_3)
        self.groupBox_5.setGeometry(QtCore.QRect(10, 190, 261, 301))
        self.groupBox_5.setAutoFillBackground(False)
        self.groupBox_5.setObjectName("groupBox_5")
        self.CheckPlayer1 = QtWidgets.QCheckBox(self.groupBox_5)
        self.CheckPlayer1.setGeometry(QtCore.QRect(10, 30, 70, 17))
        self.CheckPlayer1.setObjectName("CheckPlayer1")
        self.PlayerID1 = QtWidgets.QLineEdit(self.groupBox_5)
        self.PlayerID1.setGeometry(QtCore.QRect(80, 30, 161, 20))
        self.PlayerID1.setObjectName("PlayerID1")
        self.Label_Selel_3 = QtWidgets.QLabel(self.groupBox_5)
        self.Label_Selel_3.setGeometry(QtCore.QRect(10, 80, 41, 16))
        self.Label_Selel_3.setObjectName("Label_Selel_3")
        self.BuyBIN_2 = QtWidgets.QSpinBox(self.groupBox_5)
        self.BuyBIN_2.setGeometry(QtCore.QRect(60, 60, 91, 16))
        self.BuyBIN_2.setMinimum(200)
        self.BuyBIN_2.setMaximum(15000000)
        self.BuyBIN_2.setSingleStep(100)
        self.BuyBIN_2.setObjectName("BuyBIN_2")
        self.SellBIN_2 = QtWidgets.QSpinBox(self.groupBox_5)
        self.SellBIN_2.setGeometry(QtCore.QRect(160, 80, 91, 16))
        self.SellBIN_2.setMinimum(200)
        self.SellBIN_2.setMaximum(15000000)
        self.SellBIN_2.setSingleStep(100)
        self.SellBIN_2.setObjectName("SellBIN_2")
        self.Label_Selel_4 = QtWidgets.QLabel(self.groupBox_5)
        self.Label_Selel_4.setGeometry(QtCore.QRect(160, 60, 41, 16))
        self.Label_Selel_4.setObjectName("Label_Selel_4")
        self.SellBid_2 = QtWidgets.QSpinBox(self.groupBox_5)
        self.SellBid_2.setGeometry(QtCore.QRect(60, 80, 91, 16))
        self.SellBid_2.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
        self.SellBid_2.setMinimum(150)
        self.SellBid_2.setMaximum(15000000)
        self.SellBid_2.setSingleStep(100)
        self.SellBid_2.setObjectName("SellBid_2")
        self.label_11 = QtWidgets.QLabel(self.groupBox_5)
        self.label_11.setGeometry(QtCore.QRect(10, 60, 41, 16))
        self.label_11.setObjectName("label_11")
        self.Label_Selel_7 = QtWidgets.QLabel(self.groupBox_5)
        self.Label_Selel_7.setGeometry(QtCore.QRect(160, 160, 41, 16))
        self.Label_Selel_7.setObjectName("Label_Selel_7")
        self.PlayerID2 = QtWidgets.QLineEdit(self.groupBox_5)
        self.PlayerID2.setGeometry(QtCore.QRect(80, 130, 161, 20))
        self.PlayerID2.setObjectName("PlayerID2")
        self.BuyBIN_3 = QtWidgets.QSpinBox(self.groupBox_5)
        self.BuyBIN_3.setGeometry(QtCore.QRect(60, 160, 91, 16))
        self.BuyBIN_3.setMinimum(200)
        self.BuyBIN_3.setMaximum(15000000)
        self.BuyBIN_3.setSingleStep(100)
        self.BuyBIN_3.setObjectName("BuyBIN_3")
        self.Label_Selel_8 = QtWidgets.QLabel(self.groupBox_5)
        self.Label_Selel_8.setGeometry(QtCore.QRect(10, 180, 41, 16))
        self.Label_Selel_8.setObjectName("Label_Selel_8")
        self.SellBid_3 = QtWidgets.QSpinBox(self.groupBox_5)
        self.SellBid_3.setGeometry(QtCore.QRect(60, 180, 91, 16))
        self.SellBid_3.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
        self.SellBid_3.setMinimum(150)
        self.SellBid_3.setMaximum(15000000)
        self.SellBid_3.setSingleStep(100)
        self.SellBid_3.setObjectName("SellBid_3")
        self.SellBIN_3 = QtWidgets.QSpinBox(self.groupBox_5)
        self.SellBIN_3.setGeometry(QtCore.QRect(160, 180, 91, 16))
        self.SellBIN_3.setMinimum(200)
        self.SellBIN_3.setMaximum(15000000)
        self.SellBIN_3.setSingleStep(100)
        self.SellBIN_3.setObjectName("SellBIN_3")
        self.label_14 = QtWidgets.QLabel(self.groupBox_5)
        self.label_14.setGeometry(QtCore.QRect(10, 160, 41, 16))
        self.label_14.setObjectName("label_14")
        self.CheckPlayer2 = QtWidgets.QCheckBox(self.groupBox_5)
        self.CheckPlayer2.setGeometry(QtCore.QRect(10, 130, 70, 17))
        self.CheckPlayer2.setObjectName("CheckPlayer2")
        self.Label_Selel_9 = QtWidgets.QLabel(self.groupBox_5)
        self.Label_Selel_9.setGeometry(QtCore.QRect(160, 250, 41, 16))
        self.Label_Selel_9.setObjectName("Label_Selel_9")
        self.PlayerID3 = QtWidgets.QLineEdit(self.groupBox_5)
        self.PlayerID3.setGeometry(QtCore.QRect(80, 220, 161, 20))
        self.PlayerID3.setObjectName("PlayerID3")
        self.BuyBIN_4 = QtWidgets.QSpinBox(self.groupBox_5)
        self.BuyBIN_4.setGeometry(QtCore.QRect(60, 250, 91, 16))
        self.BuyBIN_4.setMinimum(200)
        self.BuyBIN_4.setMaximum(15000000)
        self.BuyBIN_4.setSingleStep(100)
        self.BuyBIN_4.setObjectName("BuyBIN_4")
        self.Label_Selel_10 = QtWidgets.QLabel(self.groupBox_5)
        self.Label_Selel_10.setGeometry(QtCore.QRect(10, 270, 41, 16))
        self.Label_Selel_10.setObjectName("Label_Selel_10")
        self.SellBid_4 = QtWidgets.QSpinBox(self.groupBox_5)
        self.SellBid_4.setGeometry(QtCore.QRect(60, 270, 91, 16))
        self.SellBid_4.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
        self.SellBid_4.setMinimum(150)
        self.SellBid_4.setMaximum(15000000)
        self.SellBid_4.setSingleStep(100)
        self.SellBid_4.setObjectName("SellBid_4")
        self.SellBIN_4 = QtWidgets.QSpinBox(self.groupBox_5)
        self.SellBIN_4.setGeometry(QtCore.QRect(160, 270, 91, 16))
        self.SellBIN_4.setMinimum(200)
        self.SellBIN_4.setMaximum(15000000)
        self.SellBIN_4.setSingleStep(100)
        self.SellBIN_4.setObjectName("SellBIN_4")
        self.label_15 = QtWidgets.QLabel(self.groupBox_5)
        self.label_15.setGeometry(QtCore.QRect(10, 250, 41, 16))
        self.label_15.setObjectName("label_15")
        self.CheckPlayer3 = QtWidgets.QCheckBox(self.groupBox_5)
        self.CheckPlayer3.setGeometry(QtCore.QRect(10, 220, 70, 17))
        self.CheckPlayer3.setObjectName("CheckPlayer3")
        self.line = QtWidgets.QFrame(self.groupBox_5)
        self.line.setGeometry(QtCore.QRect(0, 105, 261, 21))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.line_2 = QtWidgets.QFrame(self.groupBox_5)
        self.line_2.setGeometry(QtCore.QRect(0, 200, 261, 21))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.SnipeBTN = QtWidgets.QPushButton(self.groupBox_3)
        self.SnipeBTN.setGeometry(QtCore.QRect(10, 500, 321, 51))
        self.SnipeBTN.setObjectName("SnipeBTN")
        self.groupBox_2 = QtWidgets.QGroupBox(Dialog)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 120, 431, 451))
        self.groupBox_2.setObjectName("groupBox_2")
        self.textBrowser = QtWidgets.QTextBrowser(self.groupBox_2)
        self.textBrowser.setGeometry(QtCore.QRect(10, 20, 411, 421))
        self.textBrowser.setObjectName("textBrowser")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        #============================================================================================================================
        # Button triggers
        
        def login():
            mail = self.MailTXT.text()
            pswd = self.PswdTXT.text()
            SQ = self.SQTXT.text()
            sms=False
            if str(self.PlatformSelect.currentText()) == "Playstation 4":
                platform = "ps4"
            elif str(self.PlatformSelect.currentText()) == "Playstation 3":
                platform = "ps3"
            elif str(self.PlatformSelect.currentText()) == "Xbox One":
                platform = "xbox"
            elif str(self.PlatformSelect.currentText()) == "Xbox 360":
                platform = "xbox360"
            else:
                platform = "pc"
            if self.Check2Step.isChecked() == True:
                sms=True
            
            sendLoginRequest( mail , pswd , SQ , platform, sms )

        def snipe():
            print("Coins availible to snipe = {}".format( bot.credits ))
            if self.CheckPlayer1.isChecked() == False:
                SellMin = self.SellBid.text()
                if self.SellInstant.isChecked() == False:
                    SellMin = 0
                SnipeNow( self.PlayerID.text() , self.BuyBIN.text() , SellMin , self.SellBIN.text() , self.RPM.value() , self.SnipeMin.value() )
            else: 
                players[0] = self.PlayerID1.text()
                Bins[0] = self.BuyBIN1.text()
                SellMins[0] = self.SellBid1.text()
                SellMaxs[0] = self.SellBIN.text()
                if self.CheckPlayer2.isChecked() == True:
                    players[1] = self.PlayerID2.text()
                    Bins[1] = self.BuyBIN2.text()
                    SellMins[1] = self.SellBid2.text()
                    SellMaxs[1] = self.SellBIN2.text()
                    if self.CheckPlayer3.isChecked() == True:
                        players[2] = self.PlayerID3.text()
                        Bins[2] = self.BuyBIN3.text()
                        SellMins[2] = self.SellBid3.text()
                        SellMaxs[2] = self.SellBIN3.text()
            print("Done sniping...")

            

        self.LoginBTN.clicked.connect( login )
        self.SnipeBTN.clicked.connect( snipe )


#=========================================================================================================================================================================

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "FIFA 18 Autobuyer"))
        Dialog.setWindowIcon(QtGui.QIcon('icon.png'))
        self.groupBox.setTitle(_translate("Dialog", "Login Form"))
        self.LoginBTN.setText(_translate("Dialog", "Login"))
        self.label_2.setText(_translate("Dialog", "Password:"))
        # easy login while coding
        self.MailTXT.setText(_translate("Dialog", "email"))
        self.PswdTXT.setText(_translate("Dialog", "password"))
        self.SQTXT.setText(_translate("Dialog", "SQ"))
        self.label_3.setText(_translate("Dialog", "Security Answer:"))
        self.Check2Step.setText(_translate("Dialog", "2 Step Verification?"))
        self.PlatformSelect.setItemText(0, _translate("Dialog", "Playstation 4"))
        self.PlatformSelect.setItemText(1, _translate("Dialog", "Playstation 3"))
        self.PlatformSelect.setItemText(2, _translate("Dialog", "Xbox One"))
        self.PlatformSelect.setItemText(3, _translate("Dialog", "Xbox 360"))
        self.PlatformSelect.setItemText(4, _translate("Dialog", "PC"))
        self.label.setText(_translate("Dialog", "Email:"))
        self.groupBox_3.setTitle(_translate("Dialog", "Sniping settings"))
        self.label_5.setText(_translate("Dialog", "Player ID:"))
        self.label_4.setText(_translate("Dialog", "Speed:"))
        self.label_6.setText(_translate("Dialog", "Buy for:"))
        self.Label_Selel.setText(_translate("Dialog", "BIN sell:"))
        self.Label_Selel_2.setText(_translate("Dialog", "Bid sell:"))
        self.SellInstant.setText(_translate("Dialog", "Sell Instant"))
        self.AutoUpdate.setText(_translate("Dialog", "Auto-update"))
        self.groupBox_4.setTitle(_translate("Dialog", "Scheduler"))
        self.label_7.setText(_translate("Dialog", "Snipe for"))
        self.label_8.setText(_translate("Dialog", "minutes"))
        self.label_10.setText(_translate("Dialog", "minutes"))
        self.label_12.setText(_translate("Dialog", "minutes"))
        self.StartSnipeCheck.setText(_translate("Dialog", "Start after"))
        self.StopSnipeCheck.setText(_translate("Dialog", "Stop after"))
        self.label_9.setText(_translate("Dialog", "On Error:"))
        self.RadioErrorStop.setText(_translate("Dialog", "Stop"))
        self.RadioErrorPause.setText(_translate("Dialog", "Pause 5 min"))
        self.groupBox_5.setTitle(_translate("Dialog", "Multiple players"))
        self.CheckPlayer1.setText(_translate("Dialog", "Player ID:"))
        self.Label_Selel_3.setText(_translate("Dialog", "Bid sell:"))
        self.Label_Selel_4.setText(_translate("Dialog", "BIN sell:"))
        self.label_11.setText(_translate("Dialog", "Buy for:"))
        self.Label_Selel_7.setText(_translate("Dialog", "BIN sell:"))
        self.Label_Selel_8.setText(_translate("Dialog", "Bid sell:"))
        self.label_14.setText(_translate("Dialog", "Buy for:"))
        self.CheckPlayer2.setText(_translate("Dialog", "Player ID:"))
        self.Label_Selel_9.setText(_translate("Dialog", "BIN sell:"))
        self.Label_Selel_10.setText(_translate("Dialog", "Bid sell:"))
        self.label_15.setText(_translate("Dialog", "Buy for:"))
        self.CheckPlayer3.setText(_translate("Dialog", "Player ID:"))
        self.SnipeBTN.setText(_translate("Dialog", "Start sniping"))
        self.groupBox_2.setTitle(_translate("Dialog", "Settings"))
        self.textBrowser.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Logs here........................</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))









#============================================================================================================================
# other stuff

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

