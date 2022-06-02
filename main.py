from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QPixmap
import cv2
import sys

qtcreator_file = "design.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtcreator_file)
file_path = ""

class designWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.parcourir.clicked.connect(self.get_image)
        self.afficheR.clicked.connect(self.showRedChannel)
        self.afficheV.clicked.connect(self.showGreenChannel)
        self.afficheB.clicked.connect(self.showBlueChannel)
        self.valid.clicked.connect(self.showNewImage)
        self.cntrValid.clicked.connect(self.showContour)

    def get_image(self):
        global file_path
        file_path, _ = QFileDialog.getOpenFileName(self, 'Open Image File', r"<Default dir>", "Image files (*.jpg *.jpeg *.png)")
        img = cv2.imread(file_path)
        img_Qt_format = self.convert_cv_qt(img)
        self.makeFigure('original', img_Qt_format)
        self.showDimensions(img)

    def convert_cv_qt(self, cv_image):
        """Convert from an opencv image to QPixmap"""
        h, w, ch = cv_image.shape
        bytes_per_line = ch * w
        cv_image_Qt_format = QtGui.QImage(cv_image.data, w, h, bytes_per_line, QtGui.QImage.Format_BGR888)
        return QPixmap.fromImage(cv_image_Qt_format)

    def makeFigure(self, widget_name, pixmap):

        pixmap = pixmap.scaled(self.findChild(QtWidgets.QLabel, widget_name).width(), self.findChild(QtWidgets.QLabel, widget_name).height())
        self.findChild(QtWidgets.QLabel, widget_name).setPixmap(pixmap)

    def showDimensions(self, img):
        height = str(img.shape[0])
        width = str(img.shape[1])
        channels = str(img.shape[2])
        outputMessage = "Hauteur:      "+height+"\n"+"Largeur:     "+width+"\n"+"Nombre de canaux:    "+channels
        self.dimension.setText(outputMessage)

    def showBlueChannel(self):
        img = cv2.imread(file_path)
        b = img.copy()
        b[:, :, 1] = 0
        b[:, :, 2] = 0
        b_QT_format = self.convert_cv_qt(b)
        self.makeFigure("compB", b_QT_format)

    def showRedChannel(self):
        img = cv2.imread(file_path)
        r = img.copy()
        r[:, :, 0] = 0
        r[:, :, 1] = 0
        r_QT_format = self.convert_cv_qt(r)
        self.makeFigure("compR", r_QT_format)

    def showGreenChannel(self):
        img = cv2.imread(file_path)
        g = img.copy()
        g[:, :, 0] = 0
        g[:, :, 2] = 0
        g_QT_format = self.convert_cv_qt(g)
        self.makeFigure("compV", g_QT_format)

    def showNewImage(self):
        img = cv2.imread(file_path)
        if self.rbYCC.isChecked():
            newImg = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
        elif self.rbYUV.isChecked():
            newImg = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
        elif self.rbHSV.isChecked():
            newImg = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        else:
            newImg = img.copy()
        cv2.imwrite("newImg.png", newImg)
        newImg_Qt_format = self.convert_cv_qt(newImg)
        self.makeFigure("labNvImg", newImg_Qt_format)

    def getFirstThreshold(self):
        if self.txtS1.toPlainText():
            Threshold = int(self.txtS1.toPlainText())
        else:
            Threshold = 127
        return Threshold

    def getSecondThreshold(self):
        if self.txtS2.toPlainText():
            Threshold = int(self.txtS2.toPlainText())
        else:
            Threshold = 255
        return Threshold

    def showContour(self):
        img = cv2.imread(file_path)
        firstTH = self.getFirstThreshold()
        secondTH = self.getSecondThreshold()

        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(img_gray, firstTH, secondTH, cv2.THRESH_BINARY)
        contours, hierarchy = cv2.findContours(image=thresh, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
        image_copy = img.copy()
        cv2.drawContours(image=image_copy, contours=contours, contourIdx=1, color=(0, 255, 0), thickness=2,
                         lineType=cv2.LINE_AA)
        image_copy_Qt_format = self.convert_cv_qt(image_copy)
        self.makeFigure("labImgCntr", image_copy_Qt_format)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = designWindow()
    window.show()
    sys.exit(app.exec_())