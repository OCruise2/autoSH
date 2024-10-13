import os
import argparse

def get_args():
    '''Get the command line arguements passed to this script using argparse'''

    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", action='store',
                        help='.inp file(s) submit to the queue',
                        nargs='+')
    
    parser.add_argument("-ca", "--copy_all",
                        action='store_true',
                        default=False,
                        help='Copy all of the files in the current directory'
                        'to the compute node.')
    
    parser.add_argument('-cs', "--copy_scratch",
                        action='store_true',
                        default=False,
                        help='Copy all files from the scratch directory back'
                        'to this directory when the calculation is '
                        'finished.')
    
    parser.add_argument('-np', '--num_processors',
                        type=int,
                        default=0,
                        help="Override the number of cores specified in the "
                        "input file.")
    return parser.parse_args()

def num_cores(inp_filename, args):
    '''Gets the number of cores to request from the .inp file

    Returns:
        (int): Number of cores

    Raises:
        (ValueError, IndexError): If input file contains error
    '''
    _num_cores = 1 #Defaults to 1 if none specified

    try:
        keyword_line = next(line for line in open(inp_filename, 'r')
                            if line.startswith('!'))
        
        #Can find number of cores line by starting with PAL in initial command line
        for item in keyword_line.split():
            if item.lower().startswith('pal'):
                _num_cores = int(item[3:])

    except StopIteration:
        exit(f'{inp_filename} was not correctly formatted. Must have a line started with a !')

    #Could also use the %pal method in the input file (the correct way) - searching directly for nprocs
    for line in open(inp_filename, 'r'):

        if 'nprocs' in line:
            idx = next(i for i, item in enumerate(line.split())
                       if 'nprocs' == item.lower())
            
            _num_cores = int(line.split()[idx+1])

    #If user specifies directly in command line input - will overwrite
    if args.num_processors != 0:
        _num_cores = args.num_processors

    return _num_cores

def make_sh_file(sh_filename, inp_filename, args):
    """
    Print the submission script appropriate for an ORCA input file.
    ---------------------------------------------------------------
    Arguments:
        sh_filename (str): Submission script filename
        inp_filename (str): Input filename
        args (Namespace): Command line arguents
    """
    with open(sh_filename, 'w') as sh_file:
        print('#!/bin/bash',
              '#$ -cwd',
              f'#$ -pe smp {num_cores(inp_filename, args)}',
              '#$ -l s_rt=48:00:00',
              '#',
              'export ORIG=$PWD',
              'export SCR=$TMPDIR',
              'export NBOEXE=/usr/local/nbo7/bin/nbo7.i4.exe',
              f'module load {mpi_version}',
              f'cp {"*" if args.copy_all else inp_filename} $SCR',
              f'cd $SCR',
              f'{orca_path} {inp_filename} > {inp_filename.replace(".inp", ".out")}',
              'rm -f *.tmp',
              sep ='/n', file=sh_file)
        
        if args.copy_scratcj:
            print('cp -R * $ORIG', file=sh_file)
        else:
            print('cp *.xyz *.hess *.out $ORIG', file=sh_file)

        print('rm *.sh.*', file=sh_file)

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