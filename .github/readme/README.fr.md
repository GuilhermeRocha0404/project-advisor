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

Utilisez le **conseiller dans une conversation distincte, avec un espace de travail situé hors de l'arborescence du projet**. L'agent reste dans le projet et suit les instructions applicables. Une autre conversation associée au même projet peut encore charger `AGENTS.md`, `CLAUDE.md` ou d'autres règles locales.

Cela réduit le chargement automatique d'instructions propres au projet dans le contexte du conseiller. Les règles globales, les instructions des dossiers parents, les intégrations et le contexte hérité peuvent toujours s'appliquer ; l'isolation complète n'est pas garantie. Fournissez objectifs, documents sélectionnés et comptes rendus de l'agent. Le conseiller peut examiner les règles comme éléments d'analyse, en respectant la hiérarchie des instructions de l'environnement.

Conservez l'état de conseil de chaque projet dans son propre dossier externe, hors de la skill installée et, de préférence, hors du dépôt du projet. Ne publiez pas d'état privé avec la skill.

## Installation

Clonez ou téléchargez ce dépôt, puis copiez tout le dossier `skills/project-advisor` au bon endroit. Conservez `references/` et `agents/` à côté de `SKILL.md`. Examinez vos modifications locales avant d'écraser une installation existante.

| Environnement | Dossier d'installation personnel | Invocation explicite |
|---|---|---|
| Codex | `~/.agents/skills/project-advisor/` | `$project-advisor` |
| Claude Code | `~/.claude/skills/project-advisor/` | `/project-advisor` |
| OpenCode | `~/.config/opencode/skills/project-advisor/` | Sélectionnez ou chargez explicitement la skill ; voir l'option de commande ci-dessous. |

`~` désigne votre dossier personnel, y compris sous Windows. Ces chemins concernent les outils locaux ; les produits hébergés peuvent utiliser d'autres mécanismes. Si la skill n'apparaît pas, ouvrez une nouvelle session de conseil après l'installation.

### Contrôles d'invocation

Le noyau exige toujours une demande explicite d'activation. Les contrôles de l'environnement sont distincts :

- **Codex :** le fichier fourni `agents/openai.yaml` définit `policy.allow_implicit_invocation: false`.
- **Claude Code :** ajoutez `disable-model-invocation: true` à l'en-tête YAML du `SKILL.md` installé pour empêcher l'invocation à l'initiative du modèle. Ce champ est une adaptation à Claude Code, pas un élément du fichier partagé.
- **OpenCode :** ajoutez ces métadonnées, avec des valeurs textuelles, à l'en-tête du `SKILL.md` installé pour proposer une commande et retirer la skill des indications de sélection automatique :

  ```yaml
  metadata:
    opencode/slash: "true"
    opencode/autoinvoke: "false"
  ```

  Invoquez ensuite `/project-advisor` dans les versions qui prennent en charge ces réglages. Si votre client fonctionne autrement, utilisez son mécanisme explicite de chargement.

Ces ajustements concernent l'installation locale ; ils n'exigent pas plusieurs copies de la méthode dans ce dépôt. Préservez les réglages d'en-tête propres à l'environnement avant une mise à jour.

Les indications d'installation et d'invocation ont été vérifiées dans la documentation officielle de [Codex](https://learn.chatgpt.com/docs/build-skills), [Claude Code](https://code.claude.com/docs/en/skills) et [OpenCode](https://opencode.ai/docs/skills/) le 21 octobre 2026. **Cette version n'a pas été testée de bout en bout dans les trois clients.** Une vérification documentaire ne certifie pas la compatibilité à l'exécution. L'usage antérieur du conseiller en portugais a guidé cette version ; l'adaptation anglaise a encore besoin de retours de terrain plus variés.

## Activation et utilisation

Invoquez la skill avec le mécanisme de votre environnement, puis indiquez votre objectif et un dossier d'état. Par exemple :

```text
Active Project Advisor.
Utilise ce dossier externe pour l'état : /chemin/vers/mon-espace-de-conseil.
L'agent de réalisation est dans une autre conversation.
Je veux ajouter l'importation de clients par CSV à une application existante.
```

Le conseiller lit ses instructions centrales et l'état externe, ou crée l'état si nécessaire. Il reste actif dans la même conversation jusqu'à une désactivation explicite :

```text
Désactive le conseiller.
```

Dans une nouvelle conversation, réactivez la skill et indiquez le même dossier pour reprendre le projet. L'installation seule n'active jamais le rôle. Les instructions et exemples de la skill sont en anglais ; **le conseiller communique dans la langue que vous préférez**.

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

Le conseiller utilise `ADVISOR_STATE.md` dans votre espace externe. Lors de la création d'un nouvel état, un `ADVISOR_STATE_TEMPLATE.md` existant prévaut sur le schéma de secours fourni. `STATE_SCHEMA.md` ne contient que des champs génériques.

L'état peut contenir des décisions sensibles, des chemins ou des informations du projet. Choisissez soigneusement son emplacement et ses destinataires. Le `.gitignore` exclut les noms des fichiers d'état, mais cette protection ne concerne que cette copie du dépôt et ne retire pas les fichiers déjà suivis. Gardez de préférence l'état privé hors des dépôts que vous publiez.

L'état est consolidé pendant les tours actifs en cas de changement important, à la clôture d'un travail ou lors d'une reprise après réduction du contexte, selon les besoins. Il n'existe ni processus d'arrière-plan, ni hook de session, ni garantie de récupération si le contexte d'activation disparaît. Réactivez avec le même dossier si nécessaire. Sans accès aux fichiers, le conseiller peut fournir un résumé à sauvegarder au lieu de prétendre que l'état a été enregistré.

La skill fournit des instructions, pas des contrôles d'accès ni une garantie de décisions correctes. Son comportement dépend du modèle, des preuves disponibles, des instructions de l'environnement et des outils. Elle ne réalise pas le projet coordonné et ne contacte pas l'agent de sa propre initiative.

## Structure du dépôt

```text
skills/project-advisor/
├── SKILL.md                   Activation, état et continuité
├── agents/openai.yaml         Politique d'invocation de Codex
└── references/
    ├── ADVISOR_CORE.md        Méthode indépendante de plateforme
    └── STATE_SCHEMA.md        Structure de récupération de l'état
```

## Contributions

Décrivez un problème réel, le comportement attendu et pourquoi la modification aide sans ajouter de démarches inutiles. Utilisez des exemples fictifs, retirez les informations privées et indiquez l'environnement et les limites des vérifications. Préservez la distinction entre recommandations réutilisables et préférences personnelles ou propres à un projet.

Les traductions du README se trouvent dans `.github/readme/`. Gardez exemples, commandes, liens et limites cohérents avec le README anglais lors des mises à jour. N'ajoutez des liens de langue que pour les traductions présentes dans le dépôt.

## Licence

[MIT](../../LICENSE) — Copyright (c) 2026 Guilherme Rocha.
