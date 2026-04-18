# Simulation: 4 Ausbilder-Profile gegen den Ausbildungscoach

Stand 2026-04-18. Testmethode: Jedes Profil geht die App von Karte 1 bis 8 durch, versucht eine realistische Alltagsaufgabe zu erledigen, und stößt dabei auf Gaps. Ziel: konkrete Nachbesserungen ableiten.

---

## Profil A — Ausbilder Lagerlogistik Mittelbetrieb (Pragmatiker)

**Aufgabe:** „Ich brauche schnell eine Staplerunterweisung für den neuen Azubi Anton, FLL 1. LJ, B1."

**Durchgang:**
- **Karte 1:** Überfliegt die drei Grundwahrheiten, klickt auf Edupad aus Gewohnheit, ignoriert Doku-Link. **OK.**
- **Karte 2:** Sieht die Ampel, ok-Modell, versteht Pseudonymisierung ohne die Doku zu öffnen. **OK.**
- **Karte 3:** Sucht „Stapler", 0 Treffer. Liest den Hinweis („Kommissionierung / Flurförderzeug"), sucht „Flurförderzeug", **0 Treffer**. Frustrierend. Sucht „Güter", zu viele Treffer. **GAP 1.**
- **Karte 4:** Wählt FLL 3-jährig, LF 4 (Güter transportieren), 1. LJ, Sprachniveau B1, Schriftsprache unsicher, Tätigkeit „Staplerfahren im Schmalgang". Klickt 3 harte Checklisten-Punkte an (Gefährdungsbeurteilung, Unterweiser sachkundig, arbeitsplatzbezogen). Generiert Prompt → 3500 Zeichen, sehr ausführlich. Kopiert nach ChatGPT. ChatGPT liefert Entwurf. **Resultat brauchbar**, aber er muss die §-Blöcke am Anfang kürzen, weil ChatGPT sie in den Ausgabetext übernimmt. **GAP 2.**
- **Karte 5:** Schaut kurz rein, versteht den Zustandsprompt nicht sofort (Wort zu fachsprachlich?). Überspringt. **GAP 3.**
- **Karte 8:** Speichert seinen Prompt als „Stapler Anton". Gut.

**Fazit:** Brauchbar für eine konkrete Aufgabe. Die Begriffssuche war enttäuschend, der generierte Prompt war etwas lang, und Karte 5 hat er nicht verstanden.

**Konkrete Nachbesserungen:**
1. **GAP 1:** Im Hinweistext zur Suche die empfohlenen Begriffe nochmal prüfen — „Flurförderzeug" gibt aktuell 0 Treffer trotz der Empfehlung. Liste der „funktionieren sicher"-Begriffe direkt in den Placeholder.
2. **GAP 2:** Der Rechtsrahmen-Block im Prompt hat einen deutlichen Hinweis gefehlt: „ZITIERE DIESE RECHTSBLÖCKE NICHT WÖRTLICH IM ENTWURF — sie dienen nur deiner Orientierung." Nachzutragen.
3. **GAP 3:** Das Wort „Zustandsprompt" in Karte 5 braucht eine Klammererklärung für Erstnutzer. „Zustandsprompt (Diagnoseprüfung eines Textes)".

---

## Profil B — Ausbilder Spedition Großunternehmen (Optimierer)

**Aufgabe:** „Ich will 10 Übungsfragen zur Abschlussprüfung Teil 2, Zollabwicklung, für einen 3. LJ-Azubi. Reproduzierbar, damit ich die Vorlage weiter pflegen kann."

**Durchgang:**
- **Karte 7:** Wählt Spedition 3-jährig, LF 11 (Importaufträge), ap2, Stufe „Transfer", Anzahl 10, Format gemischt. Generiert Prompt. Lernfeld-Volltext ist dabei, semantische Stufe mit Speditions-Kalibrierung. **OK.**
- Er schickt an ChatGPT UND Claude parallel (er kennt Triangulation aus Karte 6). Beide antworten solide, mit unterschiedlichen Schwerpunkten. Er nimmt aus beiden die besten 10 Fragen. **Gutes Resultat.**
- **Karte 4:** Er klickt aus Neugier rein. Aha: Der Container-Modus wäre nützlich für komplexe Unterweisungen, er probiert aus. Diagnose + Entwurf funktionieren. **Starker Eindruck.**
- **Karte 5:** Er nutzt sie, um die ChatGPT-Ausgabe einer früheren Prüfungsaufgabe zu prüfen. Das Zustandsprompt-Konzept gefällt ihm. **Sehr positiv.**
- Footer: Findet Doku, liest Cowork-Abschnitt. Fängt an, sich ein about-me.md zu bauen. **Gewonnen.**

**Fazit:** Das Werkzeug liefert, was er braucht, und er findet ergänzende Features von selbst.

**Konkrete Nachbesserungen:**
- keine zwingenden — Profil B ist der Idealnutzer. Aber: Die Cowork-Doku könnte einen expliziten **Workshop-Bezug** bekommen („So bauen Sie sich aus diesem Workshop einen eigenen Dauer-Begleiter").

---

## Profil C — Ausbilder Büromanagement KMU (Skeptikerin, datenschutzaffin)

**Aufgabe:** „Ich will KI für Beratungsgespräche nutzen. Aber nur, wenn Datenschutz stimmt."

**Durchgang:**
- **Karte 2:** Liest Ampel, dann Word-Pseudonymisierungs-Abschnitt, klickt Doku-Link. In der Doku liest sie Abschnitt 3 und die FAQ zu DSGVO. Findet die ehrliche Antwort („nicht formal DSGVO-geprüft, klärt mit eurem DSB ab") **glaubwürdig**. Notiert: mit internem DSB sprechen. **OK.**
- **Karte 6:** Wählt Büromanagement, „Azubi 2. LJ", „Motivation / Perspektive". Tippt eine Situation in Stichworten ein (keine Namen). Generiert Prompt. Schickt an ChatGPT + Claude. Vergleicht. **Brauchbar.**
- **Karte 4:** Probiert Unterweisung „Umgang mit Reklamationen am Telefon". Der Rechtsblock §12 ArbSchG wirkt für diese Situation zu schwer — das ist keine Sicherheitsunterweisung. Sie ist verwirrt, ob Karte 4 überhaupt für sie passt. **GAP 4.**
- Wechselt zu **Modus B** (Einweisung). Dort fehlt aber das ganze Prompt-Formular, nur ein statischer Platzhalter-Prompt. Sie muss selbst anpassen. **GAP 5.**
- **Karte 8:** Speichert mehrere Prompts thematisch benannt. **Gut.**

**Fazit:** Datenschutz-Bedenken gut beantwortet. Karten 2, 6 und 8 funktionieren für sie. Aber Karte 4 ist auf Sicherheitsunterweisungen zugeschnitten und skaliert nicht nach unten.

**Konkrete Nachbesserungen:**
4. **GAP 4:** Karte 4 Modus A bekommt eine Eingangsfrage oder Heuristik: „Geht es um eine sicherheits- oder gefährdungsbezogene Tätigkeit? Wenn nein → wechseln Sie zu Modus B." Bzw. ein Hinweisbanner oben in Modus A.
5. **GAP 5:** Modus B soll ebenfalls ein Prompt-Formular bekommen (Beruf, Gerät/Ablauf, Zielgruppe, Zweck) + Generate-Button, analog zu Modus A aber ohne Rechtsblock.

---

## Profil D — Ausbilder Berufskraftverkehr (Stiller Verweigerer, älterer Ausbilder, Zeit knapp)

**Aufgabe:** „Mal sehen ob das was taugt. Ich habe 15 Minuten."

**Durchgang:**
- Öffnet die Seite auf dem Handy. **Nav scrollt am Smartphone**, viele Karten untereinander. Wirkt lang. **Mobile jetzt besser, aber immer noch viel zu lesen.**
- **Karte 1:** Liest zwei Sätze, überspringt den Rest. **Neutral.**
- **Karte 3:** Sucht „Lenkzeiten", 2 Treffer — er klickt, sieht mehr Kontext. **OK, er ist beeindruckt, dass das funktioniert.**
- **Karte 4:** Wählt BKF 3-jährig, LF 2 (Fahrzeuge pflegen), 1. LJ, Tätigkeit „Reifendruckprüfung". Überspringt Checkliste ganz. Generiert Prompt — alle 7 harten Punkte werden als offene Rückfragen formuliert. **ChatGPT fragt zu viele Dinge ab**, die für diese einfache Anweisung egal sind. Er ist genervt. **GAP 6.**
- Versucht Modus B. Static Platzhalter, er kopiert, ändert kaum was, ChatGPT liefert. **Besser.**
- Gibt nach 12 Minuten auf. Keine Speicherung. **Bestenfalls neutral.**

**Fazit:** Die App überfordert ihn. Für Erst-Nutzung auf dem Smartphone mit wenig Zeit nicht das richtige Werkzeug.

**Konkrete Nachbesserungen:**
6. **GAP 6:** In Karte 4 Modus A einen „Schnellmodus" anbieten: Ein Minimum-Prompt ohne Rechtsblock und ohne Rückfrage-Aufzählung, nur wenn der Ausbilder explizit sagt „ich bin sachkundig, los". Oder: Checklisten-Status ist standardmäßig „harte Punkte angenommen erfüllt" und kann aufgehoben werden.
7. **Mobile**: Für Erstbesuch eine Art „Kurzführung" — ein kleiner, ausblendbarer Box-Hinweis oben: „Ersten Prompt in 3 Klicks: Karte 4 → Beruf wählen → Prompt erzeugen → Kopieren." Ohne das fühlt sich die App auf dem Handy zu dicht an.

---

## Zusammenfassung der 7 Gaps

| Nr | Wo | Gap | Priorität |
|---|---|---|---|
| 1 | Karte 3 | Empfohlener Begriff „Flurförderzeug" liefert 0 Treffer | mittel |
| 2 | Karte 4 Prompt | §-Blöcke sollen nicht wörtlich im Entwurf erscheinen | **hoch** |
| 3 | Karte 5 | Wort „Zustandsprompt" braucht Klammerhilfe | klein |
| 4 | Karte 4 Modus A | Fehlt Hinweis auf Modus B für nicht-sicherheitsrelevante Themen | mittel |
| 5 | Karte 4 Modus B | Kein Prompt-Formular, nur statischer Platzhalter-Prompt | **hoch** |
| 6 | Karte 4 | Schnellmodus für erfahrene Ausbilder fehlt | mittel |
| 7 | Gesamt mobil | Kurzführung für Erstnutzer auf dem Smartphone fehlt | mittel |

**Nächste Korrekturrunde** nimmt die beiden Prio-hoch-Gaps (2 und 5) zuerst. Die anderen können als Patch-Liste gesammelt werden.
