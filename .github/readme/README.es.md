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

Usa al **asesor en un chat y un espacio de trabajo separados, fuera del árbol de directorios del proyecto**. Mantén al agente en el espacio del proyecto, siguiendo sus instrucciones aplicables. Otro chat asociado al mismo proyecto aún puede cargar `AGENTS.md`, `CLAUDE.md` u otras reglas locales.

Así se reduce la carga automática de instrucciones específicas del proyecto en el contexto del asesor. Todavía pueden aplicarse reglas globales, instrucciones de directorios superiores, integraciones y contexto heredado; no se garantiza aislamiento completo. Aporta el contexto necesario mediante objetivos, documentos seleccionados e informes del agente. El asesor puede examinar las reglas como evidencia, respetando la jerarquía de instrucciones del entorno.

Guarda el estado de asesoría de cada proyecto en una carpeta externa propia, fuera de la skill instalada y preferiblemente fuera del repositorio del proyecto. No publiques estado privado con la skill.

## Instalación

Clona o descarga este repositorio y copia la carpeta completa `skills/project-advisor` al destino adecuado. Conserva `references/` y `agents/` junto a `SKILL.md`. Revisa tus cambios locales antes de sobrescribir una instalación existente.

| Entorno | Carpeta de instalación personal | Invocación explícita |
|---|---|---|
| Codex | `~/.agents/skills/project-advisor/` | `$project-advisor` |
| Claude Code | `~/.claude/skills/project-advisor/` | `/project-advisor` |
| OpenCode | `~/.config/opencode/skills/project-advisor/` | Selecciona o carga la skill explícitamente; consulta la opción de comando más abajo. |

`~` representa tu directorio personal, también en Windows. Estas rutas corresponden a herramientas locales; los productos alojados pueden usar otros mecanismos. Si la skill no aparece tras instalarla, abre una nueva sesión de asesoría.

### Controles de invocación

El núcleo siempre exige una solicitud explícita de activación. Los controles del entorno son independientes:

- **Codex:** el archivo incluido `agents/openai.yaml` establece `policy.allow_implicit_invocation: false`.
- **Claude Code:** añade `disable-model-invocation: true` al frontmatter YAML del `SKILL.md` instalado para impedir invocaciones iniciadas por el modelo. Es una adaptación de Claude Code, no del archivo compartido.
- **OpenCode:** añade estos metadatos con valores de texto al frontmatter del `SKILL.md` instalado para habilitar un comando y retirar la skill de las orientaciones de selección automática:

  ```yaml
  metadata:
    opencode/slash: "true"
    opencode/autoinvoke: "false"
  ```

  Después invoca `/project-advisor` en versiones que admitan estas opciones. Si tu cliente funciona de otra forma, usa su mecanismo explícito de carga de skills.

Son ajustes de instalación locales; no requieren copias separadas de la metodología en este repositorio. Antes de actualizar, conserva la configuración de frontmatter específica del entorno.

Las instrucciones de instalación e invocación se contrastaron con la documentación oficial de [Codex](https://learn.chatgpt.com/docs/build-skills), [Claude Code](https://code.claude.com/docs/en/skills) y [OpenCode](https://opencode.ai/docs/skills/) el 21 de octubre de 2026. **Esta versión no se ha probado de extremo a extremo en los tres clientes.** Revisar documentación no certifica compatibilidad en ejecución. La experiencia previa con el asesor en portugués orientó esta versión; la adaptación inglesa aún necesita comentarios de más usos reales.

## Activación y uso

Invoca la skill mediante el mecanismo de tu entorno e indica el objetivo y una carpeta de estado. Por ejemplo:

```text
Activa Project Advisor.
Usa esta carpeta externa de estado: /ruta/a/mi-espacio-de-asesoria.
El agente de implementación está en otro chat.
Quiero añadir importación de clientes mediante CSV a una aplicación existente.
```

El asesor lee sus instrucciones centrales y el estado externo, o crea el estado cuando es necesario. Permanece activo en el mismo chat hasta que lo desactives explícitamente:

```text
Desactiva el asesor.
```

En un chat nuevo, activa de nuevo la skill e indica la misma carpeta para retomar el proyecto. La instalación por sí sola nunca activa el rol. Las instrucciones y ejemplos de la skill están en inglés; **el asesor se comunica en el idioma que prefieras**.

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

El asesor usa `ADVISOR_STATE.md` en tu espacio externo. Al crear un estado nuevo, un `ADVISOR_STATE_TEMPLATE.md` existente tiene prioridad sobre el esquema de recuperación incluido. `STATE_SCHEMA.md` contiene solo campos genéricos.

El estado puede contener decisiones sensibles, rutas o datos del proyecto. Elige deliberadamente dónde guardarlo y con quién compartirlo. El `.gitignore` excluye los nombres de archivos de estado, pero solo protege esta copia del repositorio y no elimina archivos ya rastreados. Es preferible guardar el estado privado fuera de repositorios públicos.

El estado se consolida durante turnos activos cuando cambia información relevante, al cerrar trabajo o al retomar después de una compactación, según sea necesario. No hay proceso en segundo plano, hook de sesión ni recuperación garantizada si se pierde el contexto de activación. Reactiva la skill con la misma carpeta cuando sea necesario. Sin acceso a archivos, el asesor puede entregar un resumen para que lo guardes, sin afirmar que persistió el estado.

La skill proporciona instrucciones, no controles de acceso ni garantía de decisiones correctas. Su comportamiento depende del modelo, la evidencia disponible, las instrucciones del entorno y las herramientas. No implementa el proyecto coordinado ni contacta al agente por su cuenta.

## Estructura del repositorio

```text
skills/project-advisor/
├── SKILL.md                   Activación, estado y continuidad
├── agents/openai.yaml         Política de invocación de Codex
└── references/
    ├── ADVISOR_CORE.md        Método independiente de plataforma
    └── STATE_SCHEMA.md        Estructura de recuperación del estado
```

## Contribuciones

Describe un problema real, el comportamiento esperado y por qué el cambio ayuda sin añadir proceso innecesario. Usa ejemplos sintéticos, elimina información privada e indica el entorno y los límites de las comprobaciones. Conserva la distinción entre orientación reutilizable y preferencias particulares de una persona o proyecto.

Las traducciones del README están en `.github/readme/`. Mantén ejemplos, comandos, enlaces y límites alineados con el README inglés al actualizar la documentación. Añade enlaces de idiomas solo para traducciones presentes en el repositorio.

## Licencia

[MIT](../../LICENSE) — Copyright (c) 2026 Guilherme Rocha.
