#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generiert v4 Praesentationsskript — integriert, SW-druckbar.

Konventionen:
- Sprechtext: # Heading (druckt gross)
- Dringlichkeit: !!! / !! / ! / ○  (HOCH / MITTEL / NACH BEDARF / OPT)
- UI-Eingaben: [GROSSSCHRIFT-IN-ECKIGEN-KLAMMERN]
- Copy/Paste-Prompts: 4-Space-Einrueckung, NICHT gerahmt (markierbar)
- Strukturlinien: Unicode ─ │ ┬ ┼ ┴
- Regieanweisungen: [kursiv, klein, in eckigen Klammern]

Quellen:
- triangulated_cases.json (60 Faelle)
- main_raw_v2/ (V2-Beispiel-Outputs)
- analysis_refined.json (Empirie)
"""
import json
import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict

BASE = Path(__file__).parent
TRI = json.loads((BASE / "triangulated_cases.json").read_text(encoding="utf-8"))
MANIFEST_V2 = json.loads((BASE / "manifest_v2.json").read_text(encoding="utf-8"))
REFINED = json.loads((BASE / "analysis_refined.json").read_text(encoding="utf-8"))
OUT = BASE / "praesentationsskript_v4.md"

# --- Statische Inhalte ---

LEGENDE = """════════════════════════════════════════════════════════════════
LEGENDE — wie dieses Skript gelesen wird
════════════════════════════════════════════════════════════════

# »Text in Gänsefüßchen mit großer Schrift«
  → Sprechtext. Vorlesen. Eigene Worte willkommen.

  !!!  HOCH           — Kernbotschaft, nicht streichen
  !!   MITTEL         — wichtig bei normalem Zeitbudget
  !    NACH BEDARF    — erwähnen falls Frage kommt
  ○    OPT            — nur bei viel Zeit oder gezieltem Interesse

  [Regieanweisung in eckigen Klammern, klein, nicht vorlesen]

  UI-EINGABEN in der App-Maske:
    Feld X: [WERT IN GROSSBUCHSTABEN]

  Copy/Paste-Prompts sind nicht gerahmt — einfach im Block
  markieren und mit Strg+C kopieren:

    Prompt-Text Zeile 1
    Prompt-Text Zeile 2

────────────────────────────────────────────────────────────────
"""

KARTE_0 = """════════════════════════════════════════════════════════════════
KARTE 0 — BEGRÜSSUNG, TECHNIK-CHECK
Zeitbedarf: 10 Min  |  Zustand: Ankommen → Orientiert
════════════════════════════════════════════════════════════════

VORBEREITUNG
  ☐ Ausbildungscoach geöffnet (aktuelle Version 1.1.0 live unter
    jako-odyc.github.io/prompt-dash/ausbildungscoach/)
  ☐ Link im Chat vorbereitet
  ☐ Edupad-Link bereit: edupad.ch/p/cR3mlekNEV
  ☐ ChatGPT oder Claude in zweitem Tab geöffnet
  ☐ Ein Word-Dokument mit Beispiel-Azubi-Text für Pseudonymisierung
    bereit (Karte 2 Demo)
  ☐ QR-Code-Bild groß sichtbar

───── EINSTIEG  (5 Min) ─────

# »Willkommen. Mein Name ist Jaroslav Kois, Lehrer an der

# Friedrich-List-Schule in Darmstadt. Seit 17 Jahren in der

# kaufmännischen Berufsschule mit Schwerpunkt Lagerlogistik

# und Spedition.«

# »Heute zeige ich Ihnen, wie Sie mit KI rechtssichere

# Unterweisungen, Prüfungsfragen und Beratungsmaterial

# vorbereiten. Das Werkzeug dazu heißt Ausbildungscoach.

# Es läuft komplett in Ihrem Browser — kein Account nötig.«

  !!!  Name, Schule, Rolle nennen
  !!!  Heutiges Ziel: Ausbildungscoach als Werkzeug für 5 Berufe
       (Büromanagement, FLL, Fachlagerist, Spedition, BKF)
  !!   Brücke Theorie/Praxis, Erfahrung aus Schule + Verband
  !    17 Jahre Lehrer-Hintergrund als Vertrauensbasis
  ○    Digitalisierungs-Hintergrund (KI-Erfahrungen im Übungslager)


───── TECHNIK-CHECK  (5 Min) ─────

# »Bitte scannen Sie den QR-Code mit Ihrem Smartphone,

# oder öffnen Sie den Link, den ich jetzt in den Chat

# poste. Sie sehen dann die App mit 8 Karten.«

  [Link teilen: https://jako-odyc.github.io/prompt-dash/ausbildungscoach/]
  [Edupad-Link zusätzlich teilen]
  [5 Min warten bis alle geöffnet haben. Chat-Rückmeldungen sammeln.]

  !!!  Chat-Feedback: Wer hat schon mit ChatGPT/Claude gearbeitet?
       Chat: keine / wenige / intensiv — und beruflich?
  !!   Edupad als Rückmeldekanal erklären
  !    Bei Problemen: Niemand muss etwas eingeben. Zuschauen reicht.

───── ÜBERGANG ─────

# »Lassen Sie uns zuerst kurz anschauen, wie eine KI

# tatsächlich arbeitet — und warum Kontext alles ist.«

────── Ende Karte 0 ──────

"""

KARTE_1 = """════════════════════════════════════════════════════════════════
KARTE 1 — KI VERSTEHEN + DREISPRUNG (HERZSTÜCK)
Zeitbedarf: 20 Min  |  Zustand: Orientiert → Überzeugt durch eigene Erfahrung
════════════════════════════════════════════════════════════════

VORBEREITUNG
  ☐ Karte 1 im Ausbildungscoach geöffnet (aufklappbare S1/S2/S3 sichtbar)
  ☐ Teilnehmer haben ihre KI-Apps griffbereit (ChatGPT, Claude,
     Perplexity, DeepSeek — egal welche)
  ☐ Moderatoren-Perplexity bereit als Vergleichsinstanz
  ☐ Edupad-Link sichtbar (für gemeinsame Notizen)
  ☐ Doku-Subseite parat (für Vertiefung auf Nachfrage)


───── TEIL A — EINSTIEG  (2 Min) ─────

# »Eine KI antwortet immer — aber sie weiß nichts.

# Sie berechnet, welches Wort statistisch als Nächstes

# käme. Das funktioniert erstaunlich gut. Und es geht

# oft schief.«

  !!!  KI antwortet statistisch, nicht logisch
  !!!  KI weiß nicht, was sie nicht weiß — sie rät
  !!   Je enger der Kontext, desto belastbarer die Antwort
  !    Halluzinationen sind nicht Pannen, sondern strukturell

  [App: Karte 1 zeigen, drei Grundwahrheiten kurz durchscrollen]

# »Drei Haltungen, die heute alles zusammenhalten:
# Prüfen statt glauben. Konkrete Quellen statt Allgemeinplätze.
# Mehrere KIs befragen, wo es wichtig wird.«


───── TEIL B — DER DREISPRUNG (LIVE, 15 Min) ─────

  [App scrollen bis 'Warum ein Coach? Der Dreisprung'
   — S1/S2/S3 aufklappbar, jeweils mit Kopieren-Button]

# »Wir machen jetzt dreimal dasselbe:

# eine Unterweisung zu Sicherheitsmessern für Fachlageristen

# im ersten Lehrjahr. Dreimal — mit drei verschiedenen Prompts.

# Sie geben den jeweiligen Prompt in Ihre eigene KI ein und

# vergleichen mit mir, was herauskommt.«

  !!!  Dieser Block ist der Beweis, nicht die Behauptung
  !!!  Teilnehmer erleben den Unterschied selbst
  !!   Moderator zeigt parallel live in Perplexity
  !    Je mehr KIs im Raum, desto eindrücklicher die Divergenz

  [BRUCH: Falls Teilnehmer zögern — Edupad öffnen und Prompt dort
   auch bereitstellen, damit niemand abschreiben muss]


────── B.1  STUFE 1: NAIV  (3 Min) ──────

# »Stufe 1: Das, was Sie einem Kollegen zurufen würden.

# Einen Satz, ohne Drumherum.«

  [App: S1-Block aufklappen, Kopieren-Button klicken]
  [Teilnehmer: in ihre KI paste, Enter]

  Prompt S1 (ein Satz, ohne Kontext):

      Schreib mir was für die Unterweisung zu Sicherheitsmessern bei Azubis.

  [30–60 Sek warten, bis alle ein Ergebnis sehen]

# »Was sehen Sie? Ist das gut? Ist das brauchbar?«

  !!!  Überraschung: Das ist 2026 schon erstaunlich gut
  !!!  ChatGPT bringt §12 ArbSchG, DeepSeek die 4-Stufen-Methode
  !!   Aber: duzt durchgängig, kein Lehrplanbezug, generisch
  !    Fazit hinschreiben lassen (Edupad): »überraschend brauchbar«


────── B.2  STUFE 2: STRUKTURIERT  (5 Min) ──────

# »Stufe 2: Was ein reflektierter Ausbilder selbst schreibt —

# Zielgruppe, Zweck, Dauer, Inhaltsstichpunkte. Ohne die App.«

  [App: S2-Block aufklappen, Kopieren-Button]
  [Teilnehmer: neuer Chat, paste, Enter]

  Prompt S2 (strukturiert, ohne App-Guards):

      Erstelle eine Unterweisung zur Nutzung von Sicherheitsmessern für
      Fachlageristen im 1. Ausbildungsjahr.

      Zielgruppe: Auszubildende mit gemischten Deutschkenntnissen (B1),
      15-18 Jahre.
      Zweck: Pflichtunterweisung nach Arbeitsschutzgesetz, jährlich.
      Dauer: ca. 20 Minuten.
      Format: gegliedert in Abschnitte mit Überschriften.

      Inhaltlich abzudecken: welche Messer erlaubt/nicht, Gefahren und
      typische Unfälle, richtige Schnittführung, Pflege der Klinge, PSA,
      Verhalten bei Verletzung, rechtliche Grundlagen.

      Bitte mit Lernzielen am Anfang.

  [2 Min warten]

# »Besser? Gerne. Aber schauen Sie genauer hin:«

  !!!  Gezielt suchen lassen — 5 Prüffragen an der Tafel/Folie:
         1. Wird durchgehend gesiezt — oder wechselt Du/Sie?
         2. Werden Paragraphen zitiert, die es nicht gibt?
         3. Taucht ein fachlich falscher Begriff auf
            (z. B. »Ceranmesser« als Lagerwerkzeug)?
         4. Fragt die KI nach, wenn Kontext fehlt — oder rät sie?
         5. Wird der Rahmenlehrplan des Berufs erwähnt?

  !!   »Ceranmesser« ist bei DeepSeek tatsächlich aufgetreten —
       ein Glasschaber für Kochfelder, KEIN Lagerwerkzeug.
       Das ist der Fehlertyp, der unter fachlichem Druck entsteht.

  !    Moderator macht die gleichen 5 Prüfungen parallel in Perplexity
       sichtbar


────── B.3  STUFE 3: MIT COACH  (5 Min) ──────

# »Stufe 3: Das, was der Coach aus Karte 4 hätte generieren

# können. Wir nehmen es hier als fertigen Block — in Karte 4

# zeige ich später, wie man ihn in drei Klicks selbst erzeugt.«

  [App: S3-Block aufklappen, Kopieren-Button]
  [Teilnehmer: neuer Chat, paste, Enter]
  [Hinweis: S3 ist lang — knapp 4600 Zeichen — deshalb Copy-Button]

  Prompt S3 (aus dem Ausbildungscoach, mit allen Guards):

      [Inhalt: Rechtsrahmen §12/§13 ArbSchG + DGUV V1 §4, Berufsprofil
       Fachlagerist aus BerufeNet, Sprache B1 + Schrift unsicher,
       5-Achsen-Anforderungen, ANTI-HALLUZ-REGELN (§-Whitelist),
       SIEZEN-GUARD. Nicht hier abdrucken — Teilnehmer
       kopieren ihn direkt aus der App.]

  [3 Min warten]

# »Was hat sich verändert?«

  !!!  Siezen konsistent bei beiden Modellen
  !!!  DeepSeek fragt zurück: Welches Messermodell? Welche PSA?
       Welche Gruppengröße? Sprachmittler? — exakt das, was
       eine reale Ausbilderin vorher klären würde
  !!   ChatGPT legt zwar direkt los, aber ohne erfundene §§
  !!   Explizite Meta-Aussage bei DeepSeek: »ohne erfundene Normen
       oder Gesetze« — Anti-Halluz-Guard ist angekommen

  !    Wichtig gegenüber Teilnehmern klarstellen:
       Der Coach ist kein Tipp-Ersparnis. Er ist fachliche
       Qualitätssicherung für den Prompt.


───── TEIL C — SYNTHESE  (2 Min) ─────

# »Drei Stufen, drei Qualitäten. Was der Coach wirklich macht,

# ist unsichtbare Arbeit: er hinterfragt, was im Prompt fehlen

# würde, bevor die KI zu raten anfängt.«

  !!!  Kernbotschaft: Coach = Qualitätssicherung, nicht Tippzeit
  !!   Wer struktur­iert selbst promptet, kommt weit — aber nicht
       lehrplantreu und nicht halluzinationsfrei
  !    Alle Stufen bleiben im Edupad stehen (als Belegpfad)


───── ESKALATION — HÄUFIGE RÜCKFRAGEN ─────

  FRAGE »Kann die KI denn überhaupt was Fachliches?«
   ┬ ESK-1  Ja — für Sprache, Struktur, Wiederholungen. Nicht für
            neue Sachverhalte ohne Kontext.
   ┼ ESK-2  Vergleichen Sie es mit einem sehr schnellen, sehr
            belesenen Praktikanten, der Ihr Feld nicht kennt.
   ┴ ESK-3  Drei Bereiche müssen Sie IMMER selbst prüfen: Rechtliches,
            Zahlen, betriebsspezifische Details.

  FRAGE »Muss ich dann immer den Coach benutzen?«
   ┬ ESK-4  Für rechtsrelevante Unterweisungen: ja.
   ┼ ESK-5  Für schnelle Skizzen / Brainstorming: S1 oder S2 reicht oft.
   ┴ ESK-6  Faustregel: Je höher das Empfängerrisiko, desto mehr Guard.

  FRAGE »Was, wenn die KI trotzdem Unsinn schreibt?«
   ┬ ESK-7  Die 5 Prüffragen sind der Stressto-Test (Siezen,
            Paragraphen, Begriffe, Rückfragen, Lehrplan).
   ┼ ESK-8  Zweite KI befragen — Divergenz ist Diagnose-Werkzeug.
   ┴ ESK-9  Verantwortung für Sachkunde bleibt beim Ausbilder,
            nicht bei der Maschine.


───── PERSONA-HINWEISE ─────

  (P) Pragmatiker  — »ok ich nutz den Coach, zeig die Klicks«
  (S) Skeptiker    — Dreisprung ist Material für weitere Skepsis, gut
  (V) Verweigerer  — S3 zeigen, er muss nicht selbst tippen


───── ABSCHLUSS / ÜBERGANG ─────

# »Sie haben jetzt gesehen, was der Coach tut. In Karte 2

# klären wir, was er mit Ihren Daten macht — und was nicht.«

────── Ende Karte 1 ──────

"""

KARTE_2 = """════════════════════════════════════════════════════════════════
KARTE 2 — RAHMEN & DATENSCHUTZ
Zeitbedarf: 8 Min  |  Zustand: Sensibilisiert → Datenschutzsicher
════════════════════════════════════════════════════════════════

VORBEREITUNG
  ☐ Karte 2 im Ausbildungscoach geöffnet (Ampel sichtbar)
  ☐ Word-Dokument mit Beispiel-Azubi-Text offen
  ☐ Suchen-und-Ersetzen-Dialog getestet (Strg+H)

───── EINSTIEG  (1 Min) ─────

# »Was darf in den KI-Chat — und was nicht? Es gibt eine

# einfache Faustregel: keine Personendaten, keine Geschäfts-

# geheimnisse. Und einen Fachbegriff: pseudonymisieren.«

  !!!  Pseudonymisieren ≠ anonymisieren (Fachbegriff beachten)
  !!!  Niemals: Klarnamen, Geburtsdaten, Gesundheitsdaten
  !!   Pseudonymisieren VOR dem KI-Einsatz, nicht danach


───── HAUPTINHALT — Live-Demo Word  (5 Min) ─────

  [App: Ampel grün/gelb/rot zeigen, je 30 Sek pro Farbe]

# »Grün: darf rein. Gelb: vorsichtig, pseudonymisieren.

# Rot: niemals.«

  !!!  Grün: fachliche Fragen, Entwürfe mit „Azubi A, 2. LJ"
  !!!  Gelb: betriebsinterne Abläufe generisch, ohne Namen/Daten
  !!!  Rot:  Klarnamen, Geburtsdaten, Gesundheits-/Leistungsdaten

  [Word öffnen, Azubi-Text zeigen]

# »Wir pseudonymisieren jetzt live. Drei Schritte in Word,

# drei Minuten.«

  Schritt 1:  Dokument duplizieren (Kopie als Arbeitsdatei)

  Schritt 2:  Suchen-und-Ersetzen (Strg+H):
              Vorname       → A.
              Nachname      → weglassen
              Firma         → Speditionsbetrieb
              Konkrete Orte → Region
              Geburtsdatum  → LJ 2007  (Lehrjahr-Angabe reicht)

  Schritt 3:  Sichtkontrolle — auch ohne Namen kann
              eine Beschreibung identifizierend sein, wenn
              mehrere seltene Merkmale zusammenkommen.
              (z. B. Standort + Schicht + Eintrittsjahr +
              besondere Qualifikation)

  !!   Merkmalskombinationen können identifizierend sein
  !    Reale Fotos nie hochladen
  ○    Bei Behörden/großen Betrieben: KI-Richtlinien des Arbeitgebers


───── AUSWERTUNGSLOGIK ─────

  WENN  »Mein Betrieb hat keine KI-Richtlinien — was jetzt?«
  DANN  Grundregel gilt trotzdem: keine echten Personendaten.
        Anstoß zur IT-/Betriebsrat-Kommunikation.

  WENN  »Kann ich meinen ChatGPT-Account nutzen?«
  DANN  Private Accounts: Eingaben werden ggf. für Training
        verwendet. Daher: niemals echte Personendaten.
        Firmen-Account hat Opt-out.


───── ESKALATION — HÄUFIGE RÜCKFRAGEN ─────

  FRAGE »Sind meine Daten bei ChatGPT sicher?«
   ┬ ESK-1  Deswegen: Platzhalter. Was nicht reingeht, kann nicht raus.
   ┼ ESK-2  Kostenlose Version: Eingaben können für Training verwendet
            werden. Nichts eingeben, was nicht auf einem Whiteboard
            stehen darf.
   ┴ ESK-3  Stufe 3 wäre eine lokale KI (läuft auf eigenem Rechner,
            null Daten nach außen). Das vertiefen wir nach dem Workshop.

  FRAGE »Ist Pseudonymisieren rechtssicher?«
   ┬ ESK-1  Technisch ja — wenn alle identifizierenden Merkmale weg sind.
   ┼ ESK-2  Rechtlich: KI-Nutzung insgesamt ist in Deutschland
            noch in Klärung. Pseudonymisieren ist das Minimum.
   ┴ ESK-3  Diese Empfehlung ist nicht DSGVO-geprüft.
            Bei Unsicherheit: Datenschutzbeauftragten Ihres
            Arbeitgebers fragen.


───── FACHBEGRIFF ─────

  PSEUDONYMISIERUNG — Echte Daten durch Platzhalter ersetzen,
  bevor sie in die KI kommen. Wie ein Briefumschlag ohne Absender:
  der Inhalt bleibt, die Identität nicht.

  ANONYMISIERUNG — Alle Bezüge zur Person dauerhaft unmöglich
  machen (viel strenger, oft nicht praktikabel für Beratungsfälle).


───── PERSONA-HINWEISE ─────

  (P) Pragmatiker — 3 Platzhalter genügen für 90 % der Fälle
  (S) Skeptiker   — Diese Karte gibt die Kontrolle zurück
  (V) Verweigerer — Datenschutz ist sein Alltagsthema; Einstiegspunkt


───── ABSCHLUSS / ÜBERGANG ─────

# »Jetzt wissen Sie, was rein darf. Jetzt schauen wir,

# wo es im Lehrplan steht.«

────── Ende Karte 2 ──────

"""

KARTE_3 = """════════════════════════════════════════════════════════════════
KARTE 3 — THEMEN-NAVIGATOR (Begriffssuche)
Zeitbedarf: 10 Min  |  Zustand: Datenschutzsicher → Lehrplan-Orientiert
════════════════════════════════════════════════════════════════

VORBEREITUNG
  ☐ Karte 3 im Ausbildungscoach geöffnet, Filter-Checkboxen sichtbar
  ☐ Beispiel-Suchbegriff „Kommissionierung" vorbereitet

───── EINSTIEG  (1 Min) ─────

# »Die KI kennt Ihren Lehrplan nicht wörtlich. Aber der

# Ausbildungscoach hat alle KMK-Rahmenlehrpläne und

# BerufeNet-Steckbriefe der fünf Berufe drin. Sie können

# jetzt gezielt nach Begriffen suchen — und den Volltext

# daneben scrollen.«

  !!!  12 Dokumente, ~345 KB Volltext (KMK + BIBB + BerufeNet)
  !!!  Funktioniert ohne Internet (in Offline-Kopie dabei)
  !!   Datengrundlagen: KMK-Rahmenlehrpläne, BIBB-Verordnungen,
       BerufeNet-Steckbriefe 2024


───── HAUPTINHALT — Live-Demo  (7 Min) ─────

  [App: Karte 3 öffnen, 4 Beruf-Filter checken]

# »Alle Berufe durchsuchbar. Ich suche nach

# ›Kommissionierung‹.«

  UI-EINGABE in der Maske:
    Begriff: [KOMMISSIONIERUNG]

  [Enter — Trefferliste mit 7 Treffern in 3 Dokumenten]

# »7 Treffer, 3 Dokumente. Jeder Treffer zeigt ein

# Snippet. Klicken öffnet den gesamten Lehrplan-Text

# — scrollbar, Treffer orange markiert.«

  [Klick auf ersten Treffer → Volltext-Panel öffnet sich, scrollbar]

  !!!  Klick auf Treffer → gesamter Volltext (nicht nur Ausschnitt)
  !!!  Aktiver Treffer orange (andere gelb)
  !!   Scrollbar: nach oben/unten frei blättern — wie im PDF


───── 10 KREATIVE ANWENDUNGEN (Handout, Teil II) ─────

  !!   Folgende 10 Anwendungen zeigen, dass die Suche MEHR ist
       als Suchen:

  1. Lernfeld-Überblick — „Wo kommt X vor?"
  2. Prüfungsrelevanz-Check — „Ist X prüfbar?"
  3. Lehrplan-Lücken — „Was fehlt?"
  4. Berufs-Differenzierung — „Was heißt X in Beruf A vs. B?"
  5. Fachsprache-Alltagswort-Brücke — „Stapler" vs. „Flurförderzeug"
  6. Volltext als Prompt-Kontext — direkt übergeben
  7. Unterweisungs-Themenliste generieren — aus Lernfeld
  8. ZP/AP-Mapping — welches LF in welcher Prüfung?
  9. Didaktik-Brücke — abstrakter Begriff → Alltagsbeispiel
  10. Zeitplanung — Stunden-Richtwerte zusammentragen

  [Jede Anwendung hat eine fertige Prompt-Vorlage im Handout Teil II]


───── AUSWERTUNGSLOGIK ─────

  WENN  »Warum findet die Suche ›Stapler‹ nicht?«
  DANN  Alltagsbegriffe kommen im KMK-Lehrplan oft NICHT vor.
        Fachsprache: „Flurförderzeug", „Kommissionierung",
        „Ladehilfsmittel", „Güter".

  WENN  »Ich suche ein Thema, das nicht vorkommt.«
  DANN  Das ist ein Lehrplan-Lücken-Befund! Hinweis geben:
        „Dann ist es nicht prüfungsrelevant. Kann trotzdem
        sinnvoll in der Unterweisung sein."


───── PERSONA-HINWEISE ─────

  (P) Pragmatiker — drei Klicks zum Volltext reicht
  (S) Skeptiker   — Daten sind statisch (KMK/BIBB) — keine
                    KI-Recherche, keine Halluzinationen möglich
  (V) Verweigerer — kann als reine Recherchefunktion nutzen


───── ABSCHLUSS / ÜBERGANG ─────

# »Gut. Jetzt kommt der Kern des Werkzeugs: wie Sie

# Unterweisungen mit KI vorbereiten — rechtssicher.«

────── Ende Karte 3 ──────

"""

# --- V2-Beispiel extrahieren ---

def load_v2_response(card_id, label, prefer_model="anthropic"):
    """Holt einen V2-Output zu einem Fall aus main_raw_v2/."""
    v2_raw = BASE / "main_raw_v2"
    # Dateien suchen mit passendem label
    candidates = list(v2_raw.glob(f"{card_id}*{label}*.raw.json"))
    if not candidates:
        return None
    # Bevorzugtes Modell wählen
    preferred = [c for c in candidates if prefer_model in c.name]
    if preferred:
        candidates = preferred
    try:
        raw = json.loads(candidates[0].read_text(encoding="utf-8"))
        if "error" in raw:
            return None
        return {"model": raw.get("model_key"),
                "text": raw.get("response_text", ""),
                "tokens_out": raw.get("tokens_out")}
    except Exception:
        return None


def trim_to_lines(text, n_lines=15):
    """Schneidet Text auf n Zeilen."""
    if not text:
        return ""
    lines = text.split("\n")
    if len(lines) <= n_lines:
        return text
    return "\n".join(lines[:n_lines]) + "\n    [... gekürzt. Vollständig in main_raw_v2/]"


def render_beispiel(fall, card_id, v2_response):
    """Rendert einen Karte-Beispiel-Block."""
    label = fall.get("label", "?")
    params = []
    for k, v in fall.items():
        if k in ("nature", "label", "begruendung"):
            continue
        vs = str(v)[:80]
        params.append(f"  {k}: [{vs.upper() if len(vs) < 30 else vs}]")
    out = []
    out.append(f"  BEISPIEL-FALL: {label}")
    out.append("")
    out.append("  UI-Eingaben:")
    out.extend(params)
    out.append("")
    if v2_response:
        out.append(f"  Output ({v2_response['model']}, ~{v2_response.get('tokens_out','?')} Tokens, gekürzt):")
        out.append("")
        for line in trim_to_lines(v2_response['text'], 18).split("\n"):
            out.append(f"    {line}")
    return "\n".join(out)


def render_karte_4a():
    card_id = "4a"
    naheliegend = TRI["cards"][card_id]["naheliegend"][:2]

    out = ["""════════════════════════════════════════════════════════════════
KARTE 4a — UNTERWEISUNGEN §12 ArbSchG (Modus A)
Zeitbedarf: 15 Min  |  Zustand: Lehrplan-Orientiert → Rechtssicher-Unterweisend
════════════════════════════════════════════════════════════════

VORBEREITUNG
  ☐ Karte 4 im Ausbildungscoach geöffnet, Modus A aktiv
  ☐ ChatGPT oder Claude in zweitem Tab
  ☐ Beispiel-Parametrisierung bereit (FLL + LJ 2 + Kommissionierung)

───── EINSTIEG  (2 Min) ─────

# »Unterweisungen nach §12 ArbSchG sind Pflicht:

# dokumentiert, mindestens jährlich, durch eine

# sachkundige Person. Der Ausbildungscoach gibt Ihnen

# einen strukturierten Entwurf — aber die Verantwortung

# bleibt bei Ihnen.«

  !!!  §12 ArbSchG: Pflicht, dokumentiert, jährlich
  !!!  Verantwortung bleibt beim sachkundigen Ausbilder
  !!!  Rechtsblock im Prompt ist Orientierung —
       NIE wörtlich in den Entwurf übernehmen
  !!   Gefährdungsbeurteilung muss VOR der Unterweisung vorliegen
  !    §13 ArbSchG: Unterweiser schriftlich beauftragt
  ○    Schnellmodus für erfahrene Ausbilder aktivierbar


───── HAUPTINHALT — Live-Demo  (8 Min) ─────

# »Ich zeige das jetzt Schritt für Schritt.«

  [App: Karte 4 geöffnet, Modus A]

  UI-Eingaben in die Maske:

    1. Beruf:             [FACHKRAFT FÜR LAGERLOGISTIK]
    2. Lernfeld:          [LF 5 — GÜTER KOMMISSIONIEREN]
    3. Lehrjahr:          [2. LEHRJAHR]
    4. Sprachniveau:      [A2 — EINFACHE WENDUNGEN]
    5. Schriftsprache:    [UNSICHER]
    6. Tätigkeit:         [KOMMISSIONIERUNG MIT HANDHUBWAGEN]
    7. Besonderheiten:    [SCHMALGANGREGAL, EIN AZUBI PRO SCHICHT]

  Formalia-Checkliste: 3 harte Punkte abhaken
    (Gefährdungsbeurteilung · Unterweiser sachkundig · arbeitsplatzbezogen)
  → Grüner Balken erscheint, Status "3/7 hart bestätigt"

  Klick [Prompt erzeugen] → Prompt steht in der Box
  Klick [Kopieren] → in ChatGPT einfügen → Output entsteht

  !!!  Beruf-, Lernfeld- und Lehrjahr-Angabe sind Pflicht
  !!   Schriftsprache-Achse (geübt/unsicher/sehr unsicher):
       unabhängig vom mündlichen Niveau, LEO-Studie
  !    Container-Modus: erst Diagnose, dann Entwurf — für
       fortgeschrittene Teilnehmer
  ○    Schnellmodus: Harten Punkte gelten als erfüllt,
       keine Rückfragen, kompakter Entwurf

"""]

    # Beispiel aus V2
    if naheliegend:
        fall1 = naheliegend[0]
        v2_resp = load_v2_response(card_id, fall1["label"])
        out.append("───── BEISPIEL (aus V2-Empirie, mit Anti-Halluz-Guards) ─────")
        out.append("")
        out.append(render_beispiel(fall1, card_id, v2_resp))
        out.append("")

    out.append("""───── AUSWERTUNGSLOGIK ─────

  WENN  »KI erfindet einen Paragraphen«
  DANN  Prompt-Guards wirken (nach V2-Empirie: erfundene §§
        nahezu verschwunden). Falls doch einer: Whitelist
        zeigen (§5/§12/§13 ArbSchG, DGUV V1 §4).

  WENN  »Entwurf klingt zu akademisch für Azubi auf A2«
  DANN  Sprachniveau A2 nochmal setzen, Schriftsprache
        „unsicher" aktivieren — dann Piktogramme & kurze Sätze.

  WENN  »KI zitiert §12 ArbSchG wörtlich im Entwurf«
  DANN  In V2 durch ›NICHT WÖRTLICH‹-Warnung eliminiert.
        Falls doch: Teilnehmer zeigen, wo im Prompt die
        Warnung steht — sensibilisiert für Prompt-Aufbau.


───── ESKALATION — HÄUFIGE RÜCKFRAGEN ─────

  FRAGE »Kann ich den Entwurf 1:1 als Unterweisung einsetzen?«
   ┬ ESK-1  Nein. Es ist eine VORLAGE. Sachkunde prüft und passt an.
   ┼ ESK-2  Betriebliche Gefährdungsbeurteilung ist zwingend nötig.
   ┴ ESK-3  §12 ArbSchG verlangt Anpassung an den konkreten Arbeitsplatz —
            dieser Teil bleibt menschliche Arbeit.

  FRAGE »Was, wenn die KI einen Paragraphen erfindet?«
   ┬ ESK-1  Jede §-Referenz gegenprüfen. Das ist keine Option, das ist Pflicht.
   ┼ ESK-2  Im Prompt ist eine Whitelist erlaubter §§.
   ┴ ESK-3  Empirisch: Die Guards haben erfundene §§ nahezu eliminiert
            (15 Runs · keine Halluzinationen außerhalb Whitelist).


───── FACHBEGRIFF ─────

  §12 ArbSchG — Pflicht zur Unterweisung.
  Bei Einstellung, Aufgabenwechsel, Einführung neuer Arbeitsmittel,
  mindestens jährlich. Arbeitsplatz- und tätigkeitsbezogen.
  Zu dokumentieren.

  GEFÄHRDUNGSBEURTEILUNG (§5 ArbSchG) — muss VOR der Unterweisung
  vorliegen. Die KI erstellt sie NICHT.


───── PERSONA-HINWEISE ─────

  (P) Pragmatiker — drei Klicks, brauchbarer Entwurf
  (S) Skeptiker   — Rechtsblock zeigt, was drin und was nicht
  (V) Verweigerer — kein Zwang. Entwurf kann zur manuellen
                    Überarbeitung dienen.


───── ARBEITSPHASE  (15 Min) ─────

# »Jetzt Sie. Wählen Sie einen Fall aus dem Handout

# oder tippen Sie einen eigenen. Bauen Sie einen Prompt.

# Kopieren Sie ihn in Ihre KI. Schauen Sie auf das

# Ergebnis.«

  Drei Fragen zum Nachdenken:
  - Klingt das nach einer Unterweisung, die Sie halten würden?
  - Welche Stelle müsste noch an Ihren Betrieb angepasst werden?
  - Wo würde die KI Ihnen vertrauen — wo nicht?

  [Timer 10 Min. Anschließend 2-3 Teilnehmer berichten im Chat/Edupad.]


───── ABSCHLUSS / ÜBERGANG ─────

# »Das war die formale Unterweisung. Für Geräte und

# Abläufe ohne Sicherheitsbezug gibt es den informellen

# Modus B — viel kürzer, viel schneller.«

────── Ende Karte 4a ──────

""")
    return "\n".join(out)


def render_karte_4b():
    card_id = "4b"
    naheliegend = TRI["cards"][card_id]["naheliegend"][:2]

    out = ["""════════════════════════════════════════════════════════════════
KARTE 4b — EINWEISUNGEN (Modus B, informell)
Zeitbedarf: 10 Min  |  Zustand: Rechtssicher-Unterweisend → Alltagspraktisch
════════════════════════════════════════════════════════════════

VORBEREITUNG
  ☐ Modus-B-Tab in Karte 4 bereit
  ☐ Beispiel „Bürodrucker" oder „WMS-Login" vorbereitet

───── EINSTIEG  (1 Min) ─────

# »Nicht jede Einweisung ist eine Unterweisung nach

# §12. Der Bürodrucker, die Ablagestruktur, ein

# Software-Login: das sind Einweisungen. Kürzer,

# pragmatischer, nicht dokumentationspflichtig.«

  !!!  Einweisung ist KEINE Unterweisung nach §12 ArbSchG
  !!!  Bei Sicherheitsbezug → zurück zu Modus A
  !!   Keine §-Referenzen im Einweisungstext
  !    Zielgruppen-Rolle prägt den Ton (Azubi ≠ neuer Mitarbeiter)


───── HAUPTINHALT — Live-Demo  (5 Min) ─────

# »Modus B ist schlichter: Gerät, Zielperson, fertig.«

  UI-Eingaben:

    1. Beruf (optional):   [BÜROMANAGEMENT]
    2. Rolle:              [NEUER AZUBI, ERSTE WOCHE]
    3. Gerät/Ablauf:       [BÜRODRUCKER HP 4250 BEDIENEN]
    4. Umfang:             [NORMAL (1 SEITE, 15 MINUTEN)]
    5. Sprachniveau:       [B1 — ALLTAGSSPRACHE]
    6. Besonderheiten:     (optional leer lassen)

  Klick [Prompt erzeugen] → kurzer, praxisnaher Prompt
  Klick [Kopieren] → KI erzeugt Einweisungstext

  !!!  Beruf-Feld ist optional — bei reinen Büroabläufen nicht nötig
  !!   Umfang steuert die Länge sichtbar (kurz/normal/ausführlich)

"""]

    if naheliegend:
        fall = naheliegend[0]
        v2_resp = load_v2_response(card_id, fall["label"])
        out.append("───── BEISPIEL (aus V2-Empirie) ─────")
        out.append("")
        out.append(render_beispiel(fall, card_id, v2_resp))
        out.append("")

    out.append("""───── AUSWERTUNGSLOGIK ─────

  WENN  »KI schreibt §12 ArbSchG in die Einweisung«
  DANN  Sollte in V2 nicht mehr vorkommen (Anti-§12-Guard wirkt).
        Falls doch: Prompt-Box zeigen, Guard-Text markieren.

  WENN  »Einweisung klingt wie eine Unterweisung«
  DANN  Umfang reduzieren (kurz statt ausführlich). Ton-Marker
        „informell" im Prompt verstärken.


───── ESKALATION ─────

  FRAGE »Brauche ich wirklich beide Modi — oder reicht einer?«
   ┬ ESK-1  Sie brauchen beide. Modus A: rechtliche Pflicht.
            Modus B: Alltagsroutine.
   ┼ ESK-2  Mischung ist rechtlich problematisch. Entweder oder.
   ┴ ESK-3  Grenzfall ist meist klar: „Kann das zu einem Arbeits-
            unfall führen?" → ja: Modus A. Sonst: Modus B.


───── FACHBEGRIFF ─────

  EINWEISUNG — Praktische Erklärung eines Geräts oder Ablaufs
  ohne formale Pflichten. Ersetzt KEINE Unterweisung bei
  sicherheitsrelevanten Tätigkeiten.


───── PERSONA-HINWEISE ─────

  (P) Pragmatiker — schnell, alltagstauglich, kein Rechtsballast
  (V) Verweigerer — kurze Texte, kein Stress


───── ARBEITSPHASE  (4 Min) ─────

# »Kurzer Durchlauf: wählen Sie ein Gerät oder eine

# Software, die bei Ihnen jeder Neue lernen muss.

# Bauen Sie eine Einweisung.«

  [Timer 4 Min. Kurze Rückmeldung im Chat.]


───── ABSCHLUSS / ÜBERGANG ─────

# »Wenn Sie schon Material haben — einen Entwurf,

# ein Rundschreiben, eine Prüfungsaufgabe —, dann

# kann die KI das prüfen. Dazu kommt jetzt Karte 5.«

────── Ende Karte 4b ──────

""")
    return "\n".join(out)


def render_karte_5():
    card_id = "5"
    naheliegend = TRI["cards"][card_id]["naheliegend"][:1]

    out = ["""════════════════════════════════════════════════════════════════
KARTE 5 — MATERIAL ANALYSIEREN (Zustandsprompt)
Zeitbedarf: 10 Min  |  Zustand: Alltagspraktisch → Diagnostisch
════════════════════════════════════════════════════════════════

VORBEREITUNG
  ☐ Karte 5 geöffnet
  ☐ Ein eigener Text zum Einfügen bereit (Entwurf aus Karte 4a,
    Rundmail, Prüfungsaufgabe)

───── EINSTIEG  (2 Min) ─────

# »Karte 5 ist anders als die anderen. Hier schreibt

# die KI NICHT. Sie PRÜFT. Das nennt sich Zustandsprompt:

# Sie geben einen eigenen Text, die KI diagnostiziert

# entlang von fünf Achsen.«

  !!!  Zustandsprompt = Diagnoseprüfung, NICHT Neufassung
  !!!  Ihre Fachsprache bleibt erhalten
  !!   5 Achsen: Vollständigkeit · Eindeutigkeit ·
       Empfängerrisiko · Struktur · Ton
  !    Container-Modus: KI prüft zuerst, welche Achsen
       für DIESEN Text relevant sind


───── HAUPTINHALT — Live-Demo  (5 Min) ─────

  UI-Eingaben:

    1. Beruf:             [FLL]  (optional)
    2. Lehrjahr:          [2. LEHRJAHR]
    3. Zweck:             [UNTERWEISUNGSENTWURF]
    4. Sprachniveau:      [A2]
    5. Zu analysierender Text:
       [EIGENER TEXT IN DIE TEXTAREA EINFÜGEN]
    6. Container-Modus:   [☑ AKTIVIEREN]

  Klick [Prompt erzeugen] → Prompt enthält den Text als
  Anhang, KI antwortet strukturiert

  !!!  Text nicht aus sensitiven Quellen ohne Pseudonymisierung
  !!   Container-Modus ist empfohlen — verhindert irrelevante
       Kritik bei Kurztexten

"""]

    if naheliegend:
        fall = naheliegend[0]
        v2_resp = load_v2_response(card_id, fall["label"])
        out.append("───── BEISPIEL (aus V2-Empirie) ─────")
        out.append("")
        out.append(render_beispiel(fall, card_id, v2_resp))
        out.append("")

    out.append("""───── AUSWERTUNGSLOGIK ─────

  WENN  »KI schreibt eine Neufassung statt Diagnose«
  DANN  Container-Modus noch nicht aktiv gewesen?
        Oder: Prompt-Zeile ›DIAGNOSE, nicht Neufassung‹
        hervorheben.

  WENN  »Kritik trifft nicht auf meinen Text zu«
  DANN  Zielgruppe/Zweck präzisieren. Bei A2 ist andere
        Kritik relevant als bei C1.


───── ESKALATION ─────

  FRAGE »Mein Text ist vertraulich — kann ich den einfach einfügen?«
   ┬ ESK-1  Nicht direkt. Erst pseudonymisieren (Karte 2).
   ┼ ESK-2  Nutzen Sie den Word-Trick (Strg+H) vor dem Einfügen.
   ┴ ESK-3  Bei sensiblen Texten (Personalakten etc.): gar nicht in die KI.


───── FACHBEGRIFF ─────

  ZUSTANDSPROMPT — Prompt-Muster, bei dem die KI nicht
  generiert, sondern bewertet. Die 5 Achsen kommen aus
  der OdyC-Methodik (strukturelle Qualitätsprüfung).


───── PERSONA-HINWEISE ─────

  (P) Pragmatiker — nutzen vorhandenes Material weiter
  (S) Skeptiker   — klare Diagnose statt KI-Neuschrift
  (V) Verweigerer — Kontrolle bleibt beim Menschen


───── ARBEITSPHASE  (3 Min) ─────

# »Bringen Sie einen eigenen Text (Entwurf, Rundmail,

# Arbeitsblatt). Die KI sagt Ihnen, wo Sie nachschärfen.«

  [Optional: 3 Min Zeit für Demo mit eigenem Material]


───── ABSCHLUSS / ÜBERGANG ─────

# »Jetzt kommt ein Werkzeug, das nicht nur prüft,

# sondern zwei KIs nebeneinander arbeiten lässt —

# für Beratungsvorbereitung.«

────── Ende Karte 5 ──────

""")
    return "\n".join(out)


def render_karte_6():
    card_id = "6"
    naheliegend = TRI["cards"][card_id]["naheliegend"][:1]

    out = ["""════════════════════════════════════════════════════════════════
KARTE 6 — AUSBILDUNGSBERATUNG VORBEREITEN
Zeitbedarf: 10 Min  |  Zustand: Diagnostisch → Beratungsvorbereitet
════════════════════════════════════════════════════════════════

VORBEREITUNG
  ☐ Karte 6 geöffnet
  ☐ ChatGPT UND Claude in zwei Tabs (für Triangulation live)

───── EINSTIEG  (2 Min) ─────

# »Beratung heißt: Sie führen ein Gespräch. Die KI

# führt keines. Aber sie hilft Ihnen, sich vorzubereiten.

# Und besonders gut: Zwei KIs parallel zu fragen. Wo

# beide übereinstimmen, sind Sie auf sicherem Grund.

# Wo sie abweichen, lohnt sich ein zweiter Gedanke.«

  !!!  KEINE Personendaten — pseudonymisieren ist Pflicht
  !!!  Zielkompetenzen ≠ Ist-Stand des Azubis
       (häufiges KI-Missverständnis)
  !!!  Triangulation über 2 KIs: Konsens = solide,
       Divergenz = eigenes Nachdenken
  !!   KI liefert Orientierung, KEINE Diagnose
  !    Anti-Kontaminations-Regel: nicht dieselbe KI zweimal
  ○    Cowork-Profile mit about-me.md (siehe Doku)


───── HAUPTINHALT — Live-Demo  (5 Min) ─────

  UI-Eingaben:

    1. Beruf:             [FACHKRAFT FÜR LAGERLOGISTIK]
    2. Kontext/Phase:     [AZUBI 2. LEHRJAHR]
    3. Anlass:            [LEISTUNGSABFALL ODER AUFFÄLLIGKEIT]
    4. Beobachtete Situation (pseudonymisiert, 2-3 Sätze):
       [SEIT 3 WOCHEN HÄUFIG UNPÜNKTLICH, KOMMISSIONIER-
        LEISTUNG NACHGELASSEN, WIRKT MÜDE IN TEAMGESPRÄCHEN]

  Klick [Prompt erzeugen]
  Den Prompt AN CHATGPT UND CLAUDE SCHICKEN (parallel)
  Beide Antworten nebeneinander stellen

  !!!  Situation IMMER ohne Klarnamen, Geburtsdatum, Firma
  !!   Prompt enthält Zielkompetenzen (mit „noch nicht vorausgesetzt")
  !    Claude und ChatGPT stellen oft unterschiedliche Rückfragen
       — beide nutzen

"""]

    if naheliegend:
        fall = naheliegend[0]
        v2_resp = load_v2_response(card_id, fall["label"])
        out.append("───── BEISPIEL (aus V2-Empirie, nur eine KI gezeigt) ─────")
        out.append("")
        out.append(render_beispiel(fall, card_id, v2_resp))
        out.append("")
        out.append("""  Für den Workshop: nebeneinander zeigen, wo die zwei KIs
  übereinstimmen (Konsens = solide) und wo sie divergieren
  (Divergenz = Gesprächsanker).

""")

    out.append("""───── AUSWERTUNGSLOGIK ─────

  WENN  »KI stellt Diagnosen/Etiketten auf die Person«
  DANN  Re-Prompt mit ›Keine Diagnose, nur Orientierung‹
        (steht bereits im Prompt, aber KI ignoriert gelegentlich).

  WENN  »Zwei KIs geben komplett unterschiedliche Antworten«
  DANN  Divergenz ist Info, nicht Fehler. Teilnehmer fragen:
        welche der beiden Perspektiven passt besser zum Azubi?


───── ESKALATION ─────

  FRAGE »Ist das nicht Datenschutzverstoß?«
   ┬ ESK-1  Nicht, wenn pseudonymisiert. Keine Klarnamen, keine
            eindeutigen Merkmale.
   ┼ ESK-2  Situation generisch beschreiben reicht oft. „Ein
            Azubi, 2. LJ, FLL, seit 3 Wochen unpünktlich" — das
            kann auf hundert Personen zutreffen.
   ┴ ESK-3  Bei unsicheren Fällen: gar nicht in die KI. Zurück
            zum Tel mit Ausbildungsberater/in.

  FRAGE »Kann mir die KI Diagnosen ersparen?«
   ┬ ESK-1  Nein. Diagnose ist Menschen-Arbeit. KI gibt Struktur.
   ┼ ESK-2  Nutzen Sie die KI für Gesprächsfragen und Hypothesen —
            nicht für Entscheidungen.
   ┴ ESK-3  Wenn Sie unsicher sind, rufen Sie den IHK-Ausbildungs-
            berater an. Das ist sein Job.


───── FACHBEGRIFF ─────

  TRIANGULATION — Denselben Prompt an zwei (oder mehr) KIs
  schicken. Konsens = belastbare Orientierung. Divergenz =
  Punkt zum Selber-Nachdenken.

  ZIELKOMPETENZEN — Kompetenzen, die in der Ausbildung
  ERARBEITET werden (laut BerufeNet/KMK-Lehrplan). Der
  Azubi bringt sie NICHT schon mit. Lücken sind normal.


───── PERSONA-HINWEISE ─────

  (P) Pragmatiker — Vorbereitung in 5 Min statt 20
  (S) Skeptiker   — KI gibt Orientierung, nicht Diagnose —
                    genau was er will
  (V) Verweigerer — reine Vorbereitung, Gespräch führt der Mensch


───── ARBEITSPHASE  (3 Min) ─────

# »Formulieren Sie einen Beratungsfall aus Ihrem

# Alltag — pseudonymisiert. Prompt an 2 KIs. Vergleichen.«

  [Timer 3 Min, Paarvergleich im Edupad]


───── ABSCHLUSS / ÜBERGANG ─────

# »Jetzt Prüfungsvorbereitung — Karte 7.«

────── Ende Karte 6 ──────

""")
    return "\n".join(out)


def render_karte_7():
    card_id = "7"
    naheliegend = TRI["cards"][card_id]["naheliegend"][:1]

    out = ["""════════════════════════════════════════════════════════════════
KARTE 7 — FACHGESPRÄCHE & PRÜFUNGSVORBEREITUNG
Zeitbedarf: 10 Min  |  Zustand: Beratungsvorbereitet → Prüfungs-Coach
════════════════════════════════════════════════════════════════

VORBEREITUNG
  ☐ Karte 7 geöffnet
  ☐ Prüfungsteil-Dropdown und Schwierigkeitsstufen-Dropdown bereit

───── EINSTIEG  (2 Min) ─────

# »IHK-Prüfungskataloge sind urheberrechtlich geschützt —

# ich darf sie nicht in die App einbauen. Aber der KMK-

# Rahmenlehrplan ist frei. Und die KI kann im Geist

# dieses Lehrplans Übungsfragen erzeugen. Nicht als

# Katalogersatz — als Trainingsmaterial.«

  !!!  IHK-AkA-Prüfungskataloge NICHT in KI einbauen (urheberrechtlich)
  !!!  Lernfeld-Volltext aus KMK-RLP ist gemeinfrei — wird
       automatisch in den Prompt eingebettet
  !!!  Schwierigkeitsstufen: Grundkenntnisse · Vertiefung ·
       Transferleistung
  !!   Beruf-spezifisch kalibriert: Transfer für FL ≠ Transfer
       für Spedition
  !    AkA-Katalog 2. Auflage Winter 2025/26 bleibt Referenz —
       via u-form-shop.de
  ○    Format: offene Fragen, MC, Fallstudie, gemischt


───── HAUPTINHALT — Live-Demo  (5 Min) ─────

  UI-Eingaben:

    1. Beruf:             [FACHKRAFT FÜR LAGERLOGISTIK]
    2. Lernfeld:          [LF 5 — GÜTER KOMMISSIONIEREN (2. LJ)]
    3. Prüfungsteil:      [ABSCHLUSSPRÜFUNG TEIL 2]
    4. Schwierigkeitsstufe: [TRANSFERLEISTUNG]
    5. Anzahl Fragen:     [5]
    6. Format:            [FALLSTUDIE + TEILFRAGEN]

  Klick [Prompt erzeugen] → Prompt enthält Lernfeld-Volltext
  Klick [Kopieren] → KI erzeugt 5 Fragen mit Kernpunkten + Nachfragen

  !!!  Lernfeld wählen ist Pflicht — sonst halluziniert die KI LF-Nummern
  !!   Lernfeld-Guard im Prompt: KI darf nur innerhalb der
       max. LF des Berufs bleiben

"""]

    if naheliegend:
        fall = naheliegend[0]
        v2_resp = load_v2_response(card_id, fall["label"])
        out.append("───── BEISPIEL (aus V2-Empirie) ─────")
        out.append("")
        out.append(render_beispiel(fall, card_id, v2_resp))
        out.append("")

    out.append("""───── AUSWERTUNGSLOGIK ─────

  WENN  »Fragen zu leicht oder zu schwer für den Prüfungsteil«
  DANN  Stufe (Grund/Vertiefung/Transfer) wechseln.
        Ggf. Anzahl reduzieren (5 statt 10) für bessere Qualität.

  WENN  »KI nennt Lernfelder, die es im Beruf nicht gibt«
  DANN  Sollte in V2 nicht mehr passieren (Lernfeld-Guard wirkt).
        Falls doch: nochmaliges Generieren.


───── ESKALATION ─────

  FRAGE »Kann ich die Fragen 1:1 in der Prüfung stellen?«
   ┬ ESK-1  Übungsfragen — nicht Klausur. Als Trainingsmaterial
            prima, nicht als IHK-Ersatz.
   ┼ ESK-2  Die KI kennt den AkA-Katalog NICHT — sie arbeitet
            im Geist des Lehrplans.
   ┴ ESK-3  Für echte Prüfungen: AkA-Katalog 2. Auflage beim
            u-form-shop.de kaufen.


───── FACHBEGRIFF ─────

  LERNFELD — Strukturelement des KMK-Rahmenlehrplans.
  Jeder Beruf hat 8-13 Lernfelder, verteilt auf 2-3 Lehrjahre.
  Jedes Lernfeld hat einen Zeitrichtwert in Stunden.

  SEMANTISCHE STUFEN:
  - Grundkenntnisse — Faktenabfrage
  - Vertiefung — Zusammenhänge, Verfahren
  - Transferleistung — neue Situation, Abwägung


───── PERSONA-HINWEISE ─────

  (P) Pragmatiker — 5 Übungsfragen in 3 Minuten
  (S) Skeptiker   — Urheberrecht klar getrennt (AkA vs. KMK-RLP)


───── ARBEITSPHASE  (3 Min) ─────

# »Wählen Sie einen Beruf und ein Lernfeld. Bauen Sie

# 5 Fragen. Lesen Sie einen Satz — passt er zum Niveau?«

  [Timer 3 Min]


───── ABSCHLUSS / ÜBERGANG ─────

# »Letzte Karte: Was speichern Sie sich — und wie

# nehmen Sie alles offline mit?«

────── Ende Karte 7 ──────

""")
    return "\n".join(out)


KARTE_8 = """════════════════════════════════════════════════════════════════
KARTE 8 — EIGENE PROMPTS + OFFLINE-KOPIE
Zeitbedarf: 5 Min  |  Zustand: Prüfungs-Coach → Dauerhaft-Befähigt
════════════════════════════════════════════════════════════════

VORBEREITUNG
  ☐ Karte 8 geöffnet
  ☐ Offline-Kopie-Button selbst schon einmal gedrückt

───── EINSTIEG + HAUPTINHALT  (5 Min) ─────

# »Was Sie heute gebaut haben, bleibt bei Ihnen.

# Alles, was Sie in die App tippen, speichert nur

# Ihr eigener Browser. Kein Server. Keine Konten.«

  !!!  Daten verlassen das Gerät nicht (localStorage/IndexedDB)
  !!!  Offline-Kopie-Button erzeugt eine vollständige HTML-Datei
       (~440 KB) — funktioniert ohne Internet
  !!   Eigene Prompts speichern (Titel + Text) — für jede Karte
  !    Prüfmodus-Karte (operator-card.html) — weiterführendes Werkzeug
  ○    Cowork-Profile mit about-me.md als nächste Stufe (Doku)

  [Live: Eigener Prompt speichern → Offline-Kopie herunterladen
   → Datei öffnen → zeigen, dass alle Karten + eigene Prompts da sind]


───── ESKALATION ─────

  FRAGE »Auf iPhone/iPad — funktioniert das?«
   ┬ ESK-1  Safari: Teilen-Menü → In Dateien sichern.
   ┼ ESK-2  Android Chrome: Drei-Punkte-Menü → Zum Startbildschirm.
   ┴ ESK-3  Details im Footer der App.


───── PERSONA-HINWEISE ─────

  (P) Pragmatiker — eine Datei, fertig
  (V) Verweigerer — keine Abhängigkeit vom Internet


───── ABSCHLUSS / ÜBERGANG ─────

# »Wir haben alles durch. Zeit für Fragen.«

────── Ende Karte 8 ──────

"""

ABSCHLUSS = """════════════════════════════════════════════════════════════════
ABSCHLUSS
Zeitbedarf: 5 Min  |  Zustand: Dauerhaft-Befähigt → Entlassen
════════════════════════════════════════════════════════════════

# »Was Sie heute gesehen haben, läuft komplett in

# Ihrem Browser. Es kostet nichts — außer dem KI-Account,

# den Sie ohnehin haben. Es ist auf diese fünf Berufe

# zugeschnitten. Und es wird weitergepflegt.«

  !!!  URL wiederholen: jako-odyc.github.io/prompt-dash/ausbildungscoach/
  !!!  QR-Code nochmal zeigen
  !!   Doku-Link (/ausbildungscoach/doku/) für Fragen nach dem Workshop
  !    Kontakt: jaro_kois@web.de
  !    Einladung zur Rückmeldung: welche Karte fehlt noch? welcher Beruf?
  ○    Erwähnung nächster Workshops / Materialgenerator


───── EMPIRIE-KURZFASSUNG (für Fragen) ─────

  Das Werkzeug wurde mit 270 Triangulations-Runs gegen
  3 KIs getestet (GPT-5, Claude Sonnet 4, DeepSeek).

  Anti-Halluzinations-Regeln wurden in einer zweiten
  Runde (V2) mit 45 Runs verifiziert:
  - Duzen-Rate fiel von 47 % auf 9 %
  - Erfundene Paragraphen: praktisch verschwunden
  - Lernfeld-Halluzinationen: 0 (Guard wirkt)
  - Kosten Empirie: ca. 15 €

  Wissenschaftliche Basis: OdyC-Framework (EXP-001-Sonde).


# »Vielen Dank für Ihre Zeit — bitte kurz Feedback im

# Edupad.«

────── Ende Workshop ──────

"""


# --- Handout Teil II: Fall-Sammlung ---

def render_handout(tri):
    out = []
    out.append("""
════════════════════════════════════════════════════════════════════════
                          TEIL II — TEILNEHMER-HANDOUT
                 Fall-Sammlung zum Durchprobieren
════════════════════════════════════════════════════════════════════════

Alle Fälle hier stammen aus der Triangulation dreier KIs (GPT-5,
Claude Sonnet 4, DeepSeek) — keine erfundenen Szenarien, sondern
Alltags-Konstellationen, die die KIs übereinstimmend als
realistisch vorgeschlagen haben.

Anleitung:
  1. Einen Fall auswählen (oder eigenen Beruf/eigenes Thema).
  2. Ausbildungscoach öffnen, passende Karte.
  3. UI-Felder mit den unten angegebenen Werten füllen.
  4. Prompt erzeugen, in Ihre KI einfügen, Ergebnis prüfen.
  5. Drei Fragen notieren:
     - Klingt das nach Ihrem Betrieb?
     - Was würden Sie ändern vor dem Einsatz?
     - Wo vertrauen Sie der KI, wo nicht?

""")
    for card_id in ["4a", "4b", "5", "6", "7"]:
        card_title = {
            "4a": "Karte 4a — Unterweisungen §12 ArbSchG",
            "4b": "Karte 4b — Einweisungen (informell)",
            "5": "Karte 5 — Material-Zustandsprüfung",
            "6": "Karte 6 — Beratungsvorbereitung",
            "7": "Karte 7 — Prüfungsfragen",
        }[card_id]
        out.append(f"════════════════════════════════════════════════════════════════════════")
        out.append(f"{card_title.upper()}")
        out.append(f"════════════════════════════════════════════════════════════════════════")
        out.append("")
        for i, case in enumerate(tri["cards"][card_id]["naheliegend"], 1):
            out.append(f"──── Fall {i}: {case.get('label','?')} ────")
            out.append("")
            for k, v in case.items():
                if k in ("label", "nature"):
                    continue
                label_map = {
                    "beruf_key": "Beruf",
                    "lehrjahr": "Lehrjahr",
                    "lf_nr": "Lernfeld-Nummer",
                    "sprache": "Sprachniveau (mündlich)",
                    "schrift": "Schriftsprache",
                    "taetigkeit": "Tätigkeit / Thema",
                    "thema": "Gerät / Ablauf",
                    "umfang": "Umfang",
                    "rolle": "Rolle der Zielperson",
                    "zweck": "Zweck des Materials",
                    "text": "Zu analysierender Text",
                    "context": "Kontext / Phase",
                    "anlass": "Anlass",
                    "situation": "Beobachtete Situation",
                    "pruefung": "Prüfungsteil",
                    "stufe": "Schwierigkeitsstufe",
                    "anzahl": "Anzahl Fragen",
                    "format": "Format",
                    "kontext": "Besonderheiten",
                }
                label = label_map.get(k, k)
                vs = str(v)
                if len(vs) < 60:
                    out.append(f"  {label:30s} [{vs.upper()}]")
                else:
                    # Langer Text → mehrzeilig, eingerückt
                    out.append(f"  {label}:")
                    for line in vs.split("\n"):
                        out.append(f"    {line}")
            out.append("")
        out.append("")
    return "\n".join(out)


# --- Karte-3-Kreativ als Teil III ---

KARTE_3_KREATIV = """
════════════════════════════════════════════════════════════════════════
                 TEIL III — KARTE 3 KREATIV (10 Anwendungen)
════════════════════════════════════════════════════════════════════════

Die Begriffssuche in Karte 3 kann mehr als Suchen. Zehn fertige
Prompt-Vorlagen zum Kopieren, jede mit einem passenden
Use-Case-Schema.


──── 1. Lernfeld-Überblick ────

"Wo kommt der Begriff X im Lehrplan aller 5 Berufe vor?"

Workflow:
  1. In Karte 3 den Begriff suchen.
  2. Trefferverteilung über Berufe ablesen.
  3. Passende Treffer in den Volltext aufklappen.
  4. Gewünschten Lernfeld-Abschnitt kopieren.

Prompt zum Kopieren:

    Du bist Ausbildungsexperte. Ich habe in Rahmenlehrplänen nach
    "[BEGRIFF]" gesucht und folgende Trefferstellen gefunden — was
    verbindet diese Vorkommen inhaltlich, und was sind die typischen
    Lernziele?

    Treffer 1 (Beruf: [BERUF]):
    [AUSZUG EINFÜGEN]

    Treffer 2 (Beruf: [BERUF]):
    [AUSZUG EINFÜGEN]

    AUFGABE: Destilliere 3-5 gemeinsame Kernkompetenzen, die mit
    diesem Begriff verbunden sind. Nenne Unterschiede zwischen
    den Berufen.


──── 2. Prüfungsrelevanz-Check ────

"Ist dieses Thema prüfbar — und auf welcher Stufe?"

Prompt zum Kopieren:

    Ich prüfe einen Azubi und frage mich, ob "[THEMA]"
    prüfungsrelevant ist. Der Rahmenlehrplan enthält folgende Stelle:

    [AUSZUG EINFÜGEN]

    AUFGABE:
    - Ist dieses Thema eher Zwischenprüfung oder Abschlussprüfung?
    - Auf welcher Schwierigkeitsstufe wird es erwartet
      (Grundkenntnisse, Vertiefung, Transfer)?
    - Welche 3 typischen Prüfungsfragen könnten daraus entstehen?


──── 3. Lehrplan-Lücken-Check ────

"Was SOLLTE im Lehrplan stehen, aber fehlt?"

Beispiele für produktive Lücken-Suchen:
  - "KI" → meist 0 Treffer (obwohl im Berufsalltag relevant)
  - "Datenschutz" → meist schwach vertreten
  - "Nachhaltigkeit" → variiert stark

Prompt zum Kopieren:

    Im Rahmenlehrplan für [BERUF] gibt es keine oder nur rand-
    ständige Erwähnungen von "[BEGRIFF]", obwohl das Thema im
    Berufsalltag zunehmend wichtig wird.

    AUFGABE:
    - Begründe, warum das Thema trotzdem in die Ausbildung gehört.
    - Welche bestehenden Lernfelder könnten erweitert werden?
    - Entwirf 2-3 informelle Ergänzungsmodule (je 30-45 Min),
      die das Thema einbinden.


──── 4. Berufs-Differenzierung ────

"Was heißt X in Beruf A vs. Beruf B?"

Prompt zum Kopieren:

    Der Begriff "[BEGRIFF]" kommt in den Rahmenlehrplänen für zwei
    verschiedene Berufe vor, aber mit unterschiedlicher Bedeutung.

    Beruf A ([NAME]):
    [AUSZUG]

    Beruf B ([NAME]):
    [AUSZUG]

    AUFGABE:
    - Was ist der Bedeutungsunterschied?
    - Welche typischen Missverständnisse entstehen, wenn ein Azubi
      des einen Berufs das Konzept des anderen überträgt?
    - Entwirf eine 5-Minuten-Erklärung, die beide Varianten auseinanderhält.


──── 5. Fachsprache-Alltagswort-Brücke ────

"Mein Azubi sagt 'Stapler' — der Lehrplan sagt 'Flurförderzeug'.
Wie erkläre ich den Unterschied?"

Prompt zum Kopieren:

    Azubis bringen oft Alltagsbegriffe mit, die im Rahmenlehrplan
    durch Fachwörter ersetzt sind.

    Alltagswort: "[ALLTAGSWORT]"
    Fachwort im Lehrplan: "[FACHWORT]"
    Zusammenhang laut RLP: [AUSZUG]

    AUFGABE:
    - Formuliere eine Brücken-Erklärung (3 Sätze), die Alltagswort
      und Fachwort verbindet.
    - Warum benutzt der Lehrplan nicht das Alltagswort? Welche
      Präzision geht verloren/gewonnen?
    - Gib dem Azubi eine Merkhilfe.


──── 6. Volltext als Prompt-Kontext ────

Direkte Übergabe — selten nötig (Karten 4/7 machen das automatisch),
aber für Experimente:

Prompt zum Kopieren:

    Du erstellst eine Unterweisung. Der zugrundeliegende Lernfeld-
    Kontext ist:

    LERNFELD-AUSZUG:
    [VOLLTEXT EINFÜGEN — 500-1500 Zeichen]

    ZIELGRUPPE: [Beruf, Lehrjahr, Sprachniveau]
    TÄTIGKEIT: [konkret]

    AUFGABE: [Entwurf nach Standardstruktur]


──── 7. Unterweisungs-Themenliste generieren ────

Prompt zum Kopieren:

    Aus dem Lernfeld "[LERNFELD-TITEL]" sollen praxisnahe Unter-
    weisungsthemen abgeleitet werden.

    LERNFELD-INHALT:
    [AUSZUG]

    AUFGABE:
    - Liste 8-10 konkrete Unterweisungsthemen (je 1 Zeile).
    - Ordne sie nach Sicherheitsrelevanz: Pflicht (§12 ArbSchG),
      empfohlen, optional.
    - Markiere jedes Thema mit einer geschätzten Unterweisungsdauer
      (5/15/30 Min).


──── 8. Zwischen- vs. Abschlussprüfungs-Mapping ────

Prompt zum Kopieren:

    Aus dem Rahmenlehrplan für [BERUF] möchte ich eine Übersicht,
    welche Lernfelder in welcher Prüfungsphase relevant sind.

    Lernfeld-Titel und Inhalt aus RLP:
    [TEXT DER LF 1-4 (optional) ODER 5-8 ODER 9-12]

    AUFGABE:
    - Tabelle: Lernfeld | Prüfungsphase (ZP/AP1/AP2/AP) |
      Gewichtung (Schätzung)
    - 3 Lernfelder, die erfahrungsgemäß am häufigsten in
      Prüfungen auftauchen
    - 1 Lernfeld, das oft unterschätzt wird


──── 9. Didaktik-Brücke ────

"Finde Alltagsbeispiele zu abstraktem Begriff"

Prompt zum Kopieren:

    Ein Azubi versteht "[BEGRIFF]" nicht in der abstrakten Form,
    wie es der Lehrplan formuliert:

    RLP-DEFINITION:
    [AUSZUG]

    AUFGABE:
    - 3 Alltagsbeispiele, die den Begriff erfahrbar machen
      (je 2-3 Sätze).
    - 1 Lageralltags-Beispiel für den konkreten Beruf [BERUF].
    - 1 Merkhilfe (z. B. Metapher, Akronym, Bild).


──── 10. Zeitplanung der Ausbildung ────

Prompt zum Kopieren:

    Aus dem Rahmenlehrplan für [BERUF] habe ich folgende
    Zeitrichtwerte extrahiert:

    [LISTE: LF 1 – 60 Std, LF 2 – 80 Std, LF 3 – 40 Std, ...]

    AUFGABE:
    - Berechne, wie viele Unterrichtsstunden pro Woche das bedeutet
      (bei 3 Lehrjahren, 40 Schulwochen).
    - Welche Lernfelder sind besonders zeit-intensiv und sollten
      früh angegangen werden?
    - Schlage eine Reihenfolge für die betriebliche Unterweisung
      vor, die zur schulischen Reihenfolge passt.

"""


def main():
    parts = []
    parts.append(f"""ausbildungscoach — workshop-präsentationsskript
================================================

version 1.1.0  |  stand 2026-04-19
empirie-basis: 270 v1-runs + 45 v2-runs (triangulation gegen 3 KIs)
kosten experiment: ca. 15 EUR

dieses skript ist in drei teile gegliedert:

  TEIL I   — präsentationsskript (karten 0 bis 8 + einstieg + abschluss)
  TEIL II  — teilnehmer-handout mit fall-sammlung
  TEIL III — karte-3-kreativ: 10 prompt-vorlagen zum mitnehmen

druckempfehlung: a4 hochformat, einseitig, serifenlose schrift,
sprechtext-überschriften (# »...«) automatisch groß.

""")
    parts.append(LEGENDE)
    parts.append("")
    parts.append("════════════════════════════════════════════════════════════════════════")
    parts.append("                           TEIL I — PRÄSENTATIONSSKRIPT")
    parts.append("════════════════════════════════════════════════════════════════════════")
    parts.append("")
    parts.append(KARTE_0)
    parts.append(KARTE_1)
    parts.append(KARTE_2)
    parts.append(KARTE_3)
    parts.append(render_karte_4a())
    parts.append(render_karte_4b())
    parts.append(render_karte_5())
    parts.append(render_karte_6())
    parts.append(render_karte_7())
    parts.append(KARTE_8)
    parts.append(ABSCHLUSS)
    parts.append("")
    parts.append(render_handout(TRI))
    parts.append(KARTE_3_KREATIV)

    text = "\n".join(parts)
    OUT.write_text(text, encoding="utf-8")
    lines = text.count("\n")
    size_kb = len(text.encode("utf-8")) // 1024
    print(f"Generiert: {OUT}")
    print(f"  Zeilen: {lines}")
    print(f"  Groesse: {size_kb} KB")


if __name__ == "__main__":
    main()
