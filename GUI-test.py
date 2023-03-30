import tkinter
import customtkinter
import winsound
from PIL import Image
from main import *
import mingus.core.notes as notes
from mingus.containers import Note, Track, Bar, NoteContainer
from mingus.containers.instrument import MidiInstrument as mi
from mingus.midi import fluidsynth
import mingus.core.value as value
import time

customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green

app = customtkinter.CTk()  # create CTk window like you do with the Tk window
app.geometry("1000x500")
app.resizable(True, True)

accidental_font = customtkinter.CTkFont(family="system-ui", size=20, weight="bold")

note_font = customtkinter.CTkFont(family="sans-serif", size=15, weight="bold")

clef_font = customtkinter.CTkFont(family="sans-serif", size=30, weight="bold")

"""
flat_image = customtkinter.CTkImage(light_image=Image.open(".\\assets\\images\\flat_accidental.png"),
                                  dark_image=Image.open(".\\assets\\images\\flat_accidental.png"),
                                  size=(30, 30))

sharp_image = customtkinter.CTkImage(light_image=Image.open(".\\assets\\images\\sharp_accidental.png"),
                                  dark_image=Image.open(".\\assets\\images\\sharp_accidental.png"),
                                  size=(30, 30))

nat_image = customtkinter.CTkImage(light_image=Image.open(".\\assets\\images\\natural_accidental.png"),
                                  dark_image=Image.open(".\\assets\\images\\natural_accidental.png"),
                                  size=(30, 30))
"""

octave = 4
accidental = "n"
track = Track()

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
    return int(octave)

def len_button_event():
    print("length button toggled, current value:", len_var.get())

def acc_button_event():
    print("accidental button toggled, current value:", acc_var.get())

#converts numeric value of the note length radio buttons into the correct note length
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

#converts numeric value of the accidental radio buttons into the correct accidental
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

#this makes the accidental buttons unclickable (changes their text color to darkgray as defined below),
# and sets the foreground color (the color of the selected button) to darkgray as well
#this will be useful when measures can be displayed and measure checking + editing notes is implemented
#   - measure checking will add rests to each measure, these rests can be edited but should not be able
#     to be sharp/flat/natural so when a rest is selected, call this function to disable these buttons
def disable_acc_buttons():
    sharp_button.configure(state=tkinter.DISABLED, fg_color="darkgray")
    flat_button.configure(state=tkinter.DISABLED, fg_color="darkgray")
    nat_button.configure(state=tkinter.DISABLED, fg_color="darkgray")

#removes last note in the list and prints the list
def remove_note():
    global track
    if note_list:
        note_list.pop()
        note_display.pop()
        #track = remove_last_note_from_track(track)
        track = new_remove_note(track)
    new_display = ""
    for x in note_display:
        new_display = new_display + x + "  |  "
    
    note_list_display.configure(text=new_display)
    print(note_list)

def remove_note_from_list():
    if note_list:
        note_list.pop()
        note_display.pop()
    new_display = ""
    for x in note_display:
        new_display = new_display + x + "  |  "
    
    note_list_display.configure(text=new_display)
    print(note_list)

#formats the most recent note into the form "Length: NoteAccidentalOctave"
#EX: A, 4, qu_, n  ->  QU: An4
def pretty_note(note: str, oct: str, len: str, acc: str):
    #covert the len string to the correct form
    match len:
        case "wh_":
            len = "WH"
        case "ha_":
            len = "HA"
        case "qu_":
            len = "QU"
        case "ei_":
            len = "EI"
        case "qu.":
            len = "Q."
        case "ha.":
            len = "H."
    
    ret = f"{len} :  {note}{acc}{oct}"
    print(ret)
    return ret

#might want to keep a list of the "styled_note", it may be easier to implement editing notes
#   using this list rather than note_list which is just a list of (frequency, duration) tuples
def add_note_to_display(styled_note: str):
    note_display.append(styled_note)
    note_list_display.configure(text=(note_list_display.cget("text") + note_display[len(note_display)-1] + "  |  "))

def add_A():
    global track
    print("called the add_note function in GUI-test")
    styled_note = pretty_note("A", f"{get_octave()}", f"{get_note_len()}", f"{get_accidental()}")
    add_note_to_display(styled_note)
    add_note_to_list(str(f"A, {get_octave()}, {get_note_len()}, {get_accidental()}"), note_list)
    add_note_to_track(note_list, track)
    #preview_note(note_list)
    print(note_list)

def add_A_1():
    global track
    print("called the add_note function in GUI-test")
    styled_note = pretty_note("A", f"{get_octave() - 1}", f"{get_note_len()}", f"{get_accidental()}")
    add_note_to_display(styled_note)
    add_note_to_list(str(f"A, {get_octave() - 1}, {get_note_len()}, {get_accidental()}"), note_list)
    add_note_to_track(note_list, track)
    #preview_note(note_list)
    print(note_list)

def add_B():
    global track
    print("called the add_note function in GUI-test")
    styled_note = pretty_note("B", f"{get_octave()}", f"{get_note_len()}", f"{get_accidental()}")
    add_note_to_display(styled_note)
    add_note_to_list(str(f"B, {get_octave()}, {get_note_len()}, {get_accidental()}"), note_list)
    add_note_to_track(note_list, track)
    #preview_note(note_list)
    print(note_list)

def add_B_1():
    global track
    print("called the add_note function in GUI-test")
    styled_note = pretty_note("B", f"{get_octave() - 1}", f"{get_note_len()}", f"{get_accidental()}")
    add_note_to_display(styled_note)
    add_note_to_list(str(f"B, {get_octave() - 1}, {get_note_len()}, {get_accidental()}"), note_list)
    add_note_to_track(note_list, track)
    #preview_note(note_list)
    print(note_list)

def add_C():
    global track
    print("called the add_note function in GUI-test")
    styled_note = pretty_note("C", f"{get_octave()}", f"{get_note_len()}", f"{get_accidental()}")
    add_note_to_display(styled_note)
    add_note_to_list(str(f"C, {get_octave()}, {get_note_len()}, {get_accidental()}"), note_list)
    add_note_to_track(note_list, track)
    #preview_note(note_list)
    print(note_list)

def add_D():
    global track
    print("called the add_note function in GUI-test")
    styled_note = pretty_note("D", f"{get_octave()}", f"{get_note_len()}", f"{get_accidental()}")
    add_note_to_display(styled_note)
    add_note_to_list(str(f"D, {get_octave()}, {get_note_len()}, {get_accidental()}"), note_list)
    add_note_to_track(note_list, track)
    #preview_note(note_list)
    print(note_list)

def add_E():
    global track
    print("called the add_note function in GUI-test")
    styled_note = pretty_note("E", f"{get_octave()}", f"{get_note_len()}", f"{get_accidental()}")
    add_note_to_display(styled_note)
    add_note_to_list(str(f"E, {get_octave()}, {get_note_len()}, {get_accidental()}"), note_list)
    add_note_to_track(note_list, track)
    #preview_note(note_list)
    print(note_list)

def add_F():
    global track
    print("called the add_note function in GUI-test")
    styled_note = pretty_note("F", f"{get_octave()}", f"{get_note_len()}", f"{get_accidental()}")
    add_note_to_display(styled_note)
    add_note_to_list(str(f"F, {get_octave()}, {get_note_len()}, {get_accidental()}"), note_list)
    add_note_to_track(note_list, track)
    #preview_note(note_list)
    print(note_list)

def add_G():
    global track
    print("called the add_note function in GUI-test")
    styled_note = pretty_note("G", f"{get_octave()}", f"{get_note_len()}", f"{get_accidental()}")
    add_note_to_display(styled_note)
    add_note_to_list(str(f"G, {get_octave()}, {get_note_len()}, {get_accidental()}"), note_list)
    add_note_to_track(note_list, track)
    #preview_note(note_list)
    print(note_list)

def add_G_1():
    global track
    print("called the add_note function in GUI-test")
    styled_note = pretty_note("G", f"{get_octave() - 1}", f"{get_note_len()}", f"{get_accidental()}")
    add_note_to_display(styled_note)
    add_note_to_list(str(f"G, {get_octave() - 1}, {get_note_len()}, {get_accidental()}"), note_list)
    add_note_to_track(note_list, track)
    #preview_note(note_list)
    print(note_list)

def set_track(new_track):
    global track
    track = new_track

def remove_empty_bars(track):
    new_track = Track()
    #print(f"track: {track}")
    for x in track:
        #print(x.space_left())
        if x.space_left() != 1.0:
            new_track.add_bar(x)
    #print(new_track)

    #print("removed empty bars")
    track = new_track
    return track

def new_remove_note(track: Track):
    #first find the last bar in the track
    track = remove_empty_bars(track)
    #print(track)
    bars_list = track.bars
    last_bar = bars_list[len(bars_list) - 1]
    #print(last_bar)
    last_bar.remove_last_entry()
    #print(last_bar)
    track[len(track) - 1] = last_bar
    #print(track)
    return track

"""
def remove_last_note_from_track(track):
    #get the last bar in the track
    #remove_empty_bars_test(track)
    track = remove_empty_bars(track)
    print(track)
    print(len(track))

    last_bar = track[len(track) - 1]
    #print(last_bar)
    last_bar = last_bar[:len(last_bar) - 1]
    #print(last_bar)

    new_track = Track()
    #print(track)
    for x in track:
        if x != track[len(track) - 1]:
            new_track.add_bar(x)
    #print(f"new_track: {new_track}")
    #print(track)
    new_track.add_bar(Bar(last_bar))
    #print(new_track)

    print("removed last note")
    track = new_track
    return track
"""
    
"""
def remove_last_note_from_track():
    global track
    new_track = Track()
    last_bar = Bar()

    list_of_bars = track.bars
    if list_of_bars:
        curr_bar = list_of_bars[len(list_of_bars) - 1]
        last_bar = curr_bar
        print(f"curr_bar before removing note: {last_bar}")
    else:
        print("curr_bar before adding note: []")
    
    print(f"len(track.bars): {len(track.bars)}")
    print(f"track.bars: {track.bars}")

    for x in range(len(track)):
        #print(track[x])
        print(f"x: {x}")
        if x < len(track) - 1:
            new_track.add_bar(track[x])
        #else:
        #    last_bar = track[x]
        
    print(f"new_track: {new_track}")
    print(f"last_bar: {last_bar}")
    new_last_bar = Bar()
    for x in range(len(last_bar)):
        #print(last_bar[x][1])
        if x < len(last_bar) - 1:
            new_last_bar.place_notes(last_bar[x][2], last_bar[x][1])
    #print(new_last_bar)
    new_track.add_bar(new_last_bar)
    set_track(new_track)
    print("removed last note from track")
"""

#call this function immediately after add_note_to_list
def add_note_to_track(note_list, track):
    #find the note length
    note_len = len_var.get()
    list_of_bars = track.bars
    if list_of_bars and not list_of_bars[len(list_of_bars) - 1].is_full():
        curr_bar = list_of_bars[len(list_of_bars) - 1]
        print(f"curr_bar before adding note: {curr_bar}")
    else:
        print("curr_bar before adding note: []")

    match note_len:
        case 1:
            note_len = value.whole
        case 2:
            note_len = value.dots(value.half)
        case 3:
            note_len = value.half
        case 4:
            note_len = value.dots(value.quarter)
        case 5:
            note_len = value.quarter
        case 6:
            note_len = value.eighth
    
    #pull the note you just added to so you can add it to the track
    x = note_list[len(note_list) - 1]
    temp = Note()
    temp.channel = 1
    temp.velocity = 120
    temp = Note.from_hertz(temp, float(x[0]), 440)
    if not track.add_notes(temp, note_len):
        preview_note(note_list)
        note_add_warning.configure(text="Error:\nNot enough space in the\ncurrent bar for that note,\nthe note was not added.")
        remove_note_from_list()
        return
    else:
        note_add_warning.configure(text="")
    preview_note(note_list)
        


def play():
    print("called the play function in GUI-test")
    #fluidsynth.init("D:\\Capstone\\repos\\capstone-prototype\\capstone-prototype\\soundfonts\\FluidR3_GM.sf2", 'dsound')
    fluidsynth.init(".\\soundfonts\\FluidR3_GM.sf2", 'dsound')
    fluidsynth.stop_everything()

    """
    note_len = len_var.get()

    match note_len:
        case 1:
            note_len = value.whole
        case 2:
            note_len = value.dots(value.half)
        case 3:
            note_len = value.half
        case 4:
            note_len = value.dots(value.quarter)
        case 5:
            note_len = value.quarter
        case 6:
            note_len = value.eighth
    """

    global track
    
    """
    for x in note_list:
        temp = Note()
        temp = Note.from_hertz(temp, float(x[0]), 440)
        track.add_notes(temp, note_len)
        #if bar.current_beat != bar.length:
        #    bar.place_notes(temp, note_len)

            #true_note_list.append(temp)
        #else:
        #    track.add_bar(bar)
        #    temp_bar = Bar()
        #    bar = temp_bar
        #    bar.place_notes(temp, note_len)
    """
    tempo = get_tempo()
    try:
        tempo_num = int(tempo)
    except:
        tempo_num = 120

    fluidsynth.play_Track(track, 1, tempo_num)

    #playing the notes
    #for x in true_note_list:
    #    fluidsynth.play_Note(x)
    #    time.sleep(0.1)
    
    #for x in note_list:
    #    winsound.Beep(int(x[0]), x[1])

# Use CTkButton instead of tkinter Button
#button = customtkinter.CTkButton(master=app, text="CTkButton", command=button_function)
#button.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

note_list = []
note_display = []
len_var = tkinter.IntVar(app, 5)
acc_var = tkinter.IntVar(app, 3)

play_button = customtkinter.CTkButton(master=app, text="Play", command=play)
play_button.place(x=20, y=10)

tempo_button = customtkinter.CTkButton(master=app, text="Change Tempo", command=change_tempo)
tempo_button.place(x=20, y=50)

tempo_entry = customtkinter.CTkEntry(master=app,
                               width=140,
                               height=25,
                               placeholder_text="Enter a new tempo",
                               corner_radius=5)
tempo_entry.place(x=20, y=90)

delete_button = customtkinter.CTkButton(master=app, text="Delete", command=remove_note)
delete_button.place(x=20, y=130)

octave_entry = customtkinter.CTkEntry(master=app,
                               width=140,
                               height=25,
                               placeholder_text="Enter a new Octave",
                               corner_radius=5)
octave_entry.place(x=20, y=170)

A_button = customtkinter.CTkButton(master=app, text="A", command=add_A, width=40)
A_button.place(x=200, y=10)

B_button = customtkinter.CTkButton(master=app, text="B", command=add_B, width=40)
B_button.place(x=250, y=10)

C_button = customtkinter.CTkButton(master=app, text="C", command=add_C, width=40)
C_button.place(x=300, y=10)

D_button = customtkinter.CTkButton(master=app, text="D", command=add_D, width=40)
D_button.place(x=350, y=10)

E_button = customtkinter.CTkButton(master=app, text="E", command=add_E, width=40)
E_button.place(x=400, y=10)

F_button = customtkinter.CTkButton(master=app, text="F", command=add_F, width=40)
F_button.place(x=450, y=10)

G_button = customtkinter.CTkButton(master=app, text="G", command=add_G, width=40)
G_button.place(x=500, y=10)

# text="♯", font=accidental_font
sharp_button = customtkinter.CTkRadioButton(master=app, text="♯", font=accidental_font,
                                            text_color_disabled="darkgray",
                                            command=acc_button_event, variable= acc_var, value=1)
sharp_button.place(x=200, y=50, width=103)

# text="♭", font=accidental_font
flat_button = customtkinter.CTkRadioButton(master=app, text="♭", font=accidental_font,
                                            text_color_disabled="darkgray",
                                            command=acc_button_event, variable= acc_var, value=2)
flat_button.place(x=250, y=50, width=103)

# text="♮", font=accidental_font
nat_button = customtkinter.CTkRadioButton(master=app, text="♮", font=accidental_font,
                                            text_color_disabled="darkgray",
                                            command=acc_button_event, variable= acc_var, value=3)
nat_button.place(x=300, y=50, width=103)

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

len_button_1.place(x=200, y=90)
len_button_2.place(x=250, y=90)
len_button_3.place(x=300, y=90)
len_button_4.place(x=350, y=90)
len_button_5.place(x=400, y=90)
len_button_6.place(x=450, y=90)

note_list_display=customtkinter.CTkLabel(master=app, font=note_font, text="")
note_list_display.place(x=200, y=130)

note_add_warning=customtkinter.CTkLabel(master=app, font=note_font, justify="left",
                                        text="")
note_add_warning.place(relx=0.8, rely=0.05)

bass_clef=customtkinter.CTkLabel(master=app, font=clef_font, justify="left",
                                        text="BASS\nCLEF")
bass_clef.place(x=200, y=260)

a_line=customtkinter.CTkButton(master=app, text="__________________________________________________", command=add_A, height=1,
                                 fg_color="transparent", hover=False, border_width=0, anchor="n", font=note_font)
a_line.place(x=300, y=200)

g_space=customtkinter.CTkButton(master=app, text="                                                 ", command=add_G, height=10, width=405,
                                 fg_color="transparent", hover=False, border_width=0, anchor="n", font=note_font)
g_space.place(x=300, y=220)

f_line=customtkinter.CTkButton(master=app, text="__________________________________________________", command=add_F, height=1,
                                 fg_color="transparent", hover=False, border_width=0, font=note_font)
f_line.place(x=300, y=240)

e_space=customtkinter.CTkButton(master=app, text="                                                 ", command=add_E, height=10, width=405,
                                 fg_color="transparent", hover=False, border_width=0, anchor="n", font=note_font)
e_space.place(x=300, y=260)

d_line = customtkinter.CTkButton(master=app, text="__________________________________________________", command=add_D, height=1,
                                 fg_color="transparent", hover=False, border_width=0, font=note_font)
d_line.place(x=300, y=280)

c_space=customtkinter.CTkButton(master=app, text="                                                 ", command=add_C, height=10, width=405,
                                 fg_color="transparent", hover=False, border_width=0, anchor="n", font=note_font)
c_space.place(x=300, y=300)

b_line = customtkinter.CTkButton(master=app, text="__________________________________________________", command=add_B_1, height=1,
                                 fg_color="transparent", hover=False, border_width=0, font=note_font)
b_line.place(x=300, y=320)

a_space=customtkinter.CTkButton(master=app, text="                                                 ", command=add_A_1, height=10, width=405,
                                 fg_color="transparent", hover=False, border_width=0, anchor="n", font=note_font)
a_space.place(x=300, y=340)

g_line = customtkinter.CTkButton(master=app, text="__________________________________________________", command=add_G_1, height=1,
                                 fg_color="transparent", hover=False, border_width=0, font=note_font)
g_line.place(x=300, y=360)



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