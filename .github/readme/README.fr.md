# Project Advisor

[English](../../README.md) · [简体中文](README.zh-CN.md) · [Español](README.es.md) · [Português (Brasil)](README.pt-BR.md) · [日本語](README.ja.md) · [Tiếng Việt](README.vi.md) · [한국어](README.ko.md) · [فارسی](README.fa.md) · [ภาษาไทย](README.th.md) · [العربية](README.ar.md) · **Français** · [Bahasa Indonesia](README.id.md)

Une skill indépendante de la plateforme pour orienter les projets avec esprit critique, préparer des consignes ciblées pour un agent de réalisation et évaluer les résultats à partir de preuves.

Utilisez une conversation pour décider du prochain travail utile et un autre agent pour examiner, réaliser et vérifier. Le conseiller remet en question les hypothèses fragiles, recommande une démarche proportionnée et évalue les résultats. Vous gardez la maîtrise des objectifs, des priorités et des préférences.

La méthode n'impose aucun modèle, fournisseur, plugin ni service externe. Elle vise les projets de développement dans des environnements d'agents capables de charger ses instructions et ses fichiers de référence.

## Exemple de fonctionnement

Vous souhaitez ajouter l'importation de clients par CSV à une application existante.

| Étape | Qui | Exemple |
|---|---|---|
| Présenter l'objectif | Vous → conseiller | « Je veux que l'équipe importe des fichiers CSV de clients sans créer de doublons. » |
| Clarifier une ambiguïté réelle | Conseiller ↔ vous | « Une adresse e-mail répétée doit-elle mettre à jour le client existant ou être signalée pour examen ? » Vous choisissez l'examen. |
| Préparer l'exécution | Conseiller → vous | Une consigne précisant l'importation, les doublons, les contraintes d'autorisation existantes et les preuves nécessaires pour conclure. |
| Réaliser | Vous → agent | Vous transmettez la consigne à l'agent dans l'espace de travail du projet. Il examine, réalise et vérifie. |
| Rapporter le résultat | Vous → conseiller | L'agent rapporte des importations réussies et des vérifications des lignes invalides et des doublons dans un fichier. |
| Évaluer les preuves | Conseiller → vous | Il remarque que la double importation du même fichier n'a pas été vérifiée et demande ce contrôle précis. |
| Conclure ou corriger | Agent → vous → conseiller | Le comportement attendu est démontré, ou un défaut est corrigé. Le conseiller clôt la tâche lorsque les preuves suffisent. |

Il s'agit d'un exemple, pas d'une séquence obligatoire. Les tâches claires peuvent être réalisées directement ; la planification inutile et les contrôles répétés sont déconseillés. La skill ne relie pas les conversations et n'envoie pas automatiquement de messages entre elles.

## Configuration recommandée

Utilisez un dossier et un chat de conseil par projet, en dehors du dépôt cible. Un autre projet reçoit un autre dossier et un état vierge. L’agent de réalisation reste dans le dépôt. Les instructions globales et des dossiers parents peuvent toujours s’appliquer.

## Installation

Copiez tout le dossier `skills/project-advisor` dans le répertoire personnel des skills de votre environnement, avec ses sous-dossiers. Utilisez Python 3.10+ pour prévisualiser la préparation, puis ajoutez `--apply` après examen des différences. Remplacez les chemins et choisissez `codex`, `claude` ou `opencode`.

```sh
python <skill-dir>/scripts/workspace.py --workspace <advisor-dir> --project <target-dir> --harness codex
python <skill-dir>/scripts/workspace.py --workspace <advisor-dir> --project <target-dir> --harness codex --apply
```

Codex: `$project-advisor` · Claude Code: `/project-advisor` · OpenCode: `project-advisor`

[Codex / Claude Code / OpenCode — setup, updates, migration](../../skills/project-advisor/references/HARNESSES.md)

## Activation et utilisation

Ouvrez un nouveau chat dans le dossier préparé. Le chargement des instructions locales active le conseiller du projet associé ; l’installation seule n’active pas les autres chats. Vérifiez son rôle, son projet, son état et sa prochaine action. La désactivation explicite vaut pour le chat actuel ; un nouveau chat redémarre comme conseiller. Les réponses suivent votre langue préférée.

## Ce que fait le conseiller

- Relie la prochaine tâche à un résultat utile pour le projet.
- Questionne les décisions lorsqu'un problème concret apparaît et propose des solutions de remplacement.
- Pose des questions sur vos préférences, priorités, intentions et les faits que vous pouvez préciser.
- Mène une recherche ciblée pour les questions techniques ou spécialisées.
- Adapte planification, délégation et vérification au risque et à l'incertitude.
- Évalue les preuves de l'agent et s'arrête quand la tâche est suffisamment achevée.
- Respecte les choix éclairés et les limites d'autorisation.
- Maintient un point de reprise concis et actuel plutôt qu'un journal d'activité cumulatif.

## État, confidentialité et limites

`AGENTS.md` contient la méthode ; `CLAUDE.md` l’importe si nécessaire. `.advisor-workspace.json` enregistre projet, environnement, version et empreintes. L’état privé se trouve dans `ADVISOR_STATE.md` ; `CONSULTOR_STATE.md` peut être conservé. Lisez l’état avant `--adopt-existing-state`. Placez vos préférences dans `ADVISOR_LOCAL.md`. Les mises à jour présentent les différences et refusent les instructions modifiées : examinez et fusionnez ces changements. L’état existant est préservé. Aucun hook ni service en arrière-plan n’est installé. Les tests ne certifient pas le comportement de tous les clients.

## Structure du dépôt

Le modèle est la source unique de la méthode distribuée ; chaque dossier reçoit une copie versionnée. Il n’existe plus de CORE séparé. La mise à jour de la skill ne modifie pas automatiquement les espaces de travail. Ne publiez pas les états ou réglages privés.

```text
skills/project-advisor/
├── SKILL.md
├── templates/AGENTS.md
├── scripts/workspace.py
├── agents/openai.yaml
└── references/
    ├── HARNESSES.md
    └── STATE_SCHEMA.md
```

## Contributions

Décrivez un problème réel, le comportement attendu et pourquoi la modification aide sans ajouter de démarches inutiles. Utilisez des exemples fictifs, retirez les informations privées et indiquez l'environnement et les limites des vérifications. Préservez la distinction entre recommandations réutilisables et préférences personnelles ou propres à un projet.

Les traductions du README se trouvent dans `.github/readme/`. Gardez exemples, commandes, liens et limites cohérents avec le README anglais lors des mises à jour. N'ajoutez des liens de langue que pour les traductions présentes dans le dépôt.

## Licence

[MIT](../../LICENSE) — Copyright (c) 2026 Guilherme Rocha.

## 2.1.0

Révision 2.1.0 : l’état distingue la provenance des preuves et réconcilie les décisions remplacées, en préservant les contraintes et vérifications ouvertes. L’installateur utilise un schéma unique, conserve le nom historique et améliore la récupération du manifeste et du verrou. Aucune comparaison contrôlée ne démontre un gain de qualité, de temps ou de coût. Les adaptateurs ne prouvent pas le fonctionnement réel dans chaque environnement ; sans accès aux fichiers, la méthode et l’état doivent être fournis et sauvegardés manuellement.

[English technical reference](../../docs/AUDIT_2_1.md) · [Examples](../../skills/project-advisor/references/EXAMPLES.md)
