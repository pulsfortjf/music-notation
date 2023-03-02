import mingus.core.notes as notes
import mingus.core.value as value
from mingus.containers import Note, NoteContainer, Track, Bar
from mingus.midi import midi_file_out
from mingus.midi import fluidsynth
import time
#import winsound
#import pygame
#from pydub import AudioSegment
#import os
#import timidity

#def convert():
    #os.system("timidity test1.mid -Ow -o test2.wav")

"""
def play_music(music_file):
    #stream music with mixer.music module in blocking manner
    #this will stream the sound from disk while playing
    clock = pygame.time.Clock()
    try:
        pygame.mixer.music.load(music_file)
        print(f"Music file {music_file} loaded!")
    except pygame.error:
        print(f"File {(music_file, pygame.get_error())} not found! ({(music_file, pygame.get_error())})")
        return
    pygame.mixer.music.play()
    print("playing")
    while pygame.mixer.music.get_busy():
        # check if playback has finished
        print("still playing")
        clock.tick(30)
"""

def track_test():
    track = Track()
    c = Note("C-5")
    c.channel = 1
    c.velocity = 120
    e = Note("E-5")
    e.channel = 1
    e.velocity = 120
    g = Note("G-5")
    g.channel = 1
    g.velocity = 120

    track.add_notes(c, value.quarter)
    track.add_notes(e, value.quarter)
    track.add_notes(g, value.quarter)
    track.add_notes(c, value.eighth)
    track.add_notes(c, value.eighth)
    track.add_notes(e, value.quarter)
    track.add_notes(g, value.half)
    track.add_notes(c, value.quarter)

    new_track = Track()
    last_bar = Bar()
    for x in range(len(track)):
        print(track[x])
        if x < len(track) - 1:
            new_track.add_bar(track[x])
        else:
            last_bar = track[x]
    print(new_track)
    print(last_bar)
    new_last_bar = Bar()
    for x in range(len(last_bar)):
        print(last_bar[x][1])
        if x < len(last_bar) - 1:
            new_last_bar.place_notes(last_bar[x][2], last_bar[x][1])
    print(new_last_bar)
    new_track.add_bar(new_last_bar)
    print(new_track)
    track = new_track
    new_track.add_notes(e, value.quarter)
    print(new_track)
    print(track)

def play_test():
    track = Track()
    c = Note("C-5")
    c.channel = 1
    c.velocity = 120
    e = Note("E-5")
    e.channel = 1
    e.velocity = 120
    g = Note("G-5")
    g.channel = 1
    g.velocity = 120

    track.add_notes(c, value.quarter)
    track.add_notes(e, value.quarter)
    track.add_notes(g, value.quarter)
    track.add_notes(c, value.eighth)
    track.add_notes(c, value.eighth)
    track.add_notes(e, value.quarter)
    track.add_notes(g, value.half)
    track.add_notes(c, value.quarter)
    #track.add_notes(e, value.whole)
    #stores the last bar so we can remove the last note and then add the bar back
    #fluidsynth.play_Track(track, 1, 120)
    time.sleep(2)
    last_bar = track[len(track) - 1]
    print(last_bar)
    new_track = Track(track[:len(track) - 1])
    print(len(track))
    print(f"track: {track}")
    print(f"track: {track[:len(track) - 1]}")
    print(f"track: {track[len(track) - 1]}")
    print(f"last_bar: {last_bar}")
    print(f"new_track: {new_track}")
    last_bar = last_bar[0:len(last_bar) - 1]
    print(f"last_bar: {last_bar}")
    new_track.add_bar(last_bar)
    print(f"new_track: {new_track}")
    #track = Track(new_track)
    print(f"new_track: {track}")
    #fluidsynth.play_Note(n)
    #fluidsynth.play_Track(track, 1, 120)
    #time.sleep(0.5)
    track.add_notes(c, value.quarter)
    print(f"new_track: {track}")
    time.sleep(0.5)
    #fluidsynth.play_Track(track, 2, 120)

    print("success")

def get_note(notes_list):
    input_note = input("Enter a note as a capital letter A-G followed by an optional accidental # or b: ")
    if notes.is_valid_note(input_note):
        notes_list.append(input_note)
    print(notes_list)

def main():
    notes_list = []
    #get_note(notes_list)

    fluidsynth.init("D:\\Capstone\\repos\\capstone-prototype\\capstone-prototype\\soundfonts\\FluidR3_GM.SF2")

    #play_test()
    track_test()
    #nc = NoteContainer(["A-4", "C-4", "E-4", "A-4", "C-4", "E-4", "A-4", "C-4", "E-4", "A-4", "C-4", "E-4"])
    #note_list = ["A-4", "C-4", "E-4", "A-4", "C-4", "E-4", "A-4", "C-4", "E-4", "A-4", "C-4", "E-4"]
    #for x in notes_list:
    #    midi_file_out.write_Note("test1.mid", Note(x), 120, 3)
    
    """
    freq = 44100    # audio CD quality
    bitsize = -16   # unsigned 16 bit
    channels = 1    # 1 is mono, 2 is stereo
    buffer = 1024    # number of samples
    pygame.mixer.init(freq, bitsize, channels, buffer)

    # optional volume 0 to 1.0
    pygame.mixer.music.set_volume(0.8)
    #play_music("D:\\Jack\\VSCode\\repos\\capstone-prototype\\capstone-prototype\\test1.mid")
    #play_music("D:\\Jack\\VSCode\\repos\\capstone-prototype\\capstone-prototype\\home_depot_theme_song.wav")
    convert()
    play_music("D:\\Jack\\VSCode\\repos\\capstone-prototype\\capstone-prototype\\test2.wav")
    """

main()