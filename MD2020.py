"""
    This script run other groups script.

    :author: LSS
    :date: 31/06/2019
    :version: 1.0.0
"""

import csv
import os
import subprocess
import sys

# ==================================================================== #

# The report number beeing processed
report_number = 3.1

# The maximum time a group can take to run their script, in seconds
# -1 => infini
max_compute_time = -1

# The argument used to launch other processus
argument = "reel"

# -1 => pas de limite
nlimit = -1

ext = ""

# The python executable name it must python or python3
python_exec = "python"

# ==================================================================== #

for arg in sys.argv:
    # Remove the "-" to just keep what is behind
    if arg in ("-a", "--all"):
        argument = "exhaustif"
    elif arg in ("-r", "--real"):
        argument = "reel"
    elif arg.find("--ext=") != -1:
        ext = arg[6:]
    elif arg[0] == "-" and arg[1] == "n":
        nlimit = int(arg[2:])
    elif arg.find("--number=") != -1:
        nlimit = int(arg[9:])
    elif arg[0] == "-" and arg[1] == "t":
        max_compute_time = int(arg[2:])
    elif arg.find("--time=") != -1:
        max_compute_time = int(arg[7:])

print("argument:", argument)
print("ext:", ext)
print("n limit:", nlimit)
print("max compute time:", max_compute_time)

# Construct the path to the project folder
project_folder = "PROJET_PIFE_" + str(report_number)

# Construct the data folder
# data_folder = project_folder + "/DONNEES"
data_folder = os.path.join(project_folder, "DONNEES")

# Check that the folder exists
if not os.path.isdir(data_folder):
    raise FileNotFoundError("Data folder not found in: " + data_folder)

# Construct the resultat folder
resultat_folder = project_folder + "/RESULTATS"

# Construct the resultat path
resultat_path = resultat_folder + "/resultat" + ext + ".csv"

# Check that the folder exists
if not os.path.isdir(resultat_folder):
    raise FileNotFoundError("Resultat folder not found in: " + resultat_folder)

# Construct the path to the preference file
preference_path = data_folder + "/preferences" + ext + ".csv"

# Construct the path to the group file
group_path = resultat_folder + "/groupes" + ext + ".csv"

# Group assignment for all groups
result = {}

# List all the folder in the project folder
directory_list = os.listdir(project_folder)
directory_list.remove("DONNEES")
directory_list.remove("RESULTATS")
directory_list.remove("TESTS")

_stdout = sys.stdout
_stderr = sys.stderr


def enable_print():
    """Enable the print to stdout et stderr"""
    sys.stdout = _stdout
    sys.stderr = _stderr


def disable_print():
    """Disable the print to stdout et stderr"""
    sys.stdout = os.devnull
    sys.stderr = os.devnull


# For each group run this script
for group_acronym in directory_list:
    enable_print()
    print(group_acronym + " - DEBUT")
    disable_print()

    group_folder = project_folder + "/" + group_acronym
    prog_path = group_folder + "/" + group_acronym + ".py"

    if not os.path.exists(prog_path):
        enable_print()
        print("Can't load the script at: " + prog_path)
        print(group_acronym + " - ECHEC")
        continue

    # Run the group' script
    strlimit = ""
    if nlimit == -1:
        strlimit = ""
    else:
        strlimit = "--number=" + str(nlimit)

    args = [python_exec, group_acronym + ".py", "--arg=" + argument, strlimit, "--ext=" + ext]
    try:
        process = subprocess.Popen(args, stderr=subprocess.PIPE, cwd=group_folder)
    except IOError:
        _, value, traceback = sys.exc_info()
        enable_print()
        print("NOT A GROUP ERROR !")
        print(
            "ERROR: Change the 'python_exec' variable (inside the script MD2020)",
            " to either 'python' or 'python3' to make this script work")
        print("NOT A GROUP ERROR !")
        sys.exit(1)

    stderr = None

    # Try to get errors back from the script with a timeout
    try:
        if max_compute_time == -1:
            stdout, stderr = process.communicate()
        else:
            stdout, stderr = process.communicate(timeout=max_compute_time * 1.1)
    except subprocess.TimeoutExpired:
        # In the case where the script was too long,
        # just kill it and process the next group
        enable_print()
        process.kill()
        print("Script was too long")
        print(group_acronym + " - ECHEC")
        continue
    except:
        enable_print()
        process.kill()
        print("Script crashed")
        print(group_acronym + " - ECHEC")
        continue

    # If stderr is not None then an error occured in
    # print the error and pass to the next script
    if stderr is not None and len(stderr) > 0:
        enable_print()
        print(stderr.decode("utf-8"))
        print(group_acronym + " - ECHEC")
        continue

    try:
        process.kill()
    except:
        pass

    # Create the group acronym result set
    result[group_acronym] = []

    # Read the csv and save data for later
    group_csv_path = project_folder + "/" + group_acronym + "/" + group_acronym + ".csv"
    try:
        with open(group_csv_path, newline='') as group_file:
            result_reader = csv.reader(group_file, delimiter=';', quotechar='"',
                                       quoting=csv.QUOTE_MINIMAL)

            for row in result_reader:
                result[group_acronym].append(row)

            group_file.close()

            enable_print()
            print("\nGROUP " + group_acronym + " - OK")
    except IOError:
        _, value, traceback = sys.exc_info()
        enable_print()
        print('Error opening the csv file %s: %s' % (value.filename, value.strerror))
        print(group_acronym + " - ECHEC")
        continue

# Write in the CSV the result
with open(resultat_path, mode="w+", newline="") as result_file:
    result_writer = csv.writer(result_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    for group_acronym in result:
        assignments = result[group_acronym]
        for assignment in assignments:
            # Add the group acronym
            assignment = [group_acronym] + assignment
            result_writer.writerow(assignment)

        result_writer.writerow("")

    result_file.close()
