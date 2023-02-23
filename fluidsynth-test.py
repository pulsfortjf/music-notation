import time
from mingus.containers import Note
from mingus.midi import fluidsynth

def main():
    #input("Press Enter")
    fluidsynth.init("D:\\Capstone\\repos\\capstone-prototype\\capstone-prototype\\soundfonts\\FluidR3_GM.sf2", 'dsound')
    c5 = Note("C-5")

    fluidsynth.play_Note(c5)
    time.sleep(5)
    fluidsynth.stop_everything()

main()