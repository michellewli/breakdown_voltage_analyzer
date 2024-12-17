import statistics
import os


def get_file_info(filename):
    try:
        file = open(filename, 'r')
    except FileNotFoundError:
        return "file not found"

    voltage_info = []
    time_info = []
    for line in file:
        line = line.strip().split(",")
        while len(line) != 2 and line:
            line.pop()
        if line:
            time = line[0]
            voltage = line[1]

            try:
                voltage = float(voltage)
            except ValueError:
                voltage = False

            if voltage:
                voltage_info.append(voltage)
                time_info.append(time)

    info = [voltage_info, time_info]
    file.close()

    return info


def get_time(filename):
    info = get_file_info(filename)
    time_list = info[1]

    return time_list


def get_voltage(filename):
    info = get_file_info(filename)
    voltage_list = info[0]

    return voltage_list


def is_actually_increasing(previous_value, current_value):
    first_check = current_value >= previous_value
    second_check = current_value <= (0.8 * previous_value)

    return first_check or not second_check


def get_peak_info(filename):
    voltage_list = get_voltage(filename)
    time_list = get_time(filename)
    previous_value = 0.0
    i = 0
    peak_values = []
    peak_times = []

    while i < len(voltage_list):
        current_value = float(voltage_list[i])
        if is_actually_increasing(previous_value, current_value):
            previous_value = voltage_list[i]
            i += 1
        else:
            peak_values.append(previous_value)
            peak_times.append(time_list[i - 1])
            i += 1
            previous_value = 0

    return [peak_values, peak_times]


def get_peak_values(filename):
    peak_info = get_peak_info(filename)
    peak_values = peak_info[0]

    return peak_values


def get_peak_times(filename):
    peak_info = get_peak_info(filename)
    peak_times = peak_info[1]

    return peak_times


def get_average_peaks(filename):
    peaks = get_peak_values(filename)

    if peaks:
        average_peaks = statistics.mean(peaks)
    else:
        average_peaks = ""

    return average_peaks


def get_stdev_peaks(filename):
    peaks = get_peak_values(filename)
    if peaks:
        stdev_peaks = statistics.stdev(peaks)
    else:
        stdev_peaks = ""

    return stdev_peaks


def get_period(filename):
    peak_times = get_peak_times(filename)
    num_peaks = len(peak_times) - 1
    last_index = len(peak_times) - 1
    first_index = 0

    last_time = float((peak_times[last_index])) * 0.001
    first_time = float((peak_times[first_index])) * 0.001

    period = (last_time - first_time) / num_peaks

    return period

'''
def get_frequency(filename):
    period = get_period(filename)
    frequency = 1 / period

    return frequency
'''

def get_frequency(filename):
    voltage_list = get_voltage(filename)
    times_list = get_time(filename)
    peaks = get_peak_values(filename)
    peak_1 = peaks[0]
    peak_2 = peaks[len(peaks)-1]
    first_i = voltage_list.index((peak_1))
    rev_y = voltage_list[::-1]
    second_i = rev_y.index((peak_2))
    rev_time = times_list[::-1]
    time_1 = float(times_list[first_i])*(0.001)#millisecond to second
    time_2 = float(rev_time[second_i])*(0.001)
    freq = (len(peaks)-1)/(time_2-time_1)
    return freq


def get_new_data(files, new_file):
    print(f"files {files}")
    new_file = open(new_file, "w")
    print("file, mean, stdev, num peaks, frequency", file=new_file)

    for file in files:
        peaks = get_peak_values(file)
        mean = get_average_peaks(file)
        stdev = get_stdev_peaks(file)
        frequency = get_frequency(file)
        print(f"{file}, {mean}, {stdev}, {len(peaks)}, {frequency}", file=new_file)


def get_new_datum(file, new_file):
    new_file = open(new_file, "w")
    print("file, mean, stdev, num peaks, frequency", file=new_file)

    peaks = get_peak_values(file)
    mean = get_average_peaks(file)
    stdev = get_stdev_peaks(file)
    frequency = get_frequency(file)
    print(f"{file}, {mean}, {stdev}, {len(peaks)}, {frequency}", file=new_file)


def main():
    type = input("Specify whether you are entering a folder directory (a) or filename (b) or quit (q):")
    while type != "q" and type != "Q":
        if type == "a" or type == "A":
            directory = input("Enter the directory to the folder that contains the files:")
            try:
                files = os.listdir(directory)
            except OSError:
                directory = input("Enter the directory to the folder that contains the files:")
                files = os.listdir(directory)
            filename = input("Enter a title for you new data file:")
            if ".csv" not in filename:
                filename = filename + ".csv"

            multiple_data = get_new_data(files, filename)
            type = input("Specify whether you are entering a folder directory (a) or filename (b) or quit (q):")
        elif type == "b" or type == "B":
            file = input("Enter the filename:")
            try:
                open_file = open(file, 'r')
            except FileNotFoundError:
                file = input("Enter the filename:")
            filename = input("Enter a title for you new data file:")
            single_data = get_new_datum(file, filename)
            type = input("Specify whether you are entering a folder directory (a) or filename (b) or quit (q):")
        else:
            type = input("Specify whether you are entering a folder directory (a) or filename (b) or quit (q):")


main()

