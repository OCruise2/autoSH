# ORCA Job Submission Script on the Leeds HPC clusters ARC 3 and 4

## ToDO:
- Alter directory making and final copying to a folder on the /nobackup storage. Much quicker and saves on data. Users can copy over what they feel is relevant to more permanent storage solutions
- Make an argparse for deciding whether to save the .sh file or not, default to false. Currently will save .sh file to the current working directory.

## Installation
Execute the following command in the terminal once logged onto the HPC cluster.
> source <(wget -O - https://raw.githubusercontent.com/OCruise2/autoSH/main/install.sh)

## Running the Script
Navigate to the directory that contains your .inp file, then call the script and relevant filename. Multiple .inp files can be specified at once
Ex/
> orcaSH filename.inp

or

> orcaSH *.inp 

(for all .inp files in folder)

## Command Line Arguments
- <input_file.inp>: Path to input file(s) for ORCA. Multiple files can be specified
- -ca or --copy_all: (Optional) If set, copies all files in the current directory to the compute node. Default is false.
- -cs or --copy_scratch: (Optional) If set, copies all files from the scratch/temp directory back to the original directory when the calculation is finished. Default is false.
- -np or --num_processors <num>: (Optional) Overrides the number of cores specified in the input file. Defaults to 0.
- -mem or --set_memory <memory_in_GB>: (Optional) Sets the memory per core for the calculation. Default is 3 GB per core.

## Example
> orcaSH calculation.inp -ca -cs -np 4 -mem 8


Will submit a job for calculation.inp and copies all files in the current directory to the compute node. Copies all files from the scratch back into the original directory once finished. Calculation is run with 4 cores with 8 GB of memory each for a total of 64 GB.

## Potential Issues
ARC 3 and 4 currently use Python 2.7.5, if this is updated and the default file pathing changes, the script will need to be updated to include python3. 
The filepath to orca.exe has to be hardcoded, script will break if it is moved in the background.

## Potential Fixes
By loading the modules and determining where they are located. The script can easily be altered to include the correct filepaths.
For example:
> module add orca

> which orca

> /apps/applications/orca/5.0.4/1/default/bin/orca

The resulting output can be pasted into the orca_path variable (line 81 as of Oct. 14, 2024). The same thing can be done for python, execpt it occurs on line 1 of the script.
