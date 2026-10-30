# Agent Skills

[English](README.en.md) · [中文](README.zh.md) · [हिन्दी](README.hi.md) · [Español](README.es.md) · [العربية](README.ar.md) · [Français](README.fr.md) · [Português](README.pt.md) · [Русский](README.ru.md) · [বাংলা](README.bn.md) · [Deutsch](README.de.md)

Habilidades práticas para agentes de IA: instruções, scripts, modelos e verificações reutilizáveis em diferentes projetos.

[Como contribuir](../CONTRIBUTING.md) · [Licença MIT](../LICENSE)

## Catálogo

| Habilidade | Função | Idioma e requisitos |
|---|---|---|
| [build-agent-context](../skills/build-agent-context/) | Converte arquivos compactados, documentos, mensagens, links e repositórios em contexto de trabalho com fontes rastreáveis, percursos de leitura, estado e verificações de transferência | Idioma do usuário; Markdown; ferramentas de leitura conforme o formato |
| [transcribe-recording](../skills/transcribe-recording/) | Transcreve reuniões, palestras, entrevistas e aulas; verifica os falantes e prepara fontes com marcações de tempo para contexto | Windows, Linux e macOS; faster-whisper em CPU/CUDA, MLX opcional em Apple Silicon |
| [gost-7-32-2017-latex](../skills/gost-7-32-2017-latex/) | Prepara e revisa relatórios de pesquisa em LaTeX segundo GOST 7.32-2017: capa, estrutura, equações, tabelas, referências, apêndices e PDF | Russo; Python 3.10+ e XeLaTeX ou LuaLaTeX; `pdfplumber` opcional |

Cada habilidade tem uma pasta própria com o ponto de entrada `SKILL.md`, scripts e recursos.

## Instalação no Codex

Peça ao Codex:

```text
Use $skill-installer para instalar https://github.com/Girday/agent-skills/tree/main/skills/gost-7-32-2017-latex
```

Ou clone o repositório e instale uma cópia local:

```bash
git clone https://github.com/Girday/agent-skills.git
cd agent-skills
python3 scripts/install.py gost-7-32-2017-latex
```

O instalador usa `$CODEX_HOME/skills` ou `~/.codex/skills` quando `CODEX_HOME` não está definido. Ele recusa sobrescrever instalações existentes. A cópia instalada é independente do repositório e não é atualizada automaticamente. Reinicie o Codex se a habilidade não aparecer. A [documentação oficial](https://learn.chatgpt.com/docs/build-skills) explica a descoberta e a distribuição de habilidades. Este repositório fornece os arquivos-fonte; não é uma entrada publicada no diretório de plugins.

Outros agentes podem usar os recursos se aceitarem `SKILL.md`. As ferramentas de desktop específicas do Codex são opcionais; também há um fluxo por linha de comando.

## Preparar contexto para um agente

Instale `build-agent-context` com o mesmo instalador, usando seu nome ou pasta do GitHub. Depois, peça:

```text
Use $build-agent-context. Prepare contexto a partir deste arquivo compactado para
outro agente continuar o projeto. Inclua requisitos atuais, fontes, conflitos
pendentes e uma mensagem inicial. O agente receptor pode ler arquivos.
```

A habilidade escolhe entre um documento autossuficiente e um ponto de entrada curto com arquivos temáticos. Registra o que foi efetivamente lido, preserva referências aos trechos de origem e distingue requisitos, fatos verificados, hipóteses e progresso. Também atualiza contextos existentes. Não há dependências obrigatórias de execução; arquivos compactados, digitalizações e outros formatos exigem ferramentas adequadas.

Fundamentação (12 publicações selecionadas), exemplos de resultados, critérios de qualidade, cenários de avaliação e limites de validação:

- [research.md](../skills/build-agent-context/references/research.md)
- [output-patterns.md](../skills/build-agent-context/references/output-patterns.md)
- [quality-checks.md](../skills/build-agent-context/references/quality-checks.md)
- [validation.md](../skills/build-agent-context/references/validation.md)

## Usar a habilidade GOST

```text
Use $gost-7-32-2017-latex. Prepare um relatório com os materiais anexos,
gere o PDF e confira a formatação. Os requisitos da instituição estão anexados separadamente.
```

A partir da raiz do repositório:

```bash
python3 skills/gost-7-32-2017-latex/scripts/init_project.py ./my-report
python3 skills/gost-7-32-2017-latex/scripts/build.py ./my-report
python3 skills/gost-7-32-2017-latex/scripts/audit.py ./my-report
```

Após `init_project.py`, preencha `my-report/metadata.tex` e substitua o conteúdo de demonstração antes de compilar. Os campos vazios são intencionais: a auditoria deve falhar até que sejam preenchidos. Instale `pdfplumber` para verificar a geometria do PDF; sem ele, essas verificações recebem `NOT_CHECKED`.

Exemplo de oito páginas, mapa de requisitos e comportamento verificado com suas limitações:

- [example.pdf](../examples/gost-7-32-2017/example.pdf)
- [requirements.md](../skills/gost-7-32-2017-latex/references/requirements.md)
- [validation.md](../skills/gost-7-32-2017-latex/references/validation.md)

GOST 7.32-2017 trata de relatórios de pesquisa. Sua aplicação a trabalhos acadêmicos exige adaptação às regras institucionais. A habilidade diferencia requisitos, recomendações, alternativas permitidas e escolhas do modelo. As verificações automáticas auxiliam a revisão; não certificam o relatório nem confirmam assinaturas, registro ou aprovação institucional. Os modos A3 e de vários volumes estão documentados, mas não foram testados separadamente na validação inicial.

## Desenvolvimento

Crie e ative o ambiente virtual com o comando adequado ao seu shell antes de instalar as dependências e executar as verificações:

```bash
python3 -m venv .venv
python -m pip install -r requirements-dev.txt
python scripts/validate.py
python -m unittest discover -s tests -v
ruff check .
ruff format --check .
```

O teste de integração LaTeX é executado quando XeLaTeX está disponível; caso contrário, é ignorado. O GitHub Actions valida os arquivos-fonte e os testes Python; não renderiza nem certifica os relatórios gerados.

## Licença e fontes

As instruções, análises, códigos e modelos originais estão sob a [licença MIT](../LICENSE). Normas, documentação e fontes tipográficas citadas mantêm seus respectivos direitos. O texto oficial GOST e fontes proprietárias não são incluídos nem relicenciados. Os links e a edição consultada estão em [sources.md](../skills/gost-7-32-2017-latex/references/sources.md).
