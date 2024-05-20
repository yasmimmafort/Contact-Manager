# Contact-Manager
## Descrição
O **Contact Manager** é um aplicativo em Python que permite gerenciar contatos de forma eficiente. Ele oferece funcionalidades para adicionar, editar, excluir e visualizar informações de contato, como nome, telefone, e-mail e endereço. Além disso, suporta a importação de contatos a partir de um arquivo CSV.

## Estrutura do Código
### `create_connection()`

A função `create_connection` é responsável por estabelecer uma conexão com o banco de dados SQLite chamado contacts.db. Esta conexão é fundamental para a execução de todas as operações subsequentes no banco de dados, como criar tabelas, adicionar, visualizar, atualizar e excluir contatos.

```python
def create_connection():
    conn = None
    try:
        conn = sqlite3.connect('contacts.db')
    except sqlite3.Error as e:
        print(e)
    return conn
```
### Explicação

- `conn = None`: Inicializa a variável `conn` como `None`. Esta variável irá armazenar a conexão com o banco de dados se a conexão for bem-sucedida.
  
- `try: conn = sqlite3.connect('contacts.db')`: Tenta estabelecer uma conexão com o banco de dados `contacts.db` usando a função `sqlite3.connect()`. Se a conexão for bem-sucedida, a variável conn será atribuída à conexão com o banco de dados.
  
- `except sqlite3.Error as e: print(e)`: Se ocorrer um erro ao tentar estabelecer a conexão, ele será capturado pelo bloco `except`, e a mensagem de erro será impressa. Isso ajuda a identificar problemas com a conexão ao banco de dados.
  
- `return conn`: Retorna a conexão (ou `None` se a conexão não foi estabelecida). A função sempre retorna um objeto de conexão, que é usado para interagir com o banco de dados em outras partes do programa.

Esta função é fundamental para a operação do Contact Manager, pois todas as interações com o banco de dados dependem de uma conexão ativa. Se a conexão não puder ser estabelecida, as operações no banco de dados falharão.


### `create_table(conn)`

A função `create_table` é responsável por criar a tabela `contacts` no banco de dados SQLite. Esta tabela armazena as informações dos contatos, como nome, e-mail, telefone e endereço. A função garante que a tabela seja criada apenas se ainda não existir.

```python
def create_table(conn):
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS contacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        phone TEXT NOT NULL,
        address TEXT NOT NULL
    );
    """
    try:
        c = conn.cursor()
        c.execute("DROP TABLE IF EXISTS contacts")
        c.execute(create_table_sql)
    except sqlite3.Error as e:
        print(e)
```
### Explicação

- `create_table_sql`: Define o comando SQL que cria a tabela `contacts` com as seguintes colunas:
   
  - `id`: Um inteiro que serve como chave primária e é auto-incrementado.
  - `name`: Um texto que não pode ser nulo, representando o nome do contato.
  - `email`: Um texto que não pode ser nulo, representando o e-mail do contato.
  - `phone`: Um texto que não pode ser nulo, representando o telefone do contato.
  - `address`: Um texto que não pode ser nulo, representando o endereço do contato.

- `try: c = conn.cursor()`: Cria um cursor a partir da conexão fornecida (`conn`). O cursor é utilizado para executar comandos SQL no banco de dados.
  
- `c.execute("DROP TABLE IF EXISTS contacts")`: Remove a tabela `contacts` se ela já existir. Isso garante que uma nova tabela seja criada toda vez que a função for chamada, evitando conflitos com dados antigos ou estrutura de tabela diferente.

- `c.execute(create_table_sql)`: Executa o comando SQL definido anteriormente para criar a tabela `contacts`.

- `except sqlite3.Error as e: print(e)`: Captura qualquer erro que ocorra durante a execução dos comandos SQL e imprime a mensagem de erro. Isso ajuda a identificar problemas na criação da tabela.

Esta função é fundamental para a configuração inicial do banco de dados do Contact Manager, garantindo que a estrutura da tabela esteja correta e pronta para armazenar os dados dos contatos.

### `add_contatact(conn, contact)`

A função `add_contact` é responsável por adicionar um novo contato à tabela `contacts` no banco de dados SQLite. Ela insere os dados fornecidos (nome, e-mail, telefone e endereço) na tabela e retorna o ID do contato recém-adicionado.

```python
def add_contact(conn, contact):
    sql = '''INSERT INTO contacts(name, email, phone, address)
             VALUES(?, ?, ?, ?)'''
    cur = conn.cursor()
    cur.execute(sql, contact)
    conn.commit()
    return cur.lastrowid
```

### Explicação

- `sql`: Define o comando SQL para inserir um novo registro na tabela `contacts`. O comando utiliza placeholders (?) para valores que serão substituídos pelos dados do contato.

- `cur = conn.cursor()`: Cria um cursor a partir da conexão fornecida (`conn`). O cursor é utilizado para executar comandos SQL no banco de dados.

- `cur.execute(sql, contact)`: Executa o comando SQL de inserção, passando os dados do contato como parâmetros. O parâmetro `contact´ deve ser uma tupla contendo os valores (nome, e-mail, telefone e endereço) a serem inseridos.

- `conn.commit()`: Salva (ou "commita") as mudanças feitas no banco de dados. Este passo é necessário para garantir que o novo contato seja realmente adicionado à tabela.

- `return cur.lastrowid`: Retorna o ID do contato recém-adicionado. Este ID é gerado automaticamente pelo banco de dados e pode ser útil para referência futura.

### Exemplo de Uso

Aqui está um exemplo de como usar a função `add_contact`:

```python
# Supondo que `conn` é uma conexão ativa com o banco de dados
contact = ("John Doe", "john.doe@example.com", "+123456789", "123 Main St")
contact_id = add_contact(conn, contact)
print(f"Contato adicionado com ID: {contact_id}")
```

Esta função é fundamental para adicionar novos contatos ao banco de dados do Contact Manager, permitindo que o usuário armazene informações detalhadas sobre cada contato.

### `view_contacts(conn)`

A função `view_contacts` é responsável por recuperar e exibir todos os contatos armazenados na tabela `contacts` no banco de dados SQLite. Ela seleciona todos os registros da tabela e imprime cada um deles.

```python
def view_contacts(conn):
    sql = 'SELECT * FROM contacts'
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    for row in rows:
        print(row)

```

### Explicação

- `sql`: Define o comando SQL para selecionar todos os registros da tabela `contacts`. O comando `'SELECT * FROM contacts'` recupera todas as colunas de todos os registros.

- `cur = conn.cursor()`: Cria um cursor a partir da conexão fornecida (`conn`). O cursor é utilizado para executar comandos SQL no banco de dados.

- `cur.execute(sql)`: Executa o comando SQL de seleção, recuperando todos os registros da tabela `contacts`.

- `rows = cur.fetchall()`: Recupera todos os registros resultantes da execução do comando SQL e armazena-os na variável `rows`. Cada registro é representado como uma tupla.

- `for row in rows: print(row)`: Itera sobre cada registro em `rows` e imprime-o. Cada registro contém os campos `id`, `name`, `email`, `phone` e `address`.

### Exemplo de uso

```python
# Supondo que `conn` é uma conexão ativa com o banco de dados
view_contacts(conn)
```
A saída pode ser algo como:

```shell
(1, 'John Doe', 'john.doe@example.com', '+123456789', '123 Main St')
(2, 'Jane Smith', 'jane.smith@example.com', '+987654321', '456 Elm St')
```
Esta função é fundamental para visualizar todos os contatos armazenados no banco de dados do Contact Manager, permitindo que o usuário veja facilmente todas as informações dos contatos.

### `update_contact(conn, contact_id, fields)`

A função `update_contact` é responsável por atualizar as informações de um contato existente na tabela `contacts` no banco de dados SQLite. Ela permite que campos específicos de um contato sejam modificados com novos valores fornecidos.

```python
def update_contact(conn, contact_id, fields):
    set_clause = ', '.join(f"{field} = ?" for field in fields.keys())
    sql = f"UPDATE contacts SET {set_clause} WHERE id = ?"
    cur = conn.cursor()
    cur.execute(sql, list(fields.values()) + [contact_id])
    conn.commit()
```
### Explicação

- `set_clause = ', '.join(f"{field} = ?" for field in fields.keys())`: Cria uma cláusula `SET` dinâmica para o comando SQL de atualização. Esta linha gera uma string que define quais campos serão atualizados e define placeholders (``?) para os novos valores. Por exemplo, se `fields` contiver `{'name': 'Jane Doe', 'email': 'jane.doe@example.com'}`, o `set_clause` será `"name = ?, email = ?"`.

- `sql = f"UPDATE contacts SET {set_clause} WHERE id = ?"`: Cria o comando SQL de atualização usando a cláusula `SET` gerada e adiciona uma cláusula `WHERE` para especificar qual contato deve ser atualizado pelo seu `id`.

- `cur = conn.cursor()`: Cria um cursor a partir da conexão fornecida (`con`n). O cursor é utilizado para executar comandos SQL no banco de dados.

- `cur.execute(sql, list(fields.values()) + [contact_id])`: Executa o comando SQL de atualização, passando os novos valores dos campos e o `id` do contato a ser atualizado como parâmetros.

- ´conn.commit()`: Salva (ou "commita") as mudanças feitas no banco de dados. Este passo é necessário para garantir que as atualizações sejam realmente aplicadas.

### Exemplo de Uso

```python
# Supondo que `conn` é uma conexão ativa com o banco de dados
contact_id = 1
fields = {
    'name': 'Jane Doe',
    'email': 'jane.doe@example.com',
    'phone': '+987654321',
    'address': '456 Elm St'
}
update_contact(conn, contact_id, fields)
print(f"Contato com ID {contact_id} foi atualizado.")
```
Este exemplo atualiza o contato com `id` 1, modificando seu nome, e-mail, telefone e endereço com os novos valores fornecidos.

A função `update_contact` é essencial para permitir a edição de informações de contatos já existentes no banco de dados do Contact Manager, proporcionando flexibilidade na manutenção dos dados.








