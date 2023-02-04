import tkinter
import customtkinter
import winsound
from PIL import Image
from main import *

customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

app = customtkinter.CTk()  # create CTk window like you do with the Tk window
app.geometry("1200x800")

accidental_font = customtkinter.CTkFont(family="system-ui", size=20, weight="bold")

note_font = customtkinter.CTkFont(family="sans-serif", size=15, weight="bold")

flat_image = customtkinter.CTkImage(light_image=Image.open(".\\assets\\images\\flat_accidental.png"),
                                  dark_image=Image.open(".\\assets\\images\\flat_accidental.png"),
                                  size=(30, 30))

sharp_image = customtkinter.CTkImage(light_image=Image.open(".\\assets\\images\\sharp_accidental.png"),
                                  dark_image=Image.open(".\\assets\\images\\sharp_accidental.png"),
                                  size=(30, 30))

nat_image = customtkinter.CTkImage(light_image=Image.open(".\\assets\\images\\natural_accidental.png"),
                                  dark_image=Image.open(".\\assets\\images\\natural_accidental.png"),
                                  size=(30, 30))


octave = 4
accidental = "n"

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

def sharp():
    global accidental
    accidental = "#"

def flat():
    global accidental
    accidental = "b"

def natural():
    global accidental
    accidental = "n"

def button_function():
    print("button pressed")

def get_tempo():
    tempo = tempo_entry.get()
    return tempo

def change_tempo():
    tempo = get_tempo()
    calc_tempo(tempo)

def get_octave():
    octave = octave_entry.get()
    if not octave:
        octave = 4
    print(octave)
    return octave

def len_button_event():
    print("radiobutton toggled, current value:", len_var.get())

def acc_button_event():
    print("radiobutton toggled, current value:", acc_var.get())

def change_note_len():
    #options for note_len:
    #   wh_  ha.  ha_  qu.  qu_  ei_
    #default length is quarter note
        note_len = len_var.get()
        match note_len:
            case 1:
                return "wh_"
            case 2:
                return "ha."
            case 3:
                return "ha_"
            case 4:
                return "qu."
            case 5:
                return "qu_"
            case 6:
                return "ei_"
        return "qu_"

def get_note_len():
    return change_note_len()

def change_accidental():
        acc = acc_var.get()
        match acc:
            case 1:
                return "#"
            case 2:
                return "b"
            case 3:
                return "n"
        return "n"

def get_accidental():
    return change_accidental()

#removes last note in the list and prints the list
def remove_note():
    if note_list:
        note_list.pop()
    print(note_list)

def add_A():
    print("called the add_note function in GUI-test")
    add_note_to_list(str(f"A, {get_octave()}, {get_note_len()}, {get_accidental()}"), note_list)
    print(note_list)

def add_B():
    print("called the add_note function in GUI-test")
    add_note_to_list(str(f"B, {get_octave()}, {get_note_len()}, {get_accidental()}"), note_list)
    print(note_list)

def add_C():
    print("called the add_note function in GUI-test")
    add_note_to_list(str(f"C, {get_octave()}, {get_note_len()}, {get_accidental()}"), note_list)
    print(note_list)

def add_D():
    print("called the add_note function in GUI-test")
    add_note_to_list(str(f"D, {get_octave()}, {get_note_len()}, {get_accidental()}"), note_list)
    print(note_list)

def add_E():
    print("called the add_note function in GUI-test")
    add_note_to_list(str(f"E, {get_octave()}, {get_note_len()}, {get_accidental()}"), note_list)
    print(note_list)

def add_F():
    print("called the add_note function in GUI-test")
    add_note_to_list(str(f"F, {get_octave()}, {get_note_len()}, {get_accidental()}"), note_list)
    print(note_list)

def add_G():
    print("called the add_note function in GUI-test")
    add_note_to_list(str(f"G, {get_octave()}, {get_note_len()}, {get_accidental()}"), note_list)
    print(note_list)

def play():
    print("called the play function in GUI-test")
    for x in note_list:
        winsound.Beep(int(x[0]), x[1])

# Use CTkButton instead of tkinter Button
#button = customtkinter.CTkButton(master=app, text="CTkButton", command=button_function)
#button.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

note_list = []
len_var = tkinter.IntVar(app, 5)
acc_var = tkinter.IntVar(app, 3)

tempo_button = customtkinter.CTkButton(master=app, text="Tempo", command=change_tempo)
tempo_button.pack(padx=60, pady=10, anchor="w")

tempo_entry = customtkinter.CTkEntry(master=app,
                               width=140,
                               height=25,
                               placeholder_text="Enter a new tempo",
                               corner_radius=5)
tempo_entry.pack(padx=60, pady=0, anchor="w")

delete_button = customtkinter.CTkButton(master=app, text="Delete", command=remove_note)
delete_button.pack(padx=60, pady=10, anchor="w")

play_button = customtkinter.CTkButton(master=app, text="Play", command=play)
play_button.pack(padx=60, pady=0, anchor="w")

octave_entry = customtkinter.CTkEntry(master=app,
                               width=140,
                               height=25,
                               placeholder_text="Enter a new Octave",
                               corner_radius=5)
octave_entry.pack(padx=60, pady=10, anchor="w")

A_button = customtkinter.CTkButton(master=app, text="A", command=add_A, width=40)
A_button.place(relx=0.2, rely=0.05)

B_button = customtkinter.CTkButton(master=app, text="B", command=add_B, width=40)
B_button.place(relx=0.24, rely=0.05)

C_button = customtkinter.CTkButton(master=app, text="C", command=add_C, width=40)
C_button.place(relx=0.28, rely=0.05)

D_button = customtkinter.CTkButton(master=app, text="D", command=add_D, width=40)
D_button.place(relx=0.32, rely=0.05)

E_button = customtkinter.CTkButton(master=app, text="E", command=add_E, width=40)
E_button.place(relx=0.36, rely=0.05)

F_button = customtkinter.CTkButton(master=app, text="F", command=add_F, width=40)
F_button.place(relx=0.40, rely=0.05)

G_button = customtkinter.CTkButton(master=app, text="G", command=add_G, width=40)
G_button.place(relx=0.44, rely=0.05)

# text="♯", font=accidental_font
sharp_button = customtkinter.CTkRadioButton(master=app, text="♯", font=accidental_font,
                                             command=acc_button_event, variable= acc_var, value=1)
sharp_button.place(relx=0.2, rely=0.1, width=103)

# text="♭", font=accidental_font
flat_button = customtkinter.CTkRadioButton(master=app, text="♭", font=accidental_font,
                                             command=acc_button_event, variable= acc_var, value=2)
flat_button.place(relx=0.294, rely=0.1, width=103)

# text="♮", font=accidental_font
nat_button = customtkinter.CTkRadioButton(master=app, text="♮", font=accidental_font,
                                             command=acc_button_event, variable= acc_var, value=3)
nat_button.place(relx=0.388, rely=0.1, width=103)

len_button_1 = customtkinter.CTkRadioButton(master=app, text="W", font=note_font,
                                             command=len_button_event, variable= len_var, value=1)
len_button_2 = customtkinter.CTkRadioButton(master=app, text="H.", font=note_font,
                                             command=len_button_event, variable= len_var, value=2)
len_button_3 = customtkinter.CTkRadioButton(master=app, text="H", font=note_font,
                                             command=len_button_event, variable= len_var, value=3)
len_button_4 = customtkinter.CTkRadioButton(master=app, text="Q.", font=note_font,
                                             command=len_button_event, variable= len_var, value=4)
len_button_5 = customtkinter.CTkRadioButton(master=app, text="Q", font=note_font,
                                             command=len_button_event, variable= len_var, value=5)
len_button_6 = customtkinter.CTkRadioButton(master=app, text="E", font=note_font,
                                             command=len_button_event, variable= len_var, value=6)

len_button_1.place(relx=0.2, rely=0.15)
len_button_2.place(relx=0.25, rely=0.15)
len_button_3.place(relx=0.3, rely=0.15)
len_button_4.place(relx=0.35, rely=0.15)
len_button_5.place(relx=0.4, rely=0.15)
len_button_6.place(relx=0.45, rely=0.15)

"""
#these buttons will need a custom font before I can have music notes displayed on them
#this is possible with PyQT (see here https://coderslegacy.com/python/pyqt6-adding-custom-fonts/)
#I may need to redo my GUI using PyQT, or hopefully I can find/build an adapter between the two

whole_button = customtkinter.CTkButton(master=app, text="𝅝", font=note_font, command=add_G, width=40)
whole_button.place(relx=0.2, rely=0.15)

dot_half_button = customtkinter.CTkButton(master=app, text="𝅗𝅥.", font=note_font, command=add_G, width=40)
dot_half_button.place(relx=0.24, rely=0.15)

half_button = customtkinter.CTkButton(master=app, text="𝅗𝅥", font=note_font, command=add_G, width=40)
half_button.place(relx=0.28, rely=0.15)

dot_quarter_button = customtkinter.CTkButton(master=app, text="𝅘𝅥.", font=note_font, command=add_G, width=40)
dot_quarter_button.place(relx=0.32, rely=0.15)

quarter_button = customtkinter.CTkButton(master=app, text="𝅘𝅥", font=note_font, command=add_G, width=40)
quarter_button.place(relx=0.36, rely=0.15)

eighth_button = customtkinter.CTkButton(master=app, text="𝅘𝅥𝅮", font=note_font, command=add_G, width=40)
eighth_button.place(relx=0.40, rely=0.15)

#these buttons use the images instead of text but its really ugly
#I'll need to research more on using images before using these

sharp_button = customtkinter.CTkButton(master=app, text="", image=sharp_image, command=sharp)
sharp_button.place(relx=0.2, rely=0.1, width=103)

flat_button = customtkinter.CTkButton(master=app, text="", image=flat_image, command=flat)
flat_button.place(relx=0.295, rely=0.1, width=103)

nat_button = customtkinter.CTkButton(master=app, text="", image=nat_image, command=natural)
nat_button.place(relx=0.39, rely=0.1, width=103)
"""

print_notes(note_list)

#note_list = []
#takeInput(note_list)

#note_button = customtkinter.CTkButton(master=app, text="Add Note", command=takeInput(note_list))
#note_button.place(relx=0, rely=0, anchor=tkinter.CENTER)


app.mainloop()