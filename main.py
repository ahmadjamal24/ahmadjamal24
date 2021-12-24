# import required libraries
import numpy as np
import scipy.io.wavfile as wf
import sounddevice as sd
from scipy.fft import fft
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox


def plot_time(frequency, signal):
    time = np.linspace(
        0,  # start
        len(signal) / frequency,
        num=len(signal)
    )

    # using matlplotlib to plot
    # creates a new figure
    plt.figure(1)

    # title of the plot
    plt.title("Sound Wave")

    # label of x-axis
    plt.xlabel("Time")

    # actual ploting
    plt.plot(time, signal)

    # shows the plot
    # in new window
    plt.show()


def plot_spectrum(frequency, signal):
    f = np.linspace(
        0,  # start
        frequency,
        num=len(signal)
    )
    # using matlplotlib to plot
    # creates a new figure
    plt.figure(2)

    # title of the plot
    plt.title("Wave Spectrum")

    # label of x-axis
    plt.xlabel("Frequency Hz")

    # actual ploting
    plt.plot(f, signal)

    # shows the plot
    # in new window
    plt.show()


def main(sampling_freq, duration):
    def record():
        def processing():
            stop_btn.destroy()
            recording_image.destroy()
            tk.Label(panel, text="Thank You 👋", font="Helvetica 20 bold", bg="#ADEFD1", fg="#00203F", padx=10).pack(
                pady=100)

            # fourier transform of numarray (user's voice)
            f2, recording = wf.read("Recording.wav")
            recording_ft = fft(recording)
            # plot_spectrum(f2, recording_ft)
            maxi = np.amax(recording_ft)
            # To avoid repetetion of the spectrum
            half_spectrum = recording_ft[0:int(f2 / 2)]
            # The value of mean amplitude for average frequency of male and female
            print("for male", np.mean(abs(half_spectrum[85:155])), "and for female",
                  np.mean(abs(half_spectrum[165:255])))
            if np.mean(abs(half_spectrum[165:255])) < np.mean(abs(half_spectrum[85:155])) and maxi > 50:
                print("you are a man")
                tk.messagebox.showinfo('Your Gender', 'you are a man')
            elif np.mean(abs(half_spectrum[165:255])) > np.mean(abs(half_spectrum[85:155])) and maxi > 50:
                print("you are a women")
                tk.messagebox.showinfo('Your Gender', 'you are a woman')
            else:
                print("Cant recognise")
                tk.messagebox.showinfo('Your Gender', 'Cant recognise')
            panel.destroy()
            # Write the processing code here.
            main(sampling_freq, duration)

        record_btn.destroy()
        recording_image = tk.Label(panel, image=Recording_img)
        recording_image.place(relx=0.9, rely=0.1)
        stop_btn = tk.Button(panel, text="Stop", relief="raised", command=processing, image=Stop_img, cursor="hand2")
        stop_btn.place(rely=0.8, relx=0.1)

        # Start recorder with the given values
        # of duration and sample frequency
        recording = sd.rec(int(duration * sampling_freq), samplerate=sampling_freq, channels=1)
        print("Recording")
        # Record audio for the given number of seconds
        sd.wait()
        print("Recorded")
        recording_image.destroy()
        # This will convert the NumPy array to an audio
        # file with the given sampling frequency
        wf.write("Recording.wav", sampling_freq, recording)

        # plot_time(sampling_freq, recording)

    panel = tk.Frame(window, height=400, width=500, pady=20, padx=20, bd=30, bg="#ADEFD1")
    panel.place(relheight=0.8, relwidth=0.8, rely=0.1, relx=0.1)

    title = "Gender Distinguish System"
    tk.Label(panel, text=title, font="Helvetica 20 bold", bg="#ADEFD1", fg="#00203F", padx=10).pack()

    record_btn = tk.Button(panel, text="Record", relief="raised", command=record,
                           image=Record_img, cursor="hand2")
    record_btn.place(rely=0.8, relx=0.1)


# Sampling frequency (Hz)
# sampling frequecy of 16khz is enough to sample human speech
Fs = 16000
# Recording duration (s)
t = 5

# Creating a window
window = tk.Tk()
window.title("Voice Gender Distinguish System")
window.geometry('700x500')
window.configure(bg="#00203F")

# Importing animations and images
Record_img = tk.PhotoImage(
    file=r"C:\Users\Dell\Desktop\Digital signal processing\Voice Distinguish CEP\photoshot.gif")

Recording_img = tk.PhotoImage(
    file=r"C:\Users\Dell\Desktop\Digital signal processing\Voice Distinguish CEP\giphy.gif", format="gif -index 2")

Stop_img = tk.PhotoImage(
    file=r"C:\Users\Dell\Desktop\Digital signal processing\Voice Distinguish CEP\Stop.gif")

main(Fs, t)

# Footer
foot = "Designed by Ahmad Jamal &  M Abdullah(from invictus)"
footer = tk.Label(window, text=foot, font="Helvetica 10 bold", bg="#00203F", fg="#ADEFD1", padx=100)
footer.pack(side="bottom")

window.mainloop()
