# Project Advisor

[English](../../README.md) · [简体中文](README.zh-CN.md) · **Español** · [Português (Brasil)](README.pt-BR.md) · [日本語](README.ja.md) · [Tiếng Việt](README.vi.md) · [한국어](README.ko.md) · [فارسی](README.fa.md) · [ภาษาไทย](README.th.md) · [العربية](README.ar.md) · [Français](README.fr.md) · [Bahasa Indonesia](README.id.md)

Una skill independiente de la plataforma para orientar proyectos con criterio, preparar instrucciones concretas para un agente de implementación y revisar resultados a partir de evidencias.

Usa un chat para decidir qué trabajo aporta valor a continuación y otro agente para investigar, implementar y verificar. El asesor cuestiona supuestos débiles, recomienda un proceso proporcional al problema y evalúa los resultados. Tú conservas las decisiones sobre objetivos, prioridades y preferencias.

La metodología no exige ningún modelo, proveedor, plugin ni servicio externo específico. Está pensada para proyectos de desarrollo en entornos de agentes capaces de cargar sus instrucciones y archivos de referencia.

## Ejemplo del flujo de trabajo

Quieres añadir la importación de clientes mediante CSV a una aplicación existente.

| Paso | Quién | Ejemplo |
|---|---|---|
| Explicar el objetivo | Tú → asesor | «Quiero que el equipo importe archivos CSV de clientes sin crear registros duplicados». |
| Aclarar una ambigüedad real | Asesor ↔ tú | «¿Un correo repetido debe actualizar al cliente existente o señalarse para revisión?». Eliges revisión. |
| Preparar la ejecución | Asesor → tú | Una instrucción para el agente que define la importación, los duplicados, las restricciones de autorización existentes y las evidencias necesarias para terminar. |
| Ejecutar | Tú → agente | Envías la instrucción al agente en el espacio de trabajo del proyecto. Investiga, implementa y verifica. |
| Traer el resultado | Tú → asesor | El agente informa de importaciones correctas y comprobaciones de filas inválidas y duplicados dentro de un archivo. |
| Evaluar la evidencia | Asesor → tú | Detecta que no se comprobó importar el mismo archivo dos veces y pide esa verificación concreta. |
| Terminar o corregir | Agente → tú → asesor | Se demuestra el comportamiento esperado o se corrige un defecto. El asesor cierra la tarea cuando la evidencia es suficiente. |

Es un ejemplo, no una secuencia obligatoria. Las tareas claras pueden pasar directamente a ejecución; se desaconsejan la planificación innecesaria y las verificaciones repetidas. La skill no conecta chats ni envía mensajes entre ellos automáticamente.

## Configuración recomendada

Utiliza una carpeta y un chat de asesoría por proyecto, fuera del repositorio de destino. Otro proyecto necesita otra carpeta y un estado nuevo. El agente ejecutor permanece en el repositorio. Las instrucciones globales y de carpetas superiores pueden seguir aplicándose.

## Instalación

Copia toda la carpeta `skills/project-advisor` al directorio personal de skills de tu entorno, conservando sus subcarpetas. Usa Python 3.10+ para previsualizar la preparación y repite con `--apply` tras revisar las diferencias. Sustituye las rutas de ejemplo y elige `codex`, `claude` u `opencode`.

```sh
python <skill-dir>/scripts/workspace.py --workspace <advisor-dir> --project <target-dir> --harness codex
python <skill-dir>/scripts/workspace.py --workspace <advisor-dir> --project <target-dir> --harness codex --apply
```

Codex: `$project-advisor` · Claude Code: `/project-advisor` · OpenCode: `project-advisor`

[Codex / Claude Code / OpenCode — setup, updates, migration](../../skills/project-advisor/references/HARNESSES.md)

## Activación y uso

Abre un chat nuevo en la carpeta preparada. Sus instrucciones locales activan al asesor del proyecto vinculado; instalar la skill no activa otros chats. Comprueba que reconoce su función, proyecto, estado y siguiente paso. La desactivación explícita dura este chat; uno nuevo vuelve a empezar como asesor. Responde en tu idioma preferido.

## Qué hace el asesor

- Vincula la próxima tarea con un resultado útil para el proyecto.
- Cuestiona decisiones cuando detecta un problema concreto y propone alternativas.
- Pregunta por preferencias, prioridades, intención y hechos que puedas aclarar.
- Usa investigación dirigida para dudas técnicas o especializadas.
- Ajusta planificación, delegación y verificación al riesgo y la incertidumbre.
- Evalúa las evidencias del agente y termina cuando la tarea está suficientemente completada.
- Respeta las decisiones informadas y los límites de autorización.
- Mantiene un punto de reanudación conciso y actual, en vez de acumular un registro de actividades.

## Estado, privacidad y límites

`AGENTS.md` contiene el método; `CLAUDE.md` lo importa cuando corresponde. `.advisor-workspace.json` registra proyecto, entorno, versión y hashes. El estado privado está en `ADVISOR_STATE.md`; puede conservarse `CONSULTOR_STATE.md`. Lee el estado antes de usar `--adopt-existing-state`. Guarda preferencias en `ADVISOR_LOCAL.md`. Las actualizaciones muestran diferencias y rechazan instrucciones modificadas; revisa y combina los cambios. El instalador conserva el estado existente. No hay hooks ni mantenimiento en segundo plano. Los tests del instalador no certifican el comportamiento de todos los clientes.

## Estructura del repositorio

La plantilla es la única fuente distribuida del método; cada carpeta recibe una copia versionada. No existe un CORE separado. Actualizar la skill no actualiza las carpetas automáticamente. No publiques estados ni configuraciones privadas.

```text
skills/project-advisor/
├── SKILL.md
├── templates/AGENTS.md
├── scripts/workspace.py
├── agents/openai.yaml
└── references/
    ├── HARNESSES.md
    └── STATE_SCHEMA.md
```

## Contribuciones

Describe un problema real, el comportamiento esperado y por qué el cambio ayuda sin añadir proceso innecesario. Usa ejemplos sintéticos, elimina información privada e indica el entorno y los límites de las comprobaciones. Conserva la distinción entre orientación reutilizable y preferencias particulares de una persona o proyecto.

Las traducciones del README están en `.github/readme/`. Mantén ejemplos, comandos, enlaces y límites alineados con el README inglés al actualizar la documentación. Añade enlaces de idiomas solo para traducciones presentes en el repositorio.

## Licencia

[MIT](../../LICENSE) — Copyright (c) 2026 Guilherme Rocha.
