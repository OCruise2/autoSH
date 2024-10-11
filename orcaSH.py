import os
import argparse

def get_args():
    return

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

def make_sh_file():
    return

