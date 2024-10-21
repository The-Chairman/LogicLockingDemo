import circuitgraph as cg
from logiclocking import locks, write_key
import argparse
import os
import sys
from textwrap import indent
from math import floor
import json 

PERCENT_GATES=0.60

def do_full_lock( source, banyan_width, lut_width ):
    return locks.full_lock( source, banyan_width, lut_width )

def do_full_lock_mux( source, banyan_width , lut_width ):
    return locks.full_lock_mux( source, banyan_width, lut_width )

def do_inter_lock( source, bw, reduced_swd = False ):
    return locks.inter_lock( source, bw, reduced_swb = reduced_swd )

def do_lebl_lock( source, bw, ng):
    return locks.lebl( source, bw, ng )

def do_lut_lock( source, num_gates ):
    return locks.lut_lock( source, num_gates )

def do_mux_lock( source, keylen ):
    return locks.mux_lock( source, keylen )

def do_random_lut_lock( source, num_gates, lut_width ):
    return locks.random_lut_lock( source, num_gates, lut_width )

def do_sfll_flex_lock( source, width, n ):
    return locks.sfll_flex( source, width, n )

def do_sfll_hd_lock( source, width, n ):
    return locks.sfll_hd( source, width, n )

def do_trll_lock ( source, num_keys, s1_s2_ratio=1 ):
    return locks.trll(source, num_keys, s1_s2_ratio=s1_s2_ratio )

def do_tt_lock( source, width ):
    return locks.tt_lock( source, width  )

def do_tt_lock_sen( source, width ):
    return locks.tt_lock_sen( source, width )

def do_xor_lock( source, keylen ):
    return locks.xor_lock( source, keylen )

def main():
    lock_map = {
        "full_lock": {
            "callback": do_full_lock,
            },
        "full_lock_mux": { 
            "callback": do_full_lock_mux,
            },

        "inter_lock": {
            "callback": do_inter_lock, 
        },
        # "lebl": do_lebl_lock # bugged, can't import Cadical from pysat.solvers
        "lut_lock": {
            "callback": do_lut_lock,
            },
        "mux_lock": {
            "callback": do_mux_lock,
            },
        "random_lut_lock": {
            "callback": do_random_lut_lock,
            },
        "sfll_flex": {
            "callback": do_sfll_flex_lock,
            },
        "sfll_hd": {
            "callback": do_sfll_hd_lock,
            },
        "trll": {
            "callback": do_trll_lock,
            },
        "tt_lock":  {
            "callback": do_tt_lock,
            },
        "tt_lock_sen": {
            "callback": do_tt_lock_sen,
            },
        "xor_lock": {
            "callback": do_xor_lock,
            },
    }

    all_locks = lock_map.keys()

    parser = argparse.ArgumentParser(
            prog="Verilog Locker",
            description="Locks a verilog file using an algorithm in logiclocking" )

    parser.add_argument( '-f', '--filename', dest="verilog_file", required=True )
    parser.add_argument( '-b', '--basename', dest="basename", default="",
            help="use <basename> as the base for the output filenames. If this is blank\
                    (the deafult option) try to guess the name by stripping the .v off the\
                    input verilog file" )
    parser.add_argument( '-d', '--output-directory', dest="output_directory", 
                        default=".")
    parser.add_argument( '-a', '--all', dest="do_all", default=False, action="store_true",
            help="apply all locking algorithms (default: false). Note: overides -l/--locks" )
    parser.add_argument( '-l', '--locks', metavar="LOCKS", choices=all_locks, dest="locks", nargs="+",
            help="add one (or more) of the following locking algorithms: %(choices)s" )

    lock_parameter_config = parser.add_mutually_exclusive_group()
    lock_parameter_config.add_argument( '-c', '--count-gates', dest='count_gates', action="store_true",
            default=False, help=f"Use the gate count to try and use {PERCENT_GATES} to instruct lock\
                    algorithms. Otherwise, this script uses some DUMB default values" )
    lock_parameter_config.add_argument( '-u', '--use-config-file', nargs='?',
            default="lock_config.json",
            const="lock_config.json", dest='lock_config_file', 
            help="load the various lock parameters in a json config file" )

    args = parser.parse_args()

    if not os.path.isfile( args.verilog_file ):
        print( f"Error: can't find {args.verilog_file}" )
        sys.exit(-1)

    if not ( args.do_all or args.locks ):
        print( "Error: you must specify a lock(s) or -a" )
        sys.exit(-1)

    basename = os.path.splitext( args.verilog_file )[0]

    if args.basename:
        basename = args.basename

    if args.do_all:
        args.locks = all_locks

    source_file = cg.from_file( args.verilog_file )

    # load the lock configs

    lock_config = {}

    NUM_GATES = len( source_file.filter_type( ['and', 'or', 'xor', 'nor', 'nand', 'buf'] ) ) 

    script_config = {}

    if args.count_gates:
        # This is REALLY janky !!!
        p_gates = floor( NUM_GATES * PERCENT_GATES ) 
    else:
        print( args.lock_config_file )
        if not os.path.isfile( args.lock_config_file ):
            print( f"Error: can't find the config file: {args.lock_config_file}" )
            sys.exit(-1)
        else:
            script_config = json.load( open( args.lock_config_file ) )['enabled']

    #LUT_LOCK_NUM_GATES = sub_gates
    for i in set(args.locks).intersection( script_config.keys() ): 
        output_file = f"{args.output_directory}/{basename}_{i}.v"
        key_file= f"{args.output_directory}/{basename}_{i}_key.txt"
        try:
            print( f"Num gates {NUM_GATES}" )
            print( f"Generating {i}: {output_file} {key_file} with {script_config[i]['args']} and {script_config[i]['kwargs']} ...", 
                    end="" )
            cl, k = lock_map[i]["callback"]( source_file, *script_config[i]['args'], **script_config[i]['kwargs'] )
            cg.to_file( cl, output_file)
            write_key( k, key_file )
        except ValueError as ve:
            print("Value Error!")
            raise
        except Exception as e:
            print ( "failed" )
            raise
        except:
            print("unknown error")
        else:
            print( "Done!" )

if __name__ == "__main__":
    main()
