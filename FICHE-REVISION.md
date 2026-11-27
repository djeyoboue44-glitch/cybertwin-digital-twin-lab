# Fiche de révision · Jumeau numérique de cybersécurité

À réviser avant l'examen. Format court : la notion, puis ce qu'il faut pouvoir dire.

## 1. Le contexte et les trois problèmes

Centrale de traitement d'air (CTA) qui ventile deux salles d'opération. L'automate la pilote et parle **Modbus TCP**.

- **Problème 1 : l'automate obéit à tout le monde.** Modbus ne demande aucun mot de passe. N'importe quel ordinateur du réseau peut lui donner des ordres.
- **Problème 2 : les écrans peuvent mentir.** Si un attaquant fige ou décale un capteur, le poste de conduite affiche une valeur normale pendant que la salle dérive.
- **Problème 3 : on ne peut pas faire d'essais.** Impossible d'arrêter la ventilation d'un vrai bloc pour tester. Le jumeau permet de simuler sans risque.

## 2. Modbus, en bref

Protocole industriel pour lire et écrire des **registres** (cases mémoire numérotées) par le réseau. Conçu sans sécurité (pas de chiffrement, pas d'authentification). Codes de fonction utiles : 1 lire bobines, 3 lire registres de maintien, 6 écrire un registre. Une erreur se renvoie en **exception** (code 1 = fonction illégale, code 3 = valeur illégale).

## 3. La carte des registres (à connaître)

- Registres de maintien (lecture/écriture) : 0 et 1 consignes de température, 2 vitesse ventilateur, 3 seuil de pression.
- Registre **100** : maintenance cachée, non documentée. 1 = capteur figé, 2 = puissance figée, 3 = mesure décalée. C'est la porte dérobée que le pirate exploite.
- Registres d'entrée (lecture seule) : températures, humidités, pressions, vitesse, puissance.
- Valeurs stockées ×10 : 200 = 20,0 °C.

## 4. Le jumeau et son modèle

Le jumeau lit l'automate chaque seconde et **recalcule** la température et la pression attendues. Clé à retenir : il recopie les **ordres** (consignes, vitesse), pas les **mesures**. Il fait avancer sa physique et ne se recale sur le réel que si aucune alerte n'est active (sinon un attaquant pourrait le contaminer). Résultat : il fait confiance aux ordres, pas aux capteurs.

Simulation « et si ? » : le jumeau calcule en moins d'une seconde ce que deviendrait la salle (ex. ventilateur arrêté : surpression perdue en 20 s). Utile pour une cellule de crise.

## 5. Les couches de détection

Un seul détecteur ne suffit pas ; c'est le croisement qui démasque.

- **Couche réseau (sonde de la passerelle)** : qui parle, quoi, accès hors carte. Donne l'attribution (l'adresse du pirate).
- **Couche commande** : tout changement sans écriture légitime tracée = `commande_non_attribuee`.
- **Couche modèle** : écart mesure / modèle, capteur figé (variance nulle).
- **Couche métier** : consigne hors plage 18-26 °C, surpression < 10 Pa.
- **Couche IA** : écart statistique par rapport à la normalité apprise.

## 6. L'IA de détection

- Surveille **5 indicateurs** : écarts mesure/modèle des 2 températures, des 2 surpressions, et de la **puissance**.
- Apprentissage (2 min) : retient moyenne, dispersion et corrélations.
- Surveillance : calcule une **distance à la normalité** (distance de Mahalanobis), le *score*. Tient compte des corrélations, donc voit une valeur « dans les clous » qui casse une corrélation attendue.
- **Seuil** fixé automatiquement à partir des distances d'apprentissage. Quand elle alerte, elle nomme l'indicateur fautif.
- Différence avec une règle : la règle teste une variable contre un seuil fixe ; l'IA teste la cohérence d'ensemble contre un profil appris.

## 7. Les deux limites de l'IA (important)

- **Empoisonnement** : si l'attaque est active pendant l'apprentissage, l'IA l'apprend comme normale et devient aveugle. (Démontré avec A6 lancée pendant l'apprentissage.)
- **Parade** : charger un **modèle validé hors ligne** (conditions saines) au lieu d'apprendre en direct. Son seuil est plus serré.
- **Intégrité** : le modèle est **signé** (empreinte). Un fichier modifié est refusé au chargement. Protège contre la falsification du modèle.

## 8. Les trois barrières du durcissement

- **Barrière 1 — segmentation** : l'automate n'accepte que la passerelle. Attaque directe refusée au niveau réseau.
- **Barrière 2 — filtrage** : la passerelle bloque les écritures non autorisées (exception code 1).
- **Barrière 3 — sûreté locale** : l'automate refuse les valeurs dangereuses, même d'une source autorisée (exception code 3). Protège aussi des erreurs humaines.

Les barrières 1 et 2 arrêtent les intrus, la barrière 3 arrête les erreurs.

## 9. Mon détecteur (étape 14)

Cohérence **puissance / vitesse**. Relation physique : `puissance = 2,0 + 0,06 × vitesse` (kW). Si la puissance mesurée s'écarte de plus de 1 kW de l'attendu, l'une des deux valeurs est truquée → alerte. Attrape une attaque (puissance figée + ventilateur arrêté) qu'aucune règle d'origine ne voyait.

## 10. La phrase à retenir

**Le jumeau détecte, l'architecture protège.** La détection montre le problème ; seules la segmentation, le filtrage et la sûreté locale l'empêchent.
