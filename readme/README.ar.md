# Agent Skills

[English](README.en.md) · [中文](README.zh.md) · [हिन्दी](README.hi.md) · [Español](README.es.md) · [العربية](README.ar.md) · [Français](README.fr.md) · [Português](README.pt.md) · [Русский](README.ru.md) · [বাংলা](README.bn.md) · [Deutsch](README.de.md)

مهارات عملية لوكلاء الذكاء الاصطناعي: تعليمات وسكربتات وقوالب وفحوص يمكن إعادة استخدامها في مشاريع مختلفة.

[المساهمة](../CONTRIBUTING.md) · [ترخيص MIT](../LICENSE)

## دليل المهارات

| المهارة | الوظيفة | اللغة والمتطلبات |
|---|---|---|
| [build-agent-context](../skills/build-agent-context/) | يحوّل الأرشيفات والمستندات والرسائل والروابط والمستودعات إلى سياق للمهمة، مع تتبع المصادر ومسارات القراءة والحالة الحالية وفحوص التسليم | لغة المستخدم؛ Markdown؛ أدوات القراءة حسب تنسيق المدخلات |
| [transcribe-recording](../skills/transcribe-recording/) | تفريغ تسجيلات الاجتماعات والمحاضرات والمقابلات والدروس، والتحقق من المتحدثين وإعداد مواد سياقية بطوابع زمنية | Windows وLinux وmacOS؛ faster-whisper على CPU/CUDA، وMLX اختياري على Apple Silicon |
| [gost-7-32-2017-latex](../skills/gost-7-32-2017-latex/) | يُعدّ تقارير البحث في LaTeX ويراجعها وفق GOST 7.32-2017: الغلاف والبنية والمعادلات والجداول والمراجع والملاحق وفحوص PDF | الروسية؛ Python 3.10+ وXeLaTeX أو LuaLaTeX؛ و`pdfplumber` اختياري |

لكل مهارة مجلد مستقل يحتوي على نقطة الدخول `SKILL.md` والسكربتات والموارد المرتبطة بها.

## التثبيت في Codex

اطلب من Codex:

```text
استخدم $skill-installer لتثبيت https://github.com/Girday/agent-skills/tree/main/skills/gost-7-32-2017-latex
```

أو استنسخ المستودع وثبّت نسخة محلية:

```bash
git clone https://github.com/Girday/agent-skills.git
cd agent-skills
python3 scripts/install.py gost-7-32-2017-latex
```

يستخدم المثبّت `$CODEX_HOME/skills`، أو `~/.codex/skills` إذا لم يُضبط `CODEX_HOME`. ويرفض استبدال تثبيت موجود. النسخة المثبتة مستقلة عن المستودع ولا تُحدّث تلقائياً عند تغييره. أعد تشغيل Codex إذا لم تظهر المهارة. تشرح [الوثائق الرسمية](https://learn.chatgpt.com/docs/build-skills) طرق اكتشاف المهارات وتوزيعها. يوفّر هذا المستودع ملفات المصدر؛ ولا يمثل إدراجاً منشوراً في دليل الإضافات.

يمكن للوكلاء الآخرين استخدام التعليمات والموارد إذا كانوا يدعمون `SKILL.md`. أدوات سطح المكتب الخاصة بـCodex اختيارية، ويتوفر أيضاً مسار عمل عبر سطر الأوامر.

## إعداد سياق لوكيل

ثبّت `build-agent-context` بالمثبّت نفسه، باستخدام اسم المهارة أو مجلدها على GitHub، ثم اطلب:

```text
استخدم $build-agent-context. أعدّ سياقاً من هذا الأرشيف ليتابع وكيل آخر المشروع.
ضمّن المتطلبات الحالية والمصادر والتعارضات غير المحسومة وتعليمة بداية.
الوكيل المستلم يستطيع قراءة الملفات.
```

تختار المهارة بين مستند مكتفٍ بذاته ونقطة دخول مختصرة مع ملفات حسب الموضوع. تسجّل ما قُرئ فعلياً، وتحفظ مواضع المصادر، وتميّز المتطلبات والحقائق المتحققة والافتراضات والتقدم الحالي. وتدعم تحديث السياق الموجود. لا توجد تبعيات تشغيل إلزامية؛ وتحتاج الأرشيفات والمسوح الضوئية والتنسيقات الأخرى إلى أدوات قراءة مناسبة.

أساس المنهج (12 منشوراً مختاراً)، وأمثلة المخرجات، ومعايير الجودة، وسيناريوهات التقييم السلوكي، ونطاق التحقق وحدوده:

- [research.md](../skills/build-agent-context/references/research.md)
- [output-patterns.md](../skills/build-agent-context/references/output-patterns.md)
- [quality-checks.md](../skills/build-agent-context/references/quality-checks.md)
- [validation.md](../skills/build-agent-context/references/validation.md)

## استخدام مهارة GOST

```text
استخدم $gost-7-32-2017-latex. أعدّ تقريراً من المواد المرفقة، وأنشئ PDF وراجع التنسيق.
متطلبات المؤسسة مرفقة بصورة منفصلة.
```

شغّل الأوامر من المجلد الجذري للمستودع:

```bash
python3 skills/gost-7-32-2017-latex/scripts/init_project.py ./my-report
python3 skills/gost-7-32-2017-latex/scripts/build.py ./my-report
python3 skills/gost-7-32-2017-latex/scripts/audit.py ./my-report
```

بعد تشغيل `init_project.py`، أكمل `my-report/metadata.tex` واستبدل المحتوى التجريبي قبل البناء. يحتوي القالب عمداً على حقول فارغة؛ ويجب أن يفشل التدقيق حتى تُستكمل. ثبّت `pdfplumber` لتفعيل فحوص أبعاد PDF؛ وبدونه تُوسم تلك الفحوص بـ`NOT_CHECKED`.

مثال من ثماني صفحات، وخريطة المتطلبات، والسلوك المتحقق منه وحدوده:

- [example.pdf](../examples/gost-7-32-2017/example.pdf)
- [requirements.md](../skills/gost-7-32-2017-latex/references/requirements.md)
- [validation.md](../skills/gost-7-32-2017-latex/references/validation.md)

يختص GOST 7.32-2017 بتقارير البحث. وتطبيقه على الأعمال الدراسية يتطلب تكييفه مع قواعد المؤسسة. تميّز المهارة بين المتطلبات والتوصيات والبدائل المسموحة واختيارات القالب. تساعد الفحوص الآلية في المراجعة؛ لكنها لا تمنح التقرير شهادة مطابقة ولا تؤكد التوقيعات أو التسجيل أو موافقة المؤسسة. وُثّقت إجراءات A3 والتقارير متعددة المجلدات، لكنها لم تُختبر بصورة منفصلة في التحقق الأولي من القالب.

## التطوير

أنشئ البيئة الافتراضية وفعّلها بالأمر المناسب لصدفة الأوامر لديك، ثم ثبّت التبعيات وشغّل الفحوص:

```bash
python3 -m venv .venv
python -m pip install -r requirements-dev.txt
python scripts/validate.py
python -m unittest discover -s tests -v
ruff check .
ruff format --check .
```

يعمل اختبار تكامل LaTeX عند توفر XeLaTeX، وإلا يُتخطى. تتحقق GitHub Actions من ملفات المصدر واختبارات Python؛ ولا تُصيّر التقارير الناتجة أو تصادق عليها.

## الترخيص والمصادر

التعليمات والتحليلات والشيفرات والقوالب الأصلية في المستودع متاحة بموجب [ترخيص MIT](../LICENSE). تحتفظ المعايير والوثائق والخطوط المشار إليها بحقوقها الخاصة. لا يُضمّن النص الرسمي لـGOST ولا الخطوط المملوكة، ولا يعاد ترخيصها. روابط المصادر والطبعة التي روجعت موثّقة في [sources.md](../skills/gost-7-32-2017-latex/references/sources.md).
