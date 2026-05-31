# Klausur-Referenz-Orakel (Wächter)

Unabhängige Zweitimplementierung des **Datenkerns** des Klausur-Rückmeldung-Tools
(`klausur-rueckmeldung/index.html`) — für **Differential Testing**.

Das Orakel implementiert die *korrekte* Spec direkt (KMK-Notenpunkt-Tabelle, FQ-Abzug
≥3→−1 / ≥6→−2, LRS-Notenschutz, BE = Summe der Kriterien, FQ aus der Formel rekonstruiert,
wenn der Zell-Cache leer ist). Es macht **bewusst nicht** die Heuristiken des JS-Tools nach —
so machen beide *verschiedene* Fehler, und jede Abweichung ist ein Befund.

Reine Python-stdlib (`zipfile` + `re`), keine Abhängigkeiten.

## Nutzung

```bash
python oracle.py                          # Default: C:\Users\Jaro\Downloads\Klausur*.xlsx
python oracle.py pfad\zur\datei.xlsx      # einzelne Datei
python oracle.py pfad\zum\ordner          # alle *.xlsx im Ordner
```

Ausgabe pro Schüler: `BE  %  LRS  FQ  | NP stored=… computed=…`.
Eine Zeile `<-- computed != stored!` = die gespeicherte Note weicht von dem ab,
was die Regeln aus BE+FQ+LRS ergeben → **menschlich prüfen** (entweder bewusster
Lehrer-Override oder eine veraltete/zu früh gesetzte Note).

## Zwei Prüfebenen

1. **Standalone-Regelprüfung** (nur Python): `computed == stored?` für jede Note.
   Findet z. B. Noten, deren FQ-Abzug fehlt, weil die FQ nach der Note geändert wurde.
2. **Browser-Differential** (Orakel vs. JS-Tool): denselben Excel in beiden laden,
   Schülerset + BE + gespeicherte NP vergleichen. Validiert das *Parsen* des Tools.
   (`oracle-result.json` aus Lauf 1 + ein kleiner `preview_eval`-Vergleich.)

## Belegte Befunde (2026-05-31)

- **Validierung v23.5**: Differential = **0 Divergenzen** (Schülerset/BE/NP) → der
  „BE = 0 / Cha verschollen"-Fix ist unabhängig bestätigt.
- **Reality-Check**: ein erster „FQ-Bug" war ein **Blindfleck des Orakels** (es las nur
  den leeren Formel-Cache), nicht des Tools — das JS-Tool decodiert die FQ-Formel korrekt.
  Lehre: das Orakel muss mindestens so fähig sein wie das Tool, sonst Fehlalarme.
- **Echter Befund**: `Her` (stored 5 NP) ≠ Regeln (4 NP, FQ 5,417) — vom Tool-Readout
  *selbst* bestätigt. Beispiel einer veralteten Note, die der Wächter fängt.
