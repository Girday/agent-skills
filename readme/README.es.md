# Agent Skills

[English](README.en.md) · [中文](README.zh.md) · [हिन्दी](README.hi.md) · [Español](README.es.md) · [العربية](README.ar.md) · [Français](README.fr.md) · [Português](README.pt.md) · [Русский](README.ru.md) · [বাংলা](README.bn.md) · [Deutsch](README.de.md)

Herramientas prácticas para agentes de IA: instrucciones, scripts, plantillas y comprobaciones reutilizables entre proyectos.

[Contribuir](../CONTRIBUTING.md) · [Licencia MIT](../LICENSE)

## Catálogo

| Habilidad | Función | Idioma y requisitos |
|---|---|---|
| [build-agent-context](../skills/build-agent-context/) | Convierte archivos, documentos, mensajes, enlaces y repositorios en contexto para una tarea, con fuentes, rutas de lectura, estado y comprobaciones de entrega | Idioma del usuario; Markdown; herramientas de lectura según el formato |
| [transcribe-recording](../skills/transcribe-recording/) | Transcribe reuniones, ponencias, entrevistas y clases; comprueba los hablantes y prepara material con marcas de tiempo para contexto | Windows, Linux y macOS; faster-whisper en CPU/CUDA, MLX opcional en Apple Silicon |
| [gost-7-32-2017-latex](../skills/gost-7-32-2017-latex/) | Prepara y revisa informes de investigación en LaTeX según GOST 7.32-2017: portada, estructura, fórmulas, tablas, bibliografía, anexos y PDF | Plantilla en ruso; Python 3.10+ y XeLaTeX o LuaLaTeX; `pdfplumber` opcional |

Las instrucciones de las habilidades y las referencias para el agente se mantienen en inglés. El agente responde en el idioma del usuario salvo petición contraria; el idioma de los archivos generados depende de la tarea. Se conserva la redacción exacta exigida por normas, plantillas o fuentes. La plantilla GOST sigue en ruso y las transcripciones conservan el idioma de la grabación salvo que se solicite traducción.

Cada habilidad tiene su propia carpeta con un punto de entrada `SKILL.md`, scripts y recursos.

## Instalación en Codex

Pídele a Codex:

```text
Usa $skill-installer para instalar https://github.com/Girday/agent-skills/tree/main/skills/gost-7-32-2017-latex
```

También puedes clonar el repositorio e instalar una copia local:

```bash
git clone https://github.com/Girday/agent-skills.git
cd agent-skills
python3 scripts/install.py gost-7-32-2017-latex
```

El instalador utiliza `$CODEX_HOME/skills` o, si `CODEX_HOME` no está definido, `~/.codex/skills`. Rechaza sobrescribir instalaciones existentes. La copia instalada es independiente del repositorio y no se actualiza automáticamente. Reinicia Codex si la habilidad no aparece. La [documentación oficial](https://learn.chatgpt.com/docs/build-skills) describe cómo descubrir y distribuir habilidades. Este repositorio contiene fuentes; no es una entrada publicada en el directorio de plugins.

Otros agentes pueden utilizar los recursos si admiten `SKILL.md`. Las herramientas de escritorio de Codex son opcionales; también se ofrece un flujo por línea de comandos.

## Preparar contexto para un agente

Instala `build-agent-context` con el mismo instalador, indicando su nombre o carpeta de GitHub. Después, pide:

```text
Usa $build-agent-context. Prepara contexto a partir de este archivo para que otro
agente continúe el proyecto. Incluye requisitos actuales, fuentes, conflictos
pendientes y un mensaje inicial. El agente receptor puede leer archivos.
```

La habilidad elige entre un documento autosuficiente y una entrada breve con archivos temáticos. Registra qué se ha leído, conserva referencias a fragmentos originales y distingue requisitos, hechos verificados, supuestos y progreso. También actualiza contexto existente. No exige dependencias de ejecución; los archivos comprimidos, escaneos y otros formatos requieren herramientas adecuadas.

Investigación de apoyo (12 publicaciones seleccionadas), ejemplos de salida, criterios de calidad, escenarios de evaluación y límites de validación:

- [research.md](../skills/build-agent-context/references/research.md)
- [output-patterns.md](../skills/build-agent-context/references/output-patterns.md)
- [quality-checks.md](../skills/build-agent-context/references/quality-checks.md)
- [validation.md](../skills/build-agent-context/references/validation.md)

## Usar la habilidad GOST

```text
Usa $gost-7-32-2017-latex. Prepara un informe con los materiales adjuntos,
genera el PDF y revisa el formato. Los requisitos de la institución van aparte.
```

Desde la raíz del repositorio:

```bash
python3 skills/gost-7-32-2017-latex/scripts/init_project.py ./my-report
python3 skills/gost-7-32-2017-latex/scripts/build.py ./my-report
python3 skills/gost-7-32-2017-latex/scripts/audit.py ./my-report
```

Después de `init_project.py`, completa `my-report/metadata.tex` y sustituye el contenido de demostración antes de compilar. La plantilla contiene campos vacíos a propósito: la auditoría debe fallar hasta completarlos. Instala `pdfplumber` para comprobar la geometría del PDF; sin él, esas comprobaciones se marcan `NOT_CHECKED`.

Ejemplo de ocho páginas, mapa de requisitos y comportamiento verificado con sus límites:

- [example.pdf](../examples/gost-7-32-2017/example.pdf)
- [requirements.md](../skills/gost-7-32-2017-latex/references/requirements.md)
- [validation.md](../skills/gost-7-32-2017-latex/references/validation.md)

GOST 7.32-2017 se aplica a informes de investigación; su uso en trabajos académicos requiere adaptación a las normas institucionales. La habilidad distingue requisitos, recomendaciones, alternativas permitidas y decisiones de plantilla. Las comprobaciones automáticas ayudan a revisar, pero no certifican el informe ni confirman firmas, registro o aprobación institucional. Los modos A3 y de varios volúmenes están documentados, pero no se probaron por separado en la validación inicial.

## Desarrollo

Crea y activa el entorno virtual con el comando de tu shell; después instala las dependencias y ejecuta las comprobaciones:

```bash
python3 -m venv .venv
python -m pip install -r requirements-dev.txt
python scripts/validate.py
python -m unittest discover -s tests -v
ruff check .
ruff format --check .
```

La prueba de integración LaTeX se ejecuta si XeLaTeX está disponible; en caso contrario se omite. GitHub Actions valida las fuentes y las pruebas Python; no renderiza ni certifica los informes generados.

## Licencia y fuentes

Las instrucciones, análisis, código y plantillas originales están bajo la [licencia MIT](../LICENSE). Los estándares, documentación y fuentes tipográficas citados conservan sus derechos. No se incluyen ni se relicencian el texto oficial de GOST ni fuentes propietarias. Los enlaces y la edición revisada están en [sources.md](../skills/gost-7-32-2017-latex/references/sources.md).
