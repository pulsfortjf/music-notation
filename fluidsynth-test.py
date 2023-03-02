import time
from mingus.containers import Note
from mingus.midi import fluidsynth

def main():
    #input("Press Enter")
    fluidsynth.init("D:\\Capstone\\repos\\capstone-prototype\\capstone-prototype\\soundfonts\\FluidR3_GM.sf2", 'dsound')
    c5 = Note("C-5")

    ab4 = Note()

    ab4 = Note.from_hertz(ab4, 415.28, 440)
    ab4_test = Note("Ab-4")

    fluidsynth.play_Note(ab4)
    time.sleep(1)
    fluidsynth.play_Note(ab4_test)
    time.sleep(1)
    fluidsynth.stop_everything()

main()