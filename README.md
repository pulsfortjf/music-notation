# capstone-prototype
Prototype Version of my capstone music notation software

  main.py is the main driver file for the program.
  Currently it is uses command line based input from the user to obtain the notes the user wants to add to the "composition".
  The input format is Note, Octave, Length, and Sharp/Flat/Natural
  This input is processed into a tuple with the correct frequency for the pitch the user entered as well as the duration the tone should play for.
  the winsound module is used to play the sounds, specifically using the winsound.Beep() function.
