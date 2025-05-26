# ⚽ Gerenciador de Jogadores de Futebol em Console ⚽

Um aplicativo CLI para adicionar, listar, atualizar e remover jogadores de futebol, usando um arquivo JSON como base de dados.

## 🚀 Demonstração

_(Insira aqui um GIF ou vídeo curto demonstrando os comandos)_

Exemplo:

```bash
python main.py add-player --name "Neymar Jr." --team "Al-Hilal" --position "Atacante" --goals 430
python main.py list-players
python main.py list-players --team "Al-Hilal"
python main.py update-player 1 --goals 435 --team "Paris Saint-Germain"
python main.py remove-player 2
```

## 🔧 Instalação e Execução

1.  **Clone o repositório:**

    ```bash
    git clone <URL_DO_SEU_REPOSITORIO>
    cd <NOME_DO_DIRETORIO_DO_PROJETO>
    ```

2.  **Crie e ative um ambiente virtual (recomendado):**

    ```bash
    python -m venv venv
    # No Windows
    # .\venv\Scripts\activate
    # No macOS/Linux
    source venv/bin/activate
    ```

3.  **Instale as dependências:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Execute a aplicação:**
    Os comandos são executados através de `main.py`.
    ```bash
    python main.py --help
    ```
    Exemplos de uso:
    - Adicionar um jogador: `python main.py add-player` (siga os prompts)
    - Listar todos os jogadores: `python main.py list-players`
    - Listar jogadores de um time específico: `python main.py list-players --team "Nome do Time"`
    - Listar jogadores de uma posição específica: `python main.py list-players --position "Atacante"`
    - Atualizar dados de um jogador: `python main.py update-player <ID_DO_JOGADOR> --name "Novo Nome" --goals <NUMERO_DE_GOLS>`
    - Remover um jogador: `python main.py remove-player <ID_DO_JOGADOR>`

## ⚙️ Decisões Técnicas e Foco na UX

- **Linguagem:** Python, pela sua simplicidade e vasta quantidade de bibliotecas.
- **CLI Framework:** `Click` foi escolhido por facilitar a criação de CLIs robustas e amigáveis, incluindo geração automática de mensagens de ajuda, validação de parâmetros e opções interativas (prompts).
- **Persistência de Dados:** Utilização de um arquivo JSON (`players.json`) para armazenar os dados dos jogadores, com funções dedicadas para carga e salvamento.
- **Estrutura do Projeto:**
  - `main.py`: Ponto de entrada da aplicação, lida com a interface do usuário (comandos `click`) para o gerenciador de jogadores.
  - `task_operations.py`: Módulo contendo toda a lógica de negócio para manipulação dos jogadores (CRUD, gerenciamento de IDs). O nome do arquivo foi mantido por simplicidade, mas conceitualmente agora é `player_operations`.
  - `players.json`: Arquivo de banco de dados para os jogadores.
  - `tests/`: Diretório com testes unitários para as operações com jogadores.
  - `requirements.txt`: Lista as dependências do projeto (`click`, `pytest`).
- **UX (Experiência do Usuário):**
  - **Comandos Temáticos:** Os nomes dos comandos (`add-player`, `list-players`, `update-player`, `remove-player`) são diretos e alinhados com o tema de futebol.
  - **Feedback Claro:** Mensagens de sucesso e erro são exibidas para cada operação, utilizando cores para fácil distinção.
  - **Prompts Interativos:** Para adicionar jogadores, o sistema solicita nome, time, posição e número de gols.
  - **Ajuda Integrada:** Cada comando possui uma descrição e os parâmetros são explicados através de `python main.py [COMANDO] --help`.
  - **Listagem Flexível:** O comando `list-players` permite filtrar jogadores por time ou posição, e exibe os dados de forma organizada e colorida.
- **Gerenciamento de IDs:** IDs são gerados sequencialmente, garantindo unicidade mesmo após remoções.
- **Testes:** Testes unitários foram implementados para as principais funcionalidades CRUD em `task_operations.py` (agora `player_operations`) usando `pytest`.

## Formato `players.json`

O arquivo `players.json` armazena uma lista de jogadores, onde cada jogador é um objeto com os seguintes campos:

- `id` (int): Identificador único do jogador.
- `name` (str): Nome do jogador.
- `team` (str): Time atual do jogador.
- `position` (str): Posição principal do jogador.
- `goals` (int): Número total de gols na carreira (exemplo de dado numérico).

Este formato pode ser evoluído para incluir mais detalhes, como `nacionalidade`, `dataNascimento`, `historicoTimes`, etc.

## 🧪 Executando os Testes

Para rodar os testes unitários (requer `pytest` instalado):

```bash
pytest
```

No diretório raiz do projeto. Os testes agora são executados a partir de `tests/test_player_operations.py`.

## 💼 Plano de Negócios

_(Responda às seguintes perguntas aqui, adaptando para um app de gerenciamento de jogadores, se aplicável, ou mantenha o foco no desafio original de gerenciador de tarefas)_

1.  **Se você fosse lançar esse gerenciador no mercado, qual seria o modelo de negócios?**
2.  **Como atrairia seus primeiros usuários? (estratégia de aquisição, canais, etc.)**
3.  **Estimativa de CAC (Custo de Aquisição de Cliente).**
4.  **Proposta de LTV (Lifetime Value) e como maximizá‑lo.**
5.  **Estratégias de monetização possíveis (ex.: freemium, licenças, plugins).**
6.  **Estratégias de retenção (ex.: gamificação, integrações, notificações).**

---

\_Desafio de Estágio - Adaptado para tema de Futebol.
