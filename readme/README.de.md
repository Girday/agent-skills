# Agent Skills

[English](README.en.md) · [中文](README.zh.md) · [हिन्दी](README.hi.md) · [Español](README.es.md) · [العربية](README.ar.md) · [Français](README.fr.md) · [Português](README.pt.md) · [Русский](README.ru.md) · [বাংলা](README.bn.md) · [Deutsch](README.de.md)

Praktische Fähigkeiten für KI-Agenten: Anleitungen, Skripte, Vorlagen und Prüfungen zur Wiederverwendung in verschiedenen Projekten.

[Mitwirken](../CONTRIBUTING.md) · [MIT-Lizenz](../LICENSE)

## Katalog

| Fähigkeit | Zweck | Sprache und Voraussetzungen |
|---|---|---|
| [build-agent-context](../skills/build-agent-context/) | Erstellt aus Archiven, Dokumenten, Nachrichten, Links und Repositories aufgabenbezogenen Kontext mit nachvollziehbaren Quellen, Lesepfaden, Arbeitsstand und Übergabeprüfungen | Sprache des Nutzers; Markdown; Lesewerkzeuge abhängig vom Eingabeformat |
| [transcribe-recording](../skills/transcribe-recording/) | Transkribiert Besprechungen, Vorträge, Interviews und Unterricht; prüft die Sprechertrennung und erstellt Quellen mit Zeitmarken für den Kontext | Windows, Linux und macOS; faster-whisper auf CPU/CUDA, optional MLX auf Apple Silicon |
| [gost-7-32-2017-latex](../skills/gost-7-32-2017-latex/) | Erstellt und prüft Forschungsberichte in LaTeX nach GOST 7.32-2017: Titelseite, Aufbau, Gleichungen, Tabellen, Quellen, Anhänge und PDF-Prüfungen | Russische Vorlage; Python 3.10+ und XeLaTeX oder LuaLaTeX; optional `pdfplumber` |

Die Anweisungen der Fähigkeiten und die Referenzen für den Agenten werden auf Englisch gepflegt. Der Agent antwortet in der Sprache des Nutzers, sofern nichts anderes verlangt wird; die Sprache erzeugter Dateien richtet sich nach der Aufgabe. Vorgeschriebener Wortlaut aus Normen, Vorlagen oder Quellen bleibt erhalten. Die GOST-Vorlage bleibt russisch; Transkripte behalten die Sprache der Aufnahme, sofern keine Übersetzung angefordert wird.

Jede Fähigkeit liegt in einem eigenen Ordner mit `SKILL.md` als Einstieg sowie zugehörigen Skripten und Ressourcen.

## Installation in Codex

Bitten Sie Codex:

```text
Installiere mit $skill-installer https://github.com/Girday/agent-skills/tree/main/skills/gost-7-32-2017-latex
```

Alternativ klonen Sie das Repository und installieren eine lokale Kopie:

```bash
git clone https://github.com/Girday/agent-skills.git
cd agent-skills
python3 scripts/install.py gost-7-32-2017-latex
```

Der Installer verwendet `$CODEX_HOME/skills` oder, wenn `CODEX_HOME` nicht gesetzt ist, `~/.codex/skills`. Bestehende Installationen werden nicht überschrieben. Die installierte Kopie ist unabhängig vom Repository und wird nicht automatisch aktualisiert. Starten Sie Codex neu, falls die Fähigkeit nicht erscheint. Die [offizielle Dokumentation](https://learn.chatgpt.com/docs/build-skills) beschreibt Erkennung und Verteilung. Dieses Repository liefert Quelldateien; es ist kein veröffentlichter Eintrag im Plugin-Verzeichnis.

Andere Agenten können die Ressourcen nutzen, wenn sie `SKILL.md` unterstützen. Die Desktop-Werkzeuge von Codex sind optional; ein Ablauf für die Kommandozeile steht ebenfalls bereit.

## Kontext für einen Agenten vorbereiten

Installieren Sie `build-agent-context` mit demselben Installer über den Katalognamen oder GitHub-Ordner. Beispiel:

```text
Verwende $build-agent-context. Bereite aus diesem Archiv Kontext auf, damit ein
anderer Agent das Projekt fortsetzen kann. Übernimm aktuelle Anforderungen,
Quellen, offene Widersprüche und eine Startanweisung. Der Agent kann Dateien lesen.
```

Die Fähigkeit wählt zwischen einem eigenständigen Dokument und einem kurzen Einstieg mit Themendateien. Sie protokolliert tatsächlich gelesene Inhalte, erhält Quellenverweise und trennt Anforderungen, geprüfte Fakten, Annahmen und Fortschritt. Vorhandener Kontext kann aktualisiert werden. Es gibt keine zwingende Laufzeitabhängigkeit; Archive, Scans und andere Formate erfordern geeignete Lesewerkzeuge.

Grundlagen (12 ausgewählte Veröffentlichungen), Ausgabebeispiele, Qualitätskriterien, Bewertungsszenarien und Grenzen der Validierung:

- [research.md](../skills/build-agent-context/references/research.md)
- [output-patterns.md](../skills/build-agent-context/references/output-patterns.md)
- [quality-checks.md](../skills/build-agent-context/references/quality-checks.md)
- [validation.md](../skills/build-agent-context/references/validation.md)

## Die GOST-Fähigkeit verwenden

```text
Verwende $gost-7-32-2017-latex. Erstelle aus den beigefügten Unterlagen einen
Bericht, baue das PDF und prüfe die Gestaltung. Die Vorgaben der Einrichtung liegen separat bei.
```

Im Stammverzeichnis des Repositories:

```bash
python3 skills/gost-7-32-2017-latex/scripts/init_project.py ./my-report
python3 skills/gost-7-32-2017-latex/scripts/build.py ./my-report
python3 skills/gost-7-32-2017-latex/scripts/audit.py ./my-report
```

Füllen Sie nach `init_project.py` die Datei `my-report/metadata.tex` aus und ersetzen Sie vor dem Bauen die Beispielinhalte. Die Vorlage enthält bewusst leere Felder; die Prüfung muss bis zu deren Ergänzung fehlschlagen. Installieren Sie `pdfplumber` für geometrische PDF-Prüfungen. Ohne dieses Paket erhalten sie den Status `NOT_CHECKED`.

Achtseitiges Beispiel, Anforderungsübersicht und geprüfte Eigenschaften samt Grenzen:

- [example.pdf](../examples/gost-7-32-2017/example.pdf)
- [requirements.md](../skills/gost-7-32-2017-latex/references/requirements.md)
- [validation.md](../skills/gost-7-32-2017-latex/references/validation.md)

GOST 7.32-2017 gilt für Forschungsberichte. Bei Studienarbeiten müssen die Vorgaben der Einrichtung berücksichtigt werden. Die Fähigkeit unterscheidet Anforderungen, Empfehlungen, zulässige Alternativen und Vorlagenentscheidungen. Automatische Prüfungen unterstützen die Durchsicht; sie zertifizieren keinen Bericht und bestätigen weder Unterschriften noch Registrierung oder institutionelle Genehmigung. A3 und mehrbändige Berichte sind dokumentiert, wurden bei der ursprünglichen Vorlagenprüfung aber nicht gesondert getestet.

## Entwicklung

Erstellen und aktivieren Sie die virtuelle Umgebung mit dem passenden Shell-Befehl, bevor Sie Abhängigkeiten installieren und Prüfungen ausführen:

```bash
python3 -m venv .venv
python -m pip install -r requirements-dev.txt
python scripts/validate.py
python -m unittest discover -s tests -v
ruff check .
ruff format --check .
```

Der LaTeX-Integrationstest läuft bei verfügbarem XeLaTeX; andernfalls wird er übersprungen. GitHub Actions prüft die Quellen und Python-Tests, rendert oder zertifiziert aber keine erzeugten Berichte.

## Lizenz und Quellen

Eigene Anleitungen, Analysen, Programme und Vorlagen stehen unter der [MIT-Lizenz](../LICENSE). Zitierte Normen, Dokumentationen und Schriftarten behalten ihre jeweiligen Rechte. Der offizielle GOST-Text und proprietäre Schriftarten werden weder mitgeliefert noch neu lizenziert. Quellenlinks und geprüfte Ausgabe sind in [sources.md](../skills/gost-7-32-2017-latex/references/sources.md) verzeichnet.
