import matplotlib.pyplot as plt
import numpy as np
import json , os
import math
import pdb; pdb.set_trace()

def smooth_outliers(param, threshold=1000):
    """
    Smooth out the outliers in the 'param' array by replacing them with the 
    average of their valid neighbors (ignoring other outliers).
    
    Parameters:
    param (list or np.array): The parameter list/array to be smoothed.
    threshold (float): The threshold value to consider as an outlier (default is 1e12).
    
    Returns:
    np.array: The smoothed parameter array.
    """
    param = np.array(param)  # Convert param to a numpy array for easier processing
    for i in range(1, len(param) - 1):  # Avoid out-of-range errors
        if param[i] > threshold:  # Check if the value is an outlier
            # Collect valid neighbors (those that are not outliers)
            valid_neighbors = []
            if param[i-1] <= threshold:  # Check previous value
                valid_neighbors.append(param[i-1])
            if param[i+1] <= threshold:  # Check next value
                valid_neighbors.append(param[i+1])
            
            # If valid neighbors exist, replace outlier with the average of valid neighbors
            if valid_neighbors:
                param[i] = np.mean(valid_neighbors)
    return param

def get_last_beginning_times(folder, file_prefix="chap-", file_suffix=".json", num_files=100):
    """
    Get the last 100 beginning times based on the files in the folder.
    
    Parameters:
    folder (str): Path to the directory containing the files.
    file_prefix (str): Prefix of the file names to filter.
    file_suffix (str): Suffix of the file names to filter.
    num_files (int): Number of last files to extract.
    
    Returns:
    list: Sorted list of the last 100 beginning times.
    """
    # Get list of files matching the pattern
    files = [f for f in os.listdir(folder) if f.startswith(file_prefix) and f.endswith(file_suffix)]
    # Extract beginning times from the file names
    beginning_times = []
    for file in files:
        try:
            # Extract the beginning time from the file name
            parts = file[len(file_prefix):-len(file_suffix)].split('-')
            beginning_time = int(parts[0])
            beginning_times.append(beginning_time)
        except (ValueError, IndexError):
            continue  # Skip files that do not match the expected format

    # Get the last `num_files` beginning times, sorted in ascending order
    return sorted(beginning_times)[-num_files:]

def json_read(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)
    return data

def mean_value(data, mean_step):
    mean_data = []
    for i in range(1, int((len(data)-1)/mean_step)+1):
        mean_data.append(np.mean(data[(i-1)*mean_step:i*mean_step]))
    return mean_data

source_dir = '/run/media/maryamma/One Touch/project_md/project_2/analysis241205/'

parameters = {'energyMean': -1000, 'densityMean':0, 'radiusMean':-10}
key_sum = 'pathwayProfile'

dirs = ["eq", "deform/10-4", "deform/10-4/eq/0.20", "deform/10-4/eq/0.35m", "deform/10-4/eq/0.45m", "deform/press75"]

cmap = plt.get_cmap('Set1')
colors = cmap(np.linspace(0, 1, len(dirs)))

mean_step = 1
num_timewindow = 100
threshold = 100
for parameter, min_val in parameters.items():
    dir_beginning_times = {}
    # Grid subplot setup
    # Aggregate data for average and SD calculation
    dir_avg_sd = {dir: {"means": [], "sds": [], "time": []} for dir in dirs}

    for dir in dirs:
        folder_path = os.path.join(source_dir, dir)
        try:
            # Get last 100 beginning times for this directory
            dir_beginning_times[dir] = get_last_beginning_times(folder_path, num_files=num_timewindow)
        except FileNotFoundError:
            print(f"Directory not found: {folder_path}")
            dir_beginning_times[dir] = []
    # Grid subplot setup
    num_plots = num_timewindow
    cols = math.ceil(math.sqrt(num_plots))
    rows = math.ceil(num_plots / cols)
    fig, axes = plt.subplots(rows, cols, figsize=(15, 10), sharex=True, sharey=True)
    fig.suptitle(f"Parameter: {parameter}", fontsize=16)
    axes = axes.flatten()

    for dir, begining_times in dir_beginning_times.items():
        # print(dir, begining_times[0], begining_times[-1])
        for idx, begining_time in enumerate(begining_times):
            file = os.path.join(source_dir, dir, f'chap-{begining_time}-{begining_time+1000}.json')
            try:
                # Read file and process as before
                file_chap = json_read(file)
                time = file_chap[key_sum]['s']
                res = file_chap['residueSummary']['id']
                param = file_chap[key_sum][parameter]
                # Handle invalid data
                param = [min_val if (x < min_val) else x for x in param]
                param = smooth_outliers(param, threshold)

                # Calculate mean values
                mean_time_eq = mean_value(np.array(time), mean_step)
                mean_param_eq = mean_value(np.array(param), mean_step)

                # Store for average and SD calculation
                dir_avg_sd[dir]["means"].append(mean_param_eq)
                dir_avg_sd[dir]["sds"].append(np.std(param))
                dir_avg_sd[dir]["time"] = mean_time_eq

                # Plot if part of the grid
                ax = axes[idx]
                ax.plot(time, param)
                col_labels = f"{idx*1000} to {(idx+1)*1000} ps"
                ax.set_title(col_labels, fontsize=10)
            except FileNotFoundError:
                print(f"File not found: {file}")
            except KeyError as e:
                print(f"Missing key in file {file}: {e}")

    # Hide unused subplots
    for ax in axes[num_plots:]:
        ax.axis('off')
    # plt.subplots_adjust(left=0.5)  # Increase space on the left side (default is usually 0.125)
    plt.tight_layout(rect=[0, 0.1, 1, 0.96])
    fig.text(0.52, 0.1, 'pore axis (nm)', ha='center', fontsize=14)
    # fig.text(0.0, 0.5, f'{parameter[:-4]}', va='center', rotation='vertical', fontsize=14)
    fig.legend(dirs, loc='upper right', ncol=3, fontsize=12)    
    fig.suptitle(f"{parameter[:-4]}", fontsize=16)
    if parameter == 'energyMean':
        plt.ylim(-10, 10)     
    plt.savefig(f'chap_fig/{parameter[:-4]}_time_windows_{threshold}.png')

    # plt.show()

    # Plot average and SD
    fig, ax = plt.subplots(figsize=(10, 6))

    for num, dir in enumerate(dirs[1:]):
        fig, ax = plt.subplots(figsize=(10, 6))
        avg = np.mean(dir_avg_sd[dirs[0]]["means"], axis=0)
        sd = np.std(dir_avg_sd[dirs[0]]["means"], axis=0)
        ax.plot(dir_avg_sd[dirs[0]]["time"], avg, label=f"{dirs[0]}", color=colors[0])
        ax.fill_between(dir_avg_sd[dirs[0]]["time"], avg - sd, avg + sd, color=colors[0], alpha=0.3)
        avg = np.mean(dir_avg_sd[dir]["means"], axis=0)
        sd = np.std(dir_avg_sd[dir]["means"], axis=0)
        ax.plot(dir_avg_sd[dir]["time"], avg, label=f"{dir}", color=colors[num+1])
        ax.fill_between(dir_avg_sd[dir]["time"], avg - sd, avg + sd, color=colors[num+1], alpha=0.3)

        ax.set_title(f"Average and SD for {parameter[:-4]}")
        ax.set_xlabel("pore axis (nm)")
        ax.set_ylabel(f"{parameter[:-4]}")
        ax.legend()
        plt.tight_layout()
        plt.savefig(f'chap_fig/{parameter[:-4]}_{os.path.basename(dir)}_compare_with_eq_{threshold}.png')
        # plt.show()
