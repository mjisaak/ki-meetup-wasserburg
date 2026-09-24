# KI Meetup Wasserburg – One-Pager Skill

Dieses Repository enthält den **One-Pager Skill** aus dem KI Meetup Wasserburg.

Der Skill zeigt, wie sich wiederkehrendes Wissen und feste Vorgaben als Agent Skill verpacken und anschließend in verschiedenen AI Agents wiederverwenden lassen.

## Installation

Der Skill kann direkt aus diesem GitHub Repository mit der [Skills CLI](https://skills.sh/) installiert werden.

```bash
npx skills add https://github.com/mjisaak/ki-meetup-wasserburg --skill one-pager
```

Alternativ kann das Repository auch über den Kurzbezeichner angegeben werden:

```bash
npx skills add mjisaak/ki-meetup-wasserburg --skill one-pager
```

Die CLI erkennt den Skill über die Datei:

```text
skills/one-pager/SKILL.md
```

## Verwendung

Nach der Installation steht der Skill deinem AI Agent zur Verfügung.

Du musst den Skill normalerweise **nicht explizit aufrufen**. Beschreibe einfach die Aufgabe, die du erledigen möchtest. Der Agent kann den passenden Skill anhand der Beschreibung erkennen und bei Bedarf laden.

Zum Beispiel:

```text
Erstelle mir einen One-Pager zum KI Meetup Wasserburg und stelle ihn als PDF bereit.
```

Der Agent verwendet anschließend die im Skill hinterlegten Anweisungen, Referenzen, Assets und Skripte, um den One-Pager zu erstellen.

## Aufbau des Skills

```text
skills/
└── one-pager/
    ├── SKILL.md
    ├── assets/
    ├── evals/
    ├── references/
    └── scripts/
```

- **SKILL.md** – Beschreibung und Anweisungen für den Agenten
- **assets/** – Bilder, Logos und weitere Ressourcen
- **references/** – zusätzliche Informationen und Vorgaben
- **scripts/** – Skripte, die der Skill verwenden kann
- **evals/** – Beispiele und Tests zur Bewertung des Skills

## Idee hinter Agent Skills

Ein Prompt beschreibt hauptsächlich, **was** erledigt werden soll.

Ein Skill beschreibt, **wie** eine wiederkehrende Aufgabe erledigt werden soll.

> **Prompt = Was? · Skill = Wie? · Tool = Womit?**

Dadurch muss das notwendige Prozesswissen nicht bei jeder Anfrage erneut in einen langen Prompt geschrieben werden.

## Links

- [Skills.sh](https://skills.sh/)
- [KI Meetup Wasserburg](https://ki-meetup.com/wasserburg/)
