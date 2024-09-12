# MEScore
MEscore is a desktop music notation application written entirely using Python.
To facilitate the creation of a GUI, the storage of music notes, and the playback of music notes, the following external modules were used:

The CustomTKInter module was used to create the GUI. The GUI consists of buttons for note length and accidentals, a textbox to enter a new tempo, a button to change to the new tempo, a textbox to enter a new octave, buttons to enable the editing of notes in the composition, a section to display the composition with notes in a text-based format, and a staff used to insert notes into the composition.

The mingus and fluidsynth modules are used to store the composition as a collection of Note objects as well as enabling the playback feature of the program. Given an instrument library to use, the mingus module uses the play_note() function from fluidsynth to play the given note on the given instrument in the library (by default this is a piano).
