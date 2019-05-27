from models import Commande, Commande2, Parler, Slug, OCommande, Document
import pytest

def test_positif():
    assert True

def test_commande_1_argument():
    commande = Commande('manger', 'fruit')
    assert commande.rep() == "\manger{fruit}"

def test_commande_2_arguments():
    commande = Commande('chanter','faust','en allemand')
    assert commande.rep() == "\chanter[en allemand]{faust}"
       
def test_commande2_2_arguments():
    commande = Commande2('chanter','faust','en allemand')
    assert commande.rep() == "\chanter{en allemand}{faust}"
    
def test_parler():
    parlant = 'Elle'
    texte = 'Bonjour'
    parler = Parler(parlant, texte)
    assert parler.rep() == '\speak{Elle}{Bonjour}'
    
def test_slug():
    slug = Slug(True, 'Jardin', 'jour')
    assert slug.rep() == '001\n\intslug[jour]{Jardin}'
    
def test_ocmmande_instanciation():
    string = """§bonjour
comment allez-vous?"""
    oc = OCommande(string)
    assert oc.keyword == "bonjour"
    
# def test_instanciate_odocument():
#     od = Document('data/text.txt', 'essai', dict())
    
    
    
@pytest.mark.parametrize('input, output', [
    ("""§P3
bonjour""","\speak{P3}{bonjour}"),
    ("""§dd
elle rentre""", "elle rentre"),
    ("""§scene1
ext|jour|une rue""","002\n\extslug[jour]{une rue}" )
])
def test_from_old_to_new(input, output):
    truc = OCommande(input).corresponding_new_command
    assert truc.rep() == output

    