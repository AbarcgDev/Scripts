#!/bin/python3

import os
import argparse
from pathlib import Path
import shutil



parser = argparse.ArgumentParser(description="Creates latex project")
parser.add_argument(
    '--name',
    type=str,
    nargs='?',
    default="Mi titulo",
    help="The name of the document"
)
parser.add_argument(
    '--grupo',
    type=str,
    nargs='?',
    default="Mi Grupo",
    help="The group displayed at the titlepage"
)
parser.add_argument(
    '--asignatura',
    type=str,
    nargs='?',
    default="Mi asignatura",
    help="The subject displayed at titlepage"
)
parser.add_argument(
    "--docente",
    type=str,
    nargs='?',
    default="Mi Docente",
    help="The teacher displayed at titlepage"

)
parser.add_argument(
    '--fechaEntrega',
    type=str,
    nargs='?',
    default="01/01/2000",
    help="The due date displayed at titlepage"
)
args=parser.parse_args()


def main(args: argparse.Namespace):
    document_name = args.name
    document_dir = create_project_tree(document_name)
    create_template_files(document_dir)
    create_make_file(document_name, document_dir)
   

def create_project_tree(document_name: str) -> Path:
    current_dir = os.getcwd()
    print("---> Creating project tree ...")
    Path(document_name).mkdir(exist_ok=True)
    document_dir = Path(document_name)
    os.chdir(document_dir)
    Path('figs').mkdir(exist_ok=True)
    os.chdir(current_dir)
    print("     DONE")    
    return document_dir


def create_template_files(document_dir: Path):
    print("---> Creating templates")
    portada = Path('/home/abargdev/Templates/portada/')
    preamble = Path('/home/abargdev/Templates/preamble.tex')
    main = Path(f"./{document_dir.name}/{document_dir.name}.tex") 
    shutil.copytree(portada, f"./{document_dir.name}/portada")
    shutil.copy(preamble, document_dir,)
    write_main(main, document_dir, document_dir.name)
    print("     Done")


def write_main(main: Path, document_dir: Path, name: str):
    main.touch()
    open_main = main.open("a+")
    open_main.write(f"""%Main texfile

\\input{{preamble.tex}}

\\title{{{name}}}
\\author{{Abarca Godoy Alvaro}}
\\def\\grupo{{{args.grupo}}}
\\def\\asignatura{{{args.asignatura}}}
\\def\\docente{{{args.docente}}}
\\def\\fechaEntrega{{{args.fechaEntrega}}}

\\begin{{document}}
    \\input{{portada/portada.tex}}
    
    %Write your document here

\\end{{document}}

    """)

def create_make_file(document_name: str, documet_dir: Path):
    print("---> Creating Makefile")
    os.chdir(documet_dir)
    makefile = Path('Makefile')
    makefile.touch()
    open_makefile = makefile.open('a+')   
    open_makefile.write(f"""# Latex Makefile
.RECIPEPREFIX = >

NAME={document_name}
PAPER={document_name}.tex
SHELL=/bin/zsh

all:
> rubber --pdf $(PAPER)

clean:
> rubber --clean $(PAPER)

watch:
> @while [ 1 ]; do; inotifywait $(PAPER); sleep 0.01; make all; done

""")
    open_makefile.close()
    print("     DONE")

if __name__ == '__main__':
    main(args)
