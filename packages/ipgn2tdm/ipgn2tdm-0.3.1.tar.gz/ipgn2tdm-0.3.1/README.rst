ipgn2tdm
========

Tableau de marche depuis gpx iPhiGéNie

Description
-----------

Générer un tableau de marche à partir d'un fichier gpx avec des points
navigables créé avec iPhiGéNie.

Vous pouvez l' utiliser en ligne de commande ou avec l'interface graphique.

Deux fonctions existent :

- création d'un fichier gpx avec des "waypoint" à partir d'un fichier gpx avec des points
  navigables créé avec iPhiGéNie.
  Ce fichier généré est alors utilisable avec la très bonne application web https://istresrando.fr/gpxRando/
  pour générer une carte imprimable en A4.

- création d'un tableau de marche dans un document à la norme Office Open XML (docx) à partir d'un fichier gpx avec des points
  navigables créé avec iPhiGéNie.
  Les coordonnées UTM, azimuts, distances, dénivelés sont calculés automatiquement. Vous n'avez plus qu'à compéter les descriptions et finaliser la mise en forme.
  Un profil d'altitude sous forme de graphique peut compléter le document.

Depuis la version 0.3.0, vous pouvez aussi créer un tableau de marche depuis un fichier gpx avec des
"waypoints". La seule contrainte est que vos "waypoints" doivent être égaux en latitude, longitude
et élevation avec au moins un point de la trace pour être reconnus comme étape dans le tableau de marche.
 
Les versions sont disponibles sur la page : https://gitlab.com/pmakowski/ipgn2tdm/-/releases

Si vous avez Python (version 3.9 minimum) sur votre machine, vous pouvez l'installer avec `pip install ipgn2tdm`.
Vous aurez à votre disposition deux exécutables : `ipgn2tdm` la version en ligne de commande, et `ipgn2tdm_gui` la version avec interface graphique.

Sous Windows, si vous n'avez pas Python, téléchargez l'exécutable disponible sur la page https://gitlab.com/pmakowski/ipgn2tdm/-/releases


License
-------

BSD 3-Clause.

