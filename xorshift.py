'''
Xorshift modified program to generate pseudo-random numbers by using system
time and user input integers to create harder to trace inputs. This was 
inspired by cryptographic uses of atmospheric noise as cipher keys.
'''

# pull library to get system time
import time

def timeGet() -> int:
  """
  Create a function timeGet() that generates a string of numbers from the 
  date-time format of time.ctime()
  """

  # pull and return the current system time in nanoseconds
  seedMod = time.time_ns()
  return seedMod

# request user input of any integer of any length
try:
  seed = int(input("Enter a numerical integer seed: "))

  # create a function arbitrary(x, y) that takes two inputs: lowest variable 
  # and length of the range within which our pseudo-random number will be bound
  def arbitrary(base, range) -> int:
    global seed

    # run our system time function
    seedMod = timeGet()

    # modulate the user input by the integer version of the seedMod string
    modul = seed * seedMod

    # bitshift and Xor compare the binaries for the modulated seed three times
    modul ^= modul << 13
    modul ^= modul >> 17
    modul ^= modul << 5
    seed = modul

    # output the Xorshifted seed modulated to the range [0 -> range] and then
    # shift it to the base [base -> base + range]
    return (modul % (range + 1)) + base

# cast an error if the user input is anything but an integer
except ValueError:
  print("Please try again and enter an integer.")