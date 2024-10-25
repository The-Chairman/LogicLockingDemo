import argparse
import os
from xml.dom import minidom
import sys
import json
from jinja2 import FileSystemLoader, Environment
import xml.etree.ElementTree as ET

ns = {'svg': 'http://www.w3.org/2000/svg',
    'xlink': 'http://www.w3.org/1999/xlink' }

def render_svg( filename_base="", id=""):
    filename = f"{filename_base}_netlist.svg"
    if not os.path.isfile( filename ):
        filename = f"{filename_base}.svg"
    
    if not os.path.isfile( filename ):
        filename = "../resources/unknown.svg"
        
    if(os.path.isfile(filename) ):
        with open( filename,"r") as fin:
            return fin.read()
        # tree = ET.parse( filename )
        # ET.register_namespace( '', 'http://www.w3.org/2000/svg')
        # ET.register_namespace( 'xlink', 'http://www.w3.org/1999/xlink')
        # ET.register_namespace( 's', "https://github.com/nturley/netlistsvg" ) 
        # root = tree.getroot()
        # root.set("id", id)

        # return minidom.parseString(ET.tostring(root, encoding="UTF-8")).toprettyxml(indent='\n')
    else:
        return "file not found"


def render_from_template( directory, template_name, **kwargs):
    loader = FileSystemLoader( directory )
    env = Environment(loader=loader)

    def render_stats(stat_file):
        if os.path.isfile(stat_file):
            return env.get_template("stats.jinja2").render( stats=json.load( open( stat_file, "r")))
        else:
            return env.get_template("stats.jinja2").render( stats={"modules": {"design": { "foo": "bar"} }})

    env.globals['render_svg'] = render_svg
    env.globals['render_stats'] = render_stats

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
        t = f"{args.basename}_{i}.svg"
        locks[i] = {
                'filename':f"{i}/{t}",
                'filename_base': f"{i}/{args.basename}_{i}",
                'args': config['enabled'][i]['args']
                }

    with open( args.file, "w") as fout:
        fout.write( render_from_template( args.template_dir, 
            "cindex_template.html", basename=args.basename, 
            locks=locks) )

if __name__ == "__main__":
    main()
