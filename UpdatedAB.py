#   FIFA 18 Autobuyer called FIFA Engine by Seppe De Langhe

#   Using PyQt5, time, random and fut library
#   fut library = https://github.com/futapi/fut
#   
#   This is made by Seppe De Langhe
#   This program can not be used, sold or copied without my permission!

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
BIN = 0
SellMin = 0
SellMax = 0


#============================================================================================================================
# Fucntions

def SendUnassignedToTradepile( items ):
    for item in items:
        bot.sendToTradepile(item['id'])
        print("player added to tradepile!")

def SellInstantly( BID , BIN ):
    BoughtPlayer = bot.unassigned()
    idItem = BoughtPlayer['id']
    bot.sendToTradepile(-1, idItem)
    print( "Listing..." )
    bot.sell(idItem, BID , BIN , 3600)
                        
def UpdatePrice( ID , BIN , SellMin , SellMax , RPM , Min ):
    newBIN = BIN
    items = bot.searchAuctions(ctype="player", assetId=ID ,  max_buy=BIN )
    while (newBIN + ( items[0]['buyNowPrice']/20 ) ) >= items[0]['buyNowPrice']:
        print("Price update needed")     
        if newBIN > 100000:
            newBIN = newBIN - 1000
        elif newBIN > 50000:
            newBIN = newBIN - 500
        elif newBIN > 10000:
            newBIN = newBIN - 250
        elif newBIN > 1000:
            newBIN = newBIN - 100
        else:
            newBIN = newBIN - 50

    SnipeNow( ID , BIN , SellMin , SellMax , RPM , ((Min*60)-(150*RPM/60))/60 )


def SnipeNow( ID , BIN , SellMin , SellMax , RPM , Min , SellInst , AutoPrice , StartTime , OnError ):
    time.sleep( StartTime * 60 )
    while True:
        try:
            print("Searching for: {}, Coins: {} , RPM: {}" .format(BIN, bot.credits , RPM ))
            timeout = time.time() + 60*Min
            count = 0
            while True:
                if count == 150 and AutoPrice == True:
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
                            if SellInst == True:
                                SellInstantly( SellMin , SellMax )
                        except RuntimeError:
                            print('player already gone!')

                    else:
                        print( "Not enough coins, coins needed: {}" .format(item['buyNowPrice']))

                RandomHumanNum = random.randint( 1 , 3 ) / 10
                time.sleep( 60 / RPM + RandomHumanNum )
        except (RuntimeError, TypeError, NameError):
            if OnError == "Pause":
                print("An error occurred, taking a break for 5 min and retrying!")
                OnError = "Stop"
                time.sleep(300)
            else:
                print("An error occurred, stopping snipe proccess!")
                break;
            


    
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
    try:
        bot.logout()
        print("Logged out!")
    except NameError:
        print("Not logged in")


#============================================================================================================================
# UI


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(455, 405)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
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
        self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_3.setGeometry(QtCore.QRect(10, 130, 431, 251))
        self.groupBox_3.setObjectName("groupBox_3")
        self.PlayerID = QtWidgets.QLineEdit(self.groupBox_3)
        self.PlayerID.setGeometry(QtCore.QRect(92, 20, 231, 20))
        self.PlayerID.setObjectName("PlayerID")
        self.label_5 = QtWidgets.QLabel(self.groupBox_3)
        self.label_5.setGeometry(QtCore.QRect(20, 20, 47, 16))
        self.label_5.setObjectName("label_5")
        self.label_4 = QtWidgets.QLabel(self.groupBox_3)
        self.label_4.setGeometry(QtCore.QRect(360, 20, 41, 16))
        self.label_4.setObjectName("label_4")
        self.RPM = QtWidgets.QSlider(self.groupBox_3)
        self.RPM.setGeometry(QtCore.QRect(360, 50, 31, 191))
        self.RPM.setMinimum(1)
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
        self.SellBIN.setGeometry(QtCore.QRect(240, 70, 91, 16))
        self.SellBIN.setMinimum(200)
        self.SellBIN.setMaximum(15000000)
        self.SellBIN.setSingleStep(100)
        self.SellBIN.setObjectName("SellBIN")
        self.Label_Selel = QtWidgets.QLabel(self.groupBox_3)
        self.Label_Selel.setGeometry(QtCore.QRect(190, 70, 41, 16))
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
        self.SellNowCheck = QtWidgets.QCheckBox(self.groupBox_3)
        self.SellNowCheck.setGeometry(QtCore.QRect(260, 50, 81, 17))
        self.SellNowCheck.setObjectName("SellNowCheck")
        self.AutoPriceCheck = QtWidgets.QCheckBox(self.groupBox_3)
        self.AutoPriceCheck.setGeometry(QtCore.QRect(170, 50, 81, 17))
        self.AutoPriceCheck.setObjectName("AutoPriceCheck")
        self.ShedulerBox = QtWidgets.QGroupBox(self.groupBox_3)
        self.ShedulerBox.setGeometry(QtCore.QRect(10, 100, 321, 81))
        self.ShedulerBox.setObjectName("ShedulerBox")
        self.Minutes = QtWidgets.QSpinBox(self.ShedulerBox)
        self.Minutes.setGeometry(QtCore.QRect(80, 20, 42, 16))
        self.Minutes.setAlignment(QtCore.Qt.AlignCenter)
        self.Minutes.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.Minutes.setObjectName("Minutes")
        self.label_7 = QtWidgets.QLabel(self.ShedulerBox)
        self.label_7.setGeometry(QtCore.QRect(30, 20, 47, 13))
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.ShedulerBox)
        self.label_8.setGeometry(QtCore.QRect(130, 20, 41, 16))
        self.label_8.setObjectName("label_8")
        self.StopMinutes = QtWidgets.QSpinBox(self.ShedulerBox)
        self.StopMinutes.setGeometry(QtCore.QRect(80, 50, 42, 16))
        self.StopMinutes.setAlignment(QtCore.Qt.AlignCenter)
        self.StopMinutes.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.StopMinutes.setObjectName("StopMinutes")
        self.label_10 = QtWidgets.QLabel(self.ShedulerBox)
        self.label_10.setGeometry(QtCore.QRect(130, 50, 41, 16))
        self.label_10.setObjectName("label_10")
        self.StopAfterCheck = QtWidgets.QCheckBox(self.ShedulerBox)
        self.StopAfterCheck.setGeometry(QtCore.QRect(10, 50, 70, 17))
        self.StopAfterCheck.setObjectName("StopAfterCheck")
        self.label_9 = QtWidgets.QLabel(self.ShedulerBox)
        self.label_9.setGeometry(QtCore.QRect(220, 10, 47, 13))
        self.label_9.setObjectName("label_9")
        self.ErrorStopRadio = QtWidgets.QRadioButton(self.ShedulerBox)
        self.ErrorStopRadio.setGeometry(QtCore.QRect(200, 30, 82, 16))
        self.ErrorStopRadio.setObjectName("ErrorStopRadio")
        self.ErrorPauseRadio = QtWidgets.QRadioButton(self.ShedulerBox)
        self.ErrorPauseRadio.setGeometry(QtCore.QRect(200, 50, 82, 16))
        self.ErrorPauseRadio.setObjectName("ErrorPauseRadio")
        self.SnipeBTN = QtWidgets.QPushButton(self.groupBox_3)
        self.SnipeBTN.setGeometry(QtCore.QRect(10, 190, 321, 51))
        self.SnipeBTN.setObjectName("SnipeBTN")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

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
            #print("Coins availible to snipe = {}".format( bot.credits ))
            SellInst=False
            AutoPrice=False
            SleepTime = 0
            OnError = "Stop"
            print("vars set")
            if self.SellNowCheck.isChecked():
                SellInst = True
                print("Sell set")
            if self.AutoPriceCheck.isChecked():
                AutoPrice = True
                print("Auto set")
            if self.StopAfterCheck.isChecked():
                sleepTime = self.StopMinutes.value()
                print("Wait set")
            if self.ErrorPauseRadio.isChecked() == True:
                OnError = "Pause"
                print("Error set")
            SnipeNow( self.PlayerID.text() , self.BuyBIN.text() , self.SellBIN.text() , self.SellBIN.text() , self.RPM.value() , self.Minutes.value() , SellInst , AutoPrice , Wait , OnError )
            print("Done sniping...")

            

        self.LoginBTN.clicked.connect( login )
        self.SnipeBTN.clicked.connect( snipe )


#=========================================================================================================================================================================



    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "FIFA Engine"))
        MainWindow.setWindowIcon(QtGui.QIcon('icon.png'))
        self.groupBox.setTitle(_translate("MainWindow", "Account"))
        self.LoginBTN.setText(_translate("MainWindow", "Login"))
        self.label_2.setText(_translate("MainWindow", "Password:"))
        self.label_3.setText(_translate("MainWindow", "Security Answer:"))
        self.Check2Step.setText(_translate("MainWindow", "2 Step Verification?"))
        self.PlatformSelect.setItemText(0, _translate("MainWindow", "Playstation 4"))
        self.PlatformSelect.setItemText(1, _translate("MainWindow", "Playstation 3"))
        self.PlatformSelect.setItemText(2, _translate("MainWindow", "Xbox One"))
        self.PlatformSelect.setItemText(3, _translate("MainWindow", "Xbox 360"))
        self.PlatformSelect.setItemText(4, _translate("MainWindow", "PC"))
        self.label.setText(_translate("MainWindow", "Email:"))
        self.groupBox_3.setTitle(_translate("MainWindow", "Sniping settings"))
        self.label_5.setText(_translate("MainWindow", "Player ID:"))
        self.label_4.setText(_translate("MainWindow", "Speed:"))
        self.label_6.setText(_translate("MainWindow", "Buy for:"))
        self.Label_Selel.setText(_translate("MainWindow", "BIN sell:"))
        self.Label_Selel_2.setText(_translate("MainWindow", "Bid sell:"))
        self.SellNowCheck.setText(_translate("MainWindow", "Sell Instant"))
        self.AutoPriceCheck.setText(_translate("MainWindow", "Auto-update"))
        self.ShedulerBox.setTitle(_translate("MainWindow", "Scheduler"))
        self.label_7.setText(_translate("MainWindow", "Snipe for"))
        self.label_8.setText(_translate("MainWindow", "minutes"))
        self.label_10.setText(_translate("MainWindow", "minutes"))
        self.StopAfterCheck.setText(_translate("MainWindow", "Start after"))
        self.label_9.setText(_translate("MainWindow", "On Error:"))
        self.ErrorStopRadio.setText(_translate("MainWindow", "Stop"))
        self.ErrorPauseRadio.setText(_translate("MainWindow", "Pause 5 min"))
        self.SnipeBTN.setText(_translate("MainWindow", "Start sniping"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    ret = app.exec_()
    logmeout()
    sys.exit(ret)
