"""
Graphical User Interface
It creates the main windows and draw a basic graphic structure, using Tk library.

Draws a Panel according with its descriptor file, which contains option names, images, messages, etc.
"""

import Tkinter as tk
import tkFont
import Image as img
import ImageTk as imgtk
import os
import panel
import time
import config


class GUI(tk.Tk):
    WIDTH = 800
    HEIGHT = 600

    def __init__(self, queues, evtSynch, master=None):
        tk.Tk.__init__(self)
        self.synch = evtSynch

        self.resizable(width=False, height=False)  # Make window not resizable
        self.minsize(width=self.WIDTH, height=self.HEIGHT)  # Window size
        # Window at center of screen
        w = self.winfo_screenwidth()
        h = self.winfo_screenheight()
        x = w / 2 - self.WIDTH / 2
        y = h / 2 - self.HEIGHT / 2
        self.geometry("%dx%d+%d+%d" % ((self.WIDTH, self.HEIGHT) + (x, y)))

        # here the messages from Control will arrive
        # onOffQueue will contain string messages with 'on' and 'off'
        # panelQueue will contain panel that will be drawn
        self.onOffQueue, self.panelQueue = queues

        self.title('Assistive Smart Environment')  # Window title
        self.topFont = tkFont.Font(family='Helvetica', size=25, weight='bold')
        self.bottomFont = tkFont.Font(family='Helvetica', size=12, weight='bold')
        self.maxOptions = config.OPTIONS_NUM
        self._draw()
        self.after(500, self.check_queues)

    def _draw(self):
        # grid (table) geometry
        # window frame: 2 rows x 1 columns
        # up frame: 1 row x 1 column
        # bottom frame: 1 row x 4 columns
        self.upFrame = tk.Frame(self, height=360, width=760)  # create frame
        self.upFrame.grid_propagate(False)  # size fixed
        self.upFrame.columnconfigure(0, weight=1)  # first column takes all space
        self.upFrame.grid(row=0, column=0, padx=20, pady=20)  # show at top
        self.bottomFrame = tk.Frame(self, height=160, width=760)  # create frame
        self.bottomFrame.grid_propagate(False)  # size fixed
        self.bottomFrame.grid(row=1, column=0, padx=20, pady=20)  # show at bottom

        # need a reference to the current panel id
        # when the panel change, we notice this difference and call show_panel
        self.panelId = 0

        # each column take the same space, excepting arrows
        self.bottomFrame.columnconfigure(0, weight=1)
        for i in range(self.maxOptions):
            self.bottomFrame.columnconfigure(i+1, weight=2)
        self.bottomFrame.columnconfigure(self.maxOptions+1, weight=1)

    def check_queues(self):
        if not self.onOffQueue.empty():
            # an on/off command arrived
            cmd = self.onOffQueue.get_nowait()
            if cmd == 'on':
                self.deiconify()
            elif cmd == 'off':
                self.withdraw()
        if not self.panelQueue.empty():
            # a new panel needs to be drawn
            self.show_panel(self.panelQueue.get_nowait())
        # if not self.optionQueue.empty():
        #     # a new option has been selected
        #     self.show_option(self.optionQueue.get_nowait())

        self.after(100, self.check_queues)

    def show_panel(self, panel):
        self.currentPanel = panel

        # first deleting old labels and images
        for w in self.bottomFrame.winfo_children():
            w.grid_forget()
        for w in self.upFrame.winfo_children():
            w.grid_forget()

        # fill bottom frame
        self.bottomFrame.arrowimg = [None] * 2
        self.bottomFrame.littleimg = [None] * len(panel.options)  # need to store images references
        self.bottomFrame.optionLabels = [None] * len(panel.options)

        # left arrow
        imgFile = os.path.join(config.RESOURCES_PATH, 'arrow-left.png')
        icon = img.open(imgFile).resize((50, 50), img.ANTIALIAS)
        self.bottomFrame.arrowimg[0] = imgtk.PhotoImage(icon)
        tk.Label(self.bottomFrame, image=self.bottomFrame.arrowimg[0]).grid(row=1, column=0)

        for i, option in enumerate(panel.options):
            # create and visualize option label
            lbl = tk.Label(self.bottomFrame, text=option.name, font=self.bottomFont)
            if lbl['text'] == panel.currentOption.name:
                lbl.configure(bd=10)
            else:
                lbl.configure(bd=2)
            self.bottomFrame.optionLabels[i] = lbl
            self.bottomFrame.optionLabels[i].grid(column=i+1, row=0)
            # create and visualize option icon
            if option.isOn and hasattr(panel.options[i], 'imgOn'):
                imgFile = os.path.join(config.RESOURCES_PATH, panel.options[i].imgOn)
            else:
                imgFile = os.path.join(config.RESOURCES_PATH, panel.options[i].imgOff)
            icon = img.open(imgFile).resize((100, 100), img.ANTIALIAS)
            self.bottomFrame.littleimg[i] = imgtk.PhotoImage(icon)
            tk.Label(self.bottomFrame, image=self.bottomFrame.littleimg[i]).grid(row=1, column=i+1, sticky=tk.S)

        # right arrow
        imgFile = os.path.join(config.RESOURCES_PATH, 'arrow-right.png')
        icon = img.open(imgFile).resize((50, 50), img.ANTIALIAS)
        self.bottomFrame.arrowimg[1] = imgtk.PhotoImage(icon)
        tk.Label(self.bottomFrame, image=self.bottomFrame.arrowimg[1]).grid(row=1, column=self.maxOptions+1)

        # fill top frame
        # create new label
        self.upFrame.l = tk.Label(self.upFrame, text=panel.currentOption.name, font=self.topFont)
        self.upFrame.l.grid(row=0, column=0)
        # create ampulheta
        imgFile = os.path.join(config.RESOURCES_PATH, "wait.png")
        I = img.open(imgFile).resize((70, 70), img.ANTIALIAS)
        self.upFrame.a = imgtk.PhotoImage(I)
        self.upFrame.aLabel = tk.Label(self.upFrame, image=self.upFrame.a)
        self.upFrame.aLabel.grid(row=0, column=0, sticky=tk.E)
        # create new image
        imgFile = os.path.join(config.RESOURCES_PATH, panel.currentOption.imgOff)
        I = img.open(imgFile).resize((300, 300), img.ANTIALIAS)
        self.upFrame.currentImg = imgtk.PhotoImage(I)
        self.upFrame.currentImgLabel = tk.Label(self.upFrame, image=self.upFrame.currentImg)
        self.upFrame.currentImgLabel.grid(row=1, column=0, sticky=tk.S)

        self.update()
        # sleep a moment for the user to rest
        # and then wait for the command
        self.synch.wait()
        self.upFrame.aLabel.grid_forget()

# Test class
if __name__ == '__main__':
    from threading import Thread
    from time import sleep

    def simulate_control(arg):
        sleep(2)
        arg.next_option()
        sleep(2)
        arg.next_option()
        sleep(2)
        arg.switch()

    app = GUI(None)
    jsonFile = '../resources/sala.panel'
    panel = panel.Panel(jsonFile, 1)

    thread = Thread(target=simulate_control, args=(panel, ))
    thread.start()

    app.show_panel(panel)
    app.mainloop()

