---
name: one-pager
description: >-
  Erstellt und überarbeitet einseitige Event-Flyer und
  Veranstaltungsübersichten als druckfertige A4-PDF im vorgegebenen
  Layout. Verwenden für One-Pager, Flyer oder Handouts zur
  Ankündigung einer Veranstaltung.
compatibility: >-
  Requires Python 3 with qrcode and a Chromium-based browser
  (Microsoft Edge or Google Chrome) for PDF rendering.
---
# Event One-Pager

Erzeuge einen visuell konsistenten, einseitigen Event-One-Pager. Das Layout basiert auf einem bewährten Informationsfluss: Hero → Agenda → Speaker, flankiert von Zielgruppe → Ort → Anmeldung.

## Feste Gestaltungslogik

Lies bei Layoutfragen zuerst `references/layout-spec.md`.

- Verwende A4 Hochformat und genau eine Seite.
- Belege die oberen ca. 36 % mit einem dunklen Hero. Integriere bevorzugt rechts ein zum Meetup-Thema passendes Foto oder Motiv; der schwarze Verlauf hält die linke Textfläche ruhig und lesbar.
- Platziere Marke/Logo links oben und den Datums-Badge rechts oben.
- Zeige Thema, Haupttitel, Untertitel und maximal drei Fakten-Chips im Hero.
- Verwende darunter ein asymmetrisches Raster: ca. zwei Drittel für Agenda und Speaker, ein Drittel für Zusatzinformationen.
- Ordne links zuerst die Agenda und unmittelbar danach die Speaker an.
- Ordne rechts Zielgruppen-Callout, Veranstaltungsort und unten den QR-CTA an.
- Nutze Neon-Limette nur als Akzent, nicht als großflächigen Hintergrund außerhalb von Badge und CTA.
- Bewahre viel Weißraum. Kürze Inhalte, statt Schrift oder Abstände unleserlich klein zu machen.

## Workflow

1. Sammle die Inhalte in einer JSON-Datei gemäß `assets/example-content.json`.
2. Frage nur nach wirklich fehlenden Pflichtinhalten. Verwende keine erfundenen Namen, Daten, Orte oder URLs.
3. Wähle nach Möglichkeit ein hochwertiges, thematisch passendes Hero-Motiv. Besonders geeignet sind Meetup-Szenen, Technologie, Menschen im Austausch oder ein Motiv zum Vortragsthema. Das Hauptmotiv muss rechts liegen oder dorthin beschneidbar sein; links bleibt die schwarze Textfläche. Nutze nur bereitgestellte, lizenzierte oder eindeutig freigegebene Bilder. Ohne geeignetes Bild erzeugt der Renderer ein abstraktes dunkles Tech-Motiv.
4. Verwende für Speaker nach Möglichkeit echte Fotos. Priorität: vom Nutzer bereitgestelltes Foto → offizielle Speaker-/Unternehmensseite oder freigegebenes Pressefoto → abstrakter Personen-Avatar. Prüfe bei recherchierten Fotos Name und Kontext, dokumentiere die Quelle und verwende niemals das Foto einer nur ähnlich aussehenden Person.
5. Bereite Speaker-Fotos möglichst quadratisch und mit sichtbarem Gesicht vor. Der Renderer beschneidet sie kreisförmig. Fehlt ein verlässliches Foto, lasse `image` leer; der Renderer erzeugt dann automatisch einen abstrakten, namensbasierten Menschen-Avatar statt einer leeren Fläche.
6. Führe den Renderer aus:

```powershell
python "scripts/create_one_pager.py" content.json output.pdf
```

7. Prüfe die erzeugte PDF visuell. Achte besonders auf abgeschnittenen Text, überlaufende Agenda-Zeilen, korrekte Speaker-Zuordnung, einen lesbaren QR-Code und genau eine PDF-Seite.
8. Falls Inhalte nicht passen, kürze zuerst Beschreibungen. Ändere das Grundraster nur, wenn der Nutzer ausdrücklich ein anderes Format verlangt.

## Inhaltsgrenzen

- Agenda: ideal 3–4, maximal 5 Einträge; Beschreibung höchstens zwei kurze Zeilen.
- Speaker: ideal 2, maximal 3 Personen; Name plus eine kurze Rollen-/Firmenzeile.
- Zielgruppe: 3–4 kurze Nutzenpunkte.
- Fakten-Chips: maximal 3.
- Venue: Name, Straße, Ort und höchstens 2 kompakte Merkmale.
- CTA: kurze Überschrift, höchstens 3 Textzeilen, URL und QR-Code.

## Ausgabe

Liefere standardmäßig:

- die druckfertige PDF,
- die gleichnamige HTML-Datei als editierbare Quelle,
- die verwendete JSON-Datei.

Der Renderer bettet lokale Bilder und den QR-Code in die HTML-Datei ein, sodass sie transportabel bleibt.

Wenn Speaker-Fotos recherchiert wurden, liefere zusätzlich eine kurze Quellenliste. Abstrakte Fallback-Avatare benötigen keine Quelle.

## Abweichungen

Passe Farben und Logo an eine vorhandene Marke an, behalte aber Informationshierarchie und Proportionen bei. Wenn Brand-Vorgaben vorliegen, nutze deren Primärakzent anstelle der Limette und stelle ausreichenden Kontrast sicher.
