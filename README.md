# CyberTwin · jumeau numérique de cybersécurité (OT / Modbus)

Projet de travaux pratiques du Master 2 Cybersécurité (module Technologies avancées, jumeau numérique).

Ce lab construit, puis attaque, le **jumeau numérique** de la centrale de traitement d'air (CTA) qui ventile deux salles d'opération d'un établissement hospitalier fictif. L'automate simulé parle le vrai protocole industriel **Modbus TCP**. Le jumeau lit l'automate chaque seconde, recalcule avec son propre modèle ce que les salles devraient faire, compare les deux et alerte en cas d'écart. On y ajoute une détection par IA, puis on durcit l'architecture jusqu'à bloquer les attaques.

> Le code du kit pédagogique n'est pas publié ici (matériel de cours protégé). Ce dépôt contient mon compte rendu, ma fiche de révision et le détecteur que j'ai écrit.

## Contenu du dépôt

- `docs/Compte_rendu_TP_jumeau_numerique.pdf` : compte rendu complet, les 15 étapes avec captures et analyse.
- `FICHE-REVISION.md` : l'essentiel à retenir, pour réviser vite.
- `detecteur_puissance_vitesse.py` : le détecteur de cohérence puissance / vitesse que j'ai ajouté au jumeau (étape 14).

## Ce que le lab démontre

1. **Un capteur peut mentir, pas la physique.** Le jumeau ne fait pas confiance aux mesures : il les confronte à un modèle physique et au trafic réseau. Quand un attaquant fige ou décale un capteur, l'écran reste normal mais le jumeau voit la dérive.
2. **L'IA complète les règles, mais a ses limites.** Une détection apprise repère les attaques trop discrètes pour les règles fixes. En revanche elle est vulnérable à l'empoisonnement de son apprentissage, d'où l'intérêt d'un modèle validé hors ligne et signé.
3. **Détecter ne suffit pas, il faut protéger.** Tant qu'une attaque réussit, le danger demeure. La segmentation, le filtrage applicatif et la sûreté locale transforment la détection en protection, et couvrent même l'erreur humaine.

## Les attaques jouées

| Code | Attaque | Ce qu'elle exploite |
|---|---|---|
| A1 | Reconnaissance | Balayage de tous les registres, découverte du registre caché 100 |
| A2 | Sabotage de consigne | Écriture Modbus sans authentification (consigne à 30 °C) |
| A3 | Arrêt du ventilateur | Écriture de bobine, perte de la surpression du bloc |
| A4 | Capteur figé | Registre caché 100, l'écran ment pendant que la salle chauffe |
| A6 | Décalage discret | Décalage de 0,6 °C sous le seuil des règles, visible par l'IA seule |

## Les trois architectures

| | Réseau plat | Observé | Durci |
|---|---|---|---|
| Protection | aucune | passerelle transparente | segmentation + filtrage + sûreté locale |
| Attaques | réussissent, auteur inconnu | réussissent, mais attribuées | bloquées |
| Rôle du jumeau | voit les effets | voit et attribue | la protection vient de l'architecture |

## Stack technique

Python 3 (bibliothèque standard uniquement), Modbus TCP, SQLite, tableau de bord HTML, Wireshark / tshark pour l'observation du trafic. Réalisé sous Kali Linux (VMware).
