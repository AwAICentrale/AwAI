# Contribuer

Note: ce document se veut être un guide de mise en place du projet, un memo pour le processus de contribution et un endroit où se réferer pour les problèmes courants avec git.
En tant qu'introduction à l'usage général de git, il n'est pas suffisant.  

Si vous rencontrez une erreur lors d'une procédure, référez-vous à la section "Problèmes & Solutions".
Si ça ne résoud pas votre problème, consultez votre guru git/Unity local, puis ajoutez ce qu'il manquait à la section.

## Prérequis

Les logiciels suivants doivent être installés sur votre ordinateur:
* python3
Je vous conseille [PyCharm](https://www.jetbrains.com/pycharm/), [Spyder](https://pypi.org/project/spyder/) ou [Visual Studio](https://code.visualstudio.com/) comme IDE
* git:
  * Sous windows, installez [git for windows](https://gitforwindows.org/)
  * Sous macOS, git est déjà installé, il n'y a rien à faire
  * Sous linux, installez le paquet `git` pour votre distribution

## Mise en place de l'environnement de développement

### 1. Ouvrez un terminal dans lequel vous avez accès à git:

* Sous windows, lancez Git for windows (bash)
* Sous macOS et linux, ouvrez l'application Terminal, ou un terminal quelconque

Prenez note du dossier dans lequel le terminal s'est ouvert, dont le nom s'affiche avant le curseur clignotant.

### 2. Clonez le dépôt

Dans le terminal, écrivez la commande suivante et appuyez sur "Entrée":  

```
git clone https://github.com/AwAICentrale/AwAI.git
```

Votre identifiant et mot de passe de GitHub vous seront demandés. Sous windows, si vous vous trompez la première fois, vous aurez probablement une erreur en réessayant. Référez vous à la section "Problèmes & Solutions" plus bas.


## Contribuer une fonctionnalité

### 1. Vérifiez que votre version du projet est à jour

Régulièrement, il faudra que vous synchronisiez votre version locale du projet avec la version disponible sur GitHub. C'est ce que vous pouvez faire avec la commande  

```
git pull
```

Git récupère alors les derniers changements et les applique à vos fichiers locaux, sur les branches correspondantes.

### 2. Programmez la fonctionnalité

Rien de spécial ici, faites ce qu'il faut sur Python

### 3. Créez une nouvelle branche, placez-vous y

Ouvrez un terminal avec git, et placez vous dans le dossier du projet (`cd AwAI`, par exemple).  
La commande suivante crée la branche nommée `changez_ce_nom` et vous y place  

```
git checkout -b changez\_ce\_nom
```

Il n'y a pas de convention de nommage pour les branches, et ça n'a pas d'importance.

### 4. Dites à git ce que vous souhaitez partager sur ce dépôt

Pour chaque fichier `fichier_i` que vous avez modifié ou crée, entrez la commande  

```
git add fichier\_i  
```

On dit que ces fichiers sont maintenant "dans l'index".  
Note: `git status` peut vous être utile pour savoir quels fichiers ont été modifiés, crées, ou ont déjà été ajoutés à l'index.

### 5. Décrivez ces changements dans un commit

Entrez la commande  

```
git commit  
```

Git vous présente alors un éditeur de texte, dans lequel vous pouvez écrire une description de ce que vos changements font. Le but est de transmettre le "pourquoi?" plus que le "comment?", mais vous êtes libres de mettre ce que vous voulez. Une fois terminé, enregistrez et fermez l'éditeur.  
Par défaut sous windows, l'éditeur est vim. Vous avez 2 options: persévérer, ou abandonner et changer d'éditeur puis relancer la commande précédente.  
Note: le format de message de commit a respecter est le suivant:

>>>
ligne de titre: 80 caractères max

corps de la description (notez la ligne vide entre les deux)  
qui peut prendre autant des lignes que vous voulez.
>>>

### 6. Envoyez le commit sur GitLab

Avec la simple commande  
```
git push origin nom\_de\_branche
```

### 7. Ouvrez une merge request sur GitLab

Dans l'interface de GitHub, allez dans "Repository > Branches", et sur la ligne de votre branche, cliquez sur "Merge request". Remplissez le titre, la description, puis cliquez sur "Submit merge request".  
C'est terminé!

## Problèmes & Solutions

### "fatal: ni ceci ni aucun de ses répertoires parents n'est un dépôt git"

Vous êtes dans un terminal, et git est bien installé, mais vous n'êtes pas dans le répertoire du projet.  

Sous windows, le plus simple est de faire clic droit sur le dossier où vous avez cloné le projet, et de sélectionner l'option "Git for windows" pour y ouvrir un terminal.  
Sinon, vous pouvez changer de dossier dans le terminal pour vous y rendre avec la commande `cd`: par exemple `cd Documents/Projets/AwAI`, et d'une manière générale, `cd un/chemin/quelconque`.

### git push/pull vous dit que vous n'avez pas accès au dépôt, ou que vos identifiants sont incorrects

Si git vous donne cette erreur avant même de vous demander vos identifiants, c'est parce que vous vous êtes trompé de login/mot de passe la première fois et
que git a enregistré les mauvais identifiants. Ce problème ce résoud par la commande:

```
git config --system --unset credential.helper
```

Vous aurez maintenant à rentrer votre mot de passe à chaque fois que vous interagirez avec GitHub... Sous windows, la commande suivante a de bonne chances de résoudre le problème:

```
git config --global credential.helper manager
```

### Vous avez ouvert une merge request, mais il y a un conflit avec master

Il va falloir appliquer vos changements par dessus les nouveaux commits de master, ce qui implique de modifier la succession des commits sur votre branche locale tout en résolvant les conflits. C'est ce que fait la commande `rebase` de git. Voici comment l'utiliser.  

Placez-vous sur master avec `git checkout master`, mettez cette branche à jour avec `git pull origin master`, remettez-vous sur votre branche, et entrez `git rebase master`.  

Si git vous indique que tout va bien, il vous suffit de lancer `git push origin nom_de_branche --force` pour mettre à jour la merge request.  
Si git vous indique qu'il y a des conflits à résoudre manuellement, il va falloir le faire, et git vous a indiqué précisément la procédure. Éditez tous les fichiers en question, de sorte à ce qu'ils aient le contenu que vous souhaitez (il faudra entre autres enlever toute trace de <<<<<<<<<< et autres >>>>>>>>>>), puis suivez ajoutez les à l'index, et entrez `git rebase --continue`. Vous pouvez ensuite mettre à jour la merge request par `git push origin nom_de_branche --force`.

### Vous voulez modifier votre dernier commit après l'avoir fait

D'abord, vous avez toujours l'option de faire un second commit qui corrige le premier. Mais dans certains cas, ou juste pour des raisons de propreté,
modifier le commit est la bonne solution.  

Il suffit pour ça que vous fassiez vos changements dans le code (ou rien du tout si vous voulez juste changer le message de commit),
puis que vous fassiez `git add` pour chacun des fichiers modifiés, puis finalement

```
git commit --amend
```

qui vous présentera à nouveau l'éditeur de texte, avec le message de votre dernier commit, que vous pouvez changer. Le cas échéant, vous pouvez mettre à jour votre merge request avec

```
git push origin nom\_de\_branche --force
```

### Git vous empêche de changer de branche parce que vous avez des changements non validés

C'est simplement pour vous empêcher d'écraser vos changements par erreur. Si ceux-ci n'ont pas d'importance, vous pouvez dire à git de les oublier, de revenir à l'état par défaut de la branche où vous êtes actuellement:

```
git reset --hard nom\_de\_branche
```

après quoi vous pouvez `checkout` ce que vous voulez.  
Si vous tenez à sauvegarder vos changements, vous pouvez le faire à l'aide de `git stash push`, puis les restaurer avec `git stash pop`.
