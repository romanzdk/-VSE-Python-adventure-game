#Příliš žluťoučký kůň úpěl ďábelské ó - PŘÍLIŠ ŽLUŤOUČKÝ KŮŇ ÚPĚL ĎÁBELSKÉ Ó
"""
Obsahuje pouze definici třídy vytvářející pomocné řídící okno,
které usnadňuje průchod scénářem tím, že načítá jeho příkazy
a nabízí jejich zadání pouhým stiskem tlačítka.
"""
import dbg
dbg.start_mod(0, __name__)
############################################################################

import tkinter


class Helper(tkinter.Toplevel):
    """Implementace okna usnadňujícího průchod scénářem.
    """
    def __init__(self, gui, scenario):
        tkinter.Toplevel.__init__(self, width=250, height=150)
        self.resizable(False, False)
        self.title('Information')
        self.step_index = 0
        self.make_widgets()
        self.is_top_destroyed = False
        self.scenario = scenario
        self.gui = gui

    def make_widgets(self):
        """Vytvoří komponenty  okna.
        """
        top_frame_t = tkinter.Frame(self, height=100, width=250)
        top_frame_t.pack()

        self.last_command = tkinter.StringVar()
        self.last_command.set("Starý příkaz: ")
        self.label_last_command = tkinter.Label(top_frame_t,
                                                textvariable=self.last_command)
        self.label_last_command.pack()

        self.new_command = tkinter.StringVar()
        self.new_command.set("Nový příkaz: ")
        self.label_new_command = tkinter.Label(top_frame_t,
                                               textvariable=self.new_command)
        self.label_new_command.pack()

        top_frame_b = tkinter.Frame(self, height=30, width=250)
        top_frame_b.pack(fill="x")

        self.button_yes_top = tkinter.Button(top_frame_b,
                                             text='Yes',
                                             command=lambda: self.run_test())
        self.button_yes_top.place(relx=0.3)
        self.button_no_top = tkinter.Button(top_frame_b,
                                            text='No',
                                            command=lambda: self.destroy_top())
        self.button_no_top.place(relx=0.6)

    def destroy_top(self):
        self.is_top_destroyed = True
        self.destroy()

    def next_tip(self):
        """Vypíše v okně aktuálně realizovaný plus následující příkaz.
        """
        commands = self.get_test_string()
        self.last_command.set("Starý příkaz: " + commands[0])
        self.new_command.set("Nový příkaz: " + commands[1])
        self.update_idletasks()

    def get_test_string(self) -> list:
        """Získá scénář pro řídící okno.
        """
        if self.step_index == 0:
            last_command = ""
        else:
            last_command = self.scenario.steps[self.step_index].command
        if  self.step_index >= len(self.scenario.steps)-1:
            new_command = ""
        else:
            new_command = self.scenario.steps[self.step_index+1].command

        return [last_command, new_command]

    def run_test(self):
        """Spustí se při použití řídícího okna.
        """
        command = self.scenario.steps[self.step_index].command
        self.gui.execute_command(command)
        self.next_tip()
        self.step_index += 1
        if self.step_index >= len(self.scenario.steps):
            self.destroy_top()



############################################################################
dbg.stop_mod (0, __name__)
