# -*- coding: utf-8 -*-

from Tkinter import *
from PIL import Image, ImageTk

BG_W = 852
BG_H = 480
BG_C = "green"


class Aircraft(object):
    def __init__(self):
        self.bgs = []
        self.bg_count = len(self.bgs)
        self.now_bg = 0
        self.now_bg_view = 0

    def add_bg(self, bg):
        self.bgs += bg

    def set_bg(self):
        if self.now_bg > self.bg_count:
            self.now_bg = 0
            return
        self.now_bg = self.now_bg + 1



class Map(object):
    def __init__(self):
        self.tk = Tk()
        self.tk.geometry("852x480")
        self.tk.title("飞机大战")
        self.tk.resizable(width=False, height=False)
        self.cv = Canvas(self.tk, bg=BG_C, height=BG_H, width=BG_W)
        image1 = Image.open("material/background.png")
        image_ari1 = Image.open("material/hero1.png")
        image_ari2 = Image.open("material/hero2.png")
        self.bg_image = ImageTk.PhotoImage(image1)
        #保持引用
        self.ari_bg1 = ImageTk.PhotoImage(image_ari1)
        self.ari_bg2 = ImageTk.PhotoImage(image_ari2)
        self.bg = self.cv.create_image(427, 240, image=self.bg_image)
        air.now_bg_view = self.cv.create_image(400, 400, image=self.ari_bg1)
        air.add_bg([self.ari_bg1, self.ari_bg2])
        self.cv.pack()

    def set_bg(self):
        pass

    def del_air_bg(self):
        self.cv.delete(air.now_bg_view)

    def set_air_bg(self):
        air.now_bg_view=self.cv.create_image(425,400,image=air.bgs[air.now_bg])



air = Aircraft()


class Handle(object):
    def __init__(self):
        self.map = Map()

    def run(self):
        self.map.del_air_bg()
        air.set_bg()
        self.map.set_air_bg()
        self.map.set_bg()
        self.map.cv.after(200, self.run)


def app():
    hd = Handle()
    hd.run()
    hd.map.tk.mainloop()


if __name__ == '__main__':
    app()
