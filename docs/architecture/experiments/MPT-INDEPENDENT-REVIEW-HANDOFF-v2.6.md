# Encaminhamento para revisão independente — ordem v2.6

**Pacote: HANDOFF_READY / NOT_RUN.**
**Situação: AWAITING_INDEPENDENT_REVIEW_ASSIGNMENT.**
Este documento prepara a atribuição; não constitui revisão independente, aprovação ou
autorização experimental. Nenhum contato ou envio a revisor foi realizado.

## Base e materiais a entregar

Candidato **0.26**, preservado integralmente em `mpt-publication-poc/`.
HEAD conferido: `27b2db3e3818e4325e5cd3df27f4ba1bc797ab15`.
Conferência estática: 72 arquivos, 71 hashes do manifesto e 21 referências do pacote sem
divergências. Hashes demonstram integridade, não conformidade experimental.

| Material | SHA-256 verificado |
| --- | --- |
| [MANIFEST.md](mpt-publication-poc/MANIFEST.md) | 2b7b9ae27e1a911454d6120e16ac68c83f77ee24a90bc77f74cfb5f42a33cc83 |
| [EXPECTED-DECISION-PACKAGE.md](mpt-publication-poc/EXPECTED-DECISION-PACKAGE.md) | c4a87ce98a22b61668819dec7a933f2b9172f3da1a52d2181b6eacc425a4619e |

Entregar ao humano designado esses dois arquivos e os insumos da sua tarefa. A matriz
**“Order v2.5 / candidate0.26 — operational independent-review matrix”**, no início do pacote,
é a referência operacional; não a reproduzimos aqui. Usar os identificadores H01–H12 da
**seção7 desse pacote**, mais sua tabela de hashes suplementares. Não usar a numeração H
do plano de aplicação, que é diferente e contém H11 histórico explicitamente identificado.
O manifesto lista os hashes completos de cada insumo. Divergência de bytes bloqueia o uso
deste encaminhamento até nova conferência; não substituir arquivos por ZIP/cópia presumida.
Este encaminhamento fica fora do candidato, não integra sua cápsula nem altera seu manifesto.

## Atribuições, na ordem recomendada

Todos os nomes, autoridade, declaração de independência, data e assinaturas: **UNRESOLVED**.
O responsável humano deve designar os perfis abaixo e verificar sua independência dos autores
do codec, oráculo e fixtures. Um novo parecer do mesmo Codex não satisfaz esse requisito.

| Prioridade / tarefa | Perfil e insumos exatos | Resposta concreta esperada | Aceite/rejeição e dependências |
| --- | --- | --- | --- |
| 1 — IR-P02 | Revisor independente de formato binário e compatibilidade. H02, H11, H12; `runner/snapshot_compound_vectors.json`, `runner/snapshot_oracle.py` e respectivas referências suplementares | Derivação própria de frames/comprimentos; caso documental com duas ou mais linhas em uma tabela de metadados; registro histórico verificável sobre semântica @1 | Aceitar derivação somente se composição/ordem/comprimentos forem corroborados independentemente; rejeitar discrepâncias. @1 aprovado incompatível exige decisão de versão; história ausente fica UNRESOLVED. MULTI existente não cobre metadados multirow. Fixture escrita não é execução. |
| 2 — IR-P03 | Revisor independente de SQL/NULL e descritores. H03, H09, H10, H08 | Ledger dos oito campos, cláusulas exatas, premissas e oito casos NULL propostos; conclusão estática separada do pedido de evidência do DDL/view implantados | Aceitar prova estática apenas sob DDL exato; examinar NOT NULL, INNER JOIN e bicondicional de ordinal, sem depender de CHECK isolado. Divergência de cláusula invalida a premissa. Validação implantada continua pendente até evidência de ambiente obtida sob autorização própria. |
| 3 — IR-P01 | Revisor independente de esquema/serialização. H01, H09, H10, H12 | Ledger de 30 tabelas com classificação22/8, membros vazios e exemplos negativos de pertencimento/prefixo | Aceitar somente conjuntos exatos, sem omissões/duplicatas, com todos os membros vazios exigidos. Rejeitar pertencimento inferido sem regra; depende das identidades de esquema/contrato. |
| 4 — IR-P04 | Revisor independente de framing e ordenação. H04, H12; codec/reference/vetores nos hashes suplementares | Derivação sem helpers compartilhados, casos de duplicidade/colisão de representação/permutação e distinção entre PK, SQL, tempo e UI | Aceitar derivação apenas com framing inequívoco no domínio admitido e expectativas explícitas de rejeição de duplicatas/invariância de permutação. Testes futuros exigem autorização. Não alegar prova de ausência de colisões SHA ou equivalência temporal/UI; depende de P05. |
| 5 — IR-P05 | Revisor independente de tipos/precisão e domínio PostgreSQL. H05, H09, H12; `runner/snapshot_vectors.json` e fontes suplementares | Worksheet de literais e limites por versão/tipo PostgreSQL com fontes autoritativas fornecidas; casos adversariais e delimitação do que permanece não demonstrado | Rejeitar coerção, normalização, perda de escala ou confusão SQL NULL/JSON null. Aceitar apenas domínio explicitamente sustentado; não recuperar precisão perdida nem extrapolar limites Python. Evidência de armazenamento real requer autorização distinta. |
| 6 — IR-API | Revisor independente de contratos/API e responsável pelos consumidores. H06 patch, H07 comparador, H08 testes; `EXPECTED-API-MIGRATION.md`, `EXPECTED-COUNTER-PROPOSAL.md` | Tabela de verdade independente dos sete contadores; inventário interno/externo atestado pelo proprietário; casos de rejeição @2/@3 e erro/aborto/recheck | Aceitar semântica somente se ambas desigualdades e populações forem consistentes, sem relatório parcial após falha. Validade de registro não é validade do wire. Consumidores externos UNKNOWN até evidência; leitor operacional ausente não dispensa seus testes futuros. Patch não aplicado. |

As tarefas acima solicitam primeiro análise documental **S**, sem conexão ou execução.
Especificações de fixtures/casos negativos não preenchem os 428 slots nem autorizam geração.
Testes **E**, segunda implementação, consulta a banco e prova de ambiente **C** são trabalho
posterior, dependente de autorização explícita. Documentação externa deve ser fornecida pelo
humano; este encaminhamento não autoriza busca de rede ou contato com fornecedores.

## Independência e formato de retorno

Para cada IR, devolver um registro com: ID da tarefa; identidade/autoridade e vínculo do
revisor; declaração de independência e dependências compartilhadas; hashes inspecionados;
premissas; derivação ou contraexemplo; lacunas; recomendação
**APPROVE / REVISE / REJECT / DEFER**, condições e data verificáveis.
Nenhum desses campos humanos está preenchido como evidência neste documento.

Derivar expectativas do contrato/DDL, não reutilizar saídas do codec/oráculo/emissor como
verdade. Eventual segunda implementação precisa de derivação própria e autorização posterior;
um wrapper do mesmo oráculo não é independente. Preservar pareceres negativos/inconclusivos.
Os registros permitem a próxima decisão humana individualizada; não equivalem automaticamente
a decisão contratual autenticada, autorização de edição ou permissão experimental.

## Proprietários humanos ainda necessários

- **SECURITY_AUTHORITY_OWNER:** OAA real, verificador, política de confiança/escopo/revogação
  e comprovação de identidade/independência dos revisores.
- **RUNTIME_SECURITY_REVIEWER:** bytes efetivamente carregados, runtime/import closure,
  handles imutáveis e proteção contra substituição.
- **OFFLINE_EXECUTION_OWNER:** isolamento sem rede, limites nativos de CPU/memória/tempo,
  saída/cleanup e monitor externo com evidência operacional.
- **Responsável de implantação e consumidores:** DDL/view realmente aplicados, versão PostgreSQL
  e inventário externo de leitores, com procedência verificável.

Nenhuma pessoa, mecanismo, chave, certificado ou qualificação é inventada ou escolhida.
Aprovar as seis semânticas não resolve essas pendências técnicas.

## ARCH-ADAPT-001: encaminhamento restrito

Permanece **PROPOSED / REVIEW_ONLY**. Usar o checklist específico já existente no pacote:
**DM-2** recebe fonte/capacidade/direitos, sem equivalência científica B3/Nelogica;
**DM-4**, fronteiras/versionamento/topologia do caminho crítico;
**DM-6**, protocolo/UI/frescor, sem descartar eventos exigidos pelo MIR para aliviar renderização;
**DM-7**, mensuração representativa, sobrecarga, isolamento e operação.
Designar os proprietários dessas frentes; pedir somente as respostas e artefatos já definidos.
Não criar metas numéricas, executar benchmarks ou inferir desempenho real de fixtures sintéticas.

## Parada e invariantes

Próxima ação humana: designar revisores independentes, começando por IR-P02 e IR-P03, e entregar
os materiais hash-bound acima. Em seguida, recolher os registros individuais antes de decidir
sobre alterações específicas. Nenhum revisor foi designado nem acionado por este trabalho.

**AWAITING_INDEPENDENT_REVIEW_ASSIGNMENT**, nunca REVIEW_PASSED.
Candidato0.26 e seus72 arquivos preservados; apenas este encaminhamento externo foi criado.
Patch não aplicado; report@3 e seis aprovações formais pendentes; A0/fail-closed ativo.
428 slots: EMPTY43/TYPED287/MULTI98, todos UNRESOLVED; zero gerados/revisados/congelados/observados.
GENERATE_EXPECTED, REVIEW_AND_FREEZE e COMPARE_FROZEN permanecem NOT_AUTHORIZED.
EXEC-G1/PERS-G1 OPEN; PUB-T13B pendente. RH/MIR/MPT, availableAt(input)<=decisionTime,
T3a versus TP, T2a/T2b e DO_NOT_NOTIFY preservados.
Nenhum Python/SQL/teste/runner/cápsula/contêiner/banco/rede/controlador/benchmark executado;
nenhuma expectativa gerada/congelada/comparada, assinatura, commit, ZIP ou promoção de gate.
