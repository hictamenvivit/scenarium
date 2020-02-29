

from collections import namedtuple

Command = namedtuple("Command", ["type", "head", "content"])


def type_from_keyword(keyword):
    if keyword == 'dd':
        return 'dd'
    if keyword.startswith('scene'):
        return 'scene'
    if keyword.startswith('ellipse'):
        return 'ellipse'
    return 'dialogue'

def validate(block):
    assert len(block.split("\n")) == 2, "Invalid block {}".format(block)
    assert block.startswith("§"), block

def parse(block):
    _ = validate(block)
    head, tail = block.split("\n")
    return Command(
            type=type_from_keyword(head[1:]),
            head=head,
            content=tail
        )

def rawify(command):
    return "\n".join([command.head, command.content])
    

def latexify(command, dico):
    
    if command.type == "dd":
        return command.content
        
    if command.type == "dialogue":
        locuteur_initiale = command.head[1:]
        try:
            locuteur = dico["€" + locuteur_initiale]
        except KeyError:
            raise KeyError("Missing character corresponding to initial {}".format(locuteur_initiale))
        return format_as_latex("speak", arg1=locuteur, arg2=command.content, brackets=False)
        
    if command.type == "scene":
        scene_number = command.head.split("scene")[1]
        int_ext, day_night, place = command.content.split("|")
        return format_as_latex(int_ext + "slug", place, day_night, True)

def format_as_latex(command_name, arg1=None, arg2=None, brackets=False):
    template = "\\{0}{2}{{{1}}}"
    a1 = arg1 if arg1 else ''
    a2_template = "[{}]" if brackets else "{{{}}}"
    a2 = a2_template.format(arg2) if arg2 else ''
    return template.format(command_name, a1, a2)
    
    
def parse_raw_file(raw_file):
    return [parse(block) for block in raw_file.split("\n\n")]
    

def make_latex_file(raw_file):
    debut = """\\documentclass{screenplay}
\\usepackage[utf8]{inputenc}
\\title{"""
    fin = """}
\\author{Maxime Bettinelli}
\\newcommand{\\speak}[2]{
\\begin{dialogue}{#1}
#2
\\end{dialogue}
}

\\begin{document}

\\newcommand{\\temps}{
\\intslug[jour N\\&B]{L'appartement, salon}
}

\\maketitle
"""
    
