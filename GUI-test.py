import tkinter
import customtkinter
import winsound
#from main import calc_tempo
from main import *

customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

app = customtkinter.CTk()  # create CTk window like you do with the Tk window
app.geometry("600x700")

octave = 4

def octave_1():
    global octave
    octave = 1

def octave_2():
    global octave
    octave = 2

def octave_3():
    global octave
    octave = 3

def octave_4():
    global octave
    octave = 4

def octave_5():
    global octave
    octave = 5

def octave_6():
    global octave
    octave = 6

def button_function():
    print("button pressed")

#removes last note in the list and prints the list
def remove_note():
    note_list.pop()
    print(note_list)

def add_A():
    print("called the add_note function in GUI-test")
    add_note_to_list(str(f"A, {octave}, qu_, n"), note_list)
    print(note_list)

def add_B():
    print("called the add_note function in GUI-test")
    add_note_to_list(str(f"B, {octave}, qu_, n"), note_list)
    print(note_list)

def add_C():
    print("called the add_note function in GUI-test")
    add_note_to_list(str(f"C, {octave}, qu_, n"), note_list)
    print(note_list)

def add_D():
    print("called the add_note function in GUI-test")
    add_note_to_list(str(f"D, {octave}, qu_, n"), note_list)
    print(note_list)

def add_E():
    print("called the add_note function in GUI-test")
    add_note_to_list(str(f"E, {octave}, qu_, n"), note_list)
    print(note_list)

def add_F():
    print("called the add_note function in GUI-test")
    add_note_to_list(str(f"F, {octave}, qu_, n"), note_list)
    print(note_list)

def add_G():
    print("called the add_note function in GUI-test")
    add_note_to_list(str(f"G, {octave}, qu_, n"), note_list)
    print(note_list)

def play():
    print("called the play function in GUI-test")
    for x in note_list:
        winsound.Beep(int(x[0]), x[1])

# Use CTkButton instead of tkinter Button
#button = customtkinter.CTkButton(master=app, text="CTkButton", command=button_function)
#button.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

note_list = []
#takeInput(note_list)

tempo_button = customtkinter.CTkButton(master=app, text="Tempo", command=calc_tempo)
tempo_button.pack(padx=5, pady=5, anchor=tkinter.CENTER)

delete_button = customtkinter.CTkButton(master=app, text="Delete", command=remove_note)
delete_button.pack(padx=5, pady=5)

play_button = customtkinter.CTkButton(master=app, text="Play", command=play)
play_button.pack(padx=5, pady=5)

A_button = customtkinter.CTkButton(master=app, text="A", command=add_A)
A_button.pack(padx=5, pady=5)

B_button = customtkinter.CTkButton(master=app, text="B", command=add_B)
B_button.pack(padx=5, pady=5)

C_button = customtkinter.CTkButton(master=app, text="C", command=add_C)
C_button.pack(padx=5, pady=5)

D_button = customtkinter.CTkButton(master=app, text="D", command=add_D)
D_button.pack(padx=5, pady=5)

E_button = customtkinter.CTkButton(master=app, text="E", command=add_E)
E_button.pack(padx=5, pady=5)

F_button = customtkinter.CTkButton(master=app, text="F", command=add_F)
F_button.pack(padx=5, pady=5)

G_button = customtkinter.CTkButton(master=app, text="G", command=add_G)
G_button.pack(padx=5, pady=5)

oct_one_button = customtkinter.CTkButton(master=app, text="Octave 1", command=octave_1)
oct_one_button.pack(padx=5, pady=5)

oct_two_button = customtkinter.CTkButton(master=app, text="Octave 2", command=octave_2)
oct_two_button.pack(padx=5, pady=5)

oct_three_button = customtkinter.CTkButton(master=app, text="Octave 3", command=octave_3)
oct_three_button.pack(padx=5, pady=5)

oct_four_button = customtkinter.CTkButton(master=app, text="Octave 4", command=octave_4)
oct_four_button.pack(padx=5, pady=5)

oct_five_button = customtkinter.CTkButton(master=app, text="Octave 5", command=octave_5)
oct_five_button.pack(padx=5, pady=5)

oct_six_button = customtkinter.CTkButton(master=app, text="Octave 6", command=octave_6)
oct_six_button.pack(padx=5, pady=5)

"""
entry = customtkinter.CTkEntry(master=app,
                               width=120,
                               height=25,
                               corner_radius=10)
entry.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

text = entry.get()
"""

print_notes(note_list)

#note_list = []
#takeInput(note_list)

#note_button = customtkinter.CTkButton(master=app, text="Add Note", command=takeInput(note_list))
#note_button.place(relx=0, rely=0, anchor=tkinter.CENTER)

app.mainloop()