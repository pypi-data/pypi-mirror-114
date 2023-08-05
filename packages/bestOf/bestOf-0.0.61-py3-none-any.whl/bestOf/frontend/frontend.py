from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys
import numpy as np
import json
import os
print("Starting...")

sys.path.insert(1, 'bestOf/backend')


import bestOf.backend.similarity as similarity
from bestOf.backend.classDefinitions import BlinkAndCropNet, cropped_model
import bestOf.backend.blinkDetector as blinkDetector
import bestOf.backend.cropDetector as cropDetector
import bestOf.backend.evaluateSharpness as evaluateSharpness
import bestOf.backend.identifyPeople as identifyPeople
import bestOf.backend.evaluateCentering as evaluateCentering
import bestOf.backend.sitePackagePathConstructor as sitePackagePathConstructor


def loadImages(filenames):
    for filename in filenames:
        image = identifyPeople.read_img(filename)
        yield (image * 255).astype(np.uint8)[:, :, :3] if 'png' in filename else image


def read_settings():
    path = sitePackagePathConstructor.get_site_package_path(
        './bestOf/backend/settings.json')
    settings = {}
    with open(path, 'r') as settings_file:
        settings = json.load(settings_file)
    return settings


def write_settings(settings):
    path = sitePackagePathConstructor.get_site_package_path(
        './bestOf/backend/settings.json')
    with open(path, 'w') as settings_file:
        json.dump(settings, settings_file)


IMAGELIST = []
GROUPS = []

# Reference Source 1: https://learndataanalysis.org/how-to-pass-data-from-one-window-to-another-pyqt5-tutorial/


def main():
    class processingResults(QWidget):
        def __init__(self):
            super().__init__()
            self.options()
            self.setWindowTitle("Best Of")
            self.setGeometry(1550, 800, 500, 500)
            self.layout = QVBoxLayout()
            self.layout.addWidget(self.des)
            self.setLayout(self.layout)

        def display(self):
            self.__init__()
            self.show()

        def options(self):
            self.des = QGroupBox("Images Selected.",
                                 alignment=QtCore.Qt.AlignCenter)
            vert = QVBoxLayout()
            layout = QHBoxLayout()
            self.redo = QPushButton('&Run Again')
            self.redo.clicked.connect(self.imageProcessing)
            layout.addWidget(self.redo)
            self.back = QPushButton('&Back to Main Menu')
            self.back.clicked.connect(self.close)
            layout.addWidget(self.back)
            info = IMAGELIST
            groups = GROUPS
            if len(info) == 0:
                return
            # print(info)
            # print(groups)
            for group in groups:
                h = QHBoxLayout()
                for index in group:
                    lab = QLabel()
                    for el in info:
                        if el[0] == index:
                            lab.setPixmap(QPixmap(el[1]))
                    h.addWidget(lab)
                vert.addLayout(h)
            vert.addLayout(layout)
            self.des.setLayout(vert)

        def imageProcessing(self):
            image_generator = loadImages([element[1] for element in IMAGELIST])

            # Criteria should be populated from settings selections
            criteria = {
                'sharpness': 1,
                'centering': 1,
                'lighting': 0,
                'resolution': 0
            }

            if criteria['sharpness']:
                sharpness_scores = []
                for image in image_generator:
                    sharpness_scores.append(evaluateSharpness.evaluate_sharpness(
                        image))
                # index to normalized sharpness score + half of normalized subject sharpness score
                sharpness_map = {}
                for group in GROUPS:
                    group_sharpness_scores = []
                    for index in group:
                        for pos, item in enumerate(IMAGELIST):
                            if item[0] == index:
                                group_sharpness_scores.append(
                                    sharpness_scores[pos])
                                break
                    group_sharpness_scores = evaluateSharpness.normalize_sharpness_scores(
                        group_sharpness_scores)

                    avg_subject_sharpness_scores = []
                    for index in group:
                        for pos, item in enumerate(IMAGELIST):
                            if item[0] == index:
                                subject_sharpness_scores = item[3]
                                if not len(subject_sharpness_scores):
                                    avg_subject_sharpness_scores.append(0)
                                    continue

                                avg_subject_sharpness_scores.append(
                                    sum(subject_sharpness_scores) / len(subject_sharpness_scores))
                    avg_subject_sharpness_scores = evaluateSharpness.normalize_sharpness_scores(
                        avg_subject_sharpness_scores)

                    for idx_in_group, index in enumerate(group):
                        sharpness_map[index] = group_sharpness_scores[idx_in_group] + \
                            (avg_subject_sharpness_scores[idx_in_group] / 2)

                print(sharpness_map)

            if criteria['centering']:
                pass

    class settingsMenu(QWidget):
        def __init__(self):
            super().__init__()
            self.options()
            self.setWindowTitle("Settings Menu")
            self.setGeometry(1550, 800, 500, 500)
            self.layout = QVBoxLayout()
            self.layout.addWidget(self.des)
            self.setLayout(self.layout)

        def display(self):
            self.show()

        def options(self):
            self.des = QGroupBox("Apply the following criteria for image refinement.",
                                 alignment=QtCore.Qt.AlignCenter)
            layout = QHBoxLayout()

            self.closeButton = QPushButton('&Close Settings')
            self.closeButton.clicked.connect(self.close)
            layout.addWidget(self.closeButton)
            self.des.setLayout(layout)

    class mainWindow(QWidget):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("Best Of: Main Menu")
            self.resize(800, 800)
            self.setGeometry(1550, 800, 500, 500)
            self.nextWindow = settingsMenu()
            self.process = processingResults()

            self.criteria_settings = read_settings()
            print(self.criteria_settings)

            # self.progress = QProgressBar(self)
            # self.progress.setGeometry()
            self.makeUI()
            self.layout = QVBoxLayout()
            self.layout.addWidget(self.firstText)
            self.setLayout(self.layout)

        def closeEvent(self, event):
            write_settings(self.criteria_settings)

        def makeUI(self):
            self.firstText = QGroupBox("Welcome, browse your computer for images to start picture analysis.",
                                       alignment=QtCore.Qt.AlignCenter)
            layout = QHBoxLayout()
            self.addImage = QPushButton('&Add Images')
            self.addImage.clicked.connect(self.getFiles)
            layout.addWidget(self.addImage)
            self.processImage = QPushButton('&Process Image(s)')
            self.processImage.clicked.connect(self.process.display)
            layout.addWidget(self.processImage)
            self.settings = QPushButton('&More Settings')
            self.settings.clicked.connect(self.nextWindow.display)
            layout.addWidget(self.settings)
            self.firstText.setLayout(layout)

        # Grabs the files for image selection... work in progress...

        def getFiles(self):
            global IMAGELIST
            global GROUPS
            file = QFileDialog.getOpenFileNames(
                self, 'Add Files', QtCore.QDir.rootPath())
            files = ""
            layout = QVBoxLayout
            image_generator = loadImages(list(file[0]))
            vectors = []

            self.criteria_settings['sharpness'] = 2
            self.criteria_settings['resolution'] = 3

            for image in image_generator:
                v = similarity.generate_feature_vector(image)
                vectors.append(v)

            threshold = 0.8  # this should be grabbed from whatever the user set it to in the settings
            groups = similarity.group(vectors, threshold=threshold)
            # print(groups)
            GROUPS = groups

            image_generator = loadImages(list(file[0]))

            default_scores = []
            subject_sharpness_scores = []
            centering_scores = []

            for image in image_generator:
                # print('Scanning Image...')
                subjects, bounds_list = identifyPeople.crop_subjects(image)
                # print("len of subjects", len(subjects))
                blinks = 0
                crops = 0

                subject_sharpness_scores.append([])

                centering_scores.append(
                    evaluateCentering.evaluate_centering(bounds_list, image))

                for sub in subjects:
                    # identifyPeople.show_img(sub)
                    # print('Scanning Subject...')
                    if blinkDetector.test(sub):
                        blinks += 1
                    if cropDetector.test(sub):
                        crops += 1

                    subject_sharpness_scores[-1].append(
                        evaluateSharpness.evaluate_sharpness(sub))

                if len(subjects) == 0:
                    default_scores.append(0)
                    continue

                blink_score = (len(subjects) - blinks) / len(subjects)
                crop_score = (len(subjects) - crops) / len(subjects)

                default_score = blink_score + crop_score
                default_scores.append(default_score)

            if len(IMAGELIST):
                max_index = max([ind for ind in IMAGELIST[0]])
            else:
                max_index = -1

            final = zip(
                range(max_index + 1, max_index + 1 + len(file[0])), file[0], default_scores, subject_sharpness_scores, centering_scores)

            if len(IMAGELIST):
                final = final + IMAGELIST
            final = sorted(final, key=lambda x: x[2], reverse=True)
            print(final)
            IMAGELIST = final

    newApp = QApplication(sys.argv)  # Creates application class
    wind = mainWindow()
    wind.show()
    newApp.exec()  # Executes app with the window


if __name__ == '__main__':
    main()
