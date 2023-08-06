import tkinter as tk
import tkinter.ttk as ttk
import copy
import subprocess
import queue
import os
from threading import Thread

from . import backend


class InfoFrame(ttk.LabelFrame):
    def __init__(self, parent, master, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.master = master


class ImgSelect(ttk.LabelFrame):
    def __init__(self, parent, master, *args, **kwargs):
        super().__init__(parent, *args, **kwargs, text="Image Selection")
        self.parent = parent
        self.master = master
        self.init_components()
        self.place_components()

    def init_components(self):

        # LabelFrames
        self.labelframes = [
            ttk.LabelFrame(self, text=text) for text in ["Primary", "Secondary"]
        ]

        # Dropdowns
        values = self.get_options()
        self.dropdowns = [
            backend.OptionMenu(frame, variable)
            for frame, variable in zip(self.labelframes, self.master.selected_imgnames)
        ]
        self.update_values()
        self.mkcache()

    def place_components(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(3, weight=1)

        [
            labelframe.grid(row=1, column=1 + i, sticky="ew")
            for i, labelframe in enumerate(self.labelframes)
        ]
        [dropdown.pack(ipadx=0, padx=0, ipady=0, pady=0) for dropdown in self.dropdowns]
        [dropdown.config(width=15) for dropdown in self.dropdowns]

    def get_options(self):
        return ["None", *[myimg.filename for myimg in self.master.imgs]]

    def new_selection(self, ind, new_string):
        cache = copy.deepcopy(self.cache)
        self.master.selected_imgnames[ind].set(new_string)
        self.validate_selection(ind)

        if cache != self.cache:
            self.master.refresh()

    def update_values(self):
        filenames = [myimg.filename for myimg in self.master.imgs]
        options = ["None", *filenames]
        callbacks = self.generate_callbacks(options)

        for index, (var, dropdown) in enumerate(
            zip(self.master.selected_imgnames, self.dropdowns)
        ):
            menu = dropdown["menu"]
            menu.delete(0, "end")
            for string in ["None", *filenames]:
                menu.add_command(label=string, command=callbacks[index][string])

    def generate_callbacks(self, newstrings):
        callbacks = {}
        for i in range(2):
            callbacks[i] = {}
            for newstring in newstrings:
                callbacks[i][
                    newstring
                ] = lambda *args, i=i, newstring=newstring: self.new_selection(
                    i, newstring
                )
        return callbacks

    def mkcache(self):
        self.cache = copy.deepcopy(self.master.get_selected_imgnames())

    def validate_selection(self, ind, *args, **kwargs):
        """
        Once an item is selected in the dropdown:

        Enforces the following rules:
        - If an img is selected and is already in another slot, swap the old slot with the cached value of the selected slot
        - If any img is selected, the primary img cannot be None

        """
        other_ind = int(not ind)
        selected_name, other_name = (
            self.master.selected_imgnames[ind].get(),
            self.master.selected_imgnames[other_ind].get(),
        )
        selected_dropdown, other_dropdown = (
            self.dropdowns[ind],
            self.dropdowns[other_ind],
        )
        old_selected_value = self.cache[ind]

        refresh_flag = False

        if selected_name != "None" and selected_name == other_name:
            other_dropdown._variable.set(old_selected_value)

        primary_name = self.master.selected_imgnames[0].get()
        second_name = self.master.selected_imgnames[1].get()
        if primary_name == "None" and second_name != "None":
            self.master.selected_imgnames[1].set("None")
            self.master.selected_imgnames[0].set(second_name)
        self.mkcache()

    def refresh(self):
        """
        Updates structure of radio buttons.
        Applies validation rules.
        """
        self.update_values()


class ImgPosition(ttk.LabelFrame):
    def __init__(self, parent, master, *args, text="Image Position", **kwargs):
        super().__init__(parent, *args, text=text, **kwargs)
        self.parent = parent
        self.master = master
        self.init_components()
        self.place_components()

    def init_components(self):
        # Labels
        self.labels = [ttk.Label(self, text=label) for label in "XYZ"]

        # Entries
        self.entries = [
            backend.FloatRangeEntry(self, minval=minval, maxval=maxval, var=var)
            for var, minval, maxval in zip(self.master.pos, [0, 0, 0], [0, 0, 0])
        ]

        # Scales
        self.scales = [
            backend.IntScale(
                self,
                orient=tk.VERTICAL,
                variable=var,
                entry=entry,
            )
            for _, (var, entry) in enumerate(zip(self.master.pos, self.entries))
        ]

    def place_components(self):
        self.grid_columnconfigure(0, weight=1)
        [label.grid(row=1, column=i + 1) for i, label in enumerate(self.labels)]
        [
            entry.grid(row=2, column=i + 1, padx=5, pady=(0, 5))
            for i, entry in enumerate(self.entries)
        ]
        [
            scale.grid(row=3, column=i + 1, pady=(0, 10))
            for i, scale in enumerate(self.scales)
        ]
        self.grid_columnconfigure(4, weight=1)


class VOIInfo(ttk.LabelFrame):
    def __init__(self, parent, master, *args, text="VOI Info", **kwargs):
        super().__init__(parent, *args, text=text, **kwargs)
        self.parent = parent
        self.master = master
        self.init_components()
        self.place_components()

    def init_components(self):
        # Bound Labels
        self.dimlabels = [ttk.Label(self, text=label) for label in "XYZ"]
        self.poslabel = ttk.Label(self, text="Position")
        self.shapelabel = ttk.Label(self, text="Size")
        self.elsizelabel = ttk.Label(self, text="Element Size (\u03bcm)")

        # Position Entries
        self.posentries = [
            backend.FloatRangeEntry(self, minval=minval, maxval=maxval, var=var)
            for var, minval, maxval in zip(self.master.voi["pos"], [0, 0, 0], [0, 0, 0])
        ]

        # Shape Entries
        self.shapeentries = [
            backend.IntRangeEntry(self, minval=minval, maxval=maxval, var=var)
            for var, minval, maxval in zip(
                self.master.voi["shape"], [1, 1, 1], [1, 1, 1]
            )
        ]

        # Elsize entries
        self.elsizeentries = [
            backend.FloatRangeEntry(self, minval=minval, maxval=maxval, var=var)
            for var, minval, maxval in zip(
                self.master.voi["elsize"], [1, 1, 1], [1, 1, 1]
            )
        ]

    def place_components(self):
        self.grid_columnconfigure(0, weight=1)
        [label.grid(row=0, column=i + 2) for i, label in enumerate(self.dimlabels)]
        self.poslabel.grid(row=1, column=1, sticky="e")
        [
            posentry.grid(row=1, column=i + 2, padx=5, pady=5)
            for i, posentry in enumerate(self.posentries)
        ]
        self.shapelabel.grid(row=2, column=1, sticky="e")
        [
            shapeentry.grid(row=2, column=i + 2, pady=5)
            for i, shapeentry in enumerate(self.shapeentries)
        ]
        self.elsizelabel.grid(row=3, column=1, sticky="e")
        [
            elsizeentry.grid(row=3, column=i + 2, pady=5)
            for i, elsizeentry in enumerate(self.elsizeentries)
        ]
        self.grid_columnconfigure(4, weight=1)


class Options(ttk.LabelFrame):
    def __init__(self, parent, master, *args, text="Options", **kwargs):
        super().__init__(parent, *args, text=text, **kwargs)
        self.parent = parent
        self.master = master
        self.init_components()
        self.place_components()

    def init_components(self):
        self.crosshaircheck = ttk.Checkbutton(
            self, text="View Crosshairs", variable=self.master.flag_crosshair
        )
        self.voicheck = ttk.Checkbutton(
            self, text="View VOI", variable=self.master.flag_voi
        )
        self.zoomcheck = ttk.Checkbutton(
            self, text="Zoom to VOI", variable=self.master.flag_zoom
        )
        self.redbluecheck = ttk.Checkbutton(
            self, text="Red-Blue Visuals", variable=self.master.flag_redblue
        )

    def place_components(self):
        self.grid_columnconfigure(0, weight=1)
        self.crosshaircheck.grid(row=0, column=1, sticky="w")
        self.voicheck.grid(row=1, column=1, sticky="w")
        self.zoomcheck.grid(row=2, column=1, sticky="w")
        self.redbluecheck.grid(row=3, column=1, sticky="w")
        self.grid_columnconfigure(2, weight=1)


class Console(tk.Frame):  # pragma: no cover
    def __init__(self, parent=None, master=None, *args, **kwargs):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.master = master
        self.createWidgets()

        # get the path to the console.py file assuming it is in the same folder
        consolePath = os.path.join(os.path.dirname(__file__), "console.py")
        # open the console.py file (replace the path to python with the correct one for your system)
        # e.g. it might be "C:\\Python35\\python"
        self.p = subprocess.Popen(
            ["python3", consolePath],
            stdout=subprocess.PIPE,
            stdin=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        # make queues for keeping stdout and stderr whilst it is transferred between threads
        self.outQueue = queue.Queue()
        self.errQueue = queue.Queue()

        # keep track of where any line that is submitted starts
        self.line_start = 0

        # make the enter key call the self.enter function
        self.ttyText.bind("<Return>", self.enter)

        # a daemon to keep track of the threads so they can stop running
        self.alive = True
        # start the functions that get stdout and stderr in separate threads
        Thread(target=self.readFromProccessOut).start()
        Thread(target=self.readFromProccessErr).start()

        # start the write loop in the main thread
        self.writeLoop()

    def destroy(self):
        "This is the function that is automatically called when the widget is destroyed."
        self.alive = False
        # write exit() to the console in order to stop it running
        self.p.stdin.write("exit()\n".encode())
        self.p.stdin.flush()
        # call the destroy methods to properly destroy widgets
        self.ttyText.destroy()
        tk.Frame.destroy(self)

    def enter(self, e):
        "The <Return> key press handler"
        string = self.ttyText.get(1.0, tk.END)[self.line_start :]
        self.line_start += len(string)
        self.p.stdin.write(string.encode())
        self.p.stdin.flush()

    def readFromProccessOut(self):
        "To be executed in a separate thread to make read non-blocking"
        while self.alive:
            data = self.p.stdout.raw.read(1024).decode()
            self.outQueue.put(data)

    def readFromProccessErr(self):
        "To be executed in a separate thread to make read non-blocking"
        while self.alive:
            data = self.p.stderr.raw.read(1024).decode()
            self.errQueue.put(data)

    def writeLoop(self):
        "Used to write data from stdout and stderr to the Text widget"
        # if there is anything to write from stdout or stderr, then write it
        if not self.errQueue.empty():
            self.write(self.errQueue.get())
        if not self.outQueue.empty():
            self.write(self.outQueue.get())

        # run this method again after 10ms
        if self.alive:
            self.after(10, self.writeLoop)

    def write(self, string):
        self.ttyText.insert(tk.END, string)
        self.ttyText.see(tk.END)
        self.line_start += len(string)

    def createWidgets(self):
        self.ttyText = tk.Text(self, wrap=tk.WORD)
        self.ttyText.pack(fill=tk.BOTH, expand=True)
