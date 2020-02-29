

from models import parse, rawify, latexify
import json

ROOT = "/storage/emulated/0/Download/ecriture/court_métrages/chair/scenario/chair_raw.txt"



ROOT_DICO = "/storage/emulated/0/Download/ecriture/court_métrages/chair/scenario/chair_map.json"


with open(ROOT, "r") as f:
    file = f.read()
    
with open(ROOT_DICO, "r") as f:
    char_map = json.load(f)
    
blocks = file.split("\n\n")


def test_parse_1():
    assert parse("§dd\nHello").type == "dd"
    
def test_rawify():
    assert rawify(parse("§L\nBonjour")) == "§L\nBonjour"
    
    
def test_latexify():
    _ = [latexify(parse(b), char_map) for b in blocks]