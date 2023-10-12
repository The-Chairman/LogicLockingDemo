import circuitgraph as cg
from logiclocking import locks, write_key
import argparse
import os
import sys
from textwrap import indent

BANYAN_WIDTH = 8
LUT_WIDTH = 2
NUM_KEYS = 32

BW = 2
NG = 2

LUT_NUM_GATES = 8

MUX_KEY_LEN = 10

RANDOM_LUT_NUM_GATES = 8

SFLL_FLEX_WIDTH = 8
SFLL_FLEX_N = 4


SFLL_HD_WIDTH = 8
SFLL_HD_N = 4

TT_WIDTH = 8

TT_LOCK_SEN_WIDTH = 8

XOR_KEYLENGTH = 10

def do_full_lock( source, banyan_width = BANYAN_WIDTH, lut_width = LUT_WIDTH ):
    return locks.full_lock( source, banyan_width, lut_width )

def do_full_lock_mux( source, banyan_width = BANYAN_WIDTH,
        lut_width = LUT_WIDTH ):
    return locks.full_lock_mux( source, banyan_width, lut_width )

def do_inter_lock( source, bw = BW, reduced_swd = False ):
    return locks.inter_lock( source, bw, reduced_swb = reduced_swd )

def do_lebl_lock( source, bw=BANYAN_WIDTH, ng=NG ):
    return locks.lebl( source, bw, ng )

def do_lut_lock( source, num_gates = LUT_NUM_GATES ):
    return locks.lut_lock( source, num_gates )

def do_mux_lock( source, keylen = MUX_KEY_LEN ):
    return locks.mux_lock( source, keylen )

def do_random_lut_lock( source, num_gates = RANDOM_LUT_NUM_GATES, 
        lut_width = LUT_WIDTH ):
    return locks.random_lut_lock( source, num_gates, lut_width )

def do_sfll_flex_lock( source, width = SFLL_FLEX_WIDTH, 
        n = SFLL_FLEX_N ):
    return locks.sfll_flex( source, width, n )

def do_sfll_hd_lock( source, width = SFLL_HD_WIDTH, n = SFLL_HD_N ):
    return locks.sfll_hd( source, width, n )

def do_trll_lock ( source, num_keys = NUM_KEYS ):
    return locks.trll(source, num_keys)

def do_tt_lock( source, width = TT_WIDTH ):
    return locks.tt_lock( source, width  )

def do_tt_lock_sen( source, width = TT_LOCK_SEN_WIDTH ):
    return locks.tt_lock_sen( source, width )

def do_xor_lock( source, keylen = XOR_KEYLENGTH ):
    return locks.xor_lock( source, keylen )

def main():
    lock_map = {
        "full_lock": do_full_lock,
        "full_lock_mux": do_full_lock_mux,
        #"inter_lock": do_inter_lock, 
        # "lebl": do_lebl_lock # bugged, can't import Cadical from pysat.solvers
        "lut_lock": do_lut_lock,
        "mux_luck": do_mux_lock,
        "random_lut_lock": do_random_lut_lock,
        "sfll_flex": do_sfll_flex_lock,
        "sfll_hd": do_sfll_hd_lock,
        "trll": do_trll_lock,
        "tt_lock": do_tt_lock,
        "tt_lock_sen": do_tt_lock_sen,
        "xor_lock": do_xor_lock,

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
    parser.add_argument( '-a', '--all', dest="do_all", default=False, action="store_true",
            help="apply all locking algorithms (default: false). Note: overides -l/--locks" )
    parser.add_argument( '-l', '--locks', metavar="LOCKS", choices=all_locks, dest="locks", nargs="+",
            help="add one (or more) of the following locking algorithms: %(choices)s" )

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
    for i in args.locks:

        output_file = f"{basename}_{i}_locked.v"
        key_file= f"{basename}_{i}_locked_key.txt"
        print( f"Generating {i}: {output_file} {key_file}" )
        cl, k = lock_map[i]( source_file )
        cg.to_file( cl, output_file)
        write_key( k, key_file )

if __name__ == "__main__":
    main()
