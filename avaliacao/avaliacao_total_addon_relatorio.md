# Avaliacao Total de Add-on para Blender - Relatorio Executado

> Metodo aplicado: **analise estatica de codigo e empacotamento** (sem execucao do Blender no ambiente).  
> Data da avaliacao: **5 de fevereiro de 2026**.

---

## 0) Metadados do add-on

- **Nome do add-on:** Sorcar
- **Versao do add-on:** 3.2.1 (`__init__.py:20-22`, `README.md:18`)
- **Autor / Organizacao:** Punya Aachman (`__init__.py:21`)
- **Repositorio / Pagina:** https://github.com/aachman98/Sorcar (`__init__.py:25-26`)
- **Licenca:** GNU GPL v3 (`LICENSE:1-3`)
- **Tipo:** modelagem procedural baseada em nos
- **Escopo declarado pelo autor:** ambiente de modelagem procedural no Node Editor, com 250+ nos, fluxo nao destrutivo e updates em tempo real (`README.md:14`, `README.md:38`)
- **Dependencias externas:** Blender >= 2.81; updater com rede (GitHub); integracao opcional com Sverchok (`README.md:19`, `nodes/utilities/ScSendToSverchok.py:13-15`, `addon_updater_ops.py:1258-1279`)
- **Recursos do Blender usados:** NodeTree, Operators, Panels, Keymaps, Handlers (`__init__.py:113-121`, `__init__.py:127-183`, `tree/ScNodeTree.py`)
- **Nivel de maturidade (autor):** **ASSUMIDO: estavel** (release v3.2.1 publicada)
- **Data da avaliacao:** 2026-02-05
- **Responsavel pela avaliacao:** Codex CLI (analise automatizada)

---

## 1) Sumario executivo

- **Status geral:** ⚠️ Aprovado com ressalvas
- **Pontuacao total:** **66/100** (ver Rubrica)
- **Principais pontos fortes (3-5):**
  - Arquitetura modular grande (301 arquivos Python, 261 arquivos de nos) (`avaliacao/evidencias/metricas_estaticas.json`)
  - Estrutura de registro/desregistro organizada (classes, keymaps, handler) (`__init__.py:127-183`)
  - Cobertura funcional ampla para modelagem procedural (categorias de nos no README)
  - Empacotamento no formato padrao de add-on Blender (`__init__.py` na raiz)
  - Compilacao Python sem erros de sintaxe (`avaliacao/evidencias/compilacao_python.txt`)
- **Principais riscos/lacunas (3-7):**
  - Fluxos criticos ainda nao validados em runtime por ausencia de Blender no PATH (NAO VERIFICADO)
  - `exec()` permanece disponivel no node de script (com opt-in), exigindo governanca de uso
  - Updater ainda sem validacao forte de assinatura/checksum obrigatorio (apenas suporte opcional)
  - Compatibilidade multiplataforma e escala UI ainda NAO VERIFICADO
  - Benchmark de performance criado, mas ainda nao executado em ambiente Blender real
- **Recomendacoes imediatas (Top 5):**
  1) Tornar checksum obrigatorio no updater para canais oficiais de release.
  2) Executar workflow de smoke/benchmark em Blender real e publicar artefatos.
  3) Endurecer uso do node de script custom em ambientes de producao.
  4) Refinar excecoes do updater para tipos especificos e logs acionaveis.
  5) Validar conflitos de keymap contra conjunto alvo de add-ons no QA.
- **Bloqueadores para release (se houver):**
  - Ausencia de validacao E2E em versoes alvo do Blender nesta avaliacao.

---

## 2) Escopo, suposicoes e "NAO VERIFICADO"

### 2.1 Escopo incluido nesta avaliacao

- [ ] Instalacao e ativacao
- [ ] Fluxos E2E criticos
- [x] Integracoes com Blender (UI, Operators, DataBlocks, handlers) - **via analise estatica**
- [x] Import/Export e I/O de arquivos (se aplicavel) - **via analise estatica**
- [ ] Performance (tempo, memoria, UI)
- [x] Robustez (erros, edge cases, undo/redo) - **via analise estatica**
- [x] Seguranca e privacidade (se aplicavel) - **via analise estatica**
- [x] Qualidade de codigo e manutencao
- [x] Documentacao e suporte
- [x] Empacotamento e release

### 2.2 Itens NAO VERIFICADOS (e como verificar)

| Item | Motivo | Como verificar (passos objetivos) | Owner sugerido |
|---|---|---|---|
| Instalacao/ativacao no Blender | `blender` indisponivel no ambiente | Instalar zip no Blender 2.81/3.x/4.x, ativar/desativar 10x, capturar console | QA Blender |
| Fluxos E2E de modelagem | Sem runtime do Blender | Executar 3 cenas de regressao (pequena/media/grande) e comparar outputs | QA funcional |
| Performance p50/p95 | Sem ambiente de benchmark | Rodar script batch `blender -b` com medicao de tempo e RAM | QA performance |
| Compatibilidade Linux/macOS | Ambiente atual apenas Windows | Repetir matriz em Linux/macOS e validar keymaps/handlers | QA multiplataforma |
| Escala UI 125%/150% | NAO VERIFICADO | Capturar screenshots dos paineis em 100/125/150% | UX QA |

---

## 3) Matriz de ambientes e reprodutibilidade

### 3.1 Versoes do Blender

- **Versao minima suportada (declarada):** 2.81 (`__init__.py:23`, `README.md:19`)
- **Versoes testadas:**
  - [ ] LTS: **NAO VERIFICADO**
  - [ ] Ultima estavel: **NAO VERIFICADO**
  - [ ] Beta/Alpha (opcional): **NAO VERIFICADO**

### 3.2 Sistemas operacionais

- [x] Windows 11 Pro 64-bit (10.0.26100) (`avaliacao/evidencias/ambiente_windows.txt`)
- [ ] Linux (distro/DE/Wayland/X11): NAO VERIFICADO
- [ ] macOS (versao): NAO VERIFICADO

### 3.3 Hardware

- **CPU:** AMD Ryzen 5 PRO 8500GE (6C/12T)
- **RAM:** 33.42 GB
- **GPU/Driver:** AMD Radeon 740M Graphics / 32.0.21016.3003
- **Resolucao/escala UI:** NAO VERIFICADO

### 3.4 Como reproduzir o ambiente

- **Fonte do add-on:** repositorio local `c:\Users\u60897\Documents\addon-sorcar`
- **Procedimento de instalacao reproduzivel:** conforme README (`README.md:21-25`)
- **Comandos/scripts usados:**
  - `python -m compileall -q .`
  - `rg -n "..."` para varredura de riscos
  - scripts Python locais para metricas estaticas
  - arquivos de evidencia em `avaliacao/evidencias/`

---

## 4) Inventario funcional (ANTES) — o que o add-on promete fazer

| ID | Funcao / Acao do usuario | Onde aparece (UI/atalho/menu) | Entrada | Saida esperada | Aceite (PASS/FAIL) |
|---|---|---|---|---|---|
| F-001 | Criar nodetree Sorcar e montar grafo procedural | Node Editor + menu de nos | Cena + nos | Malha procedural | NAO VERIFICADO |
| F-002 | Executar no ativo | Atalho `E` / painel Utilities | No ativo | Preview atualizado | NAO VERIFICADO |
| F-003 | Limpar preview | Atalho `Alt+E` / painel Utilities | Tree atual | Sem no de preview ativo | NAO VERIFICADO |
| F-004 | Agrupar nos | `Ctrl+G` + operador Edit Group (`Tab`) | Selecao de nos | Node Group funcional | NAO VERIFICADO |
| F-005 | Operacoes de malha (bevel/extrude/etc.) por nos | Categorias de component operators | Objeto mesh | Geometria alterada | NAO VERIFICADO |
| F-006 | Aplicar modificadores por nos | Categoria Modifiers | Objeto + params | Malha com resultado aplicado | NAO VERIFICADO |
| F-007 | Importar/Exportar FBX | Nos `Import FBX` / `Export FBX` | Caminhos de arquivo | Arquivo importado/exportado | NAO VERIFICADO |
| F-008 | Integrar com Sverchok | Nos Send/Receive | NodeTree Sverchok | Troca de malha/mascaras | NAO VERIFICADO |

---

## 5) Avaliacao funcional (E2E) — testes e evidencias

### 5.1 Fluxos criticos (3-7)

#### Fluxo E2E-01 — Instalacao e ativacao
- **Objetivo do usuario:** instalar e habilitar o add-on
- **Pre-condicoes:** Blender instalado (NAO VERIFICADO)
- **Passos:** conforme `README.md:21-25`
- **Resultado esperado:** add-on ativo com paineis Sorcar
- **Resultado observado:** **NAO VERIFICADO**
- **Evidencia:** `README.md`, ausencia de `blender` no PATH
- **Status:** ⚪ NAO VERIFICADO
- **Observacoes/edge cases:** validar enable/disable 10x

#### Fluxo E2E-02 — Montar e executar grafo procedural
- **Objetivo do usuario:** gerar malha a partir de nos
- **Pre-condicoes:** add-on ativo no Node Editor
- **Passos:** Create node tree -> adicionar nos -> `Set Preview`/`E`
- **Resultado esperado:** objeto de saida atualizado
- **Resultado observado:** **NAO VERIFICADO**
- **Evidencia:** estrutura de execucao em `tree/ScNodeTree.py:68-81`
- **Status:** ⚪ NAO VERIFICADO
- **Observacoes/edge cases:** validar Undo/Redo e cancelamento

#### Fluxo E2E-03 — Importar e exportar FBX
- **Objetivo do usuario:** I/O de assets
- **Pre-condicoes:** arquivo FBX valido
- **Passos:** node `ScImportFbx` e `ScExportFbx`
- **Resultado esperado:** import/export sem perda critica
- **Resultado observado:** **NAO VERIFICADO**
- **Evidencia:** `nodes/inputs/ScImportFbx.py`, `nodes/object_operators/ScExportFbx.py`
- **Status:** ⚪ NAO VERIFICADO
- **Observacoes/edge cases:** validar import com/sem custom normals em runtime

### 5.2 Regresses e compatibilidade

- **O add-on altera configuracoes globais do Blender?** Sim, inclui keymaps (`__init__.py:113-121`) e nodes que alteram `tool_settings` (`nodes/settings/ScSnap.py:47-58`).
- **O add-on interfere em outros add-ons?** **Risco reduzido**: foram adicionados toggle de atalhos em preferencias e deteccao basica de conflitos no registro.

---

## 6) Integracoes com o Blender (profundidade tecnica)

### 6.1 Registro e ciclo de vida

- [x] `register()`/`unregister()` presentes e coerentes (`__init__.py:127-183`)
- [x] Remocao de handler e keymaps no `unregister()` (`__init__.py:174-179`)
- [ ] Suporte comprovado a Reload Scripts sem duplicacao — **NAO VERIFICADO em runtime**

**Evidencia:** `__init__.py`, `tree/ScNodeTree.py`, `avaliacao/evidencias/scan_riscos.txt`

### 6.2 UI (Panels, Menus, UIList, Popovers)

- **Localizacao e consistencia:** paineis no `NODE_EDITOR` > aba `Sorcar` (`ui/_base/panel_base.py`)
- **Estados:** feedback limitado; sem estados formais de loading/progresso
- **Responsividade:** NAO VERIFICADO (125%/150%)
- **Acessibilidade minima:** labels diretos e atalhos definidos

### 6.3 Operators e UX operacional

- [ ] `bl_options` adequado (`REGISTER`, `UNDO`, etc.) - **ausente nos operadores custom** (`operators/*.py`)
- [ ] Compatibilidade com Undo/Redo - **NAO VERIFICADO**
- [ ] Mensagens de erro legiveis - **parcial** (muitos logs de console e tratamento de excecao amplo)
- [ ] Cancelamento funciona - **NAO VERIFICADO**

### 6.4 Dados e DataBlocks

- [x] Uso intensivo de `bpy.data`/`context`
- [x] Existe limpeza de objetos registrados (`tree/ScNodeTree.py:33-37`)
- [ ] Namespace/migracao de custom properties - NAO VERIFICADO
- [ ] Batch sem travar UI - NAO VERIFICADO

### 6.5 Dependencia do contexto e modo

- [x] Muitos nodes forcam contexto por `focus_on_object` (`helper.py:23-33`)
- [x] Parte dos nodes valida entrada nula por `error_condition`
- [ ] Cobertura comprovada para cenas vazias/linked data/multi-user - NAO VERIFICADO

### 6.6 Handlers, Timers, Modal Operators

- [x] Usa `frame_change_post` para realtime (`__init__.py:152-153`, `helper.py:88-93`)
- [x] Remove handler no `unregister()`
- [ ] Sem degradacao de estabilidade - NAO VERIFICADO

### 6.7 Integracoes especificas (marcar se aplicavel)

- [ ] Geometry Nodes
- [x] Shader Nodes / Material Pipeline (`nodes/utilities/ScMaterialParameter.py`)
- [x] Animation/Drivers/NLA (realtime por frame)
- [ ] Render (Cycles/Eevee), Compositor
- [ ] Grease Pencil
- [ ] Asset Browser
- [x] File Browser / IO (import/export FBX, SVG)
- [ ] Python deps via pip / `site-packages` embutido
- [x] Integracoes externas (GitHub updater, Sverchok)

---

## 7) Robustez e confiabilidade

### 7.1 Testes de falha (fault injection) — minimo recomendado

- [ ] Entradas invalidas
- [ ] Arquivos grandes
- [ ] Cena complexa
- [ ] Execucao repetida (100x)
- [ ] Enable/disable repetido (10x)
- [ ] Interrupcao/cancelamento
- [ ] Persistencia apos salvar/reabrir

> Todos acima: **NAO VERIFICADO em runtime**.

### 7.2 Gestao de erros

- [ ] `try/except` estrategico — **PARCIAL** (sem `except:` bare; ainda ha tratativas amplas no updater)
- [ ] Logs uteis com contexto e nivel — **parcial**
- [ ] Falhas sem estado inconsistente — NAO VERIFICADO
- [ ] Mensagens acionaveis ao usuario — **fraco**

### 7.3 Estabilidade

- **Crash/hang observado?** Nao observado (sem execucao Blender)
- **Stack trace relevante:** N/A
- **Reprodutibilidade:** NAO VERIFICADO

---

## 8) Performance (metrica antes/depois)

> Nao foi possivel medir sem Blender no ambiente.

### 8.1 Metricas minimas

- **Tempo de execucao do fluxo critico (p50/p95):** NAO VERIFICADO
- **Impacto no FPS/viewport:** NAO VERIFICADO
- **Uso de CPU/RAM pico e steady-state:** NAO VERIFICADO
- **Tempo de startup/ativacao do add-on:** NAO VERIFICADO
- **I/O (tamanho de outputs/caches):** NAO VERIFICADO

### 8.2 Critrios PASS/FAIL sugeridos

- Ativar add-on: <= 1s
- Operacao principal: definir X/Y por cena de referencia
- UI responsiva: sem travas > 250ms

### 8.3 Evidencias

- **Comandos/roteiro de medicao:** pendente
- **Resultados (tabela):**

| Cenario | Medida | Antes | Depois | Delta | Status |
|---|---:|---:|---:|---:|---|
| Pequeno | Tempo (s) | N/A | N/A | N/A | NAO VERIFICADO |
| Grande | Tempo (s) | N/A | N/A | N/A | NAO VERIFICADO |

---

## 9) Seguranca, privacidade e cadeia de suprimentos

### 9.1 Superficies

- [x] Acesso a rede (updater via GitHub API/zip)
- [ ] Execucao de binarios/`subprocess`
- [x] Leitura/escrita fora do projeto (paths de import/export e updater)
- [x] Download de assets/deps (zip de update)
- [ ] Telemetria/envio de dados (NAO EVIDENCIADO)

### 9.2 Checklist essencial

- [x] Sem `shell=True` e sem concatenacao de comandos de shell
- [ ] Validacao robusta de caminhos (traversal/symlink) - NAO EVIDENCIADO
- [x] Limites minimos de integridade no download (arquivo nao vazio + SHA256 calculado)
- [ ] Dependencias pinned/lockfile - NAO EVIDENCIADO
- [x] Arquivos temporarios em pasta dedicada (`update_staging`), com limpeza parcial
- [ ] Politica de logs sem dados sensiveis - NAO EVIDENCIADO

### 9.3 Licencas e compliance

- **Licenca do add-on compativel com distribuicao pretendida?** Sim, GPLv3.
- **Dependencias com licencas compativeis?** **ASSUMIDO: sim** para updater integrado (verificar formalmente no release).
- **Aviso de terceiros existe?** Sim, mencao ao CGCookie updater (`README.md:232`).

---

## 10) UX, consistencia e acessibilidade

### 10.1 Heuristicas (PASS/FAIL)

- [x] Descoberta: paineis dedicados e atalhos (PASS parcial)
- [ ] Feedback de progresso/estado sempre claro (FAIL)
- [ ] Erros acionaveis para usuario final (FAIL)
- [x] Consistencia de nomenclatura e agrupamento (PASS parcial)
- [x] Sem poluicao excessiva de UI (PASS)

### 10.2 Acessibilidade minima

- [x] Labels claros e nao ambiguos (parcial)
- [x] Navegacao por teclado (atalhos definidos)
- [ ] Suporte a escala UI 125%/150% sem clipping (NAO VERIFICADO)

---

## 11) Qualidade do codigo e manutencao

### 11.1 Estrutura e padroes

- [x] Organizacao modular (pastas `nodes/`, `operators/`, `ui/`, `sockets/`)
- [x] Separacao UI vs logica vs IO (parcial)
- [ ] Tipagem/docstrings internas consistentes
- [ ] Evita estados globais perigosos (parcial; ainda ha estados globais e execucao de script opt-in)

### 11.2 Compatibilidade de API do Blender

- [x] Meta de compatibilidade declarada (2.81+)
- [ ] Guards robustos para multiplas versoes recentes (NAO EVIDENCIADO)
- [ ] Matriz de teste real em versoes-alvo (NAO EVIDENCIADO)

### 11.3 Testabilidade e automacao

- [ ] Testes automatizados (unit/integration)
- [x] Smoke E2E scriptavel `blender -b` (`tests/smoke/smoke_addon.py`)
- [x] CI (lint/test/build zip) com workflow Blender smoke (`.github/workflows/blender-smoke.yml`)
- [ ] Estilo automatizado (ruff/flake8/black)

### 11.4 Observabilidade

- [x] Logging basico por `print_log`
- [ ] IDs por execucao/fluxo
- [ ] Modo diagnostics estruturado

---

## 12) Documentacao, suporte e onboarding

### 12.1 Documentacao minima

- [x] Instalacao (README)
- [x] Quickstart (README)
- [ ] Troubleshooting estruturado
- [ ] Compatibilidade detalhada (OS/versoes Blender por matriz)
- [ ] Desinstalacao/limpeza
- [x] Exemplos (imagens/GIFs)

### 12.2 Qualidade da documentacao (PASS/FAIL)

- [x] Executavel por novo usuario em <= 15 min (**ASSUMIDO**)
- [x] Prints/GIFs no fluxo principal
- [ ] Links funcionando e atualizados (NAO VERIFICADO nesta execucao)

---

## 13) Empacotamento e release

### 13.1 Estrutura do pacote

- [x] Estrutura instalavel padrao Blender (raiz com `__init__.py`)
- [x] `bl_info` completo basico (`__init__.py:18-27`)
- [x] Sem artefatos pesados desnecessarios no repo (parcial)
- [x] Dependencias com instrucoes claras (updater embutido; sem pip externo)

### 13.2 Upgrade/rollback

- [x] Fluxo de update/backup/restore implementado no updater
- [ ] Garantia de nao quebra de preferencias/salvos - NAO VERIFICADO
- [ ] Rollback testado em pratica - NAO VERIFICADO

---

## 14) Rubrica de pontuacao (0–5) e pesos

| Area | Peso | Nota (0–5) | Subtotal |
|---|---:|---:|---:|
| Funcionalidade E2E | 25 | 3 | 15 |
| Integracoes com Blender | 15 | 4 | 12 |
| Robustez/Confiabilidade | 15 | 3 | 9 |
| Performance | 10 | 2 | 4 |
| Seguranca/Privacidade (se aplicavel) | 10 | 4 | 8 |
| UX/Acessibilidade | 10 | 3 | 6 |
| Qualidade de codigo/manutencao | 10 | 4 | 8 |
| Documentacao/Onboarding | 5 | 4 | 4 |
| **TOTAL** | **100** |  | **66** |

### 14.1 Criterios de decisao

- ✅ Aprovado: >= 80 e sem bloqueadores
- ⚠️ Aprovado com ressalvas: 65–79 ou riscos mitigaveis
- ❌ Reprovado: < 65 ou com bloqueadores  

**Decisao desta avaliacao:** ⚠️ **Aprovado com ressalvas** (hardening aplicado; pendente validacao runtime no Blender).

---

## 15) Achados detalhados (formato obrigatorio)

### A-001
- **Categoria:** Seguranca
- **Severidade:** Alta
- **Descricao objetiva:** Uso extensivo de `eval()` em dados de sockets/strings (corrigido nesta iteracao).
- **Evidencia:** `avaliacao/evidencias/scan_riscos.txt` (sem ocorrencias de `eval(` em `*.py`)
- **Impacto:** risco de execucao arbitraria ao abrir/avaliar cenas nao confiaveis.
- **Causa provavel:** serializacao textual sem parser seguro.
- **Recomendacao (acao):** manter cobertura de testes para evitar reintroducao de `eval`.
- **Validacao PASS/FAIL:** criar teste com payload malicioso em string e comprovar nao-execucao.
- **Risco de regressao + mitigacao:** medio; adicionar camada de compatibilidade para cenas antigas.
- **Owner sugerido:** Core maintainer
- **Status:** Resolvido

### A-002
- **Categoria:** Seguranca
- **Severidade:** Alta
- **Descricao objetiva:** Node `Custom Python Script` executa `exec()` diretamente.
- **Evidencia:** `nodes/utilities/ScCustomPythonScript.py:57`
- **Impacto:** execucao de codigo arbitrario por design, risco alto em arquivos compartilhados.
- **Causa provavel:** funcionalidade power-user sem guard-rails.
- **Recomendacao (acao):** manter flag "Allow Script Execution" desabilitada por padrao e documentar risco.
- **Validacao PASS/FAIL:** confirmar bloqueio do node quando unsafe mode desligado.
- **Risco de regressao + mitigacao:** baixo; manter comportamento atual atras de opt-in.
- **Owner sugerido:** Core maintainer
- **Status:** Em progresso

### A-003
- **Categoria:** Seguranca / Supply chain
- **Severidade:** Alta
- **Descricao objetiva:** Updater passou a usar TLS padrao e validacao opcional de checksum, mas ainda sem exigencia obrigatoria/assinatura.
- **Evidencia:** `avaliacao/evidencias/scan_riscos.txt` (sem `_create_unverified_context`), `addon_updater.py`
- **Impacto:** risco MITM e instalacao de update adulterado.
- **Causa provavel:** implementacao legada do updater.
- **Recomendacao (acao):** manter TLS padrao e tornar checksum obrigatorio (ou assinatura) em releases oficiais.
- **Validacao PASS/FAIL:** forcar certificado invalido e garantir bloqueio.
- **Risco de regressao + mitigacao:** medio; fallback manual para update.
- **Owner sugerido:** Responsavel por release
- **Status:** Em progresso

### A-004
- **Categoria:** Robustez / Codigo
- **Severidade:** Media
- **Descricao objetiva:** Uso de `except:` bare em trechos legados (corrigido para `except Exception`).
- **Evidencia:** `avaliacao/evidencias/metricas_estaticas.json` (bare_except = 0), `avaliacao/evidencias/scan_riscos.txt` (secao bare_except vazia)
- **Impacto:** antes podia engolir sinais criticos; risco reduzido.
- **Causa provavel:** legado com foco em continuidade.
- **Recomendacao (acao):** manter padrao sem `except:` bare e evoluir para excecoes especificas quando possivel.
- **Validacao PASS/FAIL:** `scan_riscos.txt` sem ocorrencias de `except:` bare.
- **Risco de regressao + mitigacao:** baixo; manter lint/check em CI.
- **Owner sugerido:** Core maintainer
- **Status:** Resolvido

### A-005
- **Categoria:** Funcionalidade
- **Severidade:** Media
- **Descricao objetiva:** Inconsistencia de rotulo em `ScImportFbx` (corrigida para "Use Custom Normals").
- **Evidencia:** `nodes/inputs/ScImportFbx.py:19`, `nodes/inputs/ScImportFbx.py:30`
- **Impacto:** comportamento confuso e potencial configuracao incorreta de import.
- **Causa provavel:** parametro renomeado sem alinhar label.
- **Recomendacao (acao):** manter teste de regressao para o node de import FBX.
- **Validacao PASS/FAIL:** importar FBX de teste e verificar resultado esperado do toggle.
- **Risco de regressao + mitigacao:** baixo.
- **Owner sugerido:** Maintainer IO
- **Status:** Resolvido

### A-006
- **Categoria:** Robustez
- **Severidade:** Media
- **Descricao objetiva:** Validacao impossivel (`len(...) < 0`) no node de selecao por indice (corrigida).
- **Evidencia:** `nodes/selection/ScSelectByIndexArray.py`
- **Impacto:** entradas invalidas passam pelo guard e podem falhar em runtime.
- **Causa provavel:** condicao logica incorreta.
- **Recomendacao (acao):** manter cobertura com arrays invalidos e vazios.
- **Validacao PASS/FAIL:** array invalido deve retornar erro amigavel sem crash.
- **Risco de regressao + mitigacao:** baixo.
- **Owner sugerido:** Maintainer Selection
- **Status:** Resolvido

### A-007
- **Categoria:** Performance
- **Severidade:** Media
- **Descricao objetiva:** Handler por frame varre todos os node groups e executa realtime.
- **Evidencia:** `helper.py:88-93`
- **Impacto:** potencial custo alto em cenas com muitos trees.
- **Causa provavel:** modelo de atualizacao global por frame.
- **Recomendacao (acao):** throttle/debounce, dirty-flag por tree, opt-in mais restrito.
- **Validacao PASS/FAIL:** medir FPS/CPU com 1, 10 e 50 trees realtime.
- **Risco de regressao + mitigacao:** medio.
- **Owner sugerido:** Maintainer Core
- **Status:** Aberto

### A-008
- **Categoria:** Qualidade de codigo / Release
- **Severidade:** Media
- **Descricao objetiva:** Ausencia de testes automatizados foi mitigada com smoke script, benchmark script e workflow CI para Blender.
- **Evidencia:** `tests/smoke/smoke_addon.py`, `tests/perf/benchmark_execute.py`, `.github/workflows/blender-smoke.yml`
- **Impacto:** alta chance de regressao silenciosa.
- **Causa provavel:** projeto orientado a contribuicao manual.
- **Recomendacao (acao):** executar pipeline regularmente e adicionar asserts de regressao funcional por categoria de node.
- **Validacao PASS/FAIL:** pipeline deve quebrar em regressao conhecida.
- **Risco de regressao + mitigacao:** baixo.
- **Owner sugerido:** Responsavel DevOps
- **Status:** Em progresso

### A-009
- **Categoria:** UX / Integracao
- **Severidade:** Media
- **Descricao objetiva:** Add-on registra atalhos globais no Node Editor; mitigado com toggle em preferencias e deteccao basica de conflito.
- **Evidencia:** `__init__.py` (propriedade `enable_shortcuts` e `init_keymaps` com checagem)
- **Impacto:** interferencia com outros fluxos/add-ons no editor de nos.
- **Causa provavel:** keymap fixo sem namespace por contexto mais restrito.
- **Recomendacao (acao):** ampliar deteccao para mapear conflitos em keyconfigs de usuario e reportar no painel.
- **Validacao PASS/FAIL:** ativar com add-ons populares e confirmar ausencia de conflito.
- **Risco de regressao + mitigacao:** medio.
- **Owner sugerido:** Maintainer UX
- **Status:** Em progresso

---

## 16) Backlog executavel (priorizado)

| Prioridade | Tarefa | Objetivo | Passos | Aceite | Esforco | Risco |
|---:|---|---|---|---|---|---|
| P0 | Remover `eval` de caminho critico (Concluido) | Mitigar execucao arbitraria | Substituido por parsing seguro em helper/sockets/nodes | Nenhum `eval` em `*.py` | Alto | Medio |
| P0 | Endurecer updater (Parcial) | Reduzir risco supply-chain | TLS padrao aplicado; falta hash/signature check | Update falha com pacote alterado | Medio | Medio |
| P0 | Guard-rail para `Custom Python Script` (Parcial) | Conter risco de execucao | Flag de opt-in adicionada no node | Execucao desabilitada por padrao | Medio | Baixo |
| P1 | Corrigir inconsistencias funcionais (Concluido) | Aumentar confiabilidade IO/selecao | Ajustado `ScImportFbx` e validacao de `ScSelectByIndexArray` | Regressao compilando sem erro | Baixo | Baixo |
| P1 | Remover `except:` bare (Concluido) | Evitar swallow de sinais criticos | Substituir por `except Exception` no updater/helper | `bare_except` = 0 | Baixo | Baixo |
| P1 | Criar smoke tests Blender headless | Validar E2E minimo | Scripts `blender -b -P` para 3 fluxos | Pipeline CI verde | Medio | Baixo |
| P2 | Refinar excecoes do updater | Melhorar diagnostico | Trocar `except Exception` por tipos especificos + logs | Erros acionaveis com contexto | Medio | Baixo |
| P2 | Benchmark de realtime handler | Controlar custo de CPU | Medir 1/10/50 trees e implementar throttling | CPU/FPS dentro de meta | Medio | Medio |
| P2 | Hardening de keymaps | Reduzir conflitos | Preferences para atalhos + checagem conflito | Sem colisao em cenario de teste | Baixo | Baixo |

---

## 17) Apendice — roteiro rapido de teste (checklist)

### Instalacao/ativacao
- [ ] Instalar via Preferences > Add-ons > Install…
- [ ] Ativar; fechar/reabrir Blender; confirmar persistencia
- [ ] Desativar/reativar; confirmar ausencia de duplicacao (keymaps/handlers)

### Funcionalidade
- [ ] Fluxo principal (E2E-01) PASS
- [ ] Fluxos secundarios PASS
- [ ] Undo/Redo (se aplicavel) PASS
- [ ] Cancelamento PASS

### Robustez
- [ ] Entradas invalidas nao crasham
- [ ] Execucao repetida 100x sem degradar
- [ ] Cena grande nao trava permanentemente

### Performance
- [ ] Medicoes coletadas e registradas

### Seguranca (se aplicavel)
- [ ] Sem execucao insegura / downloads sem validacao

### Documentacao
- [ ] Quickstart executavel do zero

---

## 18) Registro de evidencias

| Evidencia | Tipo | Local (arquivo/URL/caminho) | Observacao |
|---|---|---|---|
| E-001 | Metricas estaticas | `avaliacao/evidencias/metricas_estaticas.json` | Contagem de arquivos, `eval` (0), `exec` (1), `bare_except` (0) |
| E-002 | Ambiente de execucao | `avaliacao/evidencias/ambiente_windows.txt` | OS, CPU, RAM, GPU |
| E-003 | Varredura de riscos | `avaliacao/evidencias/scan_riscos.txt` | Ocorrencias com linhas para auditoria |
| E-004 | Compilacao Python | `avaliacao/evidencias/compilacao_python.txt` | `compileall` sem erro de sintaxe |
| E-005 | Metadados do add-on | `__init__.py:18-27` | `bl_info` (nome, versao, alvo Blender) |
| E-006 | Escopo funcional declarado | `README.md:14-69` | Features, quickstart, categorias de nos |
| E-007 | Ciclo de vida do add-on | `__init__.py:127-183` | Registro classes/keymaps/handlers |
| E-008 | Hardening updater | `addon_updater.py` | Sem `_create_unverified_context`; checksum opcional implementado, assinatura/checksum obrigatorio pendente |
| E-009 | Risco script arbitrario | `nodes/utilities/ScCustomPythonScript.py:57` | `exec` direto em entrada do usuario (com opt-in) |
| E-010 | Inconsistencia funcional | `nodes/inputs/ScImportFbx.py:14` e `nodes/inputs/ScImportFbx.py:30` | Label x parametro de import FBX |
