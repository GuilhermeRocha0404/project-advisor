# Project Advisor

[English](../../README.md) · **简体中文** · [Español](README.es.md) · [Português (Brasil)](README.pt-BR.md) · [日本語](README.ja.md) · [Tiếng Việt](README.vi.md) · [한국어](README.ko.md) · [فارسی](README.fa.md) · [ภาษาไทย](README.th.md) · [العربية](README.ar.md) · [Français](README.fr.md) · [Bahasa Indonesia](README.id.md)

一个独立于平台的 skill，用于审慎指导项目、为执行代理编写聚焦的任务指令，并依据证据评估结果。

用一个对话决定接下来值得做什么，用另一个代理调查、实现和验证。顾问会质疑薄弱的假设，推荐与问题相称的流程，并评估结果。目标、优先级和个人偏好的决定权始终在你手中。

本方法不要求特定模型、厂商、插件或外部服务。它面向能够加载相关指令和参考文件的代理环境中的开发项目。

## 工作流程示例

你想为现有应用添加通过 CSV 导入客户的功能。

| 步骤 | 参与者 | 示例 |
|---|---|---|
| 说明目标 | 你 → 顾问 | “我想让员工导入客户 CSV 文件，且不产生重复记录。” |
| 澄清真实歧义 | 顾问 ↔ 你 | “遇到重复邮箱时，应更新已有客户，还是标记为待审核？”你选择待审核。 |
| 准备执行 | 顾问 → 你 | 为执行代理编写指令，明确导入行为、重复记录处理、已有授权限制以及完成所需的证据。 |
| 执行 | 你 → 执行代理 | 你将指令交给项目工作区中的代理，由它调查、实现并验证。 |
| 带回结果 | 你 → 顾问 | 代理报告导入成功，并检查了无效行和单个文件内的重复记录。 |
| 评估证据 | 顾问 → 你 | 顾问发现尚未检查重复导入同一文件，便只要求补充这项验证。 |
| 完成或修正 | 执行代理 → 你 → 顾问 | 结果证明符合预期，或缺陷得到修正。证据充分时，顾问结束任务。 |

这只是示例，并非强制步骤。明确的任务可以直接执行；不鼓励多余的规划和重复验证。skill 不会自动连接对话，也不会在对话之间自动发送消息。

## 推荐设置

每个项目使用独立的顾问文件夹和聊天，放在目标仓库目录树之外。其他项目应使用新文件夹和全新状态。执行代理仍在目标仓库中工作。全局和父目录指令仍可能生效。

## 安装

将完整的 `skills/project-advisor` 及其子目录复制到相应环境的个人技能目录。使用 Python 3.10+ 预览工作区配置，检查差异后添加 `--apply` 再次运行。替换示例路径，并选择 `codex`、`claude` 或 `opencode`。

```sh
python <skill-dir>/scripts/workspace.py --workspace <advisor-dir> --project <target-dir> --harness codex
python <skill-dir>/scripts/workspace.py --workspace <advisor-dir> --project <target-dir> --harness codex --apply
```

Codex: `$project-advisor` · Claude Code: `/project-advisor` · OpenCode: `project-advisor`

[Codex / Claude Code / OpenCode — setup, updates, migration](../../skills/project-advisor/references/HARNESSES.md)

## 激活与使用

在准备好的文件夹中开启新聊天。加载本地指令后，代理成为绑定项目的顾问；仅安装技能不会激活其他聊天。请核对角色、项目、状态和下一步。明确停用仅对当前聊天生效；该文件夹中的新聊天默认恢复顾问角色。回复使用用户偏好的语言。

## 顾问的职责

- 将下一项任务与项目的实际价值联系起来。
- 发现具体问题时质疑决策，并提出替代方案。
- 询问偏好、优先级、意图及你能够澄清的事实。
- 对技术或专业问题进行有针对性的调查。
- 按风险和不确定性调整规划、委派与验证。
- 评估执行代理的证据，并在任务充分完成后停止。
- 尊重知情选择和授权边界。
- 维护简洁、最新的接续状态，而非不断累积活动日志。

## 状态、隐私与限制

`AGENTS.md` 保存方法；需要时由 `CLAUDE.md` 导入。`.advisor-workspace.json` 记录项目、环境、版本及文件哈希。私有状态保存在 `ADVISOR_STATE.md`，旧的 `CONSULTOR_STATE.md` 可以保留。使用 `--adopt-existing-state` 前先阅读状态。个人偏好放在 `ADVISOR_LOCAL.md`。更新会展示差异并拒绝覆盖已修改的指令；请明确审查和合并。安装器不会重写现有状态。不安装钩子或后台服务。安装器测试不等于所有客户端的运行验证。

## 仓库结构

模板是方法唯一的发布来源，每个工作区获得带版本的副本。不再保留独立 CORE。更新技能不会自动更新工作区。请勿公开私有状态、绑定信息或个人配置。

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

## 贡献

请说明真实问题、预期行为，以及修改为何能在不增加多余流程的前提下提供帮助。使用合成示例，去除私人信息，并报告行为检查的环境和限制。改进应区分可复用指导与个人或特定项目偏好。

README 译文位于 `.github/readme/`。更新文档时，请让示例、命令、链接和限制与英文 README 保持一致。仅为仓库内实际存在的译文添加语言导航链接。

## 许可证

[MIT](../../LICENSE) — Copyright (c) 2026 Guilherme Rocha.

## 2.1.0

2.1.0 修订：状态区分证据来源，清理已被替代的决定，同时保留有效约束和未完成的验证。安装程序使用统一状态模板，保留旧状态文件名，并改进清单和锁文件恢复说明。尚无对照研究证明质量、时间或成本收益。适配器测试不等于各环境中的实际运行验证；无文件访问的聊天需要手动提供方法和状态并保存更新。

[English technical reference](../../docs/AUDIT_2_1.md) · [Examples](../../skills/project-advisor/references/EXAMPLES.md)
