# Real-Time Fast Fourier Plotting

This code runs as a three module system, allowing the user to open an audio stream and take in live audio from the device microphones and graph it to either time or frequency domain. On top of this, the frequency domain plotting integrates a musical scale as a reference dictionary against which the value of the first peak in the Fourier Transform is checked. This comparison is a print-to-console, outputting the name of the closest note in the scale dictionary as a string.

In order for this code to function properly the user will need to update the file path of `surfrock.wav` to match its location in their own directory. This is a drawback and will be changed in future iterations of this project such that the code will be able to pull the current working directory or open a stream indepently of existing files.

The main functionality module is audio.py and that should be run to view graphing and peak data. Note that it might need to be run twice in order to create pycache data when pulling from other working directory modules.

### Modules:

##### xorshift.py

The xorshift module is a modified xorshift algorithm made as a pseudo-random number generator (PRNG) for use in other modules. It combines system time at function call with user entered integers in order to seed the algorithm and returns an integer within a declared range.

##### note_def.py

This module contains two classes from which to generate note and scale objects based off of a user input frequency for A4. Any transformation of a note or scale object and their generation uses equal temperament calculations for tonal relationships. The output of a scale or note can be compared using [this site](https://pages.mtu.edu/~suits/notefreqs.html).

##### audio.py

This is the main functionality module. The Wave() class object opens a pyaudio stream from any .wav file (directory needs to be explicited) and takes microphone input to graph either time or frequency domain information. The frequency domain information will also return the value of the first peak frequency and plot it while printing to console the name of the closest note in the Scale() object. This is by default set to the chromatic scale.
