# Project Advisor

[English](../../README.md) · [简体中文](README.zh-CN.md) · [Español](README.es.md) · **Português (Brasil)** · [日本語](README.ja.md) · [Tiếng Việt](README.vi.md) · [한국어](README.ko.md) · [فارسی](README.fa.md) · [ภาษาไทย](README.th.md) · [العربية](README.ar.md) · [Français](README.fr.md) · [Bahasa Indonesia](README.id.md)

Uma skill independente de plataforma para orientar projetos com senso crítico, preparar prompts objetivos para um agente trabalhador e avaliar resultados com base em evidências.

Use um chat para decidir o próximo trabalho útil e outro agente para investigar, implementar e verificar. O consultor questiona premissas frágeis, recomenda um processo proporcional ao problema e avalia os resultados. Você mantém as decisões sobre objetivos, prioridades e preferências.

A metodologia não exige um modelo, fornecedor, plugin ou serviço externo específico. Ela foi pensada para projetos de desenvolvimento em ambientes de agentes que consigam carregar suas instruções e arquivos de referência.

## Exemplo do fluxo de trabalho

Você quer adicionar a importação de clientes por CSV a uma aplicação existente.

| Etapa | Quem | Exemplo |
|---|---|---|
| Apresentar o objetivo | Você → consultor | “Quero que a equipe importe arquivos CSV de clientes sem criar registros duplicados.” |
| Esclarecer uma ambiguidade real | Consultor ↔ você | “Um e-mail repetido deve atualizar o cliente existente ou ser sinalizado para revisão?” Você escolhe revisão. |
| Preparar a execução | Consultor → você | Um prompt para o trabalhador definindo a importação, o tratamento de duplicidades, as restrições de autorização existentes e as evidências necessárias para concluir. |
| Executar | Você → trabalhador | Você encaminha o prompt ao trabalhador no workspace do projeto. Ele investiga, implementa e verifica. |
| Trazer o resultado | Você → consultor | O trabalhador relata importações bem-sucedidas e verificações de linhas inválidas e duplicidades dentro de um arquivo. |
| Avaliar as evidências | Consultor → você | Ele percebe que importar o mesmo arquivo duas vezes não foi verificado e solicita essa conferência específica. |
| Concluir ou corrigir | Trabalhador → você → consultor | O resultado demonstra o comportamento esperado, ou um defeito é corrigido. O consultor encerra a tarefa quando as evidências são suficientes. |

Esse é um exemplo, não uma sequência obrigatória. Tarefas claras podem seguir diretamente para execução; planejamento desnecessário e verificações repetidas são desencorajados. A skill não conecta nem envia mensagens automaticamente entre chats.

## Configuração recomendada

Use uma pasta e um chat de consultoria exclusivos por projeto, fora da árvore do repositório acompanhado. Outro projeto recebe outra pasta e um estado limpo. O trabalhador permanece no repositório. Instruções globais e de pastas superiores ainda podem se aplicar; não há isolamento completo.

## Instalação

Copie a pasta completa `skills/project-advisor` para o diretório pessoal de skills do ambiente, preservando `templates/`, `scripts/`, `references/` e `agents/`. Codex: `~/.agents/skills/project-advisor`; Claude Code: `~/.claude/skills/project-advisor`; OpenCode: `~/.config/opencode/skills/project-advisor`. Use Python 3.10+ para visualizar a preparação e repita com `--apply` após revisar o diff. Substitua os caminhos de exemplo e escolha `codex`, `claude` ou `opencode`.

```sh
python <skill-dir>/scripts/workspace.py --workspace <advisor-dir> --project <target-dir> --harness codex
python <skill-dir>/scripts/workspace.py --workspace <advisor-dir> --project <target-dir> --harness codex --apply
```

Codex: `$project-advisor` · Claude Code: `/project-advisor` · OpenCode: `project-advisor`

[Codex / Claude Code / OpenCode — setup, updates, migration](../../skills/project-advisor/references/HARNESSES.md)

## Ativação e uso

Abra um novo chat na pasta preparada. O carregamento das instruções locais inicia o consultor do projeto vinculado; apenas instalar a skill não ativa outros chats. Peça ao agente que identifique papel, projeto, estado e próximo passo para conferir o carregamento. A desativação explícita vale para o chat atual; um novo chat nessa pasta começa como consultor. As respostas seguem seu idioma preferido. Para retomar explicitamente, carregue o AGENTS.md local, o vínculo e o estado.

## O que o consultor faz

- Relaciona a próxima tarefa a um resultado útil para o projeto.
- Questiona decisões quando identifica um problema concreto e propõe alternativas.
- Pergunta sobre preferências, prioridades, intenção e fatos que você possa esclarecer.
- Usa investigação dirigida para dúvidas técnicas ou especializadas.
- Ajusta planejamento, delegação e verificação ao risco e à incerteza.
- Avalia as evidências do trabalhador e encerra tarefas quando estão suficientemente concluídas.
- Respeita decisões informadas e limites de autorização.
- Mantém um ponto de retomada conciso e atual, em vez de acumular um registro de atividades.

## Estado, privacidade e limites

O `AGENTS.md` instalado contém o método; `CLAUDE.md` o importa quando necessário. `.advisor-workspace.json` registra projeto, ambiente, versão e hashes dos arquivos gerenciados. `ADVISOR_STATE.md` guarda decisões privadas e progresso; o nome legado `CONSULTOR_STATE.md` pode ser preservado. Leia o estado antes de usar `--adopt-existing-state`. Guarde preferências em `ADVISOR_LOCAL.md`. Atualizações usam o mesmo comando de prévia/aplicação e recusam arquivos gerenciados modificados; revise e mescle personalizações explicitamente. O instalador nunca substitui um estado existente. A manutenção do estado continua dependente do modelo, sem hooks ou serviço em segundo plano. Documentação e testes do instalador não certificam execução em todos os ambientes.

## Estrutura do repositório

O template é a única fonte distribuída do método; cada workspace recebe uma cópia versionada. Não há CORE separado. Atualizar a skill não atualiza os workspaces silenciosamente. Mantenha estado, vínculos e preferências privadas fora do repositório público.

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

## Contribuições

Descreva um problema real, o comportamento esperado e por que a mudança proposta ajuda sem acrescentar processo desnecessário. Use exemplos sintéticos, remova informações privadas e informe o ambiente e os limites das verificações de comportamento realizadas. Melhorias devem preservar a distinção entre orientações reutilizáveis e preferências particulares de uma pessoa ou projeto.

As traduções do README ficam em `.github/readme/`. Ao atualizar a documentação, mantenha exemplos, comandos, links e limitações alinhados com o README em inglês. Adicione links de navegação somente para traduções incluídas no repositório.

## Licença

[MIT](../../LICENSE) — Copyright (c) 2026 Guilherme Rocha.

## 2.1.0

Revisão 2.1.0: o estado passa a registrar a origem das evidências e a reconciliar decisões substituídas, preservando restrições e verificações abertas. O instalador usa um esquema único, preserva o nome legado e melhora a recuperação de manifesto e trava. Não há comparação controlada que demonstre ganhos de qualidade, tempo ou custo. Adaptadores não comprovam execução real em cada ambiente; em chats sem arquivos, o método e o estado precisam ser fornecidos e salvos manualmente.

[English technical reference](../../docs/AUDIT_2_1.md) · [Examples](../../skills/project-advisor/references/EXAMPLES.md)
