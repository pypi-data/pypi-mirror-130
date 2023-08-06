# Tests de charge

Pour vérifier le bon fonctionnement de l'API avec plusieurs utilisateurs des tests de charge ont été mis en place, à l'aide de [Locust](https://locust.io/), un outil de test de charge.

Lancement :
```
poetry run locust -f tests/load_testing/load_testing.py
```

Puis se rendre à l'adresse http://0.0.0.0:8089 pour lancer un test avec le nombre d'utilisateurs souhaités.

## Tests sur les entrées qui ne font pas de calculs

Sur / et /status qui n'ont pas de calculs, à 130 requêtes par seconde :
- Les temps de réponse sont très bas : 10 ms
- La mémoire sur le serveur ne dépassent pas 2Go
- Les coeurs sur le serveur ne dépassent pas 7%

## Sur un calcul de CSG - Sans quantile

Paramètres :
- `wait_time = between(1, 5)`
- 4 worker Gunicorn
- 4 Go de RAM, 0 de swap
- Utilisation du cache limité : on le vide au début de chaque session utilisateur.
- 70 % des appels sur /state_simulation

Avec seulement 1 utilisateur actif on a rapidement un plantage faute de mémoire.

Même en activant le Memory Config d'OpenFisca, ça ne résoud pas le problème, et en plus, cela rempli le disque de fichiers temporaires.

Le taux d'erreur pour 1 utilisateur atteind 60%.

En passant à 8Go de RAM, avec 1 utilisateur on reste à 0% d'erreur et OpenFisca arrive à libérer les fichiers temporaires.

Mais à 2 utilisateurs, on atteind 42% d'erreurs.

En baissant à 2 worker Gunicorn, toujours à 2 utilisateurs, on retrouve un fonctionnement stable (A confirmer sur plus de temps).


### Tentative de ne plus conserver le résultat de create_simulation pour d'autres calculs

L'excécution du notebook prend 1min30s au lieu de 1min00, mais cela améliore-t-il la gestion mémoire ?

Avec 1 utilisateur, la mémoire est utilisée entièrement 6.8/7.9Go mais 100 simulations d'affilées ne génèrent aucun plantage, avec un temps de traitement moyen de 4 secondes.

Avec 2 utilisateurs, la mémoire est utilisée entièrement de la même façon 6.8/7.9Go, sur 200 simulations en 15 minutes, 2 sont en erreur (502). Le temps de traitement moyen est de 4.5s. 90% des simulations sont faites en moins de 6.2s.

### On remet la conservation des résultats de create_simulation pour d'autres calculs

Le temps d'éxécution du Notebook redescend à 1 minute.

Avec 2 utilisateurs, la mémoire est utilisée entièrement de la même façon 6.7/7.9Go, sur 200 simulations en 15 minutes, 8 sont en erreur (502). Le temps de traitement moyen est de 4.6s. 90% des simulations sont faites en moins de 6.6s.

=> On plante plus souvent et les temps de traitement sont moins bon, on ne va pas garder cette version pour la production, uniquement pour les notebooks.


## Avec calcul des quantiles

Paramètres :
- `wait_time = between(1, 5)`
- 1 worker Gunicorn
- 8 Go de RAM, 0 de swap
- Même appel API que le front : "assiette_csg_abattue", "csg_imposable_salaire", "csg_deductible_salaire"
- 1 utilisateur


Pas d'erreur, sur plus de 70 appels, mais le temps de calcul est long : 11 secondes de moyenne, 90% en dessous de 10 secondes. Mémoire utilisée : 7.19/7.9Go.

#### En supprimant le .copy() du calcul des quantiles

Pas d'erreur, sur plus de 170 appels, le temps de calcul est légèrement réduit : 10,1 secondes de moyenne, 90% en dessous de 10 secondes. Mémoire utilisée : 7.19/7.9Go.

#### En réduisant à 4 Go de RAM

On ne peut pas se permettre de mobiliser 8Go pour l'intégration, il faut la laisser à 4Go max de toute façon.
Mais à 4 appels, on en a déjà 2 en erreurs.
Le taux d'erreurs après 30 appels approche les 40%. 90% des requêtes sont en dessous de 13 secondes.

#### En utilisant max-requests

Le paramètre `max-requests` permet de redémarrer le worker après un certain nombre de requête. La doc indique que c'est pratique pour les memory leaks (https://docs.gunicorn.org/en/stable/settings.html?highlight=max-requests#max-requests)

Avec `-w 1 --max-requests=1`

Avec un redemarrage apres chaque requete on n'a plus d'erreurs avec seulement 4 Go de RAM, on pourrait meme se limiter a 3 Go.
Mais les temps de reponses passent a 15 secondes de moyenne.

Avec `-w 2 --max-requests=1` ce n'est pas mieux.

Avec `-w 1 --max-requests=2` ce n'est pas mieux, 16s de moyenne. 90% en dessous de 18 s. Pour 68 requêtes sans erreur.

Avec `-w 1 --max-requests=10` on retrouve un fort taux de plantage (30%) et un temps de traitement moyen de 13s avec 4Go.

##### On repasse à 8Go

Avec `-w 1 --max-requests=10` et 1 utilisateur en permanence. La mémoire ne dépasse pas 4.8Go. Sur 69 requêtes, 12s de moyenne, 90% sous 14s. 0 plantage.

Avec `-w 1 --max-requests=10` et 2 utilisateurs en permanence. 90 requêtes sans erreurs. Mais 20s de moyenne, 90% en dessous de 26s.

Avec `-w 2 --max-requests=10` et 2 utilisateurs en permanence. Sur 95 requêtes, 13 sont en erreur. 17s de moyenne, 90% sous 24 secondes. On répond donc un peu plus vite mais avec plus de plantage.

Avec `-w 2 --max-requests=5` et 2 utilisateurs en permanence. 195 - 12 erreurs (4%). 18s de moyenne, 90% sous 24 secondes.

Avec `-w 2 --max-requests=5` et 1 utilisateurs en permanence. 90% sous 12s, 11s de moyenne. On garde pour la production.
## Comment interpréter ces résultats ?

Plus on augmente le nombre de worker et le max-request, plus on répond rapidement mais plus on augmente le risque de plantage faute de mémoire.
`-w 2 --max-requests=5` Semble un bon compromis pour la production et `-w 1 --max-requests=2` pour l'intégration.

Comme on peut fonctionner pendant longtemps sans plantage en limitant l'usage ça ne semble pas une fuite mémoire.
Mais pourquoi consomme-t-on autant de mémoire alors que la mémoire consommée (RSS) par le Notebook complet n'est que de 3.5Mo ?