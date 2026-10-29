# Agent Skills

[English](README.en.md) · [中文](README.zh.md) · [हिन्दी](README.hi.md) · [Español](README.es.md) · [العربية](README.ar.md) · [Français](README.fr.md) · [Português](README.pt.md) · [Русский](README.ru.md) · [বাংলা](README.bn.md) · [Deutsch](README.de.md)

面向 AI 智能体的实用技能：可在不同项目中复用的说明、脚本、模板和检查工具。

[参与贡献](../CONTRIBUTING.md) · [MIT 许可证](../LICENSE)

## 技能目录

| 技能 | 用途 | 语言与依赖 |
|---|---|---|
| [build-agent-context](../skills/build-agent-context/) | 将压缩包、文档、消息、链接或代码仓库整理为任务上下文，包含来源追溯、阅读路径、当前状态和交接检查 | 用户的语言；Markdown；阅读工具取决于输入格式 |
| [gost-7-32-2017-latex](../skills/gost-7-32-2017-latex/) | 按 GOST 7.32-2017 编写和审查 LaTeX 科研报告，包括封面、结构、公式、表格、参考文献、附录及 PDF 检查 | 俄语；Python 3.10+；XeLaTeX 或 LuaLaTeX；可选 `pdfplumber` |

每项技能都有独立文件夹，以 `SKILL.md` 为入口，脚本和资源放在同一目录下。

## 在 Codex 中安装

向 Codex 提出请求：

```text
使用 $skill-installer 安装 https://github.com/Girday/agent-skills/tree/main/skills/gost-7-32-2017-latex
```

也可以克隆仓库并安装本地副本：

```bash
git clone https://github.com/Girday/agent-skills.git
cd agent-skills
python3 scripts/install.py gost-7-32-2017-latex
```

安装程序使用 `$CODEX_HOME/skills`；未设置 `CODEX_HOME` 时使用 `~/.codex/skills`。它拒绝覆盖已有安装。安装后的副本独立于仓库，不会随仓库更新而自动更新。如果技能没有显示，请重启 Codex。[官方技能文档](https://learn.chatgpt.com/docs/build-skills)介绍了发现和分发方式。本仓库提供技能源文件，并非已发布的插件目录条目。

其他支持 `SKILL.md` 格式的智能体也可使用这些说明和资源。Codex 专用桌面工具是可选项，同时提供命令行操作流程。

## 为智能体准备上下文

使用同一安装程序，按目录名称或 GitHub 文件夹安装 `build-agent-context`，然后提出请求：

```text
使用 $build-agent-context。根据这个压缩包准备上下文，让另一个智能体能够继续项目。
包含当前要求、来源依据、尚未解决的冲突和启动提示词。接收方智能体可以读取文件。
```

该技能会在自包含文档与“简短入口加主题文件”之间选择。它记录实际阅读范围，保留来源定位，区分要求、已验证事实、假设和当前进展，也支持更新已有上下文。没有强制运行时依赖；压缩包、扫描件等格式需要环境中具备适当的阅读工具。

方法依据（12 篇精选文献）、输出示例、质量标准、行为评估场景以及验证范围与限制：

- [research.md](../skills/build-agent-context/references/research.md)
- [output-patterns.md](../skills/build-agent-context/references/output-patterns.md)
- [quality-checks.md](../skills/build-agent-context/references/quality-checks.md)
- [validation.md](../skills/build-agent-context/references/validation.md)

## 使用 GOST 技能

```text
使用 $gost-7-32-2017-latex。根据附件材料编写报告，生成 PDF 并检查排版。
学校的具体要求另附。
```

在仓库根目录运行：

```bash
python3 skills/gost-7-32-2017-latex/scripts/init_project.py ./my-report
python3 skills/gost-7-32-2017-latex/scripts/build.py ./my-report
python3 skills/gost-7-32-2017-latex/scripts/audit.py ./my-report
```

运行 `init_project.py` 后，请填写 `my-report/metadata.tex`，并在构建前替换演示内容。初始模板故意保留未填写字段；在补全之前，审查应报告失败。安装 `pdfplumber` 可启用 PDF 几何检查；未安装时，这些检查标记为 `NOT_CHECKED`。

八页示例、要求对应表，以及已验证行为和限制：

- [example.pdf](../examples/gost-7-32-2017/example.pdf)
- [requirements.md](../skills/gost-7-32-2017-latex/references/requirements.md)
- [validation.md](../skills/gost-7-32-2017-latex/references/validation.md)

GOST 7.32-2017 适用于科研报告。用于课程作业时，必须结合学校要求进行调整。该技能区分强制要求、建议、允许的替代方案和模板选择。自动检查辅助审查，但不构成报告认证，也不能确认签名、登记或机构批准。A3 和多卷报告流程已有文档，但在初始模板验证中未单独测试。

## 开发

创建虚拟环境后，使用当前 shell 对应的命令激活，再安装依赖并执行检查：

```bash
python3 -m venv .venv
python -m pip install -r requirements-dev.txt
python scripts/validate.py
python -m unittest discover -s tests -v
ruff check .
ruff format --check .
```

LaTeX 集成测试在 XeLaTeX 可用时运行，否则跳过。GitHub Actions 检查源文件和 Python 测试，不渲染或认证生成的报告。

## 许可证与来源

仓库原创说明、分析、代码和模板采用 [MIT 许可证](../LICENSE)。引用的标准、文档和字体保留各自权利。官方 GOST 文本和专有字体未打包提供，也未重新授权。来源链接与所审查的版本记录在 [sources.md](../skills/gost-7-32-2017-latex/references/sources.md) 中。
