# Layout-Spezifikation

## Seitenraster

- Format: A4 Hochformat, 210 × 297 mm
- Hintergrund: warmes Off-White (`#F6F5F2`)
- Hero: 107 mm hoch, volle Breite
- Inhaltsrand: 14 mm links/rechts
- Hauptinhalt: 116 mm breit
- Seitenleiste: 57 mm breit
- Spaltenabstand: 9 mm
- Grundfarbe: fast schwarz (`#0A0C00`)
- Sekundärtext: warmes Grau (`#66675F`)
- Linien: `#D9D9D2`
- Akzent: Neon-Limette (`#E3FF04`)

## Hero

Die Hero-Grafik füllt den gesamten Bereich. Ein schwarzer Verlauf liegt darüber: links nahezu deckend, rechts transparent genug für das Motiv. Bevorzuge ein zum Meetup passendes Foto oder eine Illustration mit erkennbarem Motiv auf der rechten Seite. Links bleibt eine ruhige schwarze Textfläche. Fehlt ein geeignetes Bild, verwende das integrierte abstrakte Tech-Motiv statt einer komplett leeren schwarzen Fläche.

Reihenfolge:

1. Marke/Logo links oben
2. Datum in einem abgerundeten Akzent-Badge rechts oben
3. kleine gesperrte Themenzeile
4. großer Titel
5. maximal zweizeiliger Untertitel
6. bis zu drei pillenförmige Fakten-Chips

## Hauptbereich

Der Inhalt beginnt 10–12 mm unter dem Hero.

### Linke Spalte

`AGENDA` erhält einen 8-mm-Akzentstrich, eine Versalüberschrift und eine dunkle horizontale Linie. Jeder Eintrag verwendet:

- feste Zeitspalte von ca. 20 mm,
- Titel in Semibold/Bold,
- Beschreibung in Grau,
- feine Trennlinie.

`SPEAKER` folgt direkt nach der Agenda. Speaker erscheinen in gleich breiten weißen Karten mit feiner Kontur. Ein echtes, korrekt zugeordnetes Foto steht links, Name und Rolle rechts. Wenn kein verlässliches Foto verfügbar ist, steht dort ein abstrakter Personen-Avatar; leere Bildkreise sind nicht erlaubt.

### Rechte Spalte

1. Dunkle Zielgruppenkarte mit weißem Text und limettenfarbenen Punkten.
2. Weiße Location-Karte mit Name, Adresse und bis zu zwei grauen Merkmal-Badges.
3. Akzentfarbene CTA-Karte am unteren Rand mit QR-Code links und Text rechts.

Die CTA-Karte soll visuell isoliert sein; der freie Raum davor erhöht ihre Wirkung.

## Typografie

- Primär: Arial/Arial Narrow oder eine vergleichbare klare Grotesk.
- Titel: 35–38 pt, sehr fett.
- Hero-Untertitel: 13–15 pt.
- Abschnittslabels: 8–9 pt, fett, gesperrt.
- Agenda-Zeit: 11–12 pt, fett.
- Agenda-Titel: 10–11 pt, fett.
- Fließtext: 8–9 pt.
- CTA-/Kartenüberschrift: 13–15 pt, fett.

## Qualitätsregeln

- Genau eine Seite; keine automatische zweite Seite.
- Kein Text darf abgeschnitten, verdeckt oder kleiner als 7 pt sein.
- QR-Code braucht eine weiße Ruhezone und mindestens 24 mm Kantenlänge.
- Bilder niemals verzerren; immer mit `object-fit: cover` beschneiden.
- Speaker-Fotos müssen die genannte Person zeigen und aus einer bereitgestellten oder verlässlich verifizierten Quelle stammen.
- Fehlende Speaker-Fotos immer durch den integrierten abstrakten Menschen-Avatar ersetzen.
- Akzent sparsam und konsistent verwenden.
- Keine zusätzlichen Abschnitte zwischen Agenda und Speaker einfügen.
