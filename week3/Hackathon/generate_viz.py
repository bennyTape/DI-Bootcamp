"""
Script de génération de visualisation.png
Prend en argument le nom d'un utilisateur (ou index 0 par défaut)
et génère visualisation.png basé sur son historique.
"""

import sys
import json
import matplotlib
matplotlib.use('Agg')  # backend non-interactif (pas besoin de display)
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
from datetime import datetime, timedelta
import random
import os

random.seed(42)

GENRES_VALIDES = ["action", "drame", "comédie", "thriller", "sci-fi", "horreur", "romance", "animation",
                  "Action", "Drame", "Comédie", "Thriller", "Science-Fiction", "Horreur", "Romance", "Animation"]

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def get_user_name(u: dict) -> str:
    return u.get("name") or f"Utilisateur {u.get('id', '')}"


def charger_utilisateurs() -> list:
    path = os.path.join(SCRIPT_DIR, "utilisateurs.json")
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print("Fichier utilisateurs.json introuvable.")
        sys.exit(1)


def ajouter_dates(historique: list) -> list:
    """Attribue des dates aléatoires dans les 30 derniers jours si pas déjà présentes."""
    aujourd_hui = datetime.today()
    for h in historique:
        if "date" not in h or not h["date"]:
            jours_avant = random.randint(0, 30)
            h["date"] = (aujourd_hui - timedelta(days=jours_avant)).strftime("%Y-%m-%d")
    return sorted(historique, key=lambda x: x["date"])


def pie_genres(utilisateur: dict, ax: plt.Axes):
    genres = [
        h["genre"] for h in utilisateur.get("watch_history", [])
        if h.get("genre") in GENRES_VALIDES
    ]

    if not genres:
        ax.text(0.5, 0.5, "Aucun genre valide", ha='center', va='center',
                fontsize=13, transform=ax.transAxes)
        ax.set_title(f"Genres visionnés — {get_user_name(utilisateur)}", fontsize=13, fontweight="bold")
        ax.axis('off')
        return

    comptage = Counter(genres)
    labels   = list(comptage.keys())
    valeurs  = list(comptage.values())
    couleurs = plt.cm.Set3(np.linspace(0, 1, len(labels)))

    ax.pie(
        valeurs,
        labels=labels,
        autopct="%1.0f%%",
        colors=couleurs,
        startangle=140,
        pctdistance=0.8,
    )
    ax.set_title(f"Genres visionnés — {get_user_name(utilisateur)}", fontsize=13, fontweight="bold")


def line_notes(utilisateur: dict, ax: plt.Axes):
    historique = ajouter_dates(list(utilisateur.get("watch_history", [])))

    # Séparer valides et invalides
    valides   = [h for h in historique if h.get("rating") is not None and 1 <= h["rating"] <= 5]
    invalides = [h for h in historique if h.get("rating") is None or not (1 <= h.get("rating", 0) <= 5)]

    if not valides:
        ax.text(0.5, 0.5, "Aucune note valide", ha='center', va='center',
                fontsize=13, transform=ax.transAxes)
        ax.set_title(f"Notes au fil du temps — {get_user_name(utilisateur)}", fontsize=13, fontweight="bold")
        return

    dates  = [h["date"] for h in valides]
    notes  = [h["rating"] for h in valides]
    titres = [h.get("movie", "?") for h in valides]

    ax.plot(dates, notes, marker="o", color="#4C72B0", linewidth=2, markersize=7)

    for d, n, t in zip(dates, notes, titres):
        ax.annotate(t, (d, n), textcoords="offset points", xytext=(5, 5), fontsize=7, rotation=15)

    # Marquer les invalides sur l'axe X
    for h in invalides:
        ax.axvline(x=h["date"], color='red', linestyle='--', alpha=0.3, linewidth=1)
        ax.text(h["date"], 0.2, '✕', color='red', fontsize=9, ha='center')

    ax.set_title(f"Notes au fil du temps — {get_user_name(utilisateur)}", fontsize=13, fontweight="bold")
    ax.set_xlabel("Date")
    ax.set_ylabel("Note (1–5)")
    ax.set_ylim(0, 5.5)
    ax.tick_params(axis="x", rotation=30)
    ax.grid(True, alpha=0.3)


def generer_visualisation(nom_utilisateur: str = None):
    utilisateurs = charger_utilisateurs()

    if not utilisateurs:
        print("Aucun utilisateur trouvé.")
        sys.exit(1)

    # Trouver l'utilisateur par nom, sinon prendre le dernier
    cible = None
    if nom_utilisateur:
        for u in utilisateurs:
            if get_user_name(u).lower() == nom_utilisateur.lower():
                cible = u
                break

    if cible is None:
        # Prendre le dernier utilisateur ajouté (le plus récent)
        cible = utilisateurs[-1]

    print(f" Visualisation pour : {get_user_name(cible)}")

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle(f"Analyse de visionnage — {get_user_name(cible)}", fontsize=15, fontweight="bold", y=1.01)

    pie_genres(cible, axes[0])
    line_notes(cible, axes[1])

    plt.tight_layout()
    output_path = os.path.join(SCRIPT_DIR, "visualisation.png")
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f" Graphique sauvegardé dans {output_path}")


if __name__ == "__main__":
    nom = sys.argv[1] if len(sys.argv) > 1 else None
    generer_visualisation(nom)
