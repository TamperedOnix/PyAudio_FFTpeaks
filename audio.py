import pyaudio
import wave
import struct
import pandas as pd
from scipy.fftpack import fft
from scipy.signal import find_peaks
import matplotlib.pyplot as plt
import numpy as np
import note_def as nd

ref_A4 = float(input("Enter your relative base pitch of A4 in Hz: "))
test_file = "C:/Users/matti/Desktop/VScode/Final Project/surfrock.wav"

# Dictionary containing stepwise instructions for constructing a scale
# using the Note() class defined .pitchconv() method
mode = {"ionian": [0, 2, 2, 1, 2, 2, 2, 1],
        "dorian": [0, 2, 1, 2, 2, 2, 1, 2],
        "phrygian": [0, 1, 2, 2, 2, 1, 2, 2],
        "lydian": [0, 2, 2, 2, 1, 2, 2, 1],
        "myxolodian": [0, 2, 2, 1, 2, 2, 1, 2],
        "aeolian": [0, 2, 1, 2, 2, 1, 2, 2],
        "locrian": [0, 1, 2, 2, 1, 2, 2, 2], 
        "chromatic": [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]}

# Construct our reference Note() and Scale() objects from the input frequency for A4
note_A = nd.Note("A", ref_A4, 4)
A_chromatic = nd.Scale("Chromatic", note_A, mode["chromatic"])

class Wave:
    """
    Class that opens a `.wav` file and subsequently an audio stream from which
    to read live audio input from user microphone and graph it real-time.
    Takes as arguments (`filename: str`)
    ---

    ## Methods:

    - `live_plot()`: Read and graph incoming audio intensity over time.

    -`fft_plot(distance: float)`: Read and graph incoming audio intensity over
    frequency using numpy Fast Fourier Transforms. Outputs all peaks beyond the 
    input `distance` and returns the name of the corresponding closest note in the
    scale.

    """
    def __init__(self, file) -> None:
        # Declare file specifications for opening PyAudio data stream
        self.CHUNK = 1024 * 4
        self.obj = wave.open(file, "r")
        self.callback_output = []
        self.data = self.obj.readframes(self.CHUNK)
        self.rate = 44100

        # Initiate an instance of PyAudio
        self.p = pyaudio.PyAudio()

        # Open a stream with the file specifications
        self.stream = self.p.open(format = pyaudio.paInt16,
                                  channels = self.obj.getnchannels(),
                                  rate = self.rate,
                                  output = True,
                                  input = True,
                                  frames_per_buffer = self.CHUNK)

    def live_plot(self):
        """
        Read and graph incoming audio intensity over time.
        """
        plt.style.use('dark_background')

        # Set matplotlib subplots with correct chunk size buffer for writing
        # live data
        x = np.arange(0, 2 * self.CHUNK, 2)
        fig, ax = plt.subplots()
        line, = ax.plot(x, np.random.rand(self.CHUNK))

        # Bind plot window sizes
        ax.set_ylim(-255, 255)
        ax.set_xlim(0, self.CHUNK)

        plt.show(block = False)

        while True:
            # Read incoming audio data
            plot_data = self.stream.read(self.CHUNK)

            # Turn bit data into and integer then cast to array and set line to be drawn
            self.data_int = pd.DataFrame(struct.unpack(\
                            str(self.CHUNK * 2) + 'h', plot_data)).astype(dtype = "b")[::2]
            line.set_ydata(self.data_int)

            # Draw monitored audio intensity levels
            ax.draw_artist(ax.patch)
            ax.draw_artist(line)

            # Update canvas then clear for next iteration
            fig.canvas.update()
            fig.canvas.flush_events()

            # Exit program when plot window is closed
            fig.canvas.mpl_connect('close_event', exit)
        
    def fft_plot(self, distance: float):
        """
        Read and graph incoming audio intensity over
        frequency using numpy Fast Fourier Transforms. Outputs all peaks beyond the 
        input `distance` and returns the name of the corresponding closest note in the
        scale.\n
        Takes as input: (`peak distance: float`)
        """
        plt.style.use('dark_background')

        # Set matplotlib subplots with correct chunk size buffer for writing
        # live data and initialize scatterplot for peak finding
        x_fft = np.linspace(0, self.rate, self.CHUNK)
        fig, ax = plt.subplots()
        line_fft, = ax.semilogx(x_fft, np.random.rand(self.CHUNK), "-", lw = 2)
        scat = ax.scatter([], [], c = "orange", marker = "x")

        # Bind plot window sizes
        ax.set_xlim(20, self.rate / 2)
        ax.set_ylim(-1, 1.5)

        def closest_note(peaks: list, freq_list: list) -> str:
            """
            Prints to console the name (`str`) of the closest note from the
            evaluation of input frequency against the list of all frequencies 
            in our current scale.\n
            Takes as input: (`peak values: list, frequencies in scale: list`)
            """

            # Find the closest value from our scale and print its name to console
            shift_val = min(freq_list, key = lambda x: abs(x - float(peaks)))
            print(A_chromatic.getnotebyfreq(shift_val))

        # Initialize data to correct formats and chunk size for live plotting
        plot_data = self.stream.read(self.CHUNK)
        self.data_int = pd.DataFrame(struct.unpack(\
                        str(self.CHUNK * 2) + 'h', plot_data)).astype(dtype = "b")[::2]
        y_fft = fft(self.data_int)
        line_fft.set_ydata(np.abs(y_fft[0:self.CHUNK]) / (256 * self.CHUNK))

        plt.show(block = False)

        while True:
            # Read incoming audio data
            data = self.stream.read(self.CHUNK)
            
            # Convert data to bits then to array
            self.data_int = struct.unpack(str(4 * self.CHUNK) + 'B', data)
            
            # Recompute FFT and update line
            yf = fft(self.data_int)
            line_data = np.abs(yf[0:self.CHUNK])  / (128 * self.CHUNK)
            line_fft.set_ydata(line_data)

            # Find all values above threshold
            peaks, _ = find_peaks(line_data, distance = distance)
            array_peaks = np.c_[x_fft[peaks], line_data[peaks]]

            # Update the plot
            scat.set_offsets(array_peaks)
            fig.canvas.draw()
            fig.canvas.flush_events()

            # Find and print the closest note at each time step
            closest_note(x_fft[peaks][0], A_chromatic.getfreqaslist())

            # Exit program when plot window is closed
            fig.canvas.mpl_connect('close_event', exit)

"""
To see the current scale we are in you can use:
    print(A_chromatic)

The dictionary prints in order of generation and is unsorted
"""

# Calling the functions with trial and error determined test values
audio_test = Wave(test_file)
audio_test.fft_plot(2000)
