import os
import argparse

def get_args():
    '''Get the command line arguments passed to this script using argparse. 
    Nothing aside from the .inp filenames is critical'''

    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", action='store',
                        help='.inp file(s) submit to the queue',
                        nargs='+')
    
    parser.add_argument("-ca", "--copy_all",
                        action='store_true',
                        default=False,
                        help='Copy all of the files in the current directory'
                        'to the compute node. Default is false.')

    parser.add_argument('-cs', "--copy_scratch",
                        action='store_true',
                        default=False,
                        help='Copy all files from the scratch directory back'
                        'to this directory when the calculation is '
                        'finished. Default is false.')
    
    parser.add_argument('-np', '--num_processors',
                        type=int,
                        default=0,
                        help="Override the number of cores specified in the "
                        "input file. Defaults to zero, ")
    
    parser.add_argument('-mem', '--set_memory',
                        type=int,
                        default=3,
                        help='Sets the memory per core of the calculation. Defaults to 3Gb per core')
    return parser.parse_args()

def num_cores(inp_filename, args):
    '''Gets the number of cores to request from the .inp file

    Returns:
        (int): Number of cores

    Raises:
        ValueError: If the input file contains an error or is not correctly formatted.
    '''
    _num_cores = 1  # Defaults to 1 if none specified

    try:
        with open(inp_filename, 'r') as inp_file:
            for line in inp_file:
                # Check for '!' line for PAL
                if line.startswith('!'):
                    for item in line.split():
                        if item.lower().startswith('pal'):
                            _num_cores = int(item[3:])
                            break
                
                # Check for '%pal' method for nprocs
                if 'nprocs' in line.lower():
                    parts = line.split()
                    if 'nprocs' in parts:
                        idx = parts.index('nprocs')
                        if idx + 1 < len(parts):
                            _num_cores = int(parts[idx + 1])
                        else:
                            raise ValueError(f"Invalid format for 'nprocs' in {inp_filename}")

    except FileNotFoundError:
        raise ValueError(f"Input file {inp_filename} not found.")
    except ValueError as ve:
        raise ValueError(f"Error parsing {inp_filename}: {ve}")
    
    # Override with command-line argument if provided
    if args.num_processors != 0:
        _num_cores = args.num_processors

    return _num_cores

def make_sh_file(sh_filename, inp_filename, args):
    """
    Print the submission script appropriate for an ORCA input file.
    Currently uses ORCA v5.0.4 and OpenMPI v3.1.4
    ---------------------------------------------------------------
    Arguments:
        sh_filename (str): Submission script filename
        inp_filename (str): Input filename
        args (Namespace): Command line arguents
    """
    orca_path = '/apps/applications/orca/5.0.4/1/default/bin/orca'

    with open(sh_filename, 'w') as sh_file:
        # #$/bin/bash specifies to run the .sh in bash instead of sh or zsh etc
        # Submits for max 48 h runtime
        sh_file.write(f"""#$/bin/bash
#$ -V -cwd
#$ -l h_rt=48:00:00
#$ -pe smp {num_cores(inp_filename, args)}
#$ -l h_vmem={args.set_memory}G
#$ -m be

module load openmpi/3.1.4
export ORIG=$PWD
export SCR=$TMPDIR #Provided by the system but not /scratch or /tmp. Assigned on a per job basis
""")

        #Copy files to the scratch
        copy_files = '*' if args.copy_all else inp_filename
        sh_file.write(f'cp {copy_files} $SCR\n')
        sh_file.write("cd $SCR\n")

        #ORCA command itself
        output_filename = inp_filename.replace(".inp", ",out")
        sh_file.write(f"{orca_path} {inp_filename} > {output_filename}\n")

        #Cleaning up temp files - ORCA does this automatically, but if the calculation fails, 
        # they will not be removed by default
        sh_file.write("rm -f *.tmp\n")

        #Copying results back to working directory. 
        if args.copy_scratch:
            sh_file.write("cp -R * $ORIG\n")
        else:
            sh_file.write("cp *.xyz *.hess *.out $ORIG\n")

        #Removes shell output (comment out line for testing)
        #sh_file.write("rm *.sh.*\n")
    return None

if __name__ == '__main__':
    arguments=get_args()

    for filename in arguments.filenames:
        if not filename.endswith('.inp'):
            exit(f"Filename must end with .inp. Found: {filename}")

        script_filename = filename.replace('.inp', '.sh')

        #Cannot start script names with a digit - will add '_' in front
        if script_filename[0].isdigit():
            script_filename = f'_{script_filename}'

        make_sh_file(script_filename,
                     inp_filename=filename,
                     args=arguments)
        
        os.system(f'qsub {script_filename}')