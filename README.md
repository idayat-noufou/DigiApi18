## TP 3

> **Projet support** : API FastAPI (Python)
> *(voir app.py)*

---

## TP 3.1 — Analyse détaillée de la dette technique

### 3.1.1 Exécuter flake8, radon et pylint sur le projet

#### Installation des outils

```bash
pip install flake8 pylint radon
```

#### Commandes exécutées

```bash
flake8 app.py
radon cc app.py -a
pylint app.py
```

Les sorties complètes ont été sauvegardées dans les fichiers suivants :

* `flake8.txt`
* `radon.txt`
* `pylint.txt`


### 3.1.2 Noter les erreurs, warnings et valeurs de complexité

#### Résultats flake8

Principaux problèmes détectés :

* Lignes trop longues (> 79 caractères)
* Espaces et lignes vides manquantes (PEP8)
* Imports non placés en début de fichier
* Utilisation inutile de f-strings

Ces erreurs impactent principalement la **lisibilité** du code.

---

#### Résultats radon

* Complexité cyclomatique moyenne : **A**
* Aucune fonction ou méthode à forte complexité
* Code globalement simple et maintenable d’un point de vue algorithmique

---

#### Résultats pylint

* Note globale : **7.23 / 10**
* Problèmes récurrents :

  * Absence de docstrings (modules, classes, fonctions)
  * Imports mal organisés
  * Utilisation du nom réservé `id`
  * Imports placés hors top-level dans les tests

---

### 3.1.3 Compléter le tableau KPI de la dette technique

| Endpoint | Complexité cyclomatique | Code smells (pylint) | Duplication / longueur | Actions / Priorité |
|----------|-------------------------|----------------------|------------------------|--------------------|
| GET / | A (faible) | Absence de docstring | Fonction très courte | Ajouter docstring — Priorité faible |
| GET /api/v1/client | A (faible) | Absence de docstring | Pas de duplication | Ajouter docstring endpoint — Priorité moyenne |
| POST /api/v1/client | A (faible) | Absence de docstring | Pas de duplication | Ajouter docstring endpoint — Priorité moyenne |
| GET /api/v1/client/{id} | A (faible) | Utilisation du nom réservé `id`, absence de docstring | Fonction courte | Renommer `id`, ajouter docstring — Priorité moyenne |
| PATCH /api/v1/client/{id} + DELETE /api/v1/client/{id} | A (faible) | Absence de docstrings | Logique simple, pas de duplication | Ajouter docstrings — Priorité faible |


### 3.1.4 Prompt IA pour l’analyse et le plan de refactoring

Prompt utilisé :

> Voici les résultats de flake8, pylint et radon pour mon projet FastAPI.
> 
> Le projet contient les endpoints suivants :
> - GET /
> - GET /api/v1/client
> - POST /api/v1/client
> - GET /api/v1/client/{id}
> - PATCH et DELETE /api/v1/client/{id}
> 
> Analyse ces résultats et indique :
> - les problèmes les plus importants à corriger en priorité
> - les endpoints ou fonctions qui posent des problèmes de lisibilité ou de maintenance
> - les principaux code smells détectés (docstrings manquantes, nommage, imports, etc.)
> 
> Propose ensuite un plan d’actions simple et priorisé (priorité haute, moyenne, faible)
> pour réduire la dette technique, sans refonte complète du projet.


---

### 3.1.5 Classement des actions par priorité (réponse de l'IA)


#### Priorité haute

- Aucune action critique nécessaire
- Le code est stable et peu complexe.

#### Priorité moyenne

- Ajouter des docstrings aux endpoints /api/v1/client et /api/v1/client/{id}
- Renommer le paramètre id en client_id pour éviter les conflits
- Clarifier le rôle des endpoints via une documentation minimale

#### Priorité faible

- Réorganiser les imports selon les conventions Python
- Corriger les problèmes de style PEP8 signalés par flake8
- Ajouter des docstrings au endpoint racine /


## TP 3.2 — Tests de performance

### 3.2.1. Choix de l’outil de test

Pour les tests de performance, l’outil **k6** a été choisi.

### 3.2.2. Préparation des tests

Les tests sont regroupés dans le fichier `app.test.py` .

Ce fichier contient des tests minimaux pour les endpoints suivants :
- GET /
- GET /api/v1/client
- POST /api/v1/client
- GET /api/v1/client/{id}
- PATCH /api/v1/client/{id}
- DELETE /api/v1/client/{id}

### 3.2.3. Exécution des tests de charge

Les tests de charge ont été réalisés avec **k6** à l’aide du fichier `k6.test.js`,
qui contient le scénario de test.

Les endpoints testés sont :
- GET /
- GET /api/v1/client
- POST /api/v1/client

Les endpoints suivants n’ont pas été inclus dans le test de charge :
- GET /api/v1/client/{id}
- PATCH /api/v1/client/{id}
- DELETE /api/v1/client/{id}

Ces endpoints ont été ignorés afin d’éviter des dépendances entre requêtes et de
conserver un scénario de test simple et reproductible.

### 3.2.4. Collecte des métriques

Les métriques de performance ont été sauvegardées dans le fichier séparé
`k6_results.txt` à partir de la sortie du test k6.

### 3.2.5. Analyse des résultats des tests de performance

Les résultats du test de charge montrent que l’API commence à rencontrer des
limitations lorsque la charge atteint des valeurs élevées (jusqu’à 100 utilisateurs
simultanés).

Des temps de réponse très élevés ont été observés, avec un temps de réponse maximal
pouvant atteindre 60 secondes, ainsi que des timeouts sur les endpoints
`GET /api/v1/client` et `POST /api/v1/client`.

Ces comportements indiquent un goulet d’étranglement côté serveur, probablement
lié à la gestion de la concurrence et aux accès à la base de données.

Pour une API simple, une latence moyenne autour de 1 seconde reste acceptable,
mais un temps de réponse maximal aussi élevé n’est pas acceptable en conditions
réelles. Le taux d’erreur observé (environ 1,3 %) reste modéré mais doit être surveillé.

Des seuils critiques peuvent être définis comme suit :
- latence moyenne supérieure à 1 seconde
- p95 supérieur à 3 secondes
- temps de réponse maximal supérieur à 5 secondes
- taux d’erreur supérieur à 1 %
- charge supérieure à 50 utilisateurs simultanés

Au-delà de ces seuils, les performances de l’API se dégradent de manière significative.

### 3.2.6. Documentation des KPI de performance

Les niveaux de charge considérés sont :
- charge faible : ~10 utilisateurs
- charge moyenne : ~50 utilisateurs
- charge élevée : ~100 utilisateurs

| Endpoint | Niveau de charge | Latence moyenne | Temps max | Taux d’erreur | Throughput |
|---------|------------------|-----------------|-----------|---------------|------------|
| GET / | Faible | Faible | Faible | 0 % | Stable |
| GET / | Moyenne | Faible | Faible | 0 % | Stable |
| GET / | Élevée | Modérée | Modérée | < 1 % | Stable |
| GET /api/v1/client | Faible | Faible | Faible | 0 % | Stable |
| GET /api/v1/client | Moyenne | Modérée | Modérée | < 1 % | Stable |
| GET /api/v1/client | Élevée | Élevée | Très élevée (timeouts) | ~1,4 % | Dégradé |
| POST /api/v1/client | Faible | Faible | Faible | 0 % | Stable |
| POST /api/v1/client | Moyenne | Modérée | Modérée | < 1 % | Stable |
| POST /api/v1/client | Élevée | Élevée | Très élevée (timeouts) | ~1,4 % | Dégradé |
