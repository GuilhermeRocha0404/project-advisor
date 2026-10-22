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

Use o **consultor em um chat separado, com workspace fora da árvore de diretórios do projeto**. Mantenha o trabalhador no workspace do projeto, seguindo as instruções aplicáveis. Outro chat associado ao mesmo projeto ainda pode carregar seu `AGENTS.md`, `CLAUDE.md` ou outras regras locais.

Isso reduz o carregamento automático de instruções específicas do projeto no contexto do consultor. Regras globais, instruções de pastas superiores, integrações e contexto herdado ainda podem se aplicar; não há garantia de isolamento completo. Forneça o contexto necessário por meio de objetivos, documentos selecionados e relatos do trabalhador. O consultor pode examinar as regras do projeto como evidência, respeitando a hierarquia de instruções do ambiente.

Guarde o estado de consultoria de cada projeto em uma pasta externa própria, fora da skill instalada e, preferencialmente, fora do repositório do projeto. Não publique o estado privado junto com a skill.

## Instalação

Clone ou baixe este repositório e copie a pasta inteira `skills/project-advisor` para o local adequado. Preserve `references/` e `agents/` ao lado de `SKILL.md`. Revise suas alterações locais antes de substituir uma instalação existente.

| Ambiente | Pasta de instalação pessoal | Invocação explícita |
|---|---|---|
| Codex | `~/.agents/skills/project-advisor/` | `$project-advisor` |
| Claude Code | `~/.claude/skills/project-advisor/` | `/project-advisor` |
| OpenCode | `~/.config/opencode/skills/project-advisor/` | Selecione ou carregue a skill explicitamente; veja a configuração opcional de comando abaixo. |

Aqui, `~` representa sua pasta de usuário, inclusive no Windows. Os diretórios indicados se referem às ferramentas locais; produtos hospedados podem usar outros mecanismos. Após instalar, abra uma nova sessão de consultoria se a skill ainda não aparecer.

### Controles de invocação

O núcleo sempre exige um pedido explícito de ativação. Os controles do ambiente são configurados separadamente:

- **Codex:** o arquivo incluído `agents/openai.yaml` define `policy.allow_implicit_invocation: false`.
- **Claude Code:** adicione `disable-model-invocation: true` ao frontmatter YAML do `SKILL.md` instalado para impedir a invocação por iniciativa do modelo. Esse campo é uma adaptação para Claude Code e não faz parte do arquivo compartilhado neste repositório.
- **OpenCode:** adicione os metadados abaixo, com valores em texto, ao frontmatter do `SKILL.md` instalado para disponibilizar um comando e retirar a skill das orientações de seleção automática:

  ```yaml
  metadata:
    opencode/slash: "true"
    opencode/autoinvoke: "false"
  ```

  Depois, invoque `/project-advisor` nas versões que oferecem essas configurações. Se o seu cliente funcionar de outra forma, use o mecanismo explícito de carregamento de skills dele.

Esses ajustes são locais à instalação; não exigem cópias separadas da metodologia neste repositório. Antes de atualizar uma instalação, preserve as configurações de frontmatter específicas do ambiente.

As orientações de instalação e invocação foram conferidas na documentação oficial do [Codex](https://learn.chatgpt.com/docs/build-skills), [Claude Code](https://code.claude.com/docs/en/skills) e [OpenCode](https://opencode.ai/docs/skills/) em 21 de outubro de 2026. **Esta versão não foi testada de ponta a ponta nos três clientes.** Conferir a documentação não equivale a certificar compatibilidade em execução. O uso anterior do consultor em português orientou esta versão; a adaptação em inglês ainda precisa de avaliações em mais contextos reais.

## Ativação e uso

Invoque a skill pelo mecanismo do seu ambiente e informe o objetivo e a pasta de estado. Por exemplo:

```text
Ative o Project Advisor.
Use esta pasta externa de estado: /caminho/para/meu-workspace-de-consultoria.
O trabalhador de implementação está em outro chat.
Quero adicionar importação de clientes por CSV a uma aplicação existente.
```

O consultor lê suas instruções centrais e o estado externo, ou cria o estado quando necessário. Ele permanece ativo no mesmo chat até você desativá-lo explicitamente:

```text
Desative o consultor.
```

Em um novo chat, ative a skill novamente e informe a mesma pasta de estado para retomar o projeto. A instalação, sozinha, nunca ativa o papel. As instruções da skill permanecem em inglês; **o consultor se comunica no idioma que você preferir**.

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

O consultor usa `ADVISOR_STATE.md` no seu workspace externo. Ao criar um estado novo, um `ADVISOR_STATE_TEMPLATE.md` existente tem preferência sobre o esquema de recuperação incluído. O arquivo `STATE_SCHEMA.md` contém somente campos genéricos para preenchimento.

O estado pode conter decisões sensíveis, caminhos e informações do projeto. Escolha com cuidado onde armazená-lo e com quem compartilhá-lo. O `.gitignore` deste repositório exclui os nomes dos arquivos de estado, mas essa proteção vale somente dentro desta cópia do repositório e não remove arquivos que já estejam rastreados. Prefira guardar o estado privado fora dos repositórios que pretende publicar.

O estado é consolidado durante os turnos ativos quando há mudanças relevantes, ao encerrar trabalhos ou ao retomar após compactação, conforme necessário. Não há processo em segundo plano, hook de sessão ou garantia de recuperação se o contexto de ativação se perder. Quando necessário, reative a skill informando a mesma pasta de estado. Se o acesso a arquivos não estiver disponível, o consultor pode fornecer um resumo de continuidade para você salvar, em vez de afirmar que o estado foi persistido.

A skill fornece instruções, não controles de acesso ou garantia de decisões corretas. Seu comportamento depende do modelo, das evidências disponíveis, das instruções do ambiente e das ferramentas. Ela não implementa o projeto coordenado nem contata o trabalhador por iniciativa própria.

## Estrutura do repositório

```text
skills/project-advisor/
├── SKILL.md                   Ativação, estado e continuidade
├── agents/openai.yaml         Política de invocação específica do Codex
└── references/
    ├── ADVISOR_CORE.md        Método independente de plataforma
    └── STATE_SCHEMA.md        Estrutura de recuperação do estado
```

## Contribuições

Descreva um problema real, o comportamento esperado e por que a mudança proposta ajuda sem acrescentar processo desnecessário. Use exemplos sintéticos, remova informações privadas e informe o ambiente e os limites das verificações de comportamento realizadas. Melhorias devem preservar a distinção entre orientações reutilizáveis e preferências particulares de uma pessoa ou projeto.

As traduções do README ficam em `.github/readme/`. Ao atualizar a documentação, mantenha exemplos, comandos, links e limitações alinhados com o README em inglês. Adicione links de navegação somente para traduções incluídas no repositório.

## Licença

[MIT](../../LICENSE) — Copyright (c) 2026 Guilherme Rocha.
