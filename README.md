# Agent Skills

Practical skills for AI agents: instructions, scripts, templates, and checks that can be reused across projects.

Developed with assistance from OpenAI Codex.

[Русский](README.ru.md) · [Contributing](CONTRIBUTING.md) · [MIT license](LICENSE)

[English](readme/README.en.md) · [中文](readme/README.zh.md) · [हिन्दी](readme/README.hi.md) · [Español](readme/README.es.md) · [العربية](readme/README.ar.md) · [Français](readme/README.fr.md) · [Português](readme/README.pt.md) · [Русский](readme/README.ru.md) · [বাংলা](readme/README.bn.md) · [Deutsch](readme/README.de.md)

## Catalog

| Skill | What it does | Language / requirements |
|---|---|---|
| [build-agent-context](skills/build-agent-context/) | Turns archives, documents, messages, links, or a repository into task-focused agent context with source traceability, reading routes, current state, and handoff checks | User's language; Markdown; source-reading tools depend on input formats |
| [gost-7-32-2017-latex](skills/gost-7-32-2017-latex/) | Creates and reviews research reports in LaTeX using GOST 7.32-2017: title pages, structure, equations, tables, references, appendices, and PDF checks | Russian; Python 3.10+ and XeLaTeX or LuaLaTeX; optional `pdfplumber` |

Each skill is a separate folder with a `SKILL.md` entrypoint. Its scripts and resources live alongside it.

## Install in Codex

Ask Codex to install the skill from its GitHub folder:

```text
Use $skill-installer to install https://github.com/Girday/agent-skills/tree/main/skills/gost-7-32-2017-latex
```

Alternatively, clone the repository and install a local copy:

```bash
git clone https://github.com/Girday/agent-skills.git
cd agent-skills
python3 scripts/install.py gost-7-32-2017-latex
```

The local installer uses `$CODEX_HOME/skills`, or `~/.codex/skills` when `CODEX_HOME` is unset. It refuses to overwrite an existing installation. An installed copy is independent of the checkout; repository updates do not replace it automatically. If the skill does not appear, restart Codex. See the [official skill documentation](https://learn.chatgpt.com/docs/build-skills) for discovery and distribution options. This repository supplies skill sources; it is not a published plugin-directory listing.

Other agents can use the instructions and resources if they support the `SKILL.md` format. Codex-specific desktop tools are optional conveniences, with a command-line workflow provided as a fallback.

## Prepare agent context

Install `build-agent-context` with the same installer, using its catalog name or GitHub folder, then ask:

```text
Use $build-agent-context. Prepare context from this archive so another agent
can continue work on the project. Include the current requirements, evidence,
unresolved conflicts, and a starting prompt. The receiving agent can read files.
```

The skill chooses between a self-contained document and a short entrypoint with topic files. It records what was actually read, preserves source locators, and distinguishes requirements, verified facts, assumptions, and current progress. It also handles updates to existing context. It has no mandatory runtime dependency; archives, scans, and other formats require suitable reading tools in the agent's environment.

- [Research behind the workflow: 12 selected publications](skills/build-agent-context/references/research.md)
- [Output patterns and worked examples](skills/build-agent-context/references/output-patterns.md)
- [Quality checks and behavioral evaluation scenarios](skills/build-agent-context/references/quality-checks.md)
- [Validation performed and limitations](skills/build-agent-context/references/validation.md)

## Use the GOST skill

```text
Используй $gost-7-32-2017-latex. Подготовь отчёт по приложенным материалам,
собери PDF и проверь оформление. Требования учебного заведения приложены отдельно.
```

For a direct command-line workflow after cloning:

```bash
python3 skills/gost-7-32-2017-latex/scripts/init_project.py ./my-report
# Fill in my-report/metadata.tex and replace the demonstration content.
python3 skills/gost-7-32-2017-latex/scripts/build.py ./my-report
python3 skills/gost-7-32-2017-latex/scripts/audit.py ./my-report
```

The starter intentionally contains unfilled fields. Its audit should fail until those fields are completed. Install `pdfplumber` in your Python environment to enable PDF geometry checks; without it, those checks are marked `NOT_CHECKED`.

- [View an eight-page example](examples/gost-7-32-2017/example.pdf)
- [Read the requirements map](skills/gost-7-32-2017-latex/references/requirements.md)
- [See verified behavior and limitations](skills/gost-7-32-2017-latex/references/validation.md)

GOST 7.32-2017 covers research reports. Applying it to coursework is an adaptation that must account for institutional requirements. The skill distinguishes requirements, recommendations, permitted alternatives, and template choices. Automated checks assist review; they do not certify a report or confirm signatures, registration, or institutional approval. A3 and multi-volume workflows are documented but have not been separately exercised in the initial template validation.

## Development

```bash
python3 -m venv .venv
# Activate the virtual environment using your shell's command.
python -m pip install -r requirements-dev.txt
python scripts/validate.py
python -m unittest discover -s tests -v
ruff check .
ruff format --check .
```

The LaTeX integration test runs when XeLaTeX is available and otherwise reports a skip. GitHub Actions validates the source collection and Python tests; it does not render or certify generated reports.

## License and sources

Original instructions, analysis, code, and templates in this repository are available under the [MIT license](LICENSE). Referenced standards, documentation, and fonts retain their respective rights. The official GOST text and proprietary fonts are not bundled or relicensed. Source links and the reviewed edition are recorded [with the skill](skills/gost-7-32-2017-latex/references/sources.md).
