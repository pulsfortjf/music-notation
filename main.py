import winsound

#constants for duration (change this format later to use a formula)
WH = 2000
HA = 1000
QU = 500
EI = 250

#constants for each note and its corresponding frequency
C = 32.70 #Cn
CsDb = 34.65 #Cs OR Db
D = 36.71 #Dn
DsEb = 38.89 #Ds OR Eb
E = 41.20 #En
F = 43.65 #Fn
FsGb = 46.25 #Fs OR Gb
G = 49.00 #Gn
GsAb = 51.91 #Gs OR Ab
A = 55.00 #An
AsBb = 58.27 #As OR Bb
B = 61.74 #Bn

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
        case "wh":
            note_val[2] = WH
        case "ha":
            note_val[2] = HA
        case "qu":
            note_val[2] = QU
        case "ei":
            note_val[2] = EI

    #convert the notes the user input into the correct constant
    #convert the contant into the correct frequency based on the octave from the user input
    #create a tuple with that contant and the duration
    match note_match:
        case "Cn":
            return (calc_frequency(C, int(note_val[1])), note_val[2])
        case "Cs" | "Db":
            return (calc_frequency(CsDb, int(note_val[1])), note_val[2])
        case "Dn":
            return (calc_frequency(D, int(note_val[1])), note_val[2])
        case "Ds" | "Eb":
            return (calc_frequency(DsEb, int(note_val[1])), note_val[2])
        case "En":
            return (calc_frequency(E, int(note_val[1])), note_val[2])
        case "Fn":
            return (calc_frequency(F, int(note_val[1])), note_val[2])
        case "Fs" | "Gb":
            return (calc_frequency(FsGb, int(note_val[1])), note_val[2])
        case "Gn":
            return (calc_frequency(G, int(note_val[1])), note_val[2])
        case "Gs" | "Ab":
            return (calc_frequency(GsAb, int(note_val[1])), note_val[2])
        case "An":
            return (calc_frequency(A, int(note_val[1])), note_val[2])
        case "As" | "Bb":
            return (calc_frequency(AsBb, int(note_val[1])), note_val[2])
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
            case "wh":
                x = WH
            case "ha":
                x[1] = HA
            case "qu":
                x[1] = QU
            case "ei":
                x[1] = EI
    return note_list

#takes the user input to put the notes into a list and then runs the play function when the user types play
def takeInput(note_list):
    while True:
        print("Input Format: note, octave, length, sharp/flat/natural")
        print(" Where note, octave, length, and sharp/flat/natual are in the formats specified below:")
        print(" note: Capital letter A-G")
        print(" octave: A single number 1-6")
        print(" length: Whole Note = wh, Half Note = ha, Quarter Note = qu, Eighth Note = ei")
        print(" s/f/n: Sharp = #, Flat = b, Natural = n")
        print(" Example: to input a quarter note 4th Octave A natural; A, 4, qu, n")
        print("Type play when you have finished entering notes")
        inputNote = input("Enter a note: ")
        if (inputNote == "play"):
            play(note_list)
            break
        else:
            inputNote = add_note_to_list(inputNote, note_list)

def main():
    note_list = []
    takeInput(note_list)
    for x in note_list:
        print(x)

main()