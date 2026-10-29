# Agent Skills

[English](README.en.md) · [中文](README.zh.md) · [हिन्दी](README.hi.md) · [Español](README.es.md) · [العربية](README.ar.md) · [Français](README.fr.md) · [Português](README.pt.md) · [Русский](README.ru.md) · [বাংলা](README.bn.md) · [Deutsch](README.de.md)

Des compétences pratiques pour les agents d’IA : instructions, scripts, modèles et vérifications réutilisables dans différents projets.

[Contribuer](../CONTRIBUTING.md) · [Licence MIT](../LICENSE)

## Catalogue

| Compétence | Fonction | Langue et prérequis |
|---|---|---|
| [build-agent-context](../skills/build-agent-context/) | Transforme archives, documents, échanges, liens et dépôts en contexte de travail avec traçabilité des sources, parcours de lecture, état et contrôles de transmission | Langue de l’utilisateur ; Markdown ; outils de lecture selon les formats |
| [gost-7-32-2017-latex](../skills/gost-7-32-2017-latex/) | Prépare et révise des rapports de recherche en LaTeX selon GOST 7.32-2017 : couverture, structure, équations, tableaux, références, annexes et contrôles PDF | Russe ; Python 3.10+ et XeLaTeX ou LuaLaTeX ; `pdfplumber` facultatif |

Chaque compétence possède un dossier avec un point d’entrée `SKILL.md`, ses scripts et ses ressources.

## Installation dans Codex

Demandez à Codex :

```text
Utilise $skill-installer pour installer https://github.com/Girday/agent-skills/tree/main/skills/gost-7-32-2017-latex
```

Ou clonez le dépôt et installez une copie locale :

```bash
git clone https://github.com/Girday/agent-skills.git
cd agent-skills
python3 scripts/install.py gost-7-32-2017-latex
```

L’installateur utilise `$CODEX_HOME/skills`, ou `~/.codex/skills` si `CODEX_HOME` n’est pas défini. Il refuse d’écraser une installation existante. La copie installée est indépendante du dépôt et ne se met pas à jour automatiquement. Si la compétence n’apparaît pas, redémarrez Codex. La [documentation officielle](https://learn.chatgpt.com/docs/build-skills) explique la découverte et la distribution des compétences. Ce dépôt fournit leurs sources ; ce n’est pas une fiche publiée dans le répertoire des plugins.

Les autres agents peuvent utiliser ces ressources s’ils prennent en charge `SKILL.md`. Les outils de bureau propres à Codex sont facultatifs ; une procédure en ligne de commande est également fournie.

## Préparer le contexte d’un agent

Installez `build-agent-context` avec le même installateur en indiquant son nom ou son dossier GitHub, puis demandez :

```text
Utilise $build-agent-context. Prépare un contexte à partir de cette archive pour
qu’un autre agent poursuive le projet. Inclus les exigences actuelles, les sources,
les conflits non résolus et un message de départ. L’agent pourra lire des fichiers.
```

La compétence choisit entre un document autonome et un point d’entrée court accompagné de fichiers thématiques. Elle consigne les éléments réellement lus, conserve les repères des sources et distingue exigences, faits vérifiés, hypothèses et avancement. Elle permet aussi de mettre à jour un contexte existant. Aucune dépendance d’exécution n’est obligatoire ; les archives, scans et autres formats nécessitent des outils adaptés.

Fondements (12 publications sélectionnées), exemples de résultats, critères de qualité, scénarios d’évaluation et limites de validation :

- [research.md](../skills/build-agent-context/references/research.md)
- [output-patterns.md](../skills/build-agent-context/references/output-patterns.md)
- [quality-checks.md](../skills/build-agent-context/references/quality-checks.md)
- [validation.md](../skills/build-agent-context/references/validation.md)

## Utiliser la compétence GOST

```text
Utilise $gost-7-32-2017-latex. Prépare un rapport à partir des documents joints,
compile le PDF et vérifie la mise en page. Les exigences de l’établissement sont jointes séparément.
```

Depuis la racine du dépôt :

```bash
python3 skills/gost-7-32-2017-latex/scripts/init_project.py ./my-report
python3 skills/gost-7-32-2017-latex/scripts/build.py ./my-report
python3 skills/gost-7-32-2017-latex/scripts/audit.py ./my-report
```

Après `init_project.py`, remplissez `my-report/metadata.tex` et remplacez le contenu de démonstration avant la compilation. Les champs vides sont intentionnels : l’audit doit échouer tant qu’ils ne sont pas remplis. Installez `pdfplumber` pour vérifier la géométrie du PDF ; sans lui, ces contrôles portent la mention `NOT_CHECKED`.

Exemple de huit pages, correspondance des exigences et comportement vérifié avec ses limites :

- [example.pdf](../examples/gost-7-32-2017/example.pdf)
- [requirements.md](../skills/gost-7-32-2017-latex/references/requirements.md)
- [validation.md](../skills/gost-7-32-2017-latex/references/validation.md)

GOST 7.32-2017 concerne les rapports de recherche. Son application aux travaux universitaires doit tenir compte des règles de l’établissement. La compétence distingue obligations, recommandations, variantes autorisées et choix du modèle. Les contrôles automatiques facilitent la révision, mais ne certifient pas le rapport et ne confirment ni signatures, ni enregistrement, ni approbation institutionnelle. Les formats A3 et les rapports en plusieurs volumes sont documentés, mais n’ont pas été testés séparément lors de la validation initiale.

## Développement

Créez puis activez l’environnement virtuel avec la commande adaptée à votre shell avant d’installer les dépendances et de lancer les vérifications :

```bash
python3 -m venv .venv
python -m pip install -r requirements-dev.txt
python scripts/validate.py
python -m unittest discover -s tests -v
ruff check .
ruff format --check .
```

Le test d’intégration LaTeX s’exécute si XeLaTeX est disponible ; sinon il est ignoré. GitHub Actions valide les sources et les tests Python ; il ne produit pas le rendu des rapports et ne les certifie pas.

## Licence et sources

Les instructions, analyses, codes et modèles originaux sont sous [licence MIT](../LICENSE). Les normes, documentations et polices citées conservent leurs droits respectifs. Le texte officiel GOST et les polices propriétaires ne sont ni inclus ni redistribués sous une autre licence. Les liens et l’édition examinée figurent dans [sources.md](../skills/gost-7-32-2017-latex/references/sources.md).
