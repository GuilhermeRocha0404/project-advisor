# Project Advisor

[English](../../README.md) · **Português (Brasil)**

Um método de consultoria de projetos independente de modelo, com adaptadores de workspace para Codex, Claude Code e OpenCode.

Conversas longas com agentes de desenvolvimento podem perder decisões e deixar conclusões sem evidência suficiente. O Project Advisor busca manter decisões, continuidade e avaliação de evidências no workspace do consultor; um trabalhador separado investiga, implementa e verifica dentro do projeto. Você mantém o controle dos objetivos e das prioridades.

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

## Início rápido

Para um projeto existente em `../sample-app`, execute a partir da raiz deste repositório (ou substitua o caminho do script pela cópia instalada):

```sh
python skills/project-advisor/scripts/workspace.py --workspace ../sample-advisor --project ../sample-app --harness codex
python skills/project-advisor/scripts/workspace.py --workspace ../sample-advisor --project ../sample-app --harness codex --apply
```

Revise a prévia antes do segundo comando. Abra um novo chat de consultoria em `../sample-advisor` e peça: “Identifique seu papel, projeto vinculado e próximo passo. Quero que a equipe importe clientes por CSV; e-mails repetidos devem ser sinalizados para revisão. Ajude-me a escolher a primeira entrega útil.”

O `ADVISOR_STATE.md` gerado começa com fatos desconhecidos. Conforme as decisões são tomadas, o consultor mantém um ponto de retomada como neste trecho fictício; preserve as outras seções geradas e registre o que ainda for desconhecido:

```md
## Active objective and authorization
Importação de clientes por CSV; planejamento autorizado, implementação ainda não autorizada.

## Active decisions and constraints
E-mails repetidos vão para revisão; clientes existentes não devem ser sobrescritos.

## Latest worker task and evidence
Nenhuma tarefa enviada ao trabalhador e nenhuma evidência de execução recebida.

## Next step
Esclarecer quais perfis da equipe podem importar, depois preparar um prompt delimitado.
```

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

## Evidências e ambientes

Este é um método proposto, sem comparação controlada que demonstre ganhos de qualidade, tempo ou custo frente a um único agente. Testes do instalador verificam o filesystem; observações comportamentais cobrem cenários limitados.

Há adaptadores de arquivos para Codex, Claude Code e OpenCode. [HARNESSES.md](../../skills/project-advisor/references/HARNESSES.md) registra as verificações: gerar um adaptador não comprova seu carregamento real. Em chats sem acesso a arquivos, forneça o método e o estado e salve atualizações manualmente; não há validação automática do vínculo nem persistência.

## Verificações do instalador e releases

[GitHub Actions](https://github.com/GuilhermeRocha0404/project-advisor/actions/workflows/installer-tests.yml) executa `python -m unittest discover -s tests -v` em Windows e Linux com Python 3.10 e 3.12, além de macOS com Python 3.12, em pushes e Pull Requests. O workflow não adiciona dependências Python. Execute `python <skill-dir>/scripts/workspace.py --version` para identificar a versão do método; use a release ou o commit para identificar mudanças posteriores do instalador.

[Releases](https://github.com/GuilhermeRocha0404/project-advisor/releases) registram versões e mudanças para usuários; o audit preserva evidências e decisões. Não há changelog separado.

## Estado, privacidade e limites

O `AGENTS.md` instalado contém o método; `CLAUDE.md` o importa quando necessário. `.advisor-workspace.json` registra projeto, ambiente, versão e hashes dos arquivos gerenciados. `ADVISOR_STATE.md` guarda decisões privadas e progresso; o nome legado `CONSULTOR_STATE.md` pode ser preservado. Guarde preferências em `ADVISOR_LOCAL.md`. A manutenção do estado depende do modelo, sem hooks ou serviço em segundo plano.

Atualizações usam o mesmo comando de prévia/aplicação e recusam arquivos gerenciados modificados. O instalador nunca substitui um estado existente; leia-o antes de usar `--adopt-existing-state`. Novos estados POSIX solicitam permissão exclusiva do proprietário (`0600`); permissões de estados existentes são preservadas. Windows usa ACLs. Se a preparação parar antes da gravação do manifesto, siga a [recuperação de instalação interrompida](../../skills/project-advisor/references/HARNESSES.md#interrupted-first-install) para preservar o estado e revisar instruções órfãs antes de tentar novamente.

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
    ├── EXAMPLES.md
    └── STATE_SCHEMA.md
```

## Manutenção e feedback

Este é um projeto pessoal, compartilhado para uso por outras pessoas e conduzido pelo mantenedor. O mantenedor decide direção, arquitetura e implementação. [Issues](https://github.com/GuilhermeRocha0404/project-advisor/issues) são bem-vindas para bugs, incompatibilidades e experiências reais de uso. Use exemplos sintéticos pequenos e remova informações privadas. Pull Requests não são solicitados nem necessários e podem não ser aceitos.

Mantenha a documentação README somente em inglês e português do Brasil. A versão em português fica em `.github/readme/README.pt-BR.md`. Atualize as duas versões juntas para preservar o alinhamento de exemplos, comandos, links e limitações.

## Licença

[MIT](../../LICENSE) — Copyright (c) 2026 Guilherme Rocha.

## Revisão da auditoria 2.1

O estado registra a origem das evidências e reconcilia decisões substituídas, preservando restrições e verificações abertas. O instalador compartilha um esquema único, preserva nomes legados nas atualizações, valida manifestos, explica a recuperação de travas obsoletas e recusa árvores sobrepostas entre skill e workspace. Estados existentes nunca são reinicializados.

[Registro técnico em inglês](../../docs/AUDIT_2_1.md) · [Exemplos](../../skills/project-advisor/references/EXAMPLES.md)

Inglês é a referência técnica; a tradução para português não recebeu revisão independente por falante nativo.
