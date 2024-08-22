import argparse
import os
import sys
import json
from jinja2 import FileSystemLoader, Environment

def render_from_template( directory, template_name, **kwargs):
    loader = FileSystemLoader( directory )
    env = Environment(loader=loader)
    template = env.get_template(template_name)
    return template.render( **kwargs )

def main():
    argparser = argparse.ArgumentParser()

    argparser.add_argument( "-b", "--basename", required=True,
            help="the root name for this set of circuits" )
    argparser.add_argument( "-f", "--file", required=True,
            help="the name of the output file to generate" )
    argparser.add_argument( "-c", "--config-file", 
            default="lock_config.json", 
            help="the name of the config file to use (default: \
                    lock_config.json)" )
    argparser.add_argument( "-t", "--template-dir", 
            default="../html_templates",
            help="the directory jinja2 should look for html\
                    templates in (default: ../html_templates" )

    args = argparser.parse_args()

    if not os.path.isfile( args.config_file ):
        print( f"Error: can'e find config file: {args.config_file}")
        sys.exit(-1)
    
    config = json.load( open( args.config_file, "r") )

    locks = {}

    for i in config['enabled'].keys():
        t = f"{args.basename}_{i}_locked.svg"
        locks[i] = {
                'filename':t,
                'args': config['enabled'][i]['args']
                }

    with open( args.file, "w") as fout:
        fout.write( render_from_template( args.template_dir, 
            "cindex_template.html", basename=args.basename, 
            locks=locks) )



if __name__ == "__main__":
    main()
