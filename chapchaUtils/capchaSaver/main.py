import os
import sys
import time
from tkinter import *
from threading import Thread
from selenium import webdriver

class capchaSaver():
    def __init__(self):
        self.driver = None;

        self.generateUI()

    def generateUI(self):
        self.root = Tk()

        self.startButton = Button(self.root, text="Запустить браузер")
        self.closeButton = Button(self.root, text="Закрыть браузер")
        self.restartButton = Button(self.root, text="Перезапустить браузер")

        self.classesList = Listbox(self.root, height=5, width=15, selectmode=SINGLE)
        self.classesElements = open('classes.txt', 'r').read().split('\n')

        self.currentEndElementsRow = len(self.classesElements)
        for element in self.classesElements:
            self.classesList.insert(END, element)
            try:
                os.mkdir('./screens/' + element)
            except:
                pass

        self.saveButton = Button(self.root, text="Сохранить")

        self.newElement = Entry(self.root, width=25)
        self.saveNewElementButton = Button(self.root, text="Добавить класс")

        self.startButton.grid(row=1, column=1)
        self.closeButton.grid(row=1, column=2)
        self.restartButton.grid(row=1, column=3)
        self.classesList.grid(row=2, column=1)
        self.saveButton.grid(row=2, column=2, columnspan=2)
        self.newElement.grid(row=self.currentEndElementsRow, column=1, columnspan=2)
        self.saveNewElementButton.grid(row=self.currentEndElementsRow, column=3)


        self.startButton.bind('<Button-1>', self.start_browser_bind)
        self.closeButton.bind('<Button-1>', self.close_browser_bind)
        self.restartButton.bind('<Button-1>', self.restart_browser_bind)
        self.saveButton.bind('<Button-1>', self.save_screenshot_bind)
        self.saveNewElementButton.bind('<Button-1>', self.add_new_class_bind)

    def start_browser_bind(self, event):
        Thread(target=self.start_browser).start()

    def close_browser_bind(self, event):
        Thread(target=self.close_browser).start()

    def restart_browser_bind(self, event):
        Thread(target=self.restart_browser).start()

    def save_screenshot_bind(self, event):
        Thread(target=self.save_screenshot).start()

    def add_new_class_bind(self, event):
        Thread(target=self.add_new_class).start()

    def start_browser(self):
        self.driver = webdriver.Firefox(executable_path='./browsers/geckodriver.exe')
        self.driver.set_window_size(720, 640)
        self.driver.get('https://localbitcoins.net/accounts/login/')

    def close_browser(self):
        self.driver.close()
        self.driver.quit()

    def restart_browser(self):
        self.close_browser()
        self.start_browser()

    def save_screenshot(self):
        active = self.classesList.get(ACTIVE)

        filepath = './screens/' + active
        if os.path.exists(filepath) != True:
            os.mkdir(filepath)

        filename = str(len(os.listdir(filepath))) + '.png'
        filepath += '/' + filename

        self.driver.save_screenshot(filepath)

    def add_new_class(self):
        className = self.newElement.get()
        classes = open('classes.txt', 'r').read()
        classes += '\n' + className
        open('classes.txt', 'w').write(classes)
        self.classesList.insert(END, className)
        self.currentEndElementsRow += 1
        self.newElement.grid(row=self.currentEndElementsRow, column=1, columnspan=2)
        self.saveNewElementButton.grid(row=self.currentEndElementsRow, column=3)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    cs = capchaSaver()
    cs.run()