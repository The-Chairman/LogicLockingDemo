import argparse
import glob
import os
import re
import sys
import json
import pandas as pd 

def main():
    argparser = argparse.ArgumentParser()

    argparser.add_argument( "-d", "--directory", required=True,
            help="the directory containing a module instance" )
    argparser.add_argument( "-o", "--output-file", default="output.xlsx",
            help="the excel sheet to write to" )
    
    args = argparser.parse_args()

    config_file = os.path.join(args.directory, "lock_config.json")

    if not os.path.isfile( config_file ):
        print( f"Can't find config file {config_file}" )
        sys.exit(-1)

    config = json.load(open(config_file, "r"))

    full_data_set = pd.DataFrame()

    all_locks =  [ 'unlocked'] + ( sorted( config['enabled'].keys() | config['disabled'].keys() ) ) 

    for l in all_locks:
        stat_files = glob.glob( f"{args.directory}/{l}/*stats.json" )

        if stat_files and os.path.isfile( stat_files[0] ):
            data = pd.read_json( stat_files[0] )
            print( f"{stat_files[0]}")
            nr = {
                'circuit name': [args.directory],
                'lock name': [l],
                'num_cells': data['design']['num_cells'],
                'num_wires': data['design']['num_wires'],
            }
            full_data_set = pd.concat([full_data_set,pd.DataFrame(nr)] )


    if os.path.isfile( args.output_file ):
        with pd.ExcelWriter( args.output_file, mode='a', if_sheet_exists="replace" ) as writer:
            full_data_set.to_excel( writer, sheet_name=args.directory)
    else:
        with pd.ExcelWriter( args.output_file, mode='w') as writer:
            full_data_set.to_excel( writer, sheet_name=args.directory)

if __name__ == "__main__":
    main()