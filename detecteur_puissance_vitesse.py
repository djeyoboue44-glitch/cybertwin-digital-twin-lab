"""
Détecteur de cohérence puissance / vitesse (étape 14 du TP).

À insérer dans la méthode `Jumeau.detecter` du jumeau, comme 7e détecteur.

Principe physique : la puissance électrique du ventilateur dépend de sa vitesse,
selon la relation du modèle  puissance = 2,0 + 0,06 * vitesse  (en kW).
Si la puissance mesurée s'écarte trop de cette valeur attendue, c'est que l'une
des deux valeurs est truquée (capteur de vitesse ou de puissance manipulé).

Ce détecteur attrape une attaque qui fige la puissance (registre caché 100 = 2)
pendant que le ventilateur est arrêté : la vitesse réelle tombe, mais la
puissance reste figée, donc les deux ne sont plus cohérentes. Aucune règle
d'origine ne voyait ce cas.
"""

# --- bloc ajouté à la fin de Jumeau.detecter ---------------------------------

        # 7. cohérence puissance / vitesse (détecteur étudiant)
        p_attendue = 2.0 + 0.06 * m["vitesse"]
        if abs(m["puissance"] - p_attendue) > 1.0:
            self.alerte(
                ("coherence_P",), "incoherence_puissance", "modèle", "elevee",
                f"puissance {m['puissance']:.1f} kW incohérente avec vitesse "
                f"{m['vitesse']:.0f} % (attendu {p_attendue:.1f} kW)", t
            )
        else:
            self.lever(("coherence_P",))
