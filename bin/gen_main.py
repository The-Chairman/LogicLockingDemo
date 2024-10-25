import argparse
import os
from xml.dom import minidom
import sys
import json
from jinja2 import FileSystemLoader, Environment
import xml.etree.ElementTree as ET

ns = {'svg': 'http://www.w3.org/2000/svg',
    'xlink': 'http://www.w3.org/1999/xlink' }

def render_svg( filename="", id=""):
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
def render_thumbnail( module_name ):
    filename = f"./{module_name}/unlocked/{module_name}_unlocked_netlist.svg"
    if not os.path.isfile( filename ):
        filename = f"./{module_name}/unlocked/{module_name}_unlocked.svg"
    
    if not os.path.isfile( filename ):
        filename = "resources/unknown.svg"

   # with open( filename,"r") as fin:
        
        #return fin.read()
    ET.register_namespace( '', 'http://www.w3.org/2000/svg')
    ET.register_namespace( 'xlink', 'http://www.w3.org/1999/xlink')
    ET.register_namespace( 's', "https://github.com/nturley/netlistsvg" ) 
    tree = ET.parse( filename )

    root = tree.getroot()
    w = root.get("width")
    h = root.get('height')
    root.set('viewbox', f"0 0 {w} {h}")
    root.set("preserveAspectRatio", "xMidYMid meet")
    del root.attrib["width"]
    del root.attrib["height"]
    #root.set('width', '100%')
    #root.set('height', '100%')
    #root.set("transform", "scale(.25)")

    #root.set("id", id)

    return ET.tostring(root, encoding='unicode')


def render_from_template( directory, template_name, **kwargs):
    loader = FileSystemLoader( directory )
    env = Environment(loader=loader)

    env.globals['render_svg'] = render_svg
    env.globals['render_thumbnail'] = render_thumbnail

    print(directory)
    print(template_name)
    template = env.get_template(template_name)
    return template.render( **kwargs )

def main():
    argparser = argparse.ArgumentParser()

    argparser.add_argument( "-f", "--file", required=True,
            help="the name of the output file to generate" )
    argparser.add_argument( "-c", "--config-file", 
            default="module_config.json", 
            help="the name of the config file to use (default: \
                    module_config.json)" )
    argparser.add_argument( "-t", "--template-dir", 
            default="./html_templates",
            help="the directory jinja2 should look for html\
                    templates in (default: ../html_templates" )

    args = argparser.parse_args()

    if not os.path.isfile( args.config_file ):
        print( f"Error: can'e find config file: {args.config_file}")
        sys.exit(-1)
    
    config = json.load( open( args.config_file, "r") )

    with open( args.file, "w") as fout:
        fout.write( render_from_template( args.template_dir, 
            "mindex_template.html",   modules=config['modules']) )

if __name__ == "__main__":
    main()
