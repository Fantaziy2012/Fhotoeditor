from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QListWidget, QHBoxLayout, QVBoxLayout, QFileDialog
import os
from PIL import Image
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PIL import ImageFilter
from PIL.ImageFilter import SHARPEN
app = QApplication([])
win = QWidget()
win.setWindowTitle('Фоторедактор')
class ImageProcessor():
    def __init__(self):
        self.image = None # Текущее изображение
        self.dir = None # Папка по умолчанию
        self.filename = None # Текущее имя файла
        self.save_dir = 'Modyfied/' # имя подпапки для сохранения изменнёных картинок
        self.original_image = None
    def loadImage(self, dir, filename):
        self.dir = dir
        self.filename = filename
        image_path = os.path.join(dir,filename) # сформировали путь к картинке
        self.image = Image.open(image_path) # Открываем картинку обратившись по сформированнному пути
        self.original_image = self.image.copy()
    def showImage(self, path): 
        # Метод показа картинки
        pixmapimage = QPixmap(path)
        w,h = label.width(), label.height() # Узнаём ширину и высоту поля для размещения картинки
        pixmapimage = pixmapimage.scaled(w,h, Qt.KeepAspectRatio) # Qt.KeepAspectRatio - адапртирует картинку под размеры поля
        label.setPixmap(pixmapimage)
        label.show()
    def saveImage(self):
        # Сохраняет копию файлов в подпапке
        path = os.path.join(self.dir, self.save_dir) # Здесь мы создаём путь до папки modified
        if not(os.path.exists(path) or os.path.isdir(path)): # Если в файле ещё нет указанного имени или указанного имени папки
            os.mkdir(path) # Создаём папку 
        image_path = os.path.join(path, self.filename)
        self.image.save(image_path)
    def do_bw(self):
        self.image = self.image.convert('L')
        self.saveImage() 
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)
    def do_flip(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(
            self.dir,self.save_dir, self.filename
        )
        self.showImage(image_path)
    def do_sharpen(self):
        self.image = self.image.filter(SHARPEN)
        self.saveImage()
        image_path = os.path.join(
            self.dir,self.save_dir, self.filename
        )
        self.showImage(image_path)
    def do_left(self):
        self.image = self.image.rotate(90,expand = True)
        self.saveImage()
        image_path = os.path.join(
            self.dir,self.save_dir, self.filename
        )
        self.showImage(image_path)
    def do_right(self):
        self.image = self.image.rotate(-90, expand = True)
        self.saveImage()
        image_path = os.path.join(
            self.dir,self.save_dir, self.filename
        )
        self.showImage(image_path)
    def resetImage(self):
        if self.original_image is None:
            return
        self.image = self.original_image.copy()
        self.showImage(os.path.join(workdir, self.filename))
    def do_blur(self):
        self.image = self.image.filter(ImageFilter.BLUR)
        self.saveImage()
        image_path = os.path.join(
            self.dir,self.save_dir, self.filename
        )
        self.showImage(image_path)
workimage = ImageProcessor()
btn_folder = QPushButton('Папка')
list_of_files = QListWidget()
label = QLabel('Картинка')
btn_left = QPushButton('Лево')
btn_right = QPushButton('Право')
btn_mirror = QPushButton('Зеркало')
btn_sharpness = QPushButton('Резкость')
btn_blackwhite = QPushButton('ЧБ')
btn_blur = QPushButton('Блюр')
btn_reset = QPushButton('Сбросить')
col_1 = QVBoxLayout()
col_1.addWidget(btn_folder)
col_1.addWidget(list_of_files)
col_2 = QVBoxLayout()
col_2.addWidget(label)
row_1 = QHBoxLayout()
row_1.addWidget(btn_left)
row_1.addWidget(btn_right)
row_1.addWidget(btn_mirror)
row_1.addWidget(btn_sharpness)
row_1.addWidget(btn_blackwhite)
row_1.addWidget(btn_blur)
row_1.addWidget(btn_reset)
col_2.addLayout(row_1)
main_row = QHBoxLayout()
main_row.addLayout(col_1)
main_row.addLayout(col_2)
win.setLayout(main_row)
workdir = '' # Сохраняем путь до рабочей папки
# Функция выбора рабочей папки
def chooseWorkDir():
    global workdir # Обращаемся к глобальной переменной
    workdir = QFileDialog.getExistingDirectory()
def filter(files,extensions):
    result = []
    for file_name in files:
        for e in extensions:
            if file_name.endswith(e):
                result.append(file_name)
    return result
def showFilenamesList():
    chooseWorkDir()
    extensions = ['.png', '.jpeg', '.jpg', '.gif', '.webp', '.jfif']
    file_names = filter(os.listdir(workdir),extensions)
    list_of_files.clear()
    for f in file_names:
        list_of_files.addItem(f)
def showChosenImage():
    if list_of_files.currentRow() >= 0:
        filename = list_of_files.currentItem().text()
        workimage.loadImage(workdir, filename)
        image_path = os.path.join(workimage.dir, workimage.filename)
        workimage.showImage(image_path)
btn_folder.clicked.connect(showFilenamesList)
list_of_files.currentRowChanged.connect(showChosenImage)
btn_blackwhite.clicked.connect(workimage.do_bw)
btn_mirror.clicked.connect(workimage.do_flip)
btn_sharpness.clicked.connect(workimage.do_sharpen)
btn_left.clicked.connect(workimage.do_left)
btn_right.clicked.connect(workimage.do_right)
btn_reset.clicked.connect(workimage.resetImage)
btn_blur.clicked.connect(workimage.do_blur)
win.show()
app.exec_()
