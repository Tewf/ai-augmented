# AI-augmented

[![Vérifications contre reader-ergonomics](https://github.com/Tewf/ai-augmented/actions/workflows/checks.yml/badge.svg)](https://github.com/Tewf/ai-augmented/actions/workflows/checks.yml)
[![Site](https://github.com/Tewf/ai-augmented/actions/workflows/pages.yml/badge.svg)](https://tewf.github.io/ai-augmented/)

La page d'accueil d'une famille de dépôts sur le **travail augmenté par l'IA**. Une personne, un modèle de langue et
une machine partagent un projet, chacun avec un rôle. Chaque affirmation est vérifiée là où elle se tient. Cette page
tient la carte, les mots que les membres partagent et la règle qu'ils suivent, un dépôt par problème et aucun
recouvrement entre deux, et rien qu'un membre possède.

Cette page en anglais : [README.md](README.md). Les deux versions suivent le même état.

> **État (2026-11-02) :** mis en place ; les membres tiennent leur périmètre et rien de plus. Le premier travail est une
> revue de littérature sur le nom que le domaine donne à cette famille, non commencée ; le préfixe est provisoire
> jusque-là. Ce n'est ni une norme officielle, ni une étude relue par des pairs, ni un résultat nouveau.
>
> **Comment il est fait :** avec Claude, un assistant IA d'Anthropic, sous la direction du mainteneur, comme
> reader-ergonomics. Les corrections sont bienvenues sous forme d'issues.

## La carte

![Deux familles côte à côte : dans la famille reader-ergonomics, le topic et le projet ; dans la famille AI-augmented, le blueprint comme pont, le projet, l'IDE qui le met en œuvre, les agents et les cas qui l'utilisent et le mesurent, et les fondements qui lisent les cas. Le hub est au-dessus des deux et rien ne pointe vers lui.](map.svg)

<details>
<summary>Graphviz source</summary>

```dot
// The map of the two families. Colours: reader-ergonomics family blue, AI-augmented family green, the bridge orange,
// each kind named in its box; this page, the hub, has the thick border and nothing points to it.
digraph map {
  graph [rankdir=TB, nodesep=0.35, ranksep=0.45, bgcolor="white", pad=0.2, fontname="Inter", compound=true, newrank=true];
  node  [shape=box, style="rounded,filled", fontname="Inter", fontsize=13, margin="0.2,0.1", penwidth=1.5, fontcolor="#1F2328"];
  edge  [fontname="Inter", fontsize=11, color="#3D434B", fontcolor="#55575F", penwidth=1.3, arrowsize=0.8];
  HUB [label=<<b>ai-augmented</b><br/><font point-size="11" color="#55575F">the hub: map, words, rules</font>>, fillcolor="#E6F2EA", color="#2E7D4F", penwidth=2.6];
  subgraph cluster_re {
    label=<<b>reader-ergonomics family</b><br/><font point-size="11" color="#55575F">the person alone</font>>; labeljust=l; style="rounded"; color="#2F5DA8"; fontname="Inter"; fontsize=12;
    T [label=<<b>reader-ergonomics-topic</b><br/><font point-size="11" color="#55575F">one unit of writing, recursive</font>>, fillcolor="#E8EEF8", color="#2F5DA8"];
    P [label=<<b>reader-ergonomics-project</b><br/><font point-size="11" color="#55575F">one person, problem to result</font>>, fillcolor="#E8EEF8", color="#2F5DA8"];
  }
  subgraph cluster_ai {
    label=<<b>AI-augmented family</b><br/><font point-size="11" color="#55575F">person, model, machine</font>>; labeljust=l; style="rounded"; color="#2E7D4F"; fontname="Inter"; fontsize=12;
    BP [label=<<b>reader-ergonomics-blueprint</b><br/><font point-size="11" color="#55575F">the bridge: the topic with a checker</font><br/><font point-size="11" color="#55575F">per part and a model that guides</font>>, fillcolor="#FBEDE4", color="#B4541A"];
    AP [label=<<b>ai-augmented-project</b><br/><font point-size="11" color="#55575F">the project with the machine, the</font><br/><font point-size="11" color="#55575F">model and the person each set up</font>>, fillcolor="#E6F2EA", color="#2E7D4F"];
    IDE [label=<<b>ai-augmented-ide</b><br/><font point-size="11" color="#55575F">a tool inside the editor</font>>, fillcolor="#E6F2EA", color="#2E7D4F"];
    AG [label=<<b>ai-augmented-agents</b><br/><font point-size="11" color="#55575F">several agents on one project</font>>, fillcolor="#E6F2EA", color="#2E7D4F"];
    F [label=<<b>ai-augmented-foundations</b><br/><font point-size="11" color="#55575F">complete? does it converge?</font>>, fillcolor="#E6F2EA", color="#2E7D4F"];
    C [label=<<b>ai-augmented-cases</b><br/><font point-size="11" color="#55575F">real projects, measured</font>>, fillcolor="#E6F2EA", color="#2E7D4F"];
  }
  HUB -> T [style=invis];
  HUB -> BP [style=invis];
  T -> BP [label=" counterpart", style=dashed, constraint=false];
  P -> AP [label=" counterpart", style=dashed, constraint=false];
  T -> P [dir=back, label=" builds on"];
  BP -> AP [dir=back, label=" uses"];
  AP -> IDE [dir=back, label=" implements"];
  AP -> AG [dir=back, label=" uses"];
  AP -> C [dir=back, label=" measures"];
  C -> F [dir=back, label=" reads"];
  {rank=same; T; BP}
  {rank=same; P; AP}
}
```

</details>

| Membre | Problème | État |
|---|---|---|
| [reader-ergonomics-blueprint](https://github.com/Tewf/reader-ergonomics-blueprint) | le raisonnement d'une personne en arbre de topics, un vérificateur par partie, Lean d'abord, un modèle qui interprète et oriente | revue faite, référence B1 nommée, rien de construit |
| [ai-augmented-project](https://github.com/Tewf/ai-augmented-project) | comment une personne, un modèle et une machine sont mis en place et mènent un projet ensemble | périmètre seul |
| [ai-augmented-ide](https://github.com/Tewf/ai-augmented-ide) | le logiciel qui met cette méthode en œuvre dans l'éditeur | périmètre seul |
| [ai-augmented-agents](https://github.com/Tewf/ai-augmented-agents) | plusieurs agents, personnes et modèles, sur un projet : délégation, coordination, incitations | périmètre seul |
| [ai-augmented-foundations](https://github.com/Tewf/ai-augmented-foundations) | si le topic récursif encode tout problème à un coût cognitif supportable, et à quelle vitesse un projet converge, vers quoi | périmètre seul |
| [ai-augmented-cases](https://github.com/Tewf/ai-augmented-cases) | ce que chaque projet réel mené avec la méthode a coûté et produit | périmètre seul |

Le pont est partagé avec la [famille reader-ergonomics](https://github.com/Tewf/reader-ergonomics/blob/b9732b9814c71768f722691f3c5049ec2b8ed378/extending.md) : le blueprint y reste membre, et
chaque membre ici obéit à [reader-ergonomics](https://github.com/Tewf/reader-ergonomics/blob/b9732b9814c71768f722691f3c5049ec2b8ed378/standard.md) (v1.19.2) et exécute ses vérifications en CI.

## Les règles

- **Un dépôt par problème.** Un membre répond à une question ; une seconde question est un second dépôt.
- **Aucun recouvrement.** Un fait vit dans un membre ; les autres le lient. Deux membres qui revendiquent la même chose
  dans leur table de périmètre sont un constat, et le premier travail ci-dessous le fait trouver par un programme.
- **Les dépendances pointent vers le bas.** Un membre utilise ce qui est sous lui et rien au-dessus ; cette page lie
  chaque membre et rien ne lie cette page.
- **Les noms sont provisoires jusqu'au cadrage.** La première étape de chaque revue trouve comment le domaine nomme la
  chose ; le dépôt est renommé alors, et GitHub redirige l'ancienne adresse.
- **Un modèle ne décide rien.** Sa sortie est vérifiée par un programme ou lue par la personne ; la position du
  blueprint vaut pour toute la famille.

## Les mots

| Mot | Sens ici |
|---|---|
| **personne** | qui possède le projet et décide de ce qui est affirmé |
| **modèle** | un modèle de langue : il explique, propose, traduit, rédige ; il ne décide rien |
| **machine** | les programmes qui vérifient : tests, hooks, CI, un assistant de preuve |
| **vérificateur** | un programme qui rend un verdict sur une partie, là où elle se tient |
| **oracle** | le vérificateur dont le verdict est tenu pour exact |
| **brief** | ce qu'un agent remet à un autre : la tâche, ce qui est décidé, ce qui est à trouver |
| **référence** | le résultat existant auquel un nouveau est comparé ; une revue finit quand elle peut en nommer un |

## Le premier travail : une revue de littérature

Non commencée. Elle est finie quand elle peut nommer la référence.

1. **Cadrer :** comment le domaine nomme une personne, un modèle et une machine qui mènent un projet. Pistes à vérifier,
   non des noms à affirmer : intelligence augmentation, hybrid intelligence, human-AI teaming, human-in-the-loop. Le
   préfixe de la famille en découle.
2. **Revue :** les synthèses d'abord, puis les travaux fondateurs, puis qui les cite.
3. **État de l'art, et le dossier contre.**
4. **Positionnement :** à quel domaine cette famille appartient, et ce qu'elle ajoute.
5. **Référence :** le vocabulaire et la carte qu'un domaine existant donne déjà, contre ceux ci-dessus.

À côté, la vérification propre à la famille : un programme qui lit la table de périmètre de chaque membre et échoue
quand deux membres revendiquent le même « dedans ». Savoir si une table de périmètre se lit assez sûrement pour une
vérification exacte est la question qu'il doit trancher.

## Vérifier

```sh
git clone https://github.com/Tewf/reader-ergonomics
python3 reader-ergonomics/checks/run.py chemin/vers/ce/depot
```

La CI exécute les mêmes vérifications à chaque push, et une exécution échoue à la première erreur
([checks.yml](https://github.com/Tewf/ai-augmented/blob/master/.github/workflows/checks.yml)). Chaque push sur master
construit aussi le site, [tewf.github.io/ai-augmented](https://tewf.github.io/ai-augmented/)
([pages.yml](https://github.com/Tewf/ai-augmented/blob/master/.github/workflows/pages.yml)).

## Contenu

| Partie | Résumé |
|---|---|
| [decisions](decisions/) | une fiche par choix qui façonne ce dépôt, chacune ouvrant sur la décision en une phrase |

## Licence

Code sous [Apache License 2.0](LICENSE) ; prose sous [CC BY 4.0](LICENSES/CC-BY-4.0.txt). Réutilisez-le comme vous le
souhaitez, en créditant ce dépôt ; [CITATION.cff](CITATION.cff) donne une citation si besoin.
