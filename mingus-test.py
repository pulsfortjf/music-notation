import mingus.core.notes as notes
from mingus.containers import Note, NoteContainer
from mingus.midi import midi_file_out
import winsound
import pygame
from pydub import AudioSegment
import os
import timidity

def convert():
    os.system("timidity test1.mid -Ow -o test2.wav")

def play_music(music_file):
    """
    stream music with mixer.music module in blocking manner
    this will stream the sound from disk while playing
    """
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

def get_note(notes_list):
    input_note = input("Enter a note as a capital letter A-G followed by an optional accidental # or b: ")
    if notes.is_valid_note(input_note):
        notes_list.append(input_note)
    print(notes_list)

def main():
    #notes_list = []
    #get_note(notes_list)
    nc = NoteContainer(["A-4", "C-4", "E-4", "A-4", "C-4", "E-4", "A-4", "C-4", "E-4", "A-4", "C-4", "E-4"])
    note_list = ["A-4", "C-4", "E-4", "A-4", "C-4", "E-4", "A-4", "C-4", "E-4", "A-4", "C-4", "E-4"]
    for x in note_list:
        midi_file_out.write_Note("test1.mid", Note(x), 120, 3)
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
main()