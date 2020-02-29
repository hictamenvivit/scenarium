

from googletrans import Translator
t = Translator()

class Titre:
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
    def __init__(self, titre):
        self.titre = titre
        
    def rep(self):
        return self.debut + self.titre + self.fin

class Commande:
    def __init__(self, nom, argument_principal=None, argument_secondaire=None):
        self.nom = nom
        self.argument_principal = argument_principal
        self.argument_secondaire = argument_secondaire
    def rep(self):
        template = "\\{0}{2}{{{1}}}"
        a1 = self.argument_principal if self.argument_principal else ''
        a2 = '[{}]'.format(self.argument_secondaire) if self.argument_secondaire else ''
        return template.format(self.nom, a1, a2)
        
class Commande2(Commande):
    def rep(self):
        template = "\\{0}{2}{{{1}}}"
        a1 = self.argument_principal if self.argument_principal else ''
        a2 = '{{{}}}'.format(self.argument_secondaire) if self.argument_secondaire else ''
        return template.format(self.nom, a1, a2)
        
class Parler(Commande2):
    def __init__(self, parlant, texte):
        super().__init__('speak', texte, parlant)
        
class Slug(Commande):
    incr = 1
    def __init__(self, interieur, lieu, heure):
        self.number = Slug.incr
        nom = 'intslug' if interieur else 'extslug'
        super().__init__(nom, lieu, heure)
        Slug.incr += 1

    def rep(self):
        return "{}\n{}".format(
            "{0:0=3d}".format(self.number),
            super().rep())
        
class Simple():
    def __init__(self, texte):
        self.texte = texte
    def rep(self):
        return self.texte
        
        
class OCommande:
    """
    The originale commande formatted as a string with at least two lines
    """
    def __init__(self, string):
        content = string.split("\n")
        assert len(content) > 1, "OCommmande instanciated with only one line" + str(content)
        head = content[0]
        tail = "\n".join(content[1:])
        assert head.startswith('§'), "paragraph should start with keyword preceded by §" + head
        self.keyword = head[1:]
        self.content = tail
        if self.type == 'scene':
            assert len(tail.split('|')) == 3
    
    @property
    def type(self):
        if self.keyword == 'dd':
            return 'dd'
        if self.keyword.startswith('scene'):
            return 'scene'
        if self.keyword.startswith('ellipse'):
            return 'ellipse'
        return 'dialogue'
        
    @property
    def corresponding_new_command(self):

        if self.type == "dialogue":
            return Parler(parlant=self.keyword, texte=self.content)
        if self.type == "dd":
            return Simple(self.content)
        if self.type == "ellipse":
            return Simple("Ellipse: %s" % self.content)
        if self.type == "scene":
            a,b,c = self.content.split('\n')[0].split('|')
            int = a == 'int'
            heure, lieu = b,c
            return Slug(interieur=int, lieu=lieu, heure=heure)
            
    def translate(self):
        self.content = t.translate(self.content, src="fr", dest="en").text
            
        

class Document:
    def __init__(self, filepath, my_title, dico, translate=False):
        with open(filepath, 'r') as file:
            content = file.read()
            for key, value in dico.items():
                content = content.replace(key, value)
            commands_text = [i.strip() for i in content.split('\n\n')]
            o_commands = [OCommande(ct) for ct in commands_text]
            if translate:
                print("Translating...")
                _ = [i.translate() for i in o_commands]
                print("Done")
            new_commands = [Titre(my_title)] + [i.corresponding_new_command for i in o_commands] + [End()]
            reps = [i.rep() for i in new_commands]
            self.file_content = '\n\n'.join(reps)
            
    def save(self, path):
        if '€' in self.file_content:
            b = False
            example = None
            for char in self.file_content:
                if b:
                    example = char
                    break
                if char == "€":
                    b = True
            raise AttributeError('Il reste des €, for instance ' + str(example))
            
        with open(path, 'w') as file:
            file.write(self.file_content)
            
    def replace(self, dico):
        for key, value in dico.items():
            self.file_content = self.file_content.replace(key, value)
            
        


class End:
    text = "\\end{document}"
    def rep(self):
        return self.text

