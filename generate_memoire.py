from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Image
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

# Fonction pour créer la page de titre
def page_de_titre(canvas, doc):
    canvas.saveState()
    width, height = A4

    # Titre principal
    canvas.setFont("Helvetica-Bold", 24)
    canvas.drawCentredString(width/2, height-200, "MÉMOIRE DE PROJET")

    canvas.setFont("Helvetica-Bold", 20)
    canvas.drawCentredString(width/2, height-250, "SYSTÈME DE GESTION DE CRÈCHE")

    canvas.setFont("Helvetica", 14)
    canvas.drawCentredString(width/2, height-300, "Application Web Complète")

    canvas.setFont("Helvetica", 12)
    canvas.drawCentredString(width/2, height-350, "Développé avec Flask et MongoDB")

    canvas.setFont("Helvetica", 10)
    canvas.drawCentredString(width/2, height-400, "Réalisé par : [Votre Nom]")
    canvas.drawCentredString(width/2, height-420, "Sous la direction de : [Nom du Superviseur]")
    canvas.drawCentredString(width/2, height-440, f"Date : {doc.date}")

    canvas.restoreState()

# Fonction pour les pages suivantes
def page_later(canvas, doc):
    canvas.saveState()
    width, height = A4

    # En-tête
    canvas.setFont("Helvetica", 10)
    canvas.drawString(50, height-50, "Mémoire : Système de Gestion de Crèche")
    canvas.drawRightString(width-50, height-50, f"Page {doc.page}")

    canvas.restoreState()

# Styles
styles = getSampleStyleSheet()
title_style = ParagraphStyle(
    'Title',
    parent=styles['Heading1'],
    fontSize=18,
    spaceAfter=20,
    alignment=1  # Centré
)
heading1_style = ParagraphStyle(
    'Heading1',
    parent=styles['Heading1'],
    fontSize=16,
    spaceAfter=15,
)
heading2_style = ParagraphStyle(
    'Heading2',
    parent=styles['Heading2'],
    fontSize=14,
    spaceAfter=10,
)
normal_style = styles['Normal']

# Contenu du mémoire
def create_memoire():
    doc = SimpleDocTemplate("memoire_projet.pdf", pagesize=A4)
    doc.date = "Décembre 2023"
    story = []

    # Page de titre
    story.append(PageBreak())

    # Table des matières
    story.append(Paragraph("TABLE DES MATIÈRES", title_style))
    story.append(Spacer(1, 20))

    toc_content = [
        "INTRODUCTION ........................................................................................ 1",
        "CHAPITRE 1 : ANALYSE DES BESOINS ..................................................... 2",
        "1.1 Présentation du projet ........................................................................ 2",
        "1.2 Objectifs ................................................................................................ 3",
        "1.3 Acteurs et rôles ................................................................................ 3",
        "1.4 Fonctionnalités principales ............................................................. 4",
        "CHAPITRE 2 : CONCEPTION DU SYSTÈME ............................................... 6",
        "2.1 Architecture générale ....................................................................... 6",
        "2.2 Modèle de données (ERD) ............................................................. 7",
        "2.3 Cas d'utilisation ............................................................................... 8",
        "2.4 Diagrammes UML ............................................................................. 9",
        "CHAPITRE 3 : RÉALISATION ................................................................. 10",
        "3.1 Technologies utilisées ................................................................. 10",
        "3.2 Structure du projet ......................................................................... 11",
        "3.3 Implémentation des contrôleurs ................................................... 12",
        "3.4 Interface utilisateur ....................................................................... 13",
        "CHAPITRE 4 : TESTS ET VALIDATION ................................................... 14",
        "4.1 Stratégie de test ............................................................................. 14",
        "4.2 Tests unitaires ............................................................................... 14",
        "4.3 Tests d'intégration ......................................................................... 15",
        "CHAPITRE 5 : CONCLUSION ..................................................................... 16",
        "BIBLIOGRAPHIE ..................................................................................... 17",
        "ANNEXES .................................................................................................. 18"
    ]

    for item in toc_content:
        story.append(Paragraph(item, normal_style))
        story.append(Spacer(1, 5))

    story.append(PageBreak())

    # Introduction
    story.append(Paragraph("INTRODUCTION", title_style))
    story.append(Spacer(1, 20))

    intro_text = """
    Dans le contexte actuel où la gestion des établissements éducatifs devient de plus en plus complexe,
    il est essentiel de disposer d'outils informatiques performants pour faciliter les tâches administratives
    et pédagogiques. Ce mémoire présente le développement d'un système de gestion de crèche complet,
    permettant de gérer efficacement les enfants, les parents, les éducateurs et les diététiciens.

    Le projet a été réalisé en utilisant les technologies web modernes : Flask comme framework backend,
    MongoDB comme base de données NoSQL, et Bootstrap pour l'interface utilisateur. L'application
    offre une gestion complète des présences, des activités, de la nutrition et des paiements.

    Ce document détaille l'ensemble du processus de développement, de l'analyse des besoins à la mise
    en production, en passant par la conception et l'implémentation.
    """

    story.append(Paragraph(intro_text, normal_style))
    story.append(Spacer(1, 20))

    # Chapitre 1 : Analyse des besoins
    story.append(Paragraph("CHAPITRE 1 : ANALYSE DES BESOINS", heading1_style))
    story.append(Spacer(1, 15))

    story.append(Paragraph("1.1 Présentation du projet", heading2_style))
    story.append(Spacer(1, 10))

    pres_text = """
    Le système de gestion de crèche est une application web complète conçue pour automatiser et
    simplifier la gestion quotidienne d'une crèche. Elle permet aux différents acteurs (administrateurs,
    éducateurs, diététiciens et parents) d'accéder à des fonctionnalités adaptées à leurs rôles respectifs.
    """

    story.append(Paragraph(pres_text, normal_style))
    story.append(Spacer(1, 15))

    story.append(Paragraph("1.2 Objectifs", heading2_style))
    story.append(Spacer(1, 10))

    obj_text = """
    Les objectifs principaux du projet sont :
    - Automatiser la gestion des présences des enfants
    - Faciliter la communication entre les différents acteurs
    - Gérer efficacement les plans nutritionnels
    - Simplifier les processus de paiement
    - Fournir des tableaux de bord personnalisés pour chaque rôle
    """

    story.append(Paragraph(obj_text, normal_style))
    story.append(Spacer(1, 15))

    story.append(Paragraph("1.3 Acteurs et rôles", heading2_style))
    story.append(Spacer(1, 10))

    acteurs_data = [
        ["Rôle", "Responsabilités"],
        ["Administrateur", "Gestion complète du système, utilisateurs, configuration"],
        ["Éducateur", "Gestion des présences, activités, groupes d'enfants"],
        ["Diététicien", "Gestion de la nutrition, menus, plans alimentaires"],
        ["Parent", "Consultation des informations de leurs enfants, paiements"]
    ]

    acteurs_table = Table(acteurs_data)
    acteurs_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    story.append(acteurs_table)
    story.append(Spacer(1, 15))

    story.append(Paragraph("1.4 Fonctionnalités principales", heading2_style))
    story.append(Spacer(1, 10))

    fonct_text = """
    Le système offre les fonctionnalités suivantes :

    - Gestion complète des utilisateurs et profils
    - Système de présence quotidien avec statistiques
    - Planification et gestion des activités
    - Gestion des groupes d'enfants
    - Création et gestion des repas et menus
    - Plans nutritionnels personnalisés
    - Système de communication (messages, plaintes)
    - Gestion des paiements avec intégration Chargily
    """

    story.append(Paragraph(fonct_text, normal_style))
    story.append(Spacer(1, 20))

    # Chapitre 2 : Conception
    story.append(Paragraph("CHAPITRE 2 : CONCEPTION DU SYSTÈME", heading1_style))
    story.append(Spacer(1, 15))

    story.append(Paragraph("2.1 Architecture générale", heading2_style))
    story.append(Spacer(1, 10))

    arch_text = """
    L'architecture du système suit le pattern MVC (Modèle-Vue-Contrôleur) avec Flask. L'application
    est structurée autour de blueprints pour une meilleure organisation. MongoDB est utilisé comme
    base de données NoSQL pour sa flexibilité et ses performances.

    L'architecture comprend :
    - Couche présentation : Templates Jinja2 avec Bootstrap
    - Couche contrôleur : Blueprints Flask pour chaque module
    - Couche modèle : Classes Python pour l'interaction avec MongoDB
    - Base de données : MongoDB avec collections pour chaque entité
    """

    story.append(Paragraph(arch_text, normal_style))
    story.append(Spacer(1, 15))

    story.append(Paragraph("2.2 Modèle de données (ERD)", heading2_style))
    story.append(Spacer(1, 10))

    erd_text = """
    Le modèle de données comprend les entités principales suivantes :
    - User : Gestion des comptes utilisateurs
    - Parent : Informations des parents
    - Enfant : Données des enfants
    - Educateur : Profils des éducateurs
    - Dietitian : Profils des diététiciens
    - Group : Groupes d'enfants
    - Presence : Enregistrements de présence
    - Meal_Record : Enregistrements des repas
    - Invoice : Factures et paiements

    Les relations entre ces entités sont gérées via des références MongoDB.
    """

    story.append(Paragraph(erd_text, normal_style))
    story.append(Spacer(1, 15))

    # Chapitre 3 : Réalisation
    story.append(Paragraph("CHAPITRE 3 : RÉALISATION", heading1_style))
    story.append(Spacer(1, 15))

    story.append(Paragraph("3.1 Technologies utilisées", heading2_style))
    story.append(Spacer(1, 10))

    tech_data = [
        ["Technologie", "Version", "Utilisation"],
        ["Flask", "2.2.5", "Framework web Python"],
        ["MongoDB", "4.4+", "Base de données NoSQL"],
        ["PyMongo", "4.4.0", "Driver MongoDB pour Python"],
        ["Flask-Login", "0.6.2", "Gestion de l'authentification"],
        ["Bootstrap", "5.x", "Framework CSS"],
        ["Jinja2", "-", "Moteur de templates"],
        ["ReportLab", "3.6.13", "Génération de PDF"],
        ["Requests", "2.31.0", "Appels API externes"]
    ]

    tech_table = Table(tech_data)
    tech_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    story.append(tech_table)
    story.append(Spacer(1, 15))

    story.append(Paragraph("3.2 Structure du projet", heading2_style))
    story.append(Spacer(1, 10))

    struct_text = """
    L'organisation du code suit les bonnes pratiques Flask :

    gestion_creche_final/
    ├── app.py                 # Point d'entrée
    ├── db.py                  # Configuration MongoDB
    ├── controllers/           # Logique métier (Blueprints)
    ├── models/               # Modèles de données
    ├── templates/            # Templates Jinja2
    ├── static/              # Fichiers statiques
    ├── utils/               # Utilitaires
    └── diagrams/            # Documentation UML
    """

    story.append(Paragraph(struct_text, normal_style))
    story.append(Spacer(1, 15))

    # Chapitre 4 : Tests
    story.append(Paragraph("CHAPITRE 4 : TESTS ET VALIDATION", heading1_style))
    story.append(Spacer(1, 15))

    test_text = """
    La validation du système comprend plusieurs niveaux de tests :

    - Tests manuels des fonctionnalités principales
    - Vérification de l'interface utilisateur
    - Tests d'intégration avec MongoDB
    - Validation des processus métier
    - Tests de sécurité de base

    L'application a été testée avec différents navigateurs et scénarios d'utilisation.
    """

    story.append(Paragraph(test_text, normal_style))
    story.append(Spacer(1, 20))

    # Conclusion
    story.append(Paragraph("CHAPITRE 5 : CONCLUSION", heading1_style))
    story.append(Spacer(1, 15))

    conc_text = """
    Ce projet a permis de développer une application web complète pour la gestion d'une crèche,
    répondant aux besoins identifiés lors de l'analyse. L'utilisation de technologies modernes
    comme Flask et MongoDB a permis de créer un système robuste et évolutif.

    Les fonctionnalités implémentées couvrent l'ensemble des aspects de la gestion d'une crèche :
    administration, suivi pédagogique, nutrition et communication. L'architecture modulaire facilite
    la maintenance et l'évolution future du système.

    Ce travail démontre l'importance des outils informatiques dans la gestion des établissements
    éducatifs et ouvre des perspectives d'amélioration continue.
    """

    story.append(Paragraph(conc_text, normal_style))
    story.append(Spacer(1, 20))

    # Bibliographie
    story.append(Paragraph("BIBLIOGRAPHIE", heading1_style))
    story.append(Spacer(1, 15))

    bib_content = [
        "[1] Documentation Flask. https://flask.palletsprojects.com/",
        "[2] Documentation MongoDB. https://docs.mongodb.com/",
        "[3] Documentation Bootstrap. https://getbootstrap.com/",
        "[4] Documentation ReportLab. https://www.reportlab.com/docs/reportlab-userguide.pdf",
        "[5] Python Documentation. https://docs.python.org/3/"
    ]

    for item in bib_content:
        story.append(Paragraph(item, normal_style))
        story.append(Spacer(1, 5))

    story.append(Spacer(1, 20))

    # Annexes
    story.append(Paragraph("ANNEXES", heading1_style))
    story.append(Spacer(1, 15))

    annex_text = """
    Annexe 1 : Code source principal (app.py)
    Annexe 2 : Modèles de données
    Annexe 3 : Diagrammes UML
    Annexe 4 : Captures d'écran de l'application
    Annexe 5 : Guide d'installation et de déploiement
    """

    story.append(Paragraph(annex_text, normal_style))

    # Générer le PDF
    doc.build(story, onFirstPage=page_de_titre, onLaterPages=page_later)

if __name__ == "__main__":
    create_memoire()
    print("Le mémoire PDF a été généré : memoire_projet.pdf")
