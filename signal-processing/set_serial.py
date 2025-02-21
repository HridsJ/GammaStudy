import numpy as np
import serial
import matplotlib.pyplot as plt
import time
import pandas as pd
import json

# Configure the serial port
ser = serial.Serial()
ser.port = '/dev/tty.usbmodem21301'  # Replace with your Arduino's port
ser.baudrate = 9600

# Number of data points for the FFT
datapoints = 100
sampling = 0.00390625  # seconds

# Open the serial port
ser.open()
datastream = []
datastream_new = []    # To store the next 300 readings after ignoring the first 300
ignored_readings = 0   # Counter for the ignored readings

# Function to normalize data using Min-Max normalization


# Transform and plot the data
def transform(datastream):
    print('Started the transform')
    datastream = datastream - np.mean(datastream) 
    # Perform FFT
    afterfft = np.fft.fft(datastream)

    # Calculate frequency bins
    freq = np.fft.fftfreq(len(datastream), d=sampling)

    # Take positive frequencies and magnitudes
    positive_frequencies = freq[:len(datastream)//2]
    positive_magnitudes = np.abs(afterfft[:len(datastream)//2])

    mask = (positive_frequencies >= 30) & (positive_frequencies <= 60)
    filtered_frequencies = positive_frequencies[mask]
    filtered_magnitudes = positive_magnitudes[mask]
    plt.plot(filtered_frequencies, filtered_magnitudes)

    history = pd.Series(filtered_frequencies)
    history = stat(history)

    
    # Create a NumPy array with numeric data

    # Convert the NumPy array to a Python list

    # Define the path to the JSON file
    json_file_path = 'data.json'

    # Write the Python list to a JSON file
    with open(json_file_path, 'w') as json_file:
        json.dump(history, json_file)

    plt.show()  # Plot up to 50 Hz
    

    # Plot the FFT
    plt.figure(figsize=(10, 6))
    plt.plot(positive_frequencies, positive_magnitudes)  # Plot up to 50 Hz
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude")
    # plt.title(f"Normalized Frequency Spectrum (Min-Max) - Dominant: {dominant_wave}")
    plt.show()
    # plt.draw()
    # plt.pause(0.5)
    # plt.close()
     
def stat(hist):
    percentile_15 = hist.quantile(0.15)
    percentile_85 = hist.quantile(0.85)
    arr_res=[]
    arr_res.append(percentile_15)
    arr_res.append(percentile_85)
    return arr_res

try:
    while True:
        if ser.in_waiting > 0:
            try:
                # Read and decode the line from the serial port
                line = ser.readline().decode('utf-8').strip()
                time.sleep(sampling)
            except UnicodeDecodeError:
                continue  # Skip any decoding errors

            # Convert the line to an integer value
            value = int(line)
            datastream.append(value)
            print(len(datastream))
            print(value)
            # datastream_new.append(value)

            # print(f"Datastream Length: {len(datastream)}, Current Value: {value}")

            # Only process data in batches for FFT if datastream reaches 'datapoints' size
            if len(datastream) >= datapoints:
                transform(datastream)
                datastream = []  # Clear the datastream for the next batch


except KeyboardInterrupt:
    print("Program interrupted by user.")
finally:
    ser.close()
