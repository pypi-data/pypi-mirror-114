from PySide2 import QtCore
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from library.library import call_blend
# from library import call_blend
from filters import *
import sys
import os
import wsl


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(0, 0, 1300, 800)
        self.setMinimumHeight(250)
        self.setMinimumWidth(250)
        self.setMaximumHeight(1000)
        self.setMaximumWidth(1000)
        self.images_selected = {"image1": False, "image2": False}
        self.current_button = QRadioButton()
        self.setWindowTitle("PhotoBlend")
        self.buttons()
        self.radio_buttons()
        self.setIcon()

        self.images_selected = {"image1": False, "image2": False}

        # persistence
        cwd = os.getcwd()

        filename = "persistentData.txt"
        self.persistentData = cwd + "/" + filename

        # check if persistent data exists. If not, create file for it.
        if not os.path.exists(filename):
            open(filename, 'w').close()

        self.labels()
        self.show()

    def labels(self):
        if not self.images_selected["image1"] or not self.images_selected["image2"]:
            self.default_pane_label = QLabel(self)
            self.default_pane_label.setStyleSheet("border: 1px solid black")
            self.default_pane_label.setGeometry(300, 60, 675, 675)

        elif self.images_selected["image1"] and self.images_selected["image2"]:
            self.default_pane_label.clear()
            self.default_pane_label.setVisible(False)

            self.layer1_label = QLabel(self)
            self.layer1_label.setText("First Layer")
            self.layer1_label.setStyleSheet(
                "border-bottom-width: 1px; border-bottom-style: solid;border-radius: 0px; border-color: black;")
            self.layer1_label.setGeometry(390, 25, 70, 25)
            self.layer1_label.setVisible(True)

            self.pane_label1 = QLabel(self)
            self.pane_label1.setStyleSheet("border: 1px solid black")
            self.pane_label1.setGeometry(300, 60, 250, 250)
            self.pane_label1.setPixmap(
                self.pixmap1.scaled(self.pane_label1.width(), self.pane_label1.height(), QtCore.Qt.KeepAspectRatio))
            self.pane_label1.setVisible(True)

            self.layer2_label = QLabel(self)
            self.layer2_label.setText("Second Layer")
            self.layer2_label.setStyleSheet(
                "border-bottom-width: 1px; border-bottom-style: solid;border-radius: 0px; border-color: black;")
            self.layer2_label.setGeometry(815, 25, 85, 25)
            self.layer2_label.setVisible(True)

            self.pane_label2 = QLabel(self)
            self.pane_label2.setStyleSheet("border: 1px solid black")
            self.pane_label2.setGeometry(725, 60, 250, 250)
            self.pane_label2.setPixmap(
                self.pixmap2.scaled(self.pane_label2.width(), self.pane_label2.height(), QtCore.Qt.KeepAspectRatio))
            self.pane_label2.setVisible(True)

            self.result_label = QLabel(self)
            self.result_label.setText("Blend Result")
            self.result_label.setStyleSheet(
                "border-bottom-width: 1px; border-bottom-style: solid;border-radius: 0px; border-color: black;")
            self.result_label.setGeometry(590, 325, 85, 25)
            self.result_label.setVisible(True)

            self.pane_label3 = QLabel(self)
            self.pane_label3.setStyleSheet("border: 1px solid black")
            self.pane_label3.setGeometry(435, 355, 400, 400)
            self.pane_label3.setVisible(True)

        self.preview_label = QLabel(self)
        self.preview_label.setText("Image Preview")
        self.preview_label.setStyleSheet(
            "border-bottom-width: 1px; border-bottom-style: solid;border-radius: 0px; border-color: black;")
        self.preview_label.setGeometry(590, 10, 95, 25)

        self.blend_label = QLabel(self)
        self.blend_label.setText("First Layer")
        self.blend_label.setStyleSheet(
            "border-bottom-width: 1px; border-bottom-style: solid;border-radius: 0px; border-color: black;")
        self.blend_label.setGeometry(10, 10, 70, 30)

        self.blend_label = QLabel(self)
        self.blend_label.setText("Second Layer")
        self.blend_label.setStyleSheet(
            "border-bottom-width: 1px; border-bottom-style: solid;border-radius: 0px; border-color: black;")
        self.blend_label.setGeometry(10, 295, 90, 30)

        self.path_label = QLabel(self)
        self.path_label.setText("Previously Saved Image: " + self.get_previous_file())
        text_length = len("Previously Saved Image: " + self.get_previous_file())
        self.path_label.setGeometry(655 - (8 * text_length/2),770,(text_length * 8),30)

        self.modes_label = QLabel(self)
        self.modes_label.setText("Single Image Filters")
        self.modes_label.setStyleSheet(
            "border-bottom-width: 1px; border-bottom-style: solid;border-radius: 0px; border-color: black;")
        self.modes_label.setGeometry(10, 95, 125, 30)

        self.rotation_label = QLabel(self)
        self.rotation_label.setText("Other Options")
        self.rotation_label.setStyleSheet(
            "border-bottom-width: 1px; border-bottom-style: solid;border-radius: 0px; border-color: black;")
        self.rotation_label.setGeometry(10, 620, 100, 30)

        self.options_label = QLabel(self)
        self.options_label.setText("Blending Modes")
        self.options_label.setStyleSheet(
            "border-bottom-width: 1px; border-bottom-style: solid;border-radius: 0px; border-color: black;")
        self.options_label.setGeometry(10, 380, 100, 30)

    def buttons(self):
        self.file_select1 = QPushButton("Image Select", self)
        self.file_select1.setGeometry(10, 55, 150, 30)
        self.file_select1.clicked.connect(self.image1_clicked)

        self.file_select2 = QPushButton("Image Select", self)
        self.file_select2.setGeometry(10, 340, 150, 30)
        self.file_select2.clicked.connect(self.image2_clicked)

        self.rotate_button = QPushButton("Rotate", self)
        self.rotate_button.setText("Rotate 90\N{DEGREE SIGN}")
        self.rotate_button.setGeometry(10, 660, 150, 30)
        self.rotate_button.clicked.connect(self.rotate_clicked)

        self.clear_button = QPushButton("Clear", self)
        self.clear_button.setGeometry(10, 700, 150, 30)
        self.clear_button.clicked.connect(self.clear_clicked)

        self.save_button = QPushButton("Save Image", self)
        self.save_button.setGeometry(10, 740, 150, 30)
        self.save_button.clicked.connect(self.save_clicked)

    #Follow same format here when adding new radio button
    def radio_buttons(self):
        self.add_radio_button = QRadioButton(self, "Add")
        self.add_radio_button.setText("Add")
        self.add_radio_button.setGeometry(10, 420, 95, 30)
        self.add_radio_button.setToolTip('Addition of tonal values')
        self.add_radio_button.clicked.connect(self.update_blend_radio_buttons)

        self.subtract_radio_button = QRadioButton(self, "Subtract")
        self.subtract_radio_button.setText("Subtract")
        self.subtract_radio_button.setGeometry(80, 420, 95, 30)
        self.subtract_radio_button.setToolTip('Subtracts pixel values from image 1')
        self.subtract_radio_button.clicked.connect(self.update_blend_radio_buttons)

        self.mult_radio_button = QRadioButton(self, "Multiply")
        self.mult_radio_button.setText("Multiply")
        self.mult_radio_button.setGeometry(180, 420, 95, 30)
        self.mult_radio_button.setToolTip('Multiplies tonal values of the fore and background''s pixels')
        self.mult_radio_button.clicked.connect(self.update_blend_radio_buttons)

        self.screen_radio_button = QRadioButton(self, "Screen")
        self.screen_radio_button.setText("Screen")
        self.screen_radio_button.setGeometry(10, 470, 95, 30)
        self.screen_radio_button.setToolTip('Fore and background are negatively multiplied')
        self.screen_radio_button.clicked.connect(self.update_blend_radio_buttons)

        # self.opacity_radio_button = QRadioButton(self, "Opacity")
        # self.opacity_radio_button.setText("50% Opacity")
        # self.opacity_radio_button.setGeometry(210, 470, 95, 30)
        # self.opacity_radio_button.setToolTip('80% Transparency mode')
        # self.opacity_radio_button.clicked.connect(self.update_blend_radio_buttons)

        self.redchannel_radio_button = QRadioButton(self, "Red Channel")
        self.redchannel_radio_button.setText("Red Channel")
        self.redchannel_radio_button.setGeometry(180, 520, 125, 30)
        self.redchannel_radio_button.setToolTip('Enhances red pixels from images')
        self.redchannel_radio_button.clicked.connect(self.update_blend_radio_buttons)

        self.greenchannel_radio_button = QRadioButton(self, "Green Channel")
        self.greenchannel_radio_button.setText("Green Channel")
        self.greenchannel_radio_button.setGeometry(180, 570, 125, 30)
        self.greenchannel_radio_button.setToolTip('Enhances green pixels from images')
        self.greenchannel_radio_button.clicked.connect(self.update_blend_radio_buttons)

        self.bluechannel_radio_button = QRadioButton(self, "Blue Channel")
        self.bluechannel_radio_button.setText("Blue Channel")
        self.bluechannel_radio_button.setGeometry(180, 470, 125, 30)
        self.bluechannel_radio_button.setToolTip('Enhances blue pixels from images')
        self.bluechannel_radio_button.clicked.connect(self.update_blend_radio_buttons)

        self.overlay_radio_button = QRadioButton(self, "Overlay")
        self.overlay_radio_button.setText("Overlay")
        self.overlay_radio_button.setGeometry(80, 470, 95, 30)
        self.overlay_radio_button.setToolTip('Combination of Multiply and Screen modes')
        self.overlay_radio_button.clicked.connect(self.update_blend_radio_buttons)

        self.light_radio_button = QRadioButton(self, "Lighten")
        self.light_radio_button.setText("Lighten")
        self.light_radio_button.setGeometry(10, 570, 95, 30)
        self.light_radio_button.setToolTip('Takes the respective lighter pixel into the output image')
        self.light_radio_button.clicked.connect(self.update_blend_radio_buttons)

        self.dark_radio_button = QRadioButton(self, "Darken")
        self.dark_radio_button.setText("Darken")
        self.dark_radio_button.setGeometry(10, 520, 95, 30)
        self.dark_radio_button.setToolTip('Takes the respective darker pixel into the output image')
        self.dark_radio_button.clicked.connect(self.update_blend_radio_buttons)

        self.dodge_radio_button = QRadioButton(self, "Color Dodge")
        self.dodge_radio_button.setText("Color Dodge")
        self.dodge_radio_button.setGeometry(80, 520, 100, 30)
        self.dodge_radio_button.setToolTip('Enhances brightness of background based on foreground light')
        self.dodge_radio_button.clicked.connect(self.update_blend_radio_buttons)

        self.burn_radio_button = QRadioButton(self, "Color Burn")
        self.burn_radio_button.setText("Color Burn")
        self.burn_radio_button.setGeometry(80, 570, 95, 30)
        self.burn_radio_button.setToolTip('The background image is darkened by the foreground')
        self.burn_radio_button.clicked.connect(self.update_blend_radio_buttons)

        # self.crop_radio_button = QRadioButton(self, "Crop")
        # self.crop_radio_button.setText("Crop")
        # self.crop_radio_button.setGeometry(150, 450, 150, 30)
        # self.burn_radio_button.clicked.connect(self.update_blend_radio_buttons)

        self.grayscale_radio_button = QRadioButton("Gray Scale", self)
        self.grayscale_radio_button.setText("Gray Scale")
        self.grayscale_radio_button.setGeometry(180, 250, 150, 30)
        self.grayscale_radio_button.setToolTip('Convert the supplied image to grayscale')
        self.grayscale_radio_button.clicked.connect(self.update_blend_radio_buttons)

        self.blur_radio_button = QRadioButton("Blur", self)
        self.blur_radio_button.setText("Blur")
        self.blur_radio_button.setGeometry(10, 150, 95, 30)
        self.blur_radio_button.setToolTip('Performs a Gaussian blur on the supplied image')
        self.blur_radio_button.clicked.connect(self.update_blend_radio_buttons)

        self.bright_radio_button = QRadioButton("Bright", self)
        self.bright_radio_button.setText("Bright")
        self.bright_radio_button.setGeometry(100, 150, 70, 30)
        self.bright_radio_button.setToolTip('Brighten the supplied image')
        self.bright_radio_button.clicked.connect(self.update_blend_radio_buttons)

        self.hflip_radio_button = QRadioButton("Flip Horizontal", self)
        self.hflip_radio_button.setText("Flip Horizontal")
        self.hflip_radio_button.setGeometry(180, 150, 150, 30)
        self.hflip_radio_button.setToolTip('Flip an image horizontally')
        self.hflip_radio_button.clicked.connect(self.update_blend_radio_buttons)

        self.vflip_radio_button = QRadioButton("Flip Vertical", self)
        self.vflip_radio_button.setText("Flip Vertical")
        self.vflip_radio_button.setGeometry(180, 200, 150, 30)
        self.vflip_radio_button.setToolTip('Flip an image vertically')
        self.vflip_radio_button.clicked.connect(self.update_blend_radio_buttons)

        self.unsharpen_radio_button = QRadioButton("Unsharpen", self)
        self.unsharpen_radio_button.setText("Unsharpen")
        self.unsharpen_radio_button.setGeometry(10, 200, 90, 30)
        self.unsharpen_radio_button.setToolTip('Performs an unsharpen mask on the supplied image')
        self.unsharpen_radio_button.clicked.connect(self.update_blend_radio_buttons)

        self.huerotate_radio_button = QRadioButton("Hue Rotate", self)
        self.huerotate_radio_button.setText("Hue Rotate")
        self.huerotate_radio_button.setGeometry(10, 250, 90, 30)
        self.huerotate_radio_button.setToolTip('Hue rotate the supplied image by degrees')
        self.huerotate_radio_button.clicked.connect(self.update_blend_radio_buttons)

        self.contrast_radio_button = QRadioButton("Contrast", self)
        self.contrast_radio_button.setText("Contrast")
        self.contrast_radio_button.setGeometry(100, 200, 75, 30)
        self.contrast_radio_button.setToolTip('Adjust the contrast of the supplied image')
        self.contrast_radio_button.clicked.connect(self.update_blend_radio_buttons)

        self.invert_radio_button = QRadioButton("Invert", self)
        self.invert_radio_button.setText("Invert")
        self.invert_radio_button.setGeometry(100, 250, 70, 30)
        self.invert_radio_button.setToolTip('Invert each pixel within the supplied image')
        self.invert_radio_button.clicked.connect(self.update_blend_radio_buttons)


    #Follow same format as below when adding new radio button
    def update_blend_radio_buttons(self):
        self.add_radio_button.setCheckable(True)
        self.subtract_radio_button.setCheckable(True)
        self.mult_radio_button.setCheckable(True)
        self.screen_radio_button.setCheckable(True)
        #self.opacity_radio_button.setCheckable(True)
        self.redchannel_radio_button.setCheckable(True)
        self.greenchannel_radio_button.setCheckable(True)
        self.bluechannel_radio_button.setCheckable(True)
        self.overlay_radio_button.setCheckable(True)
        self.light_radio_button.setCheckable(True)
        self.dark_radio_button.setCheckable(True)
        self.dodge_radio_button.setCheckable(True)
        self.burn_radio_button.setCheckable(True)
        self.grayscale_radio_button.setCheckable(True)
        self.blur_radio_button.setCheckable(True)
        self.bright_radio_button.setCheckable(True)
        self.hflip_radio_button.setCheckable(True)
        self.vflip_radio_button.setCheckable(True)
        self.unsharpen_radio_button.setCheckable(True)
        self.huerotate_radio_button.setCheckable(True)
        self.contrast_radio_button.setCheckable(True)
        self.invert_radio_button.setCheckable(True)

        if self.images_selected["image1"] and self.images_selected["image2"]:
            self.pane_label3.clear()
            self.update_blend_photo()

        elif self.images_selected["image1"] and not self.images_selected["image2"]:
            self.update_blend_photo()

        else:
            msgBox = QMessageBox()
            msgBox.setText("Ensure an image is selected.")
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle("Warning")
            msgBox.exec_()
            self.clear_buttons()

    #Follow same format as below when adding a new radio button
    #This function unchecks all radio buttons whenever clear is clicked
    def clear_buttons(self):
        self.add_radio_button.setAutoExclusive(False)
        self.add_radio_button.setChecked(False)
        self.add_radio_button.setAutoExclusive(True)

        self.subtract_radio_button.setAutoExclusive(False)
        self.subtract_radio_button.setChecked(False)
        self.subtract_radio_button.setAutoExclusive(True)

        self.mult_radio_button.setAutoExclusive(False)
        self.mult_radio_button.setChecked(False)
        self.mult_radio_button.setAutoExclusive(True)

        self.screen_radio_button.setAutoExclusive(False)
        self.screen_radio_button.setChecked(False)
        self.screen_radio_button.setAutoExclusive(True)

        # self.opacity_radio_button.setAutoExclusive(False)
        # self.opacity_radio_button.setChecked(False)
        # self.opacity_radio_button.setAutoExclusive(True)

        self.redchannel_radio_button.setAutoExclusive(False)
        self.redchannel_radio_button.setChecked(False)
        self.redchannel_radio_button.setAutoExclusive(True)

        self.greenchannel_radio_button.setAutoExclusive(False)
        self.greenchannel_radio_button.setChecked(False)
        self.greenchannel_radio_button.setAutoExclusive(True)

        self.bluechannel_radio_button.setAutoExclusive(False)
        self.bluechannel_radio_button.setChecked(False)
        self.bluechannel_radio_button.setAutoExclusive(True)

        self.overlay_radio_button.setAutoExclusive(False)
        self.overlay_radio_button.setChecked(False)
        self.overlay_radio_button.setAutoExclusive(True)

        self.light_radio_button.setAutoExclusive(False)
        self.light_radio_button.setChecked(False)
        self.light_radio_button.setAutoExclusive(True)

        self.dark_radio_button.setAutoExclusive(False)
        self.dark_radio_button.setChecked(False)
        self.dark_radio_button.setAutoExclusive(True)

        self.dodge_radio_button.setAutoExclusive(False)
        self.dodge_radio_button.setChecked(False)
        self.dodge_radio_button.setAutoExclusive(True)

        self.burn_radio_button.setAutoExclusive(False)
        self.burn_radio_button.setChecked(False)
        self.burn_radio_button.setAutoExclusive(True)

        # self.crop_radio_button.setAutoExclusive(False)
        # self.crop_radio_button.setChecked(False)
        # self.crop_radio_button.setAutoExclusive(True)

        self.grayscale_radio_button.setAutoExclusive(False)
        self.grayscale_radio_button.setChecked(False)
        self.grayscale_radio_button.setAutoExclusive(True)

        self.blur_radio_button.setAutoExclusive(False)
        self.blur_radio_button.setChecked(False)
        self.blur_radio_button.setAutoExclusive(True)

        self.bright_radio_button.setAutoExclusive(False)
        self.bright_radio_button.setChecked(False)
        self.bright_radio_button.setAutoExclusive(True)

        self.hflip_radio_button.setAutoExclusive(False)
        self.hflip_radio_button.setChecked(False)
        self.hflip_radio_button.setAutoExclusive(True)

        self.vflip_radio_button.setAutoExclusive(False)
        self.vflip_radio_button.setChecked(False)
        self.vflip_radio_button.setAutoExclusive(True)

        self.unsharpen_radio_button.setAutoExclusive(False)
        self.unsharpen_radio_button.setChecked(False)
        self.unsharpen_radio_button.setAutoExclusive(True)

        self.huerotate_radio_button.setAutoExclusive(False)
        self.huerotate_radio_button.setChecked(False)
        self.huerotate_radio_button.setAutoExclusive(True)

        self.contrast_radio_button.setAutoExclusive(False)
        self.contrast_radio_button.setChecked(False)
        self.contrast_radio_button.setAutoExclusive(True)

        self.invert_radio_button.setAutoExclusive(False)
        self.invert_radio_button.setChecked(False)
        self.invert_radio_button.setAutoExclusive(True)

    def setIcon(self):
        appIcon = QIcon("../assets/icon.png")
        self.setWindowIcon(appIcon)

    #This function handles the event whenever the first Image Select button is clicked
    def image1_clicked(self):
        self.image1 = QFileDialog.getOpenFileName(self, "Image 1", QDir.homePath())
        if self.image1[0] != '':  # don't update pane if user cancels file opening
            self.pixmap1 = QPixmap(self.image1[0])
            self.image1_name = self.image1[0]
            if self.images_selected["image2"]:
                # if a second image is already selected, ensure the images have same size
                if self.pixmap2.width() != self.pixmap1.width() or self.pixmap2.height() != self.pixmap1.height():
                    msgBox = QMessageBox()
                    msgBox.setText("Images are not the same size.")
                    msgBox.setIcon(QMessageBox.Warning)
                    msgBox.setWindowTitle("Warning")
                    msgBox.exec_()
                else:
                    self.pane_label1.setPixmap(
                        self.pixmap1.scaled(self.pane_label1.width(), self.pane_label1.height(), QtCore.Qt.KeepAspectRatio))
                    self.images_selected["image1"] = True
            else:
                self.default_pane_label.setPixmap(
                    self.pixmap1.scaled(self.default_pane_label.width(), self.default_pane_label.height(), QtCore.Qt.KeepAspectRatio))
                self.images_selected["image1"] = True

    # This function handles the event whenever the second Image Select button is clicked
    def image2_clicked(self):
        if not self.images_selected["image1"]:
            msgBox = QMessageBox()
            msgBox.setText("Please select the first layer.")
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle("Warning")
            msgBox.exec_()

        else:
            self.image2 = QFileDialog.getOpenFileName(self, "Image 2", QDir.homePath())
            if self.image2[0] != '':  # don't update pane if user cancels file opening
                self.pixmap2 = QPixmap(self.image2[0])
                if self.pixmap2.width() != self.pixmap1.width() or self.pixmap2.height() != self.pixmap1.height():
                    msgBox = QMessageBox()
                    msgBox.setText("Images are not the same size.")
                    msgBox.setIcon(QMessageBox.Warning)
                    msgBox.setWindowTitle("Warning")
                    msgBox.exec_()
                else:
                    self.images_selected["image2"] = True
                    self.labels()


    #Where all the blending/image filtering happens
    def update_blend_photo(self):
        #Follow the same format here to add single image filters
        if self.grayscale_radio_button.isChecked():
            if self.images_selected["image1"] and not self.images_selected["image2"]:
                self.image1_name = str(self.image1)
                self.image1_name = self.image1_name[2:]
                self.image1_name = self.image1_name[:-19]
                grayscale(self.image1_name, "result.jpg")
                result = QPixmap("result.jpg")
                self.image1_name = "result.jpg"
                self.pixmap1 = result
                self.default_pane_label.setPixmap(
                    result.scaled(self.default_pane_label.width(), self.default_pane_label.height(),
                                  QtCore.Qt.KeepAspectRatio))
            else:
                grayscale("test_image.jpg", "result.jpg")
                result = QPixmap("result.jpg")
                self.image1_name = "result.jpg"
                self.pane_label3.setPixmap(
                    result.scaled(self.pane_label3.width(), self.pane_label3.height(), QtCore.Qt.KeepAspectRatio))

        elif self.blur_radio_button.isChecked():
            if self.images_selected["image1"] and not self.images_selected["image2"]:
                self.image1_name = str(self.image1)
                self.image1_name = self.image1_name[2:]
                self.image1_name = self.image1_name[:-19]
                blur(self.image1_name, "result.jpg", 20)
                result = QPixmap("result.jpg")
                self.image1_name = "result.jpg"
                self.pixmap1 = result
                self.default_pane_label.setPixmap(
                    result.scaled(self.default_pane_label.width(), self.default_pane_label.height(),
                                  QtCore.Qt.KeepAspectRatio))
            else:
                blur("test_image.jpg", "result.jpg", 20)
                result = QPixmap("result.jpg")
                self.image1_name = "result.jpg"
                self.pane_label3.setPixmap(
                    result.scaled(self.pane_label3.width(), self.pane_label3.height(), QtCore.Qt.KeepAspectRatio))

        elif self.bright_radio_button.isChecked():
            if self.images_selected["image1"] and not self.images_selected["image2"]:
                self.image1_name = str(self.image1)
                self.image1_name = self.image1_name[2:]
                self.image1_name = self.image1_name[:-19]
                brighten(self.image1_name, "result.jpg", 50)
                result = QPixmap("result.jpg")
                self.image1_name = "result.jpg"
                self.pixmap1 = result
                self.default_pane_label.setPixmap(
                    result.scaled(self.default_pane_label.width(), self.default_pane_label.height(),
                                  QtCore.Qt.KeepAspectRatio))
            else:
                brighten("test_image.jpg", "result.jpg", 20)
                result = QPixmap("result.jpg")
                self.image1_name = "result.jpg"
                self.pane_label3.setPixmap(
                    result.scaled(self.pane_label3.width(), self.pane_label3.height(), QtCore.Qt.KeepAspectRatio))

        elif self.hflip_radio_button.isChecked():
            if self.images_selected["image1"] and not self.images_selected["image2"]:
                self.image1_name = str(self.image1)
                self.image1_name = self.image1_name[2:]
                self.image1_name = self.image1_name[:-19]
                flip_horizontal(self.image1_name, "result.jpg")
                result = QPixmap("result.jpg")
                self.image1_name = "result.jpg"
                self.pixmap1 = result
                self.default_pane_label.setPixmap(
                    result.scaled(self.default_pane_label.width(), self.default_pane_label.height(),
                                  QtCore.Qt.KeepAspectRatio))
            else:
                flip_horizontal("test_image.jpg", "result.jpg")
                result = QPixmap("result.jpg")
                self.image1_name = "result.jpg"
                self.pane_label3.setPixmap(
                    result.scaled(self.pane_label3.width(), self.pane_label3.height(), QtCore.Qt.KeepAspectRatio))

        elif self.vflip_radio_button.isChecked():
            if self.images_selected["image1"] and not self.images_selected["image2"]:
                self.image1_name = str(self.image1)
                self.image1_name = self.image1_name[2:]
                self.image1_name = self.image1_name[:-19]
                flip_vertical(self.image1_name, "result.jpg")
                result = QPixmap("result.jpg")
                self.image1_name = "result.jpg"
                self.pixmap1 = result
                self.default_pane_label.setPixmap(
                    result.scaled(self.default_pane_label.width(), self.default_pane_label.height(),
                                  QtCore.Qt.KeepAspectRatio))
            else:
                flip_vertical("test_image.jpg", "result.jpg")
                result = QPixmap("result.jpg")
                self.image1_name = "result.jpg"
                self.pane_label3.setPixmap(
                    result.scaled(self.pane_label3.width(), self.pane_label3.height(), QtCore.Qt.KeepAspectRatio))

        elif self.unsharpen_radio_button.isChecked():
            if self.images_selected["image1"] and not self.images_selected["image2"]:
                self.image1_name = str(self.image1)
                self.image1_name = self.image1_name[2:]
                self.image1_name = self.image1_name[:-19]
                unsharpen(self.image1_name, "result.jpg", 20, 20)
                result = QPixmap("result.jpg")
                self.image1_name = "result.jpg"
                self.pixmap1 = result
                self.default_pane_label.setPixmap(
                    result.scaled(self.default_pane_label.width(), self.default_pane_label.height(),
                                  QtCore.Qt.KeepAspectRatio))
            else:
                unsharpen("test_image.jpg", "result.jpg", 20, 20)
                result = QPixmap("result.jpg")
                self.image1_name = "result.jpg"
                self.pane_label3.setPixmap(
                    result.scaled(self.pane_label3.width(), self.pane_label3.height(), QtCore.Qt.KeepAspectRatio))

        elif self.huerotate_radio_button.isChecked():
            if self.images_selected["image1"] and not self.images_selected["image2"]:
                self.image1_name = str(self.image1)
                self.image1_name = self.image1_name[2:]
                self.image1_name = self.image1_name[:-19]
                huerotate(self.image1_name, "result.jpg", 100)
                result = QPixmap("result.jpg")
                self.image1_name = "result.jpg"
                self.pixmap1 = result
                self.default_pane_label.setPixmap(
                    result.scaled(self.default_pane_label.width(), self.default_pane_label.height(),
                                  QtCore.Qt.KeepAspectRatio))
            else:
                huerotate("test_image.jpg", "result.jpg", 100)
                result = QPixmap("result.jpg")
                self.image1_name = "result.jpg"
                self.pane_label3.setPixmap(
                    result.scaled(self.pane_label3.width(), self.pane_label3.height(), QtCore.Qt.KeepAspectRatio))

        elif self.contrast_radio_button.isChecked():
            if self.images_selected["image1"] and not self.images_selected["image2"]:
                self.image1_name = str(self.image1)
                self.image1_name = self.image1_name[2:]
                self.image1_name = self.image1_name[:-19]
                contrast(self.image1_name, "result.jpg", 50)
                result = QPixmap("result.jpg")
                self.image1_name = "result.jpg"
                self.pixmap1 = result
                self.default_pane_label.setPixmap(
                    result.scaled(self.default_pane_label.width(), self.default_pane_label.height(),
                                  QtCore.Qt.KeepAspectRatio))
            else:
                contrast("test_image.jpg", "result.jpg", 100)
                result = QPixmap("result.jpg")
                self.image1_name = "result.jpg"
                self.pane_label3.setPixmap(
                    result.scaled(self.pane_label3.width(), self.pane_label3.height(), QtCore.Qt.KeepAspectRatio))

        elif self.invert_radio_button.isChecked():
            if self.images_selected["image1"] and not self.images_selected["image2"]:
                self.image1_name = str(self.image1)
                self.image1_name = self.image1_name[2:]
                self.image1_name = self.image1_name[:-19]
                invert(self.image1_name, "result.jpg")
                result = QPixmap("result.jpg")
                self.image1_name = "result.jpg"
                self.pixmap1 = result
                self.default_pane_label.setPixmap(
                    result.scaled(self.default_pane_label.width(), self.default_pane_label.height(),
                                  QtCore.Qt.KeepAspectRatio))
            else:
                invert("test_image.jpg", "result.jpg")
                result = QPixmap("result.jpg")
                self.image1_name = "result.jpg"
                self.pane_label3.setPixmap(
                    result.scaled(self.pane_label3.width(), self.pane_label3.height(), QtCore.Qt.KeepAspectRatio))


        #End of single image filters

        # check that two images have been selected
        elif not self.images_selected["image1"] or not self.images_selected["image2"]:
            msgBox = QMessageBox()
            msgBox.setText("Ensure two images are selected to blend.")
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle("Warning")
            msgBox.exec_()

        #Two image blending modes go here (All implemented blending functions are working as intended)
        else:
            if self.image1_name != "result.jpg":
                self.image1_name = str(self.image1)
                self.image1_name = self.image1_name[2:]
                self.image1_name = self.image1_name[:-19]
            image2_name = str(self.image2)
            image2_name = image2_name[2:]
            image2_name = image2_name[:-19]

            # call blend functions below based on user selection
            # note that blend modes are mutually exclusive

            # addition blend
            if self.add_radio_button.isChecked():
                call_blend(self.image1_name, image2_name, "add")
                result = QPixmap("test_image.jpg")
                self.pane_label3.setPixmap(
                    result.scaled(self.pane_label3.width(), self.pane_label3.height(), QtCore.Qt.KeepAspectRatio))

            # subtraction blend
            elif self.subtract_radio_button.isChecked():
                call_blend(self.image1_name, image2_name, "subtract")
                result = QPixmap("test_image.jpg")
                self.pane_label3.setPixmap(
                    result.scaled(self.pane_label3.width(), self.pane_label3.height(), QtCore.Qt.KeepAspectRatio))

            # multiply blend
            elif self.mult_radio_button.isChecked():
                call_blend(self.image1_name, image2_name, "multiply")
                result = QPixmap("test_image.jpg")
                self.pane_label3.setPixmap(
                    result.scaled(self.pane_label3.width(), self.pane_label3.height(), QtCore.Qt.KeepAspectRatio))

            # screen blend
            elif self.screen_radio_button.isChecked():
                call_blend(self.image1_name, image2_name, "screen")
                result = QPixmap("test_image.jpg")
                self.pane_label3.setPixmap(
                    result.scaled(self.pane_label3.width(), self.pane_label3.height(), QtCore.Qt.KeepAspectRatio))

            # opacity blend
            # elif self.opacity_radio_button.isChecked():
            #     call_blend(self.image1_name, image2_name, "opacity")
            #     result = QPixmap("test_image.jpg")
            #     self.pane_label3.setPixmap(
            #         result.scaled(self.pane_label3.width(), self.pane_label3.height(), QtCore.Qt.KeepAspectRatio))

            elif self.redchannel_radio_button.isChecked():
                call_blend(self.image1_name, image2_name, "redchannel")
                result = QPixmap("test_image.jpg")
                self.pane_label3.setPixmap(
                    result.scaled(self.pane_label3.width(), self.pane_label3.height(), QtCore.Qt.KeepAspectRatio))

            elif self.greenchannel_radio_button.isChecked():
                call_blend(self.image1_name, image2_name, "greenchannel")
                result = QPixmap("test_image.jpg")
                self.pane_label3.setPixmap(
                    result.scaled(self.pane_label3.width(), self.pane_label3.height(), QtCore.Qt.KeepAspectRatio))

            elif self.bluechannel_radio_button.isChecked():
                call_blend(self.image1_name, image2_name, "bluechannel")
                result = QPixmap("test_image.jpg")
                self.pane_label3.setPixmap(
                    result.scaled(self.pane_label3.width(), self.pane_label3.height(), QtCore.Qt.KeepAspectRatio))

            # overlay blend
            elif self.overlay_radio_button.isChecked():
                call_blend(self.image1_name, image2_name, "overlay")
                result = QPixmap("test_image.jpg")
                self.pane_label3.setPixmap(
                    result.scaled(self.pane_label3.width(), self.pane_label3.height(), QtCore.Qt.KeepAspectRatio))

            # light blend
            elif self.light_radio_button.isChecked():
                call_blend(self.image1_name, image2_name, "lighten")
                result = QPixmap("test_image.jpg")
                self.pane_label3.setPixmap(
                    result.scaled(self.pane_label3.width(), self.pane_label3.height(), QtCore.Qt.KeepAspectRatio))

            # dark blend
            elif self.dark_radio_button.isChecked():
                call_blend(self.image1_name, image2_name, "darken")
                result = QPixmap("test_image.jpg")
                self.pane_label3.setPixmap(
                    result.scaled(self.pane_label3.width(), self.pane_label3.height(), QtCore.Qt.KeepAspectRatio))

            # color dodge blend
            elif self.dodge_radio_button.isChecked():
                call_blend(self.image1_name, image2_name, "color_dodge")
                result = QPixmap("test_image.jpg")
                self.pane_label3.setPixmap(
                    result.scaled(self.pane_label3.width(), self.pane_label3.height(), QtCore.Qt.KeepAspectRatio))

            # color burn blend
            elif self.burn_radio_button.isChecked():
                call_blend(self.image1_name, image2_name, "color_burn")
                result = QPixmap("test_image.jpg")
                self.pane_label3.setPixmap(
                    result.scaled(self.pane_label3.width(), self.pane_label3.height(), QtCore.Qt.KeepAspectRatio))


    def save_clicked(self):
        save_name = QFileDialog.getSaveFileName(self, "Blended Image", QDir.homePath(), "Images (*.png *.jpg)")
        if self.images_selected["image1"] and not self.images_selected["image2"]:
            self.pixmap1.save(save_name[0])
        else:
            QPixmap("test_image.jpg").save(save_name[0])

        # save created image's name in persistent data
        if (save_name[0] != ""):
            file = open(self.persistentData, 'a')
            file.write("\n")
            file.write(save_name[0])
            file.close()

        # update previous file shown to user
        self.path_label.clear()
        self.path_label.setText("Previously Saved Image: " + self.get_previous_file())
        self.path_label.show()

    #Resets display to initial state
    def clear_clicked(self):
        if self.images_selected["image1"] and self.images_selected["image2"]:
            self.default_pane_label.setVisible(True)
            self.pane_label1.clear()
            self.pane_label1.setVisible(False)
            self.layer1_label.clear()
            self.layer1_label.setVisible(False)
            self.pane_label2.clear()
            self.pane_label2.setVisible(False)
            self.layer2_label.clear()
            self.layer2_label.setVisible(False)
            self.pane_label3.clear()
            self.pane_label3.setVisible(False)
            self.result_label.clear()
            self.result_label.setVisible(False)

        else:
            self.default_pane_label.setVisible(True)
            self.default_pane_label.clear()

        self.clear_buttons()
        self.image1_name = ""
        self.images_selected = {"image1": False, "image2": False}

    #Handles rotating either the default pane or the blend result pane
    def rotate_clicked(self):
        transform = QTransform().rotate(90.0)
        if self.images_selected["image1"] and not self.images_selected["image2"]:
            self.default_pane_label.setPixmap(self.default_pane_label.pixmap().transformed(transform))
        else:
            self.pane_label3.setPixmap(self.pane_label3.pixmap().transformed(transform))

    # function to retrieve persistent data
    # in this case, the previous file saved if one exists
    def get_previous_file(self):
        with open(self.persistentData, 'r') as file:
            lines = file.readlines()
            if len(lines) != 0:
                line = lines[-1]
            else:
                line = "No image created yet."
            return line

    def main():
        #wsl.set_display_to_host()
        app = QApplication(sys.argv)
        window = Window()
        browse1 = QPushButton
        sys.exit(app.exec_())


Window.main()
