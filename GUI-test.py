import tkinter
import customtkinter
from main import *
import mingus.core.notes as notes
from mingus.containers import Note, Track, Bar, NoteContainer
from mingus.containers.instrument import MidiInstrument as mi
from mingus.midi import fluidsynth
import mingus.core.value as value

customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green

app = customtkinter.CTk()  # create CTk window like you do with the Tk window
width = app.winfo_screenwidth()
height = app.winfo_screenheight()
print(width, height)
app.title("MEscore")
app.geometry(f"{width}x{height}")
#app.resizable(True, True)
app.resizable(False, True)

accidental_font = customtkinter.CTkFont(family="system-ui", size=20, weight="bold")

len_font = customtkinter.CTkFont(family="sans-serif", size=16, weight="bold")

note_font = customtkinter.CTkFont(family="sans-serif", size=14, weight="bold")

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
    global note_count
    if note_list:
        note_list.pop()
        note_display.pop()
        note_count -= 1
        #track = remove_last_note_from_track(track)
        track = new_remove_note(track)
    #new_display = ""
    #for x in note_display:
    #    new_display = new_display + x + "  |  "
    
    new_display = note_display
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

def display_note_count():
    global note_count, note_count_label, buffer
    #note_count_label.configure(text=f"note count: {note_count}\nbuffer: {buffer * 20}")
    note_count_label.configure(text="")

def update_note_count():
    global note_count
    note_len = get_note_len()
    note_count += 1
    """
    match note_len:
        case "wh_":
            note_count += 4
        case "ha.":
            note_count += 3
        case "ha_":
            note_count += 2
        case "qu.":
            note_count += 1.5
        case "qu_":
            note_count += 1
        case "ei_":
            note_count += 0.5
    """

#might want to keep a list of the "styled_note", it may be easier to implement editing notes
#   using this list rather than note_list which is just a list of (frequency, duration) tuples
def add_note_to_display(styled_note: str):
    global note_count, buffer
    if (note_count % 12) == 0 and note_count != 0:
        buffer += 1
        print(f"buffer: {buffer}")
    note_display.append(styled_note)
    if (note_count % 12) == 0 and note_count != 0: 
        note_list_display.configure(text=(note_list_display.cget("text") + "\n" + note_display[len(note_display)-1] + "  |  "))
        update_staff()
    else:
        note_list_display.configure(text=(note_list_display.cget("text") + note_display[len(note_display)-1] + "  |  "))
    #display_note_count()

def add_A():
    global track, editing, note_count
    print("called the add_note function in GUI-test")
    styled_note = pretty_note("A", f"{get_octave()}", f"{get_note_len()}", f"{get_accidental()}")
    if not editing:
        add_note_to_display(styled_note)
        add_note_to_list(str(f"A, {get_octave()}, {get_note_len()}, {get_accidental()}"), note_list)
        add_note_to_track(note_list, track)
    else:
        edit_note("A", get_octave(), get_accidental())
    update_note_count()
    #preview_note(note_list)
    print(note_list)

def add_A_1():
    global track, editing, note_count
    print("called the add_note function in GUI-test")
    styled_note = pretty_note("A", f"{get_octave() - 1}", f"{get_note_len()}", f"{get_accidental()}")
    if not editing:
        add_note_to_display(styled_note)
        add_note_to_list(str(f"A, {get_octave() - 1}, {get_note_len()}, {get_accidental()}"), note_list)
        add_note_to_track(note_list, track)
    else:
        edit_note("A", get_octave() - 1, get_accidental())
    update_note_count()
    #preview_note(note_list)
    print(note_list)

def add_A_2():
    global track, editing, note_count
    print("called the add_note function in GUI-test")
    styled_note = pretty_note("A", f"{get_octave() - 2}", f"{get_note_len()}", f"{get_accidental()}")
    if not editing:
        add_note_to_display(styled_note)
        add_note_to_list(str(f"A, {get_octave() - 2}, {get_note_len()}, {get_accidental()}"), note_list)
        add_note_to_track(note_list, track)
    else:
        edit_note("A", get_octave() - 2, get_accidental())
    update_note_count()
    #preview_note(note_list)
    print(note_list)

def add_B():
    global track, editing, note_count
    print("called the add_note function in GUI-test")
    styled_note = pretty_note("B", f"{get_octave()}", f"{get_note_len()}", f"{get_accidental()}")
    if not editing:
        add_note_to_display(styled_note)
        add_note_to_list(str(f"B, {get_octave()}, {get_note_len()}, {get_accidental()}"), note_list)
        add_note_to_track(note_list, track)
    else:
        edit_note("B", get_octave(), get_accidental())
    update_note_count()
    #preview_note(note_list)
    print(note_list)

def add_B_1():
    global track, editing, note_count
    print("called the add_note function in GUI-test")
    styled_note = pretty_note("B", f"{get_octave() - 1}", f"{get_note_len()}", f"{get_accidental()}")
    if not editing:
        add_note_to_display(styled_note)
        add_note_to_list(str(f"B, {get_octave() - 1}, {get_note_len()}, {get_accidental()}"), note_list)
        add_note_to_track(note_list, track)
    else:
        edit_note("B", get_octave() - 1, get_accidental())
    update_note_count()
    #preview_note(note_list)
    print(note_list)

def add_B_2():
    global track, editing, note_count
    print("called the add_note function in GUI-test")
    styled_note = pretty_note("B", f"{get_octave() - 2}", f"{get_note_len()}", f"{get_accidental()}")
    if not editing:
        add_note_to_display(styled_note)
        add_note_to_list(str(f"B, {get_octave() - 2}, {get_note_len()}, {get_accidental()}"), note_list)
        add_note_to_track(note_list, track)
    else:
        edit_note("B", get_octave() - 2, get_accidental())
    update_note_count()
    #preview_note(note_list)
    print(note_list)

def add_C_t():
    global track, editing, note_count
    print("called the add_note function in GUI-test")
    styled_note = pretty_note("C", f"{get_octave() + 1}", f"{get_note_len()}", f"{get_accidental()}")
    if not editing:
        add_note_to_display(styled_note)
        add_note_to_list(str(f"C, {get_octave() + 1}, {get_note_len()}, {get_accidental()}"), note_list)
        add_note_to_track(note_list, track)
    else:
        edit_note("C", get_octave() + 1, get_accidental())
    update_note_count()
    #preview_note(note_list)
    print(note_list)

def add_C():
    global track, editing, note_count
    print("called the add_note function in GUI-test")
    styled_note = pretty_note("C", f"{get_octave()}", f"{get_note_len()}", f"{get_accidental()}")
    if not editing:
        add_note_to_display(styled_note)
        add_note_to_list(str(f"C, {get_octave()}, {get_note_len()}, {get_accidental()}"), note_list)
        add_note_to_track(note_list, track)
    else:
        edit_note("C", get_octave(), get_accidental())
    update_note_count()
    #preview_note(note_list)
    print(note_list)

def add_C_1():
    global track, editing, note_count
    print("called the add_note function in GUI-test")
    styled_note = pretty_note("C", f"{get_octave() - 1}", f"{get_note_len()}", f"{get_accidental()}")
    if not editing:
        add_note_to_display(styled_note)
        add_note_to_list(str(f"C, {get_octave() - 1}, {get_note_len()}, {get_accidental()}"), note_list)
        add_note_to_track(note_list, track)
    else:
        edit_note("C", get_octave() - 1, get_accidental())
    update_note_count()
    #preview_note(note_list)
    print(note_list)

def add_D_t():
    global track, editing, note_count
    print("called the add_note function in GUI-test")
    styled_note = pretty_note("D", f"{get_octave() + 1}", f"{get_note_len()}", f"{get_accidental()}")
    if not editing:
        add_note_to_display(styled_note)
        add_note_to_list(str(f"D, {get_octave() + 1}, {get_note_len()}, {get_accidental()}"), note_list)
        add_note_to_track(note_list, track)
    else:
        edit_note("D", get_octave() + 1, get_accidental())
    update_note_count()
    #preview_note(note_list)
    print(note_list)

def add_D():
    global track, editing, note_count
    print("called the add_note function in GUI-test")
    styled_note = pretty_note("D", f"{get_octave()}", f"{get_note_len()}", f"{get_accidental()}")
    if not editing:
        add_note_to_display(styled_note)
        add_note_to_list(str(f"D, {get_octave()}, {get_note_len()}, {get_accidental()}"), note_list)
        add_note_to_track(note_list, track)
    else:
        edit_note("D", get_octave(), get_accidental())
    update_note_count()
    #preview_note(note_list)
    print(note_list)

def add_D_1():
    global track, editing, note_count
    print("called the add_note function in GUI-test")
    styled_note = pretty_note("D", f"{get_octave() - 1}", f"{get_note_len()}", f"{get_accidental()}")
    if not editing:
        add_note_to_display(styled_note)
        add_note_to_list(str(f"D, {get_octave() - 1}, {get_note_len()}, {get_accidental()}"), note_list)
        add_note_to_track(note_list, track)
    else:
        edit_note("D", get_octave() - 1, get_accidental())
    update_note_count()
    #preview_note(note_list)
    print(note_list)

def add_E_t():
    global track, editing, note_count
    print("called the add_note function in GUI-test")
    styled_note = pretty_note("E", f"{get_octave() + 1}", f"{get_note_len()}", f"{get_accidental()}")
    if not editing:
        add_note_to_display(styled_note)
        add_note_to_list(str(f"E, {get_octave() + 1}, {get_note_len()}, {get_accidental()}"), note_list)
        add_note_to_track(note_list, track)
    else:
        edit_note("E", get_octave() + 1, get_accidental())
    update_note_count()
    #preview_note(note_list)
    print(note_list)

def add_E():
    global track, editing, note_count
    print("called the add_note function in GUI-test")
    styled_note = pretty_note("E", f"{get_octave()}", f"{get_note_len()}", f"{get_accidental()}")
    if not editing:
        add_note_to_display(styled_note)
        add_note_to_list(str(f"E, {get_octave()}, {get_note_len()}, {get_accidental()}"), note_list)
        add_note_to_track(note_list, track)
    else:
        edit_note("E", get_octave(), get_accidental())
    update_note_count()
    #preview_note(note_list)
    print(note_list)

def add_E_1():
    global track, editing, note_count
    print("called the add_note function in GUI-test")
    styled_note = pretty_note("E", f"{get_octave() - 1}", f"{get_note_len()}", f"{get_accidental()}")
    if not editing:
        add_note_to_display(styled_note)
        add_note_to_list(str(f"E, {get_octave() - 1}, {get_note_len()}, {get_accidental()}"), note_list)
        add_note_to_track(note_list, track)
    else:
        edit_note("E", get_octave() - 1, get_accidental())
    update_note_count()
    #preview_note(note_list)
    print(note_list)

def add_F_t():
    global track, editing, note_count
    print("called the add_note function in GUI-test")
    styled_note = pretty_note("F", f"{get_octave() + 1}", f"{get_note_len()}", f"{get_accidental()}")
    if not editing:
        add_note_to_display(styled_note)
        add_note_to_list(str(f"F, {get_octave() + 1}, {get_note_len()}, {get_accidental()}"), note_list)
        add_note_to_track(note_list, track)
    else:
        edit_note("F", get_octave() + 1, get_accidental())
    update_note_count()
    #preview_note(note_list)
    print(note_list)

def add_F():
    global track, editing, note_count
    print("called the add_note function in GUI-test")
    styled_note = pretty_note("F", f"{get_octave()}", f"{get_note_len()}", f"{get_accidental()}")
    if not editing:
        add_note_to_display(styled_note)
        add_note_to_list(str(f"F, {get_octave()}, {get_note_len()}, {get_accidental()}"), note_list)
        add_note_to_track(note_list, track)
    else:
        edit_note("F", get_octave(), get_accidental())
    update_note_count()
    #preview_note(note_list)
    print(note_list)

def add_F_1():
    global track, editing, note_count
    print("called the add_note function in GUI-test")
    styled_note = pretty_note("F", f"{get_octave() - 1}", f"{get_note_len()}", f"{get_accidental()}")
    if not editing:
        add_note_to_display(styled_note)
        add_note_to_list(str(f"F, {get_octave() - 1}, {get_note_len()}, {get_accidental()}"), note_list)
        add_note_to_track(note_list, track)
    else:
        edit_note("F", get_octave() - 1, get_accidental())
    update_note_count()
    #preview_note(note_list)
    print(note_list)

def add_G_t():
    global track, editing, note_count
    print("called the add_note function in GUI-test")
    styled_note = pretty_note("G", f"{get_octave() + 1}", f"{get_note_len()}", f"{get_accidental()}")
    if not editing:
        add_note_to_display(styled_note)
        add_note_to_list(str(f"G, {get_octave() + 1}, {get_note_len()}, {get_accidental()}"), note_list)
        add_note_to_track(note_list, track)
    else:
        edit_note("G", get_octave() + 1, get_accidental())
    update_note_count()
    #preview_note(note_list)
    print(note_list)

def add_G():
    global track, editing, note_count
    print("called the add_note function in GUI-test")
    styled_note = pretty_note("G", f"{get_octave()}", f"{get_note_len()}", f"{get_accidental()}")
    if not editing:
        add_note_to_display(styled_note)
        add_note_to_list(str(f"G, {get_octave()}, {get_note_len()}, {get_accidental()}"), note_list)
        add_note_to_track(note_list, track)
    else:
        edit_note("G", get_octave(), get_accidental())
    update_note_count()
    #preview_note(note_list)
    print(note_list)

def add_G_1():
    global track, editing, note_count
    print("called the add_note function in GUI-test")
    styled_note = pretty_note("G", f"{get_octave() - 1}", f"{get_note_len()}", f"{get_accidental()}")
    if not editing:
        add_note_to_display(styled_note)
        add_note_to_list(str(f"G, {get_octave() - 1}, {get_note_len()}, {get_accidental()}"), note_list)
        add_note_to_track(note_list, track)
    else:
        edit_note("G", get_octave() - 1, get_accidental())
    update_note_count()
    #preview_note(note_list)
    print(note_list)

def add_G_2():
    global track, editing, note_count
    print("called the add_note function in GUI-test")
    styled_note = pretty_note("G", f"{get_octave() - 2}", f"{get_note_len()}", f"{get_accidental()}")
    if not editing:
        add_note_to_display(styled_note)
        add_note_to_list(str(f"G, {get_octave() - 2}, {get_note_len()}, {get_accidental()}"), note_list)
        add_note_to_track(note_list, track)
    else:
        edit_note("G", get_octave() - 2, get_accidental())
    update_note_count()
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

def left_arrow():
    #use the arrows first to select a bar in the track, then to select a note in that bar
    global curr_note_index, track, curr_bar_index, selected_bar
    if selected_bar:
        curr_bar = track.bars[curr_bar_index]
        selected_bar = curr_bar
        if curr_note_index > len(curr_bar.bar) - 1:
            curr_note_index = len(curr_bar.bar) - 1
        #notes = curr_bar
        #notes_list = []
        if curr_note_index > 0:
            curr_note_index -= 1
            print(f"Note at Index {curr_note_index} In Bar {curr_bar_index}: {curr_bar[curr_note_index]}")
        else:
            print(f"Note at Index {curr_note_index} In Bar {curr_bar_index}: {curr_bar[curr_note_index]}")
    else:
        if curr_bar_index > 0:
            curr_bar_index -= 1
            print(f"Bar at Index {curr_bar_index}: {track.bars[curr_bar_index]}")
        else:
            print(f"Bar at Index {curr_bar_index}: {track.bars[curr_bar_index]}")

def right_arrow():
    global curr_note_index, track, curr_bar_index, selected_bar
    if selected_bar:
        curr_bar = track.bars[curr_bar_index]
        selected_bar = curr_bar
        #notes = curr_bar
        #notes_list = []
        if curr_note_index > len(curr_bar.bar) - 1:
            curr_note_index = len(curr_bar.bar) - 1
        if curr_note_index < len(curr_bar.bar) - 1:
            curr_note_index += 1
            print(f"Note at Index {curr_note_index} In Bar {curr_bar_index}: {curr_bar[curr_note_index]}")
        else:
            print(f"Note at Index {curr_note_index} In Bar {curr_bar_index}: {curr_bar[curr_note_index]}")
    else:
        if curr_bar_index < len(track.bars) - 1:
            curr_bar_index += 1
            print(f"Bar at Index {curr_bar_index}: {track.bars[curr_bar_index]}")
        else:
            print(f"Bar at Index {curr_bar_index}: {track.bars[curr_bar_index]}")

def select_bar():
    global selected_bar
    selected_bar = True

def deselect_bar():
    global selected_bar
    selected_bar = False

def select_note():
    global track, curr_note_index, curr_bar_index, editing
    curr_bar = track.bars[curr_bar_index]
    
    print(curr_note_index)
    print(curr_bar[curr_note_index])
    editing = True

def edit_note(note_name, octave, accidental):
    global track, curr_note_index, curr_bar_index, editing, full_note_index

    print(value.dots(value.half))
    print(value.dots(value.quarter))

    notes_in_track = []
    for x in track.get_notes():
        notes_in_track.append(x)

    curr_bar = track.bars[curr_bar_index]
    note = curr_bar[curr_note_index]
    
    #add up all notes in previous bars as well as the notes that come before the curr_note_index
    #in the current bar, this will give you the position of the note in the track
    index = 0
    bars = track.bars
    for i in range(len(bars)):
        #i is a bar
        for j in bars[i]:
            #j is a note
            if i == curr_bar_index and bars[i].bar.index(j) == curr_note_index:
                break
            else:
                index += 1
    
    print(f"index of the note: {index}")
    full_note_index = index

    print(note)
    #note[1] is the note length, set this to note_len
    note_len = note[1]

    note_len_str = ""
    match note_len:
        case 1:
            note_len_str = "wh_"
        case 1.3333333333333333:
            note_len_str = "ha."
        case 2:
            note_len_str = "ha_"
        case 2.6666666666666665:
            note_len_str = "qu."
        case 4:
            note_len_str = "qu_"
        case 8:
            note_len_str = "ei_"

    #get the name of the note with the accidental attached
    if accidental != "n":
        temp = Note(note_name + accidental, octave, velocity=120)
    else:
        temp = Note(note_name, octave, velocity=120)
    
    curr_bar[curr_note_index] = temp
    track[curr_bar_index] = curr_bar
    styled_note = pretty_note(note_name, octave, note_len_str, accidental)
    edit_display(styled_note)
    editing = False

def edit_display(styled_note):
    global full_note_index, track, note_display, note_count, buffer
    note_display[full_note_index] = styled_note
    
    #now redo the display so that the note change applies
    new_display = ""
    note_count = 0
    for x in note_display:
        if (note_count % 12) == 0 and note_count != 0:
            buffer += 1
            print(f"buffer: {buffer}")
        if (note_count % 12) == 0 and note_count != 0: 
            new_display+= "\n" + x + "  |  "
            update_note_count()
            update_staff()
        else:
            new_display += x + "  |  "
            update_note_count()

    note_list_display.configure(text=new_display)

def update_staff():
    global buffer
    treble_clef.place(x=180, y=260 + (buffer * 20))
    bass_clef.place(x=200, y=460 + (buffer * 20))
    t_g_space.place(x=300, y=160 + (buffer * 20))
    t_f_line.place(x=300, y=180 + (buffer * 20))
    t_e_space.place(x=300, y=200 + (buffer * 20))
    t_d_line.place(x=300, y=220 + (buffer * 20))
    t_c_space.place(x=300, y=240 + (buffer * 20))
    t_b_line.place(x=300, y=260 + (buffer * 20))
    t_a_space.place(x=300, y=280 + (buffer * 20))
    t_g_line.place(x=300, y=300 + (buffer * 20))
    f_space.place(x=300, y=320 + (buffer * 20))
    e_line.place(x=300, y=340 + (buffer * 20))
    d_space.place(x=300, y=360 + (buffer * 20))
    c4_line.place(x=300, y=380 + (buffer * 20))
    b_space.place(x=300, y=400 + (buffer * 20))
    a_line.place(x=300, y=420 + (buffer * 20))
    g_space.place(x=300, y=440 + (buffer * 20))
    f_line.place(x=300, y=460 + (buffer * 20))
    e_space.place(x=300, y=480 + (buffer * 20))
    d_line.place(x=300, y=500 + (buffer * 20))
    c_space.place(x=300, y=520 + (buffer * 20))
    b_line.place(x=300, y=540 + (buffer * 20))
    a_space.place(x=300, y=560 + (buffer * 20))
    g_line.place(x=300, y=580 + (buffer * 20))

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
    global track
    tempo = get_tempo()
    try:
        tempo_num = int(tempo)
    except:
        tempo_num = 120

    fluidsynth.play_Track(track, 1, tempo_num)

note_list = []
note_display = []
buffer = 0
note_count = 0
len_var = tkinter.IntVar(app, 5)
acc_var = tkinter.IntVar(app, 3)
curr_note_index = 0
selected_bar = False
curr_bar_index = 0
editing = False
#the index of the note in the full track, used to edit the display string
full_note_index = 0

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

edit_button = customtkinter.CTkButton(master=app, text="Edit Note", command=select_note)
edit_button.place(x=20, y=210)

select_bar_button = customtkinter.CTkButton(master=app, text="Select Bar", command=select_bar)
select_bar_button.place(x=20, y=250)

deselect_bar_button = customtkinter.CTkButton(master=app, text="Deselect Bar", command=deselect_bar)
deselect_bar_button.place(x=20, y=290)

left_button = customtkinter.CTkButton(master=app, text="←", width=65, font=accidental_font, command=left_arrow)
left_button.place(x=20, y=330)

right_button = customtkinter.CTkButton(master=app, text="→", width=65, font=accidental_font, command=right_arrow)
right_button.place(x=95, y=330)

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

len_button_1 = customtkinter.CTkRadioButton(master=app, text="W", font=len_font,
                                             command=len_button_event, variable= len_var, value=1)
len_button_2 = customtkinter.CTkRadioButton(master=app, text="H.", font=len_font,
                                             command=len_button_event, variable= len_var, value=2)
len_button_3 = customtkinter.CTkRadioButton(master=app, text="H", font=len_font,
                                             command=len_button_event, variable= len_var, value=3)
len_button_4 = customtkinter.CTkRadioButton(master=app, text="Q.", font=len_font,
                                             command=len_button_event, variable= len_var, value=4)
len_button_5 = customtkinter.CTkRadioButton(master=app, text="Q", font=len_font,
                                             command=len_button_event, variable= len_var, value=5)
len_button_6 = customtkinter.CTkRadioButton(master=app, text="E", font=len_font,
                                             command=len_button_event, variable= len_var, value=6)

len_button_1.place(x=200, y=90)
len_button_2.place(x=250, y=90)
len_button_3.place(x=300, y=90)
len_button_4.place(x=350, y=90)
len_button_5.place(x=400, y=90)
len_button_6.place(x=450, y=90)

note_list_display=customtkinter.CTkLabel(master=app, font=note_font, text="", justify="left")
note_list_display.place(x=200, y=130)

note_add_warning=customtkinter.CTkLabel(master=app, font=note_font, justify="left",
                                        text="")
note_add_warning.place(relx=0.8, rely=0.05)

note_count_label=customtkinter.CTkLabel(master=app, font=note_font, justify="left",
                                        text="")#text="note count")
note_count_label.place(relx=0.85, rely=0.05)

treble_clef=customtkinter.CTkLabel(master=app, font=clef_font, justify="right", width=120,
                                        text="TREBLE\nCLEF")
treble_clef.place(x=180, y=260 + (buffer * 20))

bass_clef=customtkinter.CTkLabel(master=app, font=clef_font, justify="right", width=120,
                                        text="BASS\nCLEF")
bass_clef.place(x=200, y=460 + (buffer * 20))

t_g_space=customtkinter.CTkButton(master=app, text="                                                 ", command=add_G_t, height=10, width=405,
                                 fg_color="transparent", hover=False, border_width=0, anchor="n", font=note_font)
t_g_space.place(x=300, y=160 + (buffer * 20))

t_f_line=customtkinter.CTkButton(master=app, text="__________________________________________________", command=add_F_t, height=1,
                                 fg_color="transparent", hover=False, border_width=0, font=note_font)
t_f_line.place(x=300, y=180 + (buffer * 20))

t_e_space=customtkinter.CTkButton(master=app, text="                                                 ", command=add_E_t, height=10, width=405,
                                 fg_color="transparent", hover=False, border_width=0, anchor="n", font=note_font)
t_e_space.place(x=300, y=200 + (buffer * 20))

t_d_line = customtkinter.CTkButton(master=app, text="__________________________________________________", command=add_D_t, height=1,
                                 fg_color="transparent", hover=False, border_width=0, font=note_font)
t_d_line.place(x=300, y=220 + (buffer * 20))

t_c_space=customtkinter.CTkButton(master=app, text="                                                 ", command=add_C_t, height=10, width=405,
                                 fg_color="transparent", hover=False, border_width=0, anchor="n", font=note_font)
t_c_space.place(x=300, y=240 + (buffer * 20))

t_b_line = customtkinter.CTkButton(master=app, text="__________________________________________________", command=add_B, height=1,
                                 fg_color="transparent", hover=False, border_width=0, font=note_font)
t_b_line.place(x=300, y=260 + (buffer * 20))

t_a_space=customtkinter.CTkButton(master=app, text="                                                 ", command=add_A, height=10, width=405,
                                 fg_color="transparent", hover=False, border_width=0, anchor="n", font=note_font)
t_a_space.place(x=300, y=280 + (buffer * 20))

t_g_line=customtkinter.CTkButton(master=app, text="__________________________________________________", command=add_G, height=10, width=405,
                                 fg_color="transparent", hover=False, border_width=0, anchor="n", font=note_font)
t_g_line.place(x=300, y=300 + (buffer * 20))

f_space=customtkinter.CTkButton(master=app, text="                                                 ", command=add_F, height=1,
                                 fg_color="transparent", hover=False, border_width=0, font=note_font)
f_space.place(x=300, y=320 + (buffer * 20))

e_line=customtkinter.CTkButton(master=app, text="__________________________________________________", command=add_E, height=10, width=405,
                                 fg_color="transparent", hover=False, border_width=0, anchor="n", font=note_font)
e_line.place(x=300, y=340 + (buffer * 20))

d_space = customtkinter.CTkButton(master=app, text="                                                 ", command=add_D, height=1,
                                 fg_color="transparent", hover=False, border_width=0, font=note_font)
d_space.place(x=300, y=360 + (buffer * 20))

c4_line=customtkinter.CTkButton(master=app, text="_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _", command=add_C, height=10, width=405,
                                 fg_color="transparent", hover=False, border_width=0, anchor="n", font=note_font)
c4_line.place(x=300, y=380 + (buffer * 20))

b_space = customtkinter.CTkButton(master=app, text="                                                 ", command=add_B_1, height=1,
                                 fg_color="transparent", hover=False, border_width=0, font=note_font)
b_space.place(x=300, y=400 + (buffer * 20))

a_line=customtkinter.CTkButton(master=app, text="__________________________________________________", command=add_A_1, height=1,
                                 fg_color="transparent", hover=False, border_width=0, anchor="n", font=note_font)
a_line.place(x=300, y=420 + (buffer * 20))

g_space=customtkinter.CTkButton(master=app, text="                                                 ", command=add_G_1, height=10, width=405,
                                 fg_color="transparent", hover=False, border_width=0, anchor="n", font=note_font)
g_space.place(x=300, y=440 + (buffer * 20))

f_line=customtkinter.CTkButton(master=app, text="__________________________________________________", command=add_F_1, height=1,
                                 fg_color="transparent", hover=False, border_width=0, font=note_font)
f_line.place(x=300, y=460 + (buffer * 20))

e_space=customtkinter.CTkButton(master=app, text="                                                 ", command=add_E_1, height=10, width=405,
                                 fg_color="transparent", hover=False, border_width=0, anchor="n", font=note_font)
e_space.place(x=300, y=480 + (buffer * 20))

d_line = customtkinter.CTkButton(master=app, text="__________________________________________________", command=add_D_1, height=1,
                                 fg_color="transparent", hover=False, border_width=0, font=note_font)
d_line.place(x=300, y=500 + (buffer * 20))

c_space=customtkinter.CTkButton(master=app, text="                                                 ", command=add_C_1, height=10, width=405,
                                 fg_color="transparent", hover=False, border_width=0, anchor="n", font=note_font)
c_space.place(x=300, y=520 + (buffer * 20))

b_line = customtkinter.CTkButton(master=app, text="__________________________________________________", command=add_B_2, height=1,
                                 fg_color="transparent", hover=False, border_width=0, font=note_font)
b_line.place(x=300, y=540 + (buffer * 20))

a_space=customtkinter.CTkButton(master=app, text="                                                 ", command=add_A_2, height=10, width=405,
                                 fg_color="transparent", hover=False, border_width=0, anchor="n", font=note_font)
a_space.place(x=300, y=560 + (buffer * 20))

g_line = customtkinter.CTkButton(master=app, text="__________________________________________________", command=add_G_2, height=1,
                                 fg_color="transparent", hover=False, border_width=0, font=note_font)
g_line.place(x=300, y=580 + (buffer * 20))



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

app.mainloop()