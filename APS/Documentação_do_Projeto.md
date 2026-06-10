# Documentação do Projeto - Sistema de Gestão Reprodutiva Bovino

## 1. Descrição e Delimitação do Escopo
O sistema consiste em um software de gestão e controle reprodutivo para rebanhos bovinos. Destinado a proprietários rurais e médicos veterinários, o sistema resolve o problema da perda de histórico e da falta de rastreabilidade no ciclo de matrizes. Suas principais funcionalidades contemplam o cadastro de animais (machos e fêmeas), o controle automatizado de estados reprodutivos (Vazia, Inseminada e Prenha) e o registro histórico de eventos no manejo, como inseminações, diagnósticos de gestação (toque), partos e abortos.

## 2. Fase de Análise

### a) Requisitos Funcionais (RF)

| Identificador | Descrição | Prioridade | Depende de |
| :--- | :--- | :--- | :--- |
| **RF01** | O sistema deverá permitir o gerenciamento (inclusão, visualização, atualização e exclusão) de proprietários. | Alta | - |
| **RF02** | O sistema deverá permitir o gerenciamento de médicos veterinários. | Alta | - |
| **RF03** | O sistema deverá permitir o gerenciamento (inclusão, visualização, atualização e exclusão) de animais machos e fêmeas. | Alta | - |
| **RF04** | O sistema deverá permitir ao usuário registrar o evento de inseminação para uma fêmea. | Alta | RF02, RF03 |
| **RF05** | O sistema deverá transitar automaticamente o estado da fêmea para "Inseminada" ao registrar inseminação. | Alta | RF04 |
| **RF06** | O sistema deverá permitir ao usuário com perfil de Médico Veterinário registrar o evento de diagnóstico de gestação (toque). | Alta | RF02, RF03, RF05 |
| **RF07** | O sistema deverá transitar o estado da fêmea para "Prenha" caso o diagnóstico seja positivo. | Alta | RF06 |
| **RF08** | O sistema deverá permitir ao usuário registrar o evento de parto, gerando o histórico na matriz. | Alta | RF02, RF03, RF07 |
| **RF09** | O sistema deverá transitar o estado da fêmea de "Prenha" para "Vazia" após o registro de um parto. | Alta | RF08 |
| **RF10** | O sistema deverá permitir a listagem de todo o histórico de eventos reprodutivos de uma fêmea específica. | Alta | RF03 |
| **RF11** | O sistema deverá transitar o estado da fêmea para "Vazia" caso o diagnóstico seja negativo, registrando a falha da inseminação. | Alta | RF06 |
| **RF12** | O sistema deverá permitir registrar o evento de aborto para uma fêmea prenha, gerando o histórico na matriz. | Alta | RF02, RF03, RF07 |
| **RF13** | O sistema deverá transitar o estado da fêmea de "Prenha" para "Vazia" após o registro de um aborto. | Alta | RF12 |

### b) Regras de Negócio (RN)

| Identificador | Descrição | Prioridade | Depende de |
| :--- | :--- | :--- | :--- |
| **RN01** | Uma fêmea que se encontra no estado "Vazia" ou "Inseminada" não poderá receber o registro de um evento de "Parto" ou "Aborto". | Alta | RF08, RF09, RF12 |
| **RN02** | Todo evento reprodutivo registrado (Inseminação, Diagnóstico, Parto, Aborto) deverá possuir obrigatoriamente um Médico Veterinário ou Proprietário responsável atrelado. | Alta | RF04, RF06, RF08, RF12 |
| **RN03** | Apenas usuários cadastrados e logados como Médicos Veterinários (CRMV válido) terão permissão para acessar e registrar o Diagnóstico de Gestação (Toque). | Alta | RF06 |

### c) Requisitos Não Funcionais (RNF)

| Identificador | Descrição | Categoria | Escopo | Prioridade | Depende de |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **RNF01** | O sistema deverá ser desenvolvido na linguagem Python usando Orientação a Objetos. | Implementação | Sistema | Alta | - |
| **RNF02** | O sistema deverá possuir uma interface gráfica desenvolvida com a biblioteca Tkinter. | Interface | Sistema | Alta | - |
| **RNF03** | O sistema deverá armazenar os dados em um banco de dados relacional PostgreSQL. | Restrições de Software | Sistema | Alta | - |
| **RNF04** | O sistema deverá implementar obrigatoriamente os padrões de projeto DAO e State. | Implementação | Sistema | Alta | - |
| **RNF05** | O sistema deverá validar o CPF de proprietários e veterinários. | Restrições de Integridade | Funcionalidade | Alta | RF01, RF02 |

## Diagrama de Casos de Uso

Abaixo apresentamos o Diagrama de Casos de Uso do sistema. Este modelo visual delimita a fronteira da aplicação e mapeia as interações entre os usuários externos e as funcionalidades internas. 

O diagrama reflete nossas regras de negócio e controle de acesso, evidenciando a separação de papéis entre o **Proprietário** (focado na gestão e registros cotidianos) e o **Veterinário** (com exclusividade técnica sobre laudos clínicos). Além disso, destaca a reutilização de rotinas através de relacionamentos de `<<include>>` para a validação de responsáveis, e fluxos condicionais de `<<extend>>` para transições de estados reprodutivos.

![Diagrama de Casos de Uso do Sistema da Fazenda](diagramas/diagrama_casos_de_uso.png)

## 3. Especificação dos Casos de Uso

### UC01 - Gerenciar Pessoas
**Atores:** Proprietário
**Pré-condições:** Nenhuma
**Fluxo Principal:**
1. O usuário acessa o módulo de gestão de pessoas.
2. Insere ou altera os dados (CPF, Nome, Telefone, e CRMV no caso de veterinários).
3. O sistema valida os dados e salva as informações no banco de dados.

**Pós-condições:** Perfil registrado e habilitado para ser selecionado como responsável no sistema.

---

### UC02 - Gerenciar Animais
**Atores:** Proprietário
**Pré-condições:** Nenhuma
**Fluxo Principal:**
1. O usuário informa os dados da matriz bovina (Brinco, Raça).
2. O sistema define o estado reprodutivo inicial da fêmea como "Vazia".
3. O sistema persiste o animal no banco de dados.

**Fluxos Alternativos:** * **Brinco Duplicado:** O sistema bloqueia o cadastro se o número de identificação já existir no banco.

**Pós-condições:** Matriz bovina disponível para receber registros de manejo.

---

### UC03 - Registrar Inseminação
**Atores:** Proprietário, Veterinário
**Pré-condições:** A fêmea selecionada deve estar no estado "Vazia".
**Fluxo Principal:**
1. O usuário seleciona a fêmea, a data do procedimento e a pessoa responsável.
2. O sistema aciona o `<<include>>` **validar_responsavel**.
3. O sistema altera o estado da fêmea para "Inseminada".
4. O sistema gera uma nova linha na tabela de histórico de manejo.

**Fluxos Alternativos:** * **Estado Incorreto:** O sistema bloqueia a ação caso a matriz não esteja "Vazia".

**Pós-condições:** Estado atualizado para "Inseminada" e evento salvo no histórico.

---

### UC04 - Registrar Aborto
**Atores:** Proprietário, Veterinário
**Pré-condições:** A fêmea selecionada deve estar obrigatoriamente no estado "Prenha".
**Fluxo Principal:**
1. O usuário seleciona a fêmea, o responsável e a opção de registrar aborto, informando a data.
2. O sistema aciona o `<<include>>` **validar_responsavel**.
3. O sistema altera automaticamente o estado da matriz de "Prenha" para "Vazia".
4. O sistema salva o evento negativo no histórico de manejo.

**Fluxos Alternativos:** * **Estado Incorreto:** O sistema impede o registro se a fêmea não estiver "Prenha".

**Pós-condições:** Gestação interrompida no sistema, estado retorna para "Vazia" e histórico é gravado.

---

### UC05 - Registrar Parto
**Atores:** Proprietário, Veterinário
**Pré-condições:** A fêmea selecionada deve estar no estado "Prenha".
**Fluxo Principal:**
1. O usuário informa a data do nascimento do bezerro e o responsável pelo parto.
2. O sistema aciona o `<<include>>` **validar_responsavel**.
3. O sistema altera o estado da fêmea de "Prenha" para "Vazia".
4. O sistema salva o evento no histórico de manejo.

**Fluxos Alternativos:** * **Estado Incorreto:** O sistema bloqueia caso não haja gestação confirmada.

**Pós-condições:** Ciclo concluído com sucesso, matriz pronta para nova estação de monta.

---

### UC06 - Registrar Diagnóstico (Toque)
**Atores:** Veterinário
**Pré-condições:** A fêmea deve estar no estado "Inseminada".
**Fluxo Principal:**
1. O usuário seleciona a fêmea, informa a data do exame clínico e seleciona o Veterinário responsável.
2. O sistema aciona o `<<include>>` **validar_responsavel** para confirmação das credenciais técnicas (CRMV).
3. O usuário informa o resultado do diagnóstico.
4. O sistema registra o laudo técnico com assinatura do profissional no histórico.

**Fluxos Alternativos:**
* **Acesso Negado:** O sistema bloqueia a ação se a pessoa selecionada como responsável não tiver perfil de Veterinário.
* **Toque Positivo:** O sistema aciona o `<<extend>>` **mudar_para_prenha**.
* **Toque Negativo:** O sistema aciona o `<<extend>>` **mudar_para_vazia**.

**Pós-condições:** Laudo técnico salvo e estado da matriz atualizado conforme o resultado do exame.

---

### UC07 - Validar Responsável (`<<include>>`)
**Atores:** Sistema (acionado internamente)
**Pré-condições:** O usuário deve ter disparado um evento de manejo (Inseminação, Parto, Aborto ou Diagnóstico).
**Fluxo Principal:**
1. O sistema recebe a requisição de evento.
2. Verifica qual pessoa foi selecionada na interface como autora da ação.
3. Confere se o perfil dessa pessoa possui as permissões necessárias (ex: exigência de CRMV para laudos).
4. Carimba o CPF do responsável no registro a ser salvo no banco.

**Pós-condições:** Evento autorizado e atrelado ao responsável correto para o histórico de manejo.

---

### UC08 - Mudar para Prenha (`<<extend>>`)
**Atores:** Sistema (acionado internamente)
**Pré-condições:** Foi registrado um laudo "Positivo" no UC06.
**Fluxo Principal:**
1. O sistema intercepta o resultado positivo do toque.
2. Aplica a regra de negócio do Padrão State, instanciando o estado "Prenha" para a fêmea.
3. Atualiza a coluna de estado no banco de dados.

**Pós-condições:** Matriz assume o estado gestacional com sucesso.

---

### UC09 - Mudar para Vazia (`<<extend>>`)
**Atores:** Sistema (acionado internamente)
**Pré-condições:** Foi registrado um laudo "Negativo" no UC06.
**Fluxo Principal:**
1. O sistema intercepta o resultado negativo do toque (falha na inseminação).
2. Aplica a regra de negócio do Padrão State, instanciando o estado "Vazia" para a fêmea.
3. Atualiza a coluna de estado no banco de dados.

**Pós-condições:** Matriz retorna ao estado inicial, pronta para nova tentativa na estação de monta.