#Příliš žluťoučký kůň úpěl ďábelské ó - PŘÍLIŠ ŽLUŤOUČKÝ KŮŇ ÚPĚL ĎÁBELSKÉ Ó
"""
Dokumentační komentář modulu.
"""
import dbg
dbg.start_mod(0, __name__)
############################################################################

import tkinter

import os
import importlib

from tkinter.scrolledtext import ScrolledText

from .Helper import *

game     = None
scenario = None


class GUI(tkinter.Frame):
    """
    Implementace třídy GUI definující aplikační okno
    umožňující zrychlené ovládání pomocí tlačítek
    """

    def __init__(self, helper=False):
        """Inicializuje aplikační okno.
        """
        tkinter.Frame.__init__(self)
        self.master.minsize(800, 300)
        self.pack(fill='both', expand=True, padx=10, pady=10)
        self.make_widgets()
        if helper:
            self.helper = Helper(self, scenario)
        self.mainloop()

    def make_widgets(self):
        """Vytvoří potřebné komponenty.
        """
        self.f_left = tkinter.Frame(self)
        self.f_left.pack(fill='both', side="left")

        frame = tkinter.Frame(self, bg='grey')
        frame.pack(fill='both', expand=True, side="left")

        self.f_right = tkinter.Frame(self)
        self.f_right.pack(fill='both', side="left")

        frame_red = tkinter.Frame(frame, bg="red")
        frame_red.pack(fill='both', expand=True, padx=10, pady=10)

        self.text = ScrolledText(frame_red, state=tkinter.DISABLED)
        self.text.place(relheight=1, relwidth=1)

        frame_green = tkinter.Frame(frame, bg='grey')
        frame_green.pack(fill='both', padx=10, pady=(0, 10))
        frame_green.grid_propagate(False)

        self.entry = tkinter.Entry(frame_green)
        self.entry.pack(fill='both', padx=(0, 10), expand=True)
        self.entry.pack(side='left')
        self.entry.bind('<Return>',
                        lambda event: self.execute_command(self.entry.get()))

        button = tkinter.Button(frame_green, text='Proveď',
                                command=lambda: self.execute_command(self.entry.get()))
        button.pack(fill='y')
        button.pack(side='left')
        self.update_space()

    def show_message(self, message: str) -> None:
        """Doplní do zobrazovaného testu odpověď hry.
        """
        self.text.configure(state='normal')
        self.text.insert(tkinter.END, message)
        self.text.yview_pickplace("end")
        self.text.configure(state='disabled')

    def execute_command(self, command: str) -> None:
        """Zpracuje zadaný příkaz a vrátí string se zprávou pro uživatele.
        """
        executed_command = game.execute_command(command)
        message = executed_command
        self.show_message("\n" + 50 * "_" + "\n\n" + command + "\n" + message)
        self.update_space()
        self.clear_entry()

    def clear_entry(self):
        """Vyčistí příkazový řádek"""
        self.entry.delete(0, tkinter.END)

    def update_space(self):
        """Aktualizuje tlačítka a a připraví zadání dalšího příkazu.
        """
        self.clear_frames()
        if game.isAlive():
            bag_items = game.bag().items
            place_neighbors = list(game.world().current_place().neighbors)
            place_items = list(game.world().current_place().items)
        else:
            bag_items = []
            place_neighbors = []
            place_items = []
        act = game.basic_actions()

        tkinter.Label(self.f_left, text="== Předměty v batohu==").grid()
        self.add_all_buttons(bag_items, act.PUT_DOWN_NAME, "left")
        tkinter.Label(self.f_right, text="== Objekty v prostoru ==").grid()
        self.add_all_buttons(place_items, act.TAKE_NAME, "right")
        tkinter.Label(self.f_right, text="== Sousední prostory ==").grid()
        self.add_all_buttons(place_neighbors, act.MOVE_NAME, "right")

    def add_all_buttons(self, list_of_things, command, side):
        """Vytvoří v panelech potřebná tlačítka a návěští.
        """
        if side == "left":
            frame = self.f_left
        elif side == "right":
            frame = self.f_right
        else:
            raise Exception("wrong side attribute must be left or right")
        for i in range(len(list_of_things)):
            button = tkinter.Button(frame, text=list_of_things[i])
            button.grid(sticky="W")
            button.config(command=lambda i=i:
            self.execute_command(command +
                                 " " +
                                 list_of_things[i].name
                                 ))

    def clear_frames(self):
        """Vyčistí panely tlačítek.
        """
        for child in self.f_left.winfo_children():
            child.destroy()
        for child in self.f_right.winfo_children():
            child.destroy()


class Chooser(tkinter.Frame):
    """Instance vytvoří okno, v němž si uživatel může vybrat adventuru,
    která se následně spustí.
    """
    def __init__(self):
        """V rámci inicializace otevře okno s přehledem dostupných her.
        """
        super().__init__()
        self.master.protocol("WM_DELETE_WINDOW", lambda: os._exit(0))
        choices = []
        root = os.path.abspath(os.curdir)
        tree = os.listdir(root + "\\game")
        for p in tree:
            if p[-3:] == "api" or \
                    p[-5:] == "tests" or \
                    p == "Helper.py" or \
                    p == "gui.py" or \
                    p == "__init__.py" or \
                    p == "__pycache__":
                pass
            else:
                choices.append(p)

        choicesvar = tkinter.StringVar(value=choices)
        tkinter.Label(self, text="Vyberte hru:").pack()
        self.list = tkinter.Listbox(self, listvariable=choicesvar)
        self.list.pack()
        b = tkinter.Button(self, text="Potvrdit",
                           command=lambda: self.on_button_click())
        b.pack()
        self.pack()
        self.mainloop()

    def on_button_click(self):
        """Definuje reakci na stisk tlačítka.
        """
        for i in self.list.curselection():
            self.import_adventure(self.list.get(i))

    def import_adventure(self, name: str):
        """Importuje hru a šťastný scénář pro helper.
        """
        global game
        global scenario
        factory = importlib.import_module("game." + name + ".factory")
        game = factory.game()
        scenario = factory.scenarios()[0]

        self.master.destroy()



############################################################################
dbg.stop_mod (0, __name__)
