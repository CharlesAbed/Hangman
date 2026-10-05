from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    PageTemplate,
    Paragraph,
    PageBreak,
    Preformatted,
    Spacer,
    Table,
    TableStyle,
)

OUTPUT = Path(__file__).with_name("guide_hangman_debutant.pdf")

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(
    name="TitleCustom", parent=styles["Title"], alignment=TA_CENTER,
    fontName="Helvetica-Bold", fontSize=23, leading=28, textColor=colors.HexColor("#153B50"),
    spaceAfter=18,
))
styles.add(ParagraphStyle(
    name="Subtitle", parent=styles["Normal"], alignment=TA_CENTER,
    fontSize=11, leading=15, textColor=colors.HexColor("#49616B"), spaceAfter=18,
))
styles.add(ParagraphStyle(
    name="H1Custom", parent=styles["Heading1"], fontName="Helvetica-Bold",
    fontSize=17, leading=21, textColor=colors.HexColor("#153B50"), spaceBefore=12, spaceAfter=8,
))
styles.add(ParagraphStyle(
    name="H2Custom", parent=styles["Heading2"], fontName="Helvetica-Bold",
    fontSize=13, leading=17, textColor=colors.HexColor("#A23E48"), spaceBefore=9, spaceAfter=5,
))
styles.add(ParagraphStyle(
    name="BodyCustom", parent=styles["BodyText"], fontSize=10.2, leading=14,
    spaceAfter=6,
))
styles.add(ParagraphStyle(
    name="Small", parent=styles["BodyText"], fontSize=8.8, leading=12,
    textColor=colors.HexColor("#49616B"),
))
styles.add(ParagraphStyle(
    name="Callout", parent=styles["BodyText"], fontSize=10, leading=14,
    backColor=colors.HexColor("#EAF4F4"), borderColor=colors.HexColor("#9BC5C3"),
    borderWidth=0.7, borderPadding=8, spaceBefore=5, spaceAfter=8,
))
styles.add(ParagraphStyle(
    name="CodeCustom", fontName="Courier", fontSize=7.8, leading=10,
    leftIndent=8, rightIndent=8, backColor=colors.HexColor("#F2F4F5"),
    borderColor=colors.HexColor("#D3DADD"), borderWidth=0.5, borderPadding=7,
    spaceBefore=4, spaceAfter=8,
))


def P(text, style="BodyCustom"):
    return Paragraph(text, styles[style])


def code(text):
    return Preformatted(text.strip("\n"), styles["CodeCustom"])


def bullet(text):
    return P("&bull; " + text)


def title(text):
    return P(text, "H1Custom")


def subtitle(text):
    return P(text, "H2Custom")


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#718096"))
    canvas.drawString(1.5 * cm, 1 * cm, "Guide Hangman - niveau débutant")
    canvas.drawRightString(19.5 * cm, 1 * cm, f"Page {doc.page}")
    canvas.restoreState()


doc = BaseDocTemplate(
    str(OUTPUT), pagesize=A4, rightMargin=1.5 * cm, leftMargin=1.5 * cm,
    topMargin=1.4 * cm, bottomMargin=1.6 * cm,
)
doc.addPageTemplates([PageTemplate(id="main", frames=[Frame(
    doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="normal"
)], onPage=footer)])

story = []
story += [
    P("Comprendre ton jeu du pendu", "TitleCustom"),
    P("Guide pas a pas pour debuter en Python", "Subtitle"),
    P("Ce document explique les fonctionnements presents dans ton dossier <b>hangman</b> avec des mots simples. Chaque partie contient l'enonce, l'idee, un exemple de ton exercice et une petite tache a refaire seul.", "Callout"),
    title("1. Avant de commencer"),
    P("Un programme est une suite d'instructions. Python lit ces instructions de haut en bas. Dans un jeu, certaines instructions sont repetees dans une boucle et d'autres sont rangees dans des fonctions."),
    subtitle("Les mots importants"),
    bullet("<b>Variable</b> : une boite qui garde une valeur. Exemple : <font name='Courier'>penalties = 0</font>."),
    bullet("<b>Fonction</b> : un petit bloc de code reutilisable. Elle commence par <font name='Courier'>def</font>."),
    bullet("<b>Condition</b> : une question qui decide quoi faire. Elle utilise <font name='Courier'>if</font>, <font name='Courier'>elif</font> et <font name='Courier'>else</font>."),
    bullet("<b>Boucle</b> : du code repete. Ici, on utilise <font name='Courier'>while</font> pour continuer la partie."),
    bullet("<b>Evenement</b> : une action du joueur, par exemple un clic ou la fermeture de la fenetre."),
    subtitle("Le plan general du pendu"),
    code("1. Choisir un mot secret\n2. Afficher des tirets a la place des lettres\n3. Demander une lettre au joueur\n4. Verifier si la lettre est dans le mot\n5. Ajouter une erreur si elle est fausse\n6. Arreter si le mot est trouve ou si la limite d'erreurs est atteinte"),
    title("2. Exercice console : choisir et afficher un mot"),
    P("<b>Enonce de l'exercice :</b> lire un fichier contenant un mot par ligne, choisir un mot au hasard et afficher les lettres trouvees. Les lettres inconnues doivent etre remplacees par un tiret bas."),
    subtitle("Fonction choose_word"),
    code("def choose_word(arguments):\n    content = arguments.word_list.read_text(encoding=\"utf-8\")\n    words = []\n\n    for line in content.splitlines():\n        word = line.strip().upper()\n        if word.isalpha():\n            words.append(word)\n\n    return random.choice(words)"),
    P("<b>Explication :</b> <font name='Courier'>read_text</font> lit le fichier. <font name='Courier'>splitlines()</font> separe le texte ligne par ligne. <font name='Courier'>strip()</font> enleve les espaces et le retour a la ligne. <font name='Courier'>upper()</font> transforme le mot en majuscules. Enfin, <font name='Courier'>random.choice</font> choisit un element au hasard."),
    P("<b>Exemple :</b> si le fichier contient <font name='Courier'>chat</font>, <font name='Courier'>python</font> et <font name='Courier'>bateau</font>, le programme peut choisir <font name='Courier'>PYTHON</font>. Le choix change d'une partie a l'autre."),
    subtitle("Fonction display_word"),
    code("def display_word():\n    result = \"\"\n\n    for letter in word:\n        if letter in found_letters:\n            result += letter + \" \"\n        else:\n            result += \"_ \"\n\n    return result"),
    P("Ici, <font name='Courier'>word</font> est le mot secret et <font name='Courier'>found_letters</font> contient les lettres deja trouvees. <font name='Courier'>return</font> renvoie le resultat a l'endroit ou la fonction a ete appelee."),
    P("<b>Exemple corrige :</b> mot = <font name='Courier'>CHAT</font> et lettres trouvees = <font name='Courier'>{A, T}</font>. L'affichage devient <font name='Courier'>_ _ A T</font>."),
    subtitle("La boucle de jeu"),
    code("while penalties < MAX_PENALTIES:\n    guess = input(\"$> \").strip().upper()\n\n    if len(guess) == 1:\n        if guess in word:\n            found_letters.add(guess)\n        else:\n            penalties += 1"),
    P("La boucle continue tant que le nombre de penalites est inferieur au maximum. <font name='Courier'>input</font> attend la reponse du joueur. <font name='Courier'>len(guess)</font> donne le nombre de caracteres. Une lettre correcte est ajoutee dans l'ensemble <font name='Courier'>found_letters</font>; une mauvaise lettre augmente <font name='Courier'>penalties</font>."),
    subtitle("A faire seul"),
    bullet("Change le nombre maximum de penalites et observe le resultat."),
    bullet("Ajoute un message quand le joueur propose une lettre deja trouvee."),
    bullet("Teste le mot <font name='Courier'>CHAT</font> avec les lettres <font name='Courier'>A</font> puis <font name='Courier'>X</font>."),
]

story += [PageBreak(), title("3. Exercice console complet : options et score"),
    P("<b>Enonce de l'exercice :</b> rendre le jeu configurable avec un fichier de mots obligatoire, un nombre maximum de penalites, une longueur de mot et un theme. Gerer les erreurs de fichier et enregistrer le meilleur score."),
    subtitle("Lire les arguments"),
    code("parser.add_argument(\"word_list\", type=Path,\n                    help=\"text file containing one word per line\")\nparser.add_argument(\"--penalties\", type=int, default=12)\nparser.add_argument(\"--length\", type=int)\nparser.add_argument(\"--theme\", default=\"general\")"),
    P("Un argument est une information donnee au lancement du programme. Exemple : <font name='Courier'>python challenge.py my_wordlist.txt --penalties 6 --length 5 --theme animaux</font>. Le fichier est obligatoire; les autres options sont facultatives car elles ont une valeur par defaut."),
    subtitle("Verifier les erreurs"),
    code("if arguments.penalties < 1:\n    parser.error(\"--penalties must be at least 1\")\n\nif arguments.length is not None and arguments.length < 1:\n    parser.error(\"--length must be at least 1\")"),
    P("La condition empeche des valeurs impossibles. <font name='Courier'>is not None</font> signifie : une longueur a ete donnee. Une bonne verification evite que le programme continue avec une mauvaise valeur."),
    P("<b>Exemple :</b> avec <font name='Courier'>--penalties 0</font>, le programme affiche une erreur car une partie doit permettre au moins une penalite."),
    subtitle("Les lettres et le mot complet"),
    code("if len(guess) == 1:\n    if guess in word:\n        found_letters.add(guess)\n    else:\n        penalties += 1\n\nelif len(guess) > 1:\n    if guess == word:\n        print(\"correct guess\")\n        break\n    penalties = min(penalties + 5, MAX_PENALTIES)"),
    P("Une proposition d'un seul caractere est traitee comme une lettre. Une proposition plus longue est traitee comme un mot entier. Un mauvais mot coute ici 5 penalites, mais <font name='Courier'>min</font> empeche de depasser la limite."),
    subtitle("Le meilleur score"),
    code("def get_high_score():\n    # Lire highscore.txt\n    # Pour chaque ligne : nombre;date\n    # Garder le plus petit nombre\n    return best_attempts, best_date\n\ndef save_high_score(attempts):\n    with HIGH_SCORE_FILE.open(\"a\", encoding=\"utf-8\") as file:\n        file.write(f\"{attempts};{today}\\n\")"),
    P("Le fichier <font name='Courier'>highscore.txt</font> garde une ligne comme <font name='Courier'>4;2026-09-18</font>. Le plus petit nombre de tentatives est le meilleur score. Le mode <font name='Courier'>a</font> signifie ajouter a la fin du fichier."),
    subtitle("A faire seul"),
    bullet("Lance le jeu avec <font name='Courier'>--theme espace</font> et explique le message affiche."),
    bullet("Ajoute un refus pour les caracteres speciaux comme <font name='Courier'>!</font>."),
    bullet("Ajoute une ligne de score et verifie qu'elle est relue au prochain lancement."),
]

story += [PageBreak(), title("4. Exercice Pygame : la version graphique"),
    P("<b>Enonce de l'exercice :</b> creer une fenetre Pygame, dessiner le pendu, afficher un clavier de lettres, permettre au joueur de cliquer, afficher la victoire ou la defaite et proposer un bouton Rejouer."),
    subtitle("Initialiser Pygame et la fenetre"),
    code("import pygame\nimport random\nfrom pathlib import Path\n\npygame.init()\nWIDTH = 800\nHEIGHT = 600\nscreen = pygame.display.set_mode((WIDTH, HEIGHT))\npygame.display.set_caption(\"Hangman\")"),
    P("<font name='Courier'>pygame.init()</font> prepare Pygame. <font name='Courier'>screen</font> represente la fenetre. Sa taille est de 800 pixels de large et 600 pixels de haut."),
    subtitle("Dessiner une forme"),
    code("pygame.draw.rect(screen, (90, 180, 80), (0, 500, WIDTH, 100))\npygame.draw.line(screen, wood_color, (600, 500), (600, 100), 15)\npygame.draw.circle(screen, skin_color, (700, 180), 30)"),
    P("Chaque couleur est un tuple <font name='Courier'>(rouge, vert, bleu)</font>. Un rectangle represente le sol, une ligne represente la potence et un cercle represente la tete."),
    subtitle("Faire apparaitre le personnage progressivement"),
    code("if wrong_guesses >= 1:\n    pygame.draw.circle(screen, skin_color, (700, 180), 30)\n\nif wrong_guesses >= 2:\n    pygame.draw.line(screen, clothes_color, (700, 210), (700, 300), 8)"),
    P("La valeur <font name='Courier'>wrong_guesses</font> compte les mauvaises lettres. A 1 erreur, on dessine la tete; a 2 erreurs, le corps; puis les bras et les jambes. C'est une condition qui controle le dessin."),
    subtitle("Detecter un clic sur une touche"),
    code("rect = pygame.Rect(x, y, KEY_WIDTH, KEY_HEIGHT)\n\nif rect.collidepoint(position):\n    if letter not in used_letters:\n        used_letters.append(letter)\n        if letter not in secret_word:\n            wrong_guesses += 1"),
    P("<font name='Courier'>pygame.Rect</font> decrit la zone d'un bouton. <font name='Courier'>collidepoint</font> repond vrai si la souris est dans cette zone. La lettre est ajoutee une seule fois dans <font name='Courier'>used_letters</font>."),
    subtitle("Connaitre l'etat de la partie"),
    code("def check_game_status():\n    if wrong_guesses >= 6:\n        return \"lose\"\n\n    for letter in secret_word:\n        if letter not in used_letters:\n            return \"playing\"\n\n    return \"win\""),
    P("La fonction renvoie un mot simple : <font name='Courier'>playing</font>, <font name='Courier'>win</font> ou <font name='Courier'>lose</font>. Si six erreurs sont atteintes, la partie est perdue. Sinon, on cherche encore une lettre non trouvee. S'il n'en reste plus, le joueur a gagne."),
]

story += [PageBreak(), title("5. La boucle Pygame expliquee"),
    subtitle("Recevoir les evenements"),
    code("running = True\n\nwhile running:\n    for event in pygame.event.get():\n        if event.type == pygame.QUIT:\n            running = False\n\n        if event.type == pygame.MOUSEBUTTONDOWN:\n            if game_status == \"playing\":\n                check_keyboard_click(event.pos)\n            else:\n                check_restart_click(event.pos)"),
    P("La boucle tourne environ 60 fois par seconde. <font name='Courier'>pygame.event.get()</font> recupere les actions en attente. Si le joueur clique sur la croix, <font name='Courier'>running</font> devient <font name='Courier'>False</font>, donc la boucle se termine normalement. Si le joueur clique, le programme choisit entre le clavier et le bouton Rejouer."),
    subtitle("Redessiner l'ecran"),
    code("draw_background()\ndraw_gallows()\ndraw_character()\ndraw_keyboard()\ndraw_word()\ndraw_game_status(game_status)\n\nif game_status != \"playing\":\n    draw_restart_button()\n\npygame.display.flip()\nclock.tick(60)"),
    P("A chaque tour, on redessine toute la scene. <font name='Courier'>pygame.display.flip()</font> rend le nouveau dessin visible. <font name='Courier'>clock.tick(60)</font> limite la vitesse a 60 images par seconde."),
    subtitle("Rejouer une partie"),
    code("def restart_game():\n    global used_letters, wrong_guesses\n    global game_status, secret_word\n\n    used_letters = []\n    wrong_guesses = 0\n    game_status = \"playing\"\n    secret_word = choose_word()"),
    P("La fonction remet toutes les valeurs dans leur etat de depart. <font name='Courier'>global</font> indique que la fonction modifie les variables creees en dehors d'elle."),
    subtitle("Pourquoi le jeu se fermait apres une defaite ?"),
    code("word_rect = word_text.get_rect(center=(400, 440))\nscreen.blit(word_text, word_rect)"),
    P("La variable doit garder exactement le meme nom. Avant la correction, le code utilisait <font name='Courier'>world_rect</font> alors que la variable s'appelait <font name='Courier'>word_rect</font>. Python ne trouvait pas <font name='Courier'>world_rect</font> et arretait le programme avec une erreur <font name='Courier'>NameError</font>."),
    P("<b>Regle debutant :</b> quand une fenetre se ferme toute seule, lance le programme depuis le terminal. Le message d'erreur indique souvent la ligne qui a provoque l'arret."),
]

story += [PageBreak(), title("6. Corrections et points a verifier"),
    subtitle("Correction 1 : chemin du fichier"),
    P("Dans la version Pygame, <font name='Courier'>Path(\"my_wordlist.txt\")</font> cherche le fichier dans le dossier depuis lequel tu lances Python. Lance donc le programme depuis le dossier <font name='Courier'>hangman</font>, ou utilise un chemin construit a partir du fichier Python."),
    code("from pathlib import Path\n\nBASE_DIR = Path(__file__).parent\nWORD_LIST_FILE = BASE_DIR / \"my_wordlist.txt\""),
    P("<font name='Courier'>__file__</font> represente le fichier Python actuel. <font name='Courier'>parent</font> represente son dossier. Cette version est plus solide si tu lances le programme depuis un autre endroit."),
    subtitle("Correction 2 : accents dans la liste"),
    P("Dans <font name='Courier'>challenge.py</font>, le test <font name='Courier'>word.isascii()</font> refuse les lettres accentuees. Le mot <font name='Courier'>éléctrique</font> sera donc ignore. Pour un jeu limite aux lettres A-Z, c'est normal. Pour accepter le francais, il faut retirer ce test et choisir une regle claire pour les accents."),
    subtitle("Correction 3 : fichiers vides"),
    P("<font name='Courier'>highscore.py</font> et <font name='Courier'>task 3.4.py</font> sont actuellement vides. Ce n'est pas une erreur : ce sont des fichiers prevus pour des exercices ou des extensions a completer."),
    subtitle("Methode pour travailler seul"),
    bullet("Lis l'enonce et souligne les donnees a memoriser : mot, lettres, erreurs, score."),
    bullet("Ecris d'abord une petite fonction qui fait une seule chose."),
    bullet("Teste avec un exemple tres petit : mot = <font name='Courier'>CHAT</font>."),
    bullet("Observe le message d'erreur avant de modifier le code."),
    bullet("Ajoute une seule modification, puis relance le programme."),
    title("7. Exercices d'entrainement"),
    P("<b>Exercice A :</b> ecris une fonction <font name='Courier'>mask_word(word, found_letters)</font> qui transforme <font name='Courier'>PYTHON</font> en <font name='Courier'>_ Y _ H _ N</font> quand les lettres trouvees sont <font name='Courier'>Y, H, N</font>."),
    P("<b>Correction :</b> parcourir chaque lettre avec une boucle. Ajouter la lettre si elle est dans <font name='Courier'>found_letters</font>, sinon ajouter <font name='Courier'>_</font>."),
    code("def mask_word(word, found_letters):\n    result = []\n    for letter in word:\n        if letter in found_letters:\n            result.append(letter)\n        else:\n            result.append(\"_\")\n    return \" \".join(result)"),
    P("<b>Exercice B :</b> ecris une fonction <font name='Courier'>is_won(word, found_letters)</font> qui renvoie <font name='Courier'>True</font> seulement si toutes les lettres du mot ont ete trouvees."),
    P("<b>Correction :</b> utiliser <font name='Courier'>all</font>. Cette fonction renvoie vrai seulement si toutes les conditions sont vraies."),
    code("def is_won(word, found_letters):\n    return all(letter in found_letters for letter in word)"),
    P("<b>Exercice C :</b> ajoute un bouton Rejouer qui remet les erreurs a zero, vide les lettres utilisees et choisit un nouveau mot. La correction est la fonction <font name='Courier'>restart_game</font> de <font name='Courier'>full game.py</font>."),
    P("Tu peux maintenant cacher les corrections, refaire les trois exercices, puis comparer ton resultat avec ce guide."),
]


doc.build(story)
print(f"PDF cree : {OUTPUT}")
