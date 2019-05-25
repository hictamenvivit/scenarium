import os
import json
from models import Document

ROOT = '/data/data/com.termux/files/home/storage/downloads/ecriture/court_métrages'


def build_paths(project_name):
    root = os.path.join(ROOT, project_name, 'scenario')
    return tuple([os.path.join(root, "{}{}".format(project_name, tail)) for tail in ["_raw.txt", "_map.json"]] + [root])

def build_scenario(project_name):
    text_path, my_map, root = build_paths(project_name)
    with open(my_map, 'r') as file:
        dico = json.load(file)
    dico = {**dico, **{k.replace('€', '§'):'§'+v for k,v in dico.items() } }
    document = Document(text_path, project_name, dico=dico)
    tex_filename = '{}.tex'.format(project_name)
    pdf_filename = '{}.pdf'.format(project_name)
    document.save(tex_filename)
    os.system("pdflatex {}".format(tex_filename))
    os.system("mv {} {}".format(pdf_filename, os.path.join(root)))
    os.system("rm *.log *.aux *.tex")
