🐍 Snake Game

Snake Game est une réinterprétation du célèbre jeu Snake développée en Python avec Pygame. Le projet conserve les mécaniques emblématiques du jeu original tout en les enrichissant avec des animations dynamiques, des effets visuels modernes et une interface utilisateur soignée.

<img width="600" height="458" alt="image" src="https://github.com/user-attachments/assets/5a072322-6671-4dc2-bf62-2ac8f7c4f500" />

📦 Installation
1. Cloner le dépôt
```
git clone https://github.com/DevMerline/SnakeGame.git
```

3. Installer les dépendances
```
pip install pygame
```
5. Lancer le jeu
```
python snake.py
```
🎯 Contrôles
Action	Touche
Haut	↑ ou W
Bas	↓ ou S
Gauche	← ou A
Droite	→ ou D
Rejouer	Espace

⚙️ Fonctionnement du jeu :

Le serpent est représenté par une liste de coordonnées :
```
self.body = [
    [x, y],
    [x - 1, y],
    [x - 2, y]
]
```
À chaque mise à jour :

Une nouvelle tête est ajoutée.
La queue est supprimée.
Lorsqu'un fruit est mangé, la suppression de la queue est ignorée pour faire grandir le serpent.
Détection des collisions

Le jeu vérifie :

Collision avec les murs
Collision avec le propre corps du serpent
```
if head in self.body[1:]:
    return True
Génération des fruits
```
Les fruits apparaissent aléatoirement dans la grille tout en évitant les positions occupées par le serpent.
```
while True:
    position = random_position()
    if position not in snake_body:
        break
```
Les effets visuels:

Fruits:
- Effet de pulsation via une fonction sinus
- Halo lumineux animé
  
Serpent:
- Dégradé de couleur de la tête vers la queue
- Animation ondulatoire légère
- Contours arrondis
- Particules

Lorsqu'un fruit est mangé :
```
for _ in range(15):
    self.particles.append(...)
```
Chaque particule possède :

- Une vitesse aléatoire
- Une durée de vie
- Une transparence décroissante
- Système de score
- +10 points par fruit collecté
- Conservation du meilleur score pendant la session
