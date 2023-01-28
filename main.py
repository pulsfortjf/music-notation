import winsound

#default tempo is 120 bpm, if the user inputs "tempo" this will be changed to whatever the user selects
_QU_len = 500
_WH_len = int(_QU_len * 4)
_HA_len = int(_QU_len * 2)
_EI_len = int(_QU_len * 0.5)
_QU_dot = int(_QU_len + _EI_len)
_HA_dot = int(_HA_len + _QU_len)

#constants for each note and its corresponding frequency
C = 32.70 #Cn
_CsDb = 34.65 #Cs OR Db
D = 36.71 #Dn
_DsEb = 38.89 #Ds OR Eb
E = 41.20 #En
F = 43.65 #Fn
_FsGb = 46.25 #Fs OR Gb
G = 49.00 #Gn
_GsAb = 51.91 #Gs OR Ab
A = 55.00 #An
_AsBb = 58.27 #As OR Bb
B = 61.74 #Bn

def calc_tempo():
    #first, prompt user to enter a tempo and take user input
    print("Tempo should be entered as a string of digits and it must be greater than 0")
    print("The tempo should be entered in BPM where the quarter note gets the beat")
    while True:
        #use try to set tempo to an int from the user input
        try:    
            tempo = int(input("Enter a tempo: "))
        #if input can't be converted to int then the string is invalid
        except:
            print("Invalid tempo, please input a valid tempo")
            print("Tempo should be entered as a string of digits and it must be greater than 0")
            print("The tempo should be entered in BPM where the quarter note gets the beat")
        #if no errors occur, continue to valid the tempo
        else:
            if tempo <= 0:
                print("Tempo must be greater than 0.")
            else:
                global _WH_len, _HA_len, _QU_len, _EI_len, _QU_dot, _HA_dot
                _QU_len = int((60 / tempo) * 1000)
                _WH_len = int(_QU_len * 4)
                _HA_len = int(_QU_len * 2)
                _EI_len = int(_QU_len * 0.5)
                _QU_dot = int(_QU_len + _EI_len)
                _HA_dot = int(_HA_len + _QU_len)
                print(f"Tempo is now set to {int(60 / (_QU_len / 1000))} BPM")
                break

#plays the notes the user input using winsound.Bee
def play(note_list):
    #loop through the list and play each sound at the frequency specified and for the duration specified
    for x in note_list:
        winsound.Beep(int(x[0]), x[1])


    #delete this later, its just so VSCode doesnt tell me there are errors
    #winsound.Beep(440, 1000)

#adds the specific note to the list of notes
def add_note_to_list(inputNote, note_list):
    note_list.append(calc_note(inputNote))
    #print(note_list)

#takes the user input in its initial form and converts it to the tuple of (frequency, duration) that winsound.Beep can accept
def calc_note(note):
    #input will be in the form "note, octave, length, s/f/n"
    #the length and octave can be ignored, we need to take the note and the s/f/n and find which note constant it matches
    temp = str(note)
    note_val = temp.split(", ")

    if note_val[3] == "#":
        note_val[3] = "s"

    note_match = note_val[0] + note_val[3]

    #convert the lowercase length from the user into the correct length constant
    match note_val[2]:
        case "wh_":
            note_val[2] = _WH_len
        case "ha_":
            note_val[2] = _HA_len
        case "qu_":
            note_val[2] = _QU_len
        case "ei_":
            note_val[2] = _EI_len
        case "qu.":
            note_val[2] = _QU_dot
        case "ha.":
            note_val[2] = _HA_dot

    #convert the notes the user input into the correct constant
    #convert the contant into the correct frequency based on the octave from the user input
    #create a tuple with that contant and the duration
    match note_match:
        case "Cn":
            return (calc_frequency(C, int(note_val[1])), note_val[2])
        case "Cs" | "Db":
            return (calc_frequency(_CsDb, int(note_val[1])), note_val[2])
        case "Dn":
            return (calc_frequency(D, int(note_val[1])), note_val[2])
        case "Ds" | "Eb":
            return (calc_frequency(_DsEb, int(note_val[1])), note_val[2])
        case "En":
            return (calc_frequency(E, int(note_val[1])), note_val[2])
        case "Fn":
            return (calc_frequency(F, int(note_val[1])), note_val[2])
        case "Fs" | "Gb":
            return (calc_frequency(_FsGb, int(note_val[1])), note_val[2])
        case "Gn":
            return (calc_frequency(G, int(note_val[1])), note_val[2])
        case "Gs" | "Ab":
            return (calc_frequency(_GsAb, int(note_val[1])), note_val[2])
        case "An":
            return (calc_frequency(A, int(note_val[1])), note_val[2])
        case "As" | "Bb":
            return (calc_frequency(_AsBb, int(note_val[1])), note_val[2])
        case "Bn":
            return (calc_frequency(B, int(note_val[1])), note_val[2])

#takes the user input note (i.e A) and Octave (i.e 4) and returns the correct frequency for that note and octave (i.e A4 = 440)
def calc_frequency(input_note, n):
    frequency = input_note
    if n == 1:
        return frequency
    else:
        for x in range(n-1):
            frequency = frequency * 2
    
    return frequency

#formats the user input length into milliseconds which is the format that winsound.Beep requires
def format_duration(note_list):
    for x in note_list:
        match x[1]:
            case "wh_":
                x = _WH_len
            case "ha_":
                x[1] = _HA_len
            case "qu_":
                x[1] = _QU_len
            case "ei_":
                x[1] = _EI_len
            case "qu.":
                x[1] = _QU_dot
            case "ha.":
                x[1] = _HA_dot
    return note_list

def valid_input(inputNote):
    #if input is play or tempo, that command is needed in order to continue the program so return true
    if inputNote == "play" or inputNote == "tempo":
        return True
    
    valid_note = "ABCDEFG"
    valid_octave = "123456"
    valid_length = ["wh_", "ha_", "ha.", "qu_", "qu.", "ei_"]
    valid_accidental = "#bn"
    #input string should be exactly 12 characters, anything else is automatically invalid
    if len(inputNote) != 12:
        return False
    else:
        #input should have a comma and a space separating each part; split the string using ", " and the resulting list should be length 4, if not, the string is invalid
        note_parts = str(inputNote).split(", ")
        if len(note_parts) != 4:
            print("Inputs must be in 4 parts all separated by a single comma and a space.")
            return False
        else:
            #check each part of the list to see if that portion is valid, if all parts are valid, return True, if any part is not, return False
            if len(note_parts[0]) != 1 or (note_parts[0] not in valid_note):
                print("The Note you entered was not valid.")
                return False
            if len(note_parts[1]) != 1 or (note_parts[1] not in valid_octave):
                print("The Octave you entered was not valid.")
                return False
            if len(note_parts[2]) != 3 or (note_parts[2] not in valid_length):
                print("The Length you entered was not valid.")
                return False
            if len(note_parts[3]) != 1 or (note_parts[3] not in valid_accidental):
                print("The Accidental you entered was not valid.")
                return False
        return True

#takes the user input to put the notes into a list and then runs the play function when the user types play
def takeInput(note_list):
    while True:
        print(" Input Format: note, octave, length, sharp/flat/natural")
        print("     Where note, octave, length, and sharp/flat/natual are in the formats specified below:")
        print("     note: Capital letter A-G")
        print("     octave: A single number 1-6")
        print("     length: Whole Note = wh_, Half Note = ha_, Dotted Half Note = ha., Quarter Note = qu_, Dotted Quarter Note = qu., Eighth Note = ei_")
        print("     s/f/n: Sharp = #, Flat = b, Natural = n")
        print("     Example: to input a quarter note 4th Octave A natural; A, 4, qu_, n")
        print(f" Current tempo = {int(60 / (_QU_len / 1000))}")
        print(" Type play when you have finished entering notes, type exit to quit the program, or type tempo to change the tempo")
        inputNote = input("Enter a note: ")
        if valid_input(inputNote):
            if inputNote == "play":
                play(note_list)
                break
            elif inputNote == "tempo":
                calc_tempo()
            else:
                inputNote = add_note_to_list(inputNote, note_list)
        else:
            if inputNote == "exit":
                break
            print("Input is invalid, please follow the specified format")

def main():
    #testing if winsound.PlaySound will play a wav file and how that function works
    #winsound.PlaySound("home_depot_theme_song.WAV", winsound.SND_FILENAME)
    note_list = []
    takeInput(note_list)
    for x in note_list:
        print(x)

main()