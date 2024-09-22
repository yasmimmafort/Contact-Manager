# Contact-Manager
## Descrição
O **Contact Manager** é um aplicativo em Python que permite gerenciar contatos de forma eficiente. Ele oferece funcionalidades para adicionar, editar, excluir e visualizar informações de contato, como nome, telefone, e-mail e endereço. Além disso, suporta a importação de contatos a partir de um arquivo CSV.

# Instalação

## Requisitos

- Python (versão 3.7 ou superior)
- pip

# Passos para Instalação

1. Clone o repositório para sua máquina local:
```sh
git clone https://github.com/yasmimmafort/contact-manager.git
```
2. Navegue até o diretório do projeto:
```sh
cd contact-manager
```
3. Crie um ambiente virtual (opcional, mas recomendado):
```sh
python -m venv venv
source venv/bin/activate   # No Windows, use `venv\Scripts\activate`
```
# Uso

## Executando o projeto

Para iniciar o Contact Manager, execute o seguinte comando:

```sh
python main.py
```
## Exemplo de Uso

```python
import sqlite3
from contact_manager import create_connection, add_contact, view_contacts

conn = create_connection()

# Adicionando um novo contato
contact = ("John Doe", "john.doe@example.com", "+123456789", "123 Main St")
add_contact(conn, contact)

# Visualizando todos os contatos
view_contacts(conn)

conn.close()
```
## Importando Contatos de um Arquivo CSV

Para importar contatos de um arquivo CSV, certifique-se de que o arquivo siga o formato abaixo:

```csv
Name,Email,Phone,Address
John Doe,john.doe@example.com,+123456789,123 Main St
```
Depois, execute o seguinte comando dentro do script principal:

```python
import_from_csv('contacts.csv')
```

## Menu Interativo

O Contact Manager também oferece um menu interativo para gerenciar os contatos. Para utilizá-lo, basta executar o script `main.py` e seguir as instruções no terminal.

## Estrutura do Código
## `create_connection()`

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
## Explicação

- `conn = None`: Inicializa a variável `conn` como `None`. Esta variável irá armazenar a conexão com o banco de dados se a conexão for bem-sucedida.
  
- `try: conn = sqlite3.connect('contacts.db')`: Tenta estabelecer uma conexão com o banco de dados `contacts.db` usando a função `sqlite3.connect()`. Se a conexão for bem-sucedida, a variável conn será atribuída à conexão com o banco de dados.
  
- `except sqlite3.Error as e: print(e)`: Se ocorrer um erro ao tentar estabelecer a conexão, ele será capturado pelo bloco `except`, e a mensagem de erro será impressa. Isso ajuda a identificar problemas com a conexão ao banco de dados.
  
- `return conn`: Retorna a conexão (ou `None` se a conexão não foi estabelecida). A função sempre retorna um objeto de conexão, que é usado para interagir com o banco de dados em outras partes do programa.

Esta função é fundamental para a operação do Contact Manager, pois todas as interações com o banco de dados dependem de uma conexão ativa. Se a conexão não puder ser estabelecida, as operações no banco de dados falharão.


## `create_table(conn)`

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

## `add_contatact(conn, contact)`

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

## `view_contacts(conn)`

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

## `update_contact(conn, contact_id, fields)`

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

- `cur = conn.cursor()`: Cria um cursor a partir da conexão fornecida (`conn`). O cursor é utilizado para executar comandos SQL no banco de dados.

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

## `delete_contact(conn, id)`

A função delete_contact é responsável por excluir um contato específico da tabela contacts no banco de dados SQLite. Ela remove o registro correspondente ao id fornecido.


```python
def delete_contact(conn, id):
    sql = 'DELETE FROM contacts WHERE id=?'
    cur = conn.cursor()
    cur.execute(sql, (id,))
    conn.commit()
```
### Explicação

- `sql = 'DELETE FROM contacts WHERE id=?'`: Define o comando SQL para excluir um registro da tabela `contacts` com base no `id` fornecido. O `?` é um placeholder para o valor do `id` que será substituído durante a execução do comando.

- `cur = conn.cursor()`: Cria um cursor a partir da conexão fornecida (`conn`). O cursor é utilizado para executar comandos SQL no banco de dados.

- `cur.execute(sql, (id,))`: Executa o comando SQL de exclusão, passando o valor do `id` como parâmetro. É importante notar que o valor do `id` é passado como uma tupla (`id`,), conforme necessário pela função execute.

- `conn.commit()`: Salva (ou "commita") as mudanças feitas no banco de dados. Este passo é necessário para garantir que a exclusão do registro seja efetivada.

### Exemplo de Uso

```python
contact_id = 1
delete_contact(conn, contact_id)
print(f"Contato com ID {contact_id} foi excluído.")
```
Este exemplo exclui o contato com o `id` 1 da tabela `contacts`. Após a execução da função `delete_contact`, o contato correspondente será removido do banco de dados.

A função `delete_contact` é crucial para permitir a remoção de contatos indesejados ou obsoletos do banco de dados do Contact Manager, ajudando a manter a integridade e a organização dos dados.

## `is_valid_email(email)`

A função `is_valid_email` verifica se um determinado e-mail possui um formato válido, seguindo um padrão específico. Ela utiliza expressões regulares para validar o formato do e-mail.

```python
def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email)
```
### Explicação 

- `pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'`: Define um padrão de expressão regular que corresponde a um endereço de e-mail válido. Este padrão verifica se o e-mail contém uma parte local seguida por `@`, seguida por um domínio, e se o domínio possui uma extensão válida.

- `re.match(pattern, email)`: Utiliza a função match do módulo re para verificar se o e-mail fornecido corresponde ao padrão definido. Se corresponder, a função retorna um objeto correspondente, indicando que o e-mail é válido. Caso contrário, retorna None, indicando que o e-mail não é válido.

### Exemplo de Uso

```python
email = "example@example.com"
if is_valid_email(email):
    print("O e-mail é válido.")
else:
    print("O e-mail é inválido.")
```
Este exemplo verifica se o e-mail `"example@example.com"` é válido usando a função `is_valid_email` e imprime uma mensagem correspondente.

A função `is_valid_email` é útil para validar endereços de e-mail fornecidos pelo usuário antes de serem inseridos no banco de dados do Contact Manager, ajudando a garantir a integridade e a validade dos dados.

## `is_valid_phone(phone)`

A função `is_valid_phone` verifica se um determinado número de telefone possui um formato válido, seguindo um padrão específico. Ela utiliza expressões regulares para validar o formato do número de telefone.

```python
def is_valid_phone(phone):
    pattern = r'^[\d\+\-\(\) ]+$'
    return re.match(pattern, phone)
```

### Explicação

- `pattern = r'^[\d\+\-\(\) ]+$'`: Define um padrão de expressão regular que corresponde a um número de telefone válido. Este padrão verifica se o número de telefone contém apenas dígitos (`\d`), sinais de adição (`+`), traços (`-`), parênteses (`(` e `)`) e espaços (` `).

- `re.match(pattern, phone)`: Utiliza a função `match` do módulo `re` para verificar se o número de telefone fornecido corresponde ao padrão definido. Se corresponder, a função retorna um objeto correspondente, indicando que o número de telefone é válido. Caso contrário, retorna `None`, indicando que o número de telefone não é válido.

### Exemplo de Uso 

```python
phone = "+1234567890"
if is_valid_phone(phone):
    print("O número de telefone é válido.")
else:
    print("O número de telefone é inválido.")
```

Este exemplo verifica se o número de telefone `"+1234567890"` é válido usando a função `is_valid_phone` e imprime uma mensagem correspondente.

A função `is_valid_phone` é útil para validar números de telefone fornecidos pelo usuário antes de serem inseridos no banco de dados do Contact Manager, ajudando a garantir a integridade e a validade dos dados.

## `import_from_csv(filename)`

A função `import_from_csv` permite importar dados de um arquivo CSV para o banco de dados SQLite do Contact Manager. Ela lê o arquivo CSV fornecido, valida os dados de cada linha e os insere na tabela contacts do banco de dados.

```python
def import_from_csv(filename):
    conn = create_connection()
    create_table(conn)
    try:
        with open(filename, mode='r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                name = row['Name']
                if ' ' not in name:
                    print(f"Nome inválido (sem sobrenome): {name}, pulando...")
                    continue
                email = row['Email']
                phone = row['Phone']
                address = row['Address']
                if not (name and email and phone and address):
                    print(f"Dados incompletos para {name}, pulando...")
                    continue
                if not is_valid_email(email):
                    print(f"Email inválido: {email}, pulando...")
                    continue
                if not is_valid_phone(phone):
                    print(f"Telefone inválido: {phone}, pulando...")
                    continue
                contact = (name, email, phone, address)
                add_contact(conn, contact)
    except FileNotFoundError:
        print(f"O arquivo {filename} não foi encontrado.")
    conn.close()
```
### Exlplicação

- 'conn = create_connection()': Cria uma conexão com o banco de dados SQLite utilizando a função 'create_connection'. Esta conexão será usada para inserir os dados do arquivo CSV no banco de dados.

- `create_table(conn)`: Garante que a tabela `contacts` esteja criada no banco de dados. Se a tabela já existir, essa função não terá efeito. Se não existir, ela será criada.

- `with open(filename, mode='r') as file:`: Abre o arquivo CSV fornecido em modo de leitura (`'r'`) utilizando um contexto de arquivo. Isso garante que o arquivo seja fechado automaticamente após o término do bloco de código, mesmo em caso de erro.

- `csv_reader = csv.DictReader(file)`: Cria um leitor de CSV que trata cada linha como um dicionário, onde as chaves são os cabeçalhos das colunas e os valores são os dados correspondentes.

- O loop `for row in csv_reader:` itera sobre cada linha do arquivo CSV.

- `name = row['Name']`, `email = row['Email']`, `phone = row['Phone']`, `address = row['Address']`: Extrai os valores de cada coluna do dicionário para as variáveis correspondentes.

- As verificações `if ' ' not in name`, `if not (name and email and phone and address)`, `if not is_valid_email(email)`, `if not is_valid_phone(phone)`: Validam os dados de cada linha do CSV. Se os dados não atenderem aos critérios especificados, a linha será pulada e uma mensagem de aviso será exibida.

- `contact = (name, email, phone, address)`: Cria uma tupla contendo os dados do contato para serem adicionados ao banco de dados.

- `add_contact(conn, contact)`: Chama a função `add_contact` para adicionar o contato ao banco de dados.

- `except FileNotFoundError:`: Captura a exceção caso o arquivo CSV não seja encontrado e exibe uma mensagem de aviso.

- `conn.close()`: Fecha a conexão com o banco de dados após a conclusão da importação.

  ### Exemplo de Uso

```python
import_from_csv('contatos.csv')
```

Este exemplo importa dados do arquivo CSV `'contatos.csv'` para o banco de dados do Contact Manager.

A função `import_from_csv` é fundamental para permitir a importação de grandes conjuntos de dados de contatos armazenados em arquivos CSV para o banco de dados do aplicativo, simplificando o processo de gerenciamento de contatos.

## `contact_exist(conn, contact,_id)`

A função `contact_exists` verifica se um determinado contato com o ID fornecido existe na tabela `contacts` do banco de dados SQLite do Contact Manager. Ela retorna `True` se o contato existir e `False` caso contrário.

```python
def contact_exists(conn, contact_id):
    sql = 'SELECT 1 FROM contacts WHERE id = ?'
    cur = conn.cursor()
    cur.execute(sql, (contact_id,))
    return cur.fetchone() is not None
```
### Explicação

- `sql = 'SELECT 1 FROM contacts WHERE id = ?'`: Define um comando SQL de consulta que seleciona apenas um valor (`1`) da tabela `contacts` onde o `id` corresponde ao `contact_id` fornecido.

- `cur = conn.cursor()`: Cria um cursor a partir da conexão fornecida (`conn`). O cursor é utilizado para executar comandos SQL no banco de dados.

- `cur.execute(sql, (contact_id,))`: Executa o comando SQL de consulta, passando o `contact_id` como parâmetro. O `contact_id` é fornecido como uma tupla `(contact_id,)`, conforme necessário pela função `execute`.

- `cur.fetchone() is not None`: Recupera o primeiro resultado da consulta utilizando o método `fetchone()` do cursor. Se houver algum resultado, o contato existe na tabela `contacts` e a função retorna `True`. Caso contrário, a função retorna `False`.

### Exemplo de Uso

```python
contact_id = 1
if contact_exists(conn, contact_id):
    print(f"O contato com ID {contact_id} existe.")
else:
    print(f"O contato com ID {contact_id} não existe.")
```
Este exemplo verifica se o contato com o ID `1` existe na tabela `contacts` usando a função `contact_exists` e imprime uma mensagem correspondente. A função `contact_exists` é útil para verificar a existência de um contato antes de realizar operações de atualização ou exclusão, garantindo que apenas contatos válidos sejam afetados.

## `get_validated_input(prompt, validation_func=None)`

A função `get_validated_input` solicita uma entrada do usuário, exibe um prompt (`prompt`) e valida essa entrada de acordo com uma função de validação especificada (`validation_func`). Se a entrada do usuário passar na validação, ela é retornada. Caso contrário, uma mensagem de erro é exibida e o usuário é solicitado a fornecer uma entrada válida.

```python
def get_validated_input(prompt, validation_func=None):
    while True:
        user_input = input(prompt)
        if validation_func:
            if validation_func(user_input):
                return user_input
            else:
                print("Entrada inválida. Tente novamente.")
        else:
            return user_input
```

### Explicação

- `prompt`: É uma string que contém uma mensagem ou instrução para solicitar a entrada do usuário.

- `validation_func=None`: É uma função opcional de validação que verifica se a entrada do usuário é válida. Se fornecida, esta função é chamada com a entrada do usuário como argumento.

- `while True:`: Inicia um loop infinito para solicitar entrada do usuário até que uma entrada válida seja fornecida.

- `user_input = input(prompt)`: Exibe o prompt para o usuário e espera que ele forneça uma entrada, que é armazenada na variável `user_input`.

- `if validation_func:`: Verifica se uma função de validação foi fornecida.
    
    - `if validation_func(user_input):`: Chama a função de validação (`validation_func`) com a entrada do usuário como argumento. Se a função de validação retornar `True`, indica que a entrada do usuário é válida e ela é retornada pela função `get_validated_input`.
 
    - `else:`: Se a entrada do usuário não for válida de acordo com a função de validação, uma mensagem de erro é exibida e o loop continua, solicitando novamente uma entrada válida.

- `else:`: Se nenhuma função de validação foi fornecida, a entrada do usuário é retornada imediatamente pela função `get_validated_input`.

### Exemplo de Uso

```python
name = get_validated_input("Nome: ", lambda x: len(x) > 0)
```
Neste exemplo, a função `get_validated_input` é usada para solicitar o nome do usuário. A função de validação fornecida (`lambda x: len(x) > 0`) verifica se o comprimento da entrada do usuário é maior que zero, garantindo que o usuário forneça um nome válido.

A função `get_validated_input` é útil para solicitar entradas do usuário em várias partes do aplicativo, garantindo que essas entradas atendam aos critérios de validação especificados.

## `main()`

A função `main()` é a função principal do aplicativo Contact Manager. Ela controla o fluxo de execução do programa, exibindo um menu de opções para o usuário e coordenando as ações correspondentes a cada opção escolhida.

```python
def main():
    database = 'contacts.db'
    conn = create_connection()

    while True:
        print("\nMenu:")
        print("1. Adicionar Contato")
        print("2. Visualizar Contatos")
        print("3. Atualizar Contato")
        print("4. Deletar Contato")
        print("5. Sair")
        choice = get_validated_input("Escolha uma opção: ", lambda x: x in {'1', '2', '3', '4', '5'})

        if choice == '1':
            # Adicionar um novo contato
        elif choice == '2':
            # Visualizar contatos existentes
        elif choice == '3':
            # Atualizar um contato existente
        elif choice == '4':
            # Deletar um contato existente
        elif choice == '5':
            # Sair do programa
            conn.close()
            break
        else:
            print("Opção inválida. Tente novamente.")
```

### Explicação

- `database = 'contacts.db'`: Define o nome do banco de dados SQLite que será utilizado pelo aplicativo Contact Manager.

- `conn = create_connection()`: Cria uma conexão com o banco de dados utilizando a função `create_connection()`.

- `while True:`: Inicia um loop infinito que continua até que o usuário escolha a opção de sair (`'5'`).

- `print("\nMenu:")`: Exibe o menu de opções para o usuário.

- `choice = get_validated_input("Escolha uma opção: ", lambda x: x in {'1', '2', '3', '4', '5'})`: Solicita ao usuário que escolha uma opção do menu e valida a entrada do usuário para garantir que seja uma das opções válidas (`'1'`, `'2'`, `'3'`, `'4'` ou `'5'`).

- O bloco `if-elif-else` verifica a escolha do usuário e executa a ação correspondente a cada opção selecionada.

- `if choice == '1':`, `elif choice == '2':`, `elif choice == '3':`, `elif choice == '4':`, `elif choice == '5':`: Cada bloco verifica a escolha do usuário e chama a função apropriada para realizar a ação desejada.

- O bloco `else:` é acionado se o usuário inserir uma opção inválida e exibe uma mensagem de erro.

- `conn.close()`: Fecha a conexão com o banco de dados quando o usuário escolhe sair do programa.

### Exemplo de Uso

```python
if __name__ == '__main__':
    import_from_csv('contacts_with_errors.csv')
    main()
```

Este exemplo importa dados do arquivo CSV `'contacts_with_errors.csv'` para o banco de dados e, em seguida, inicia a função `main()`, permitindo que o usuário interaja com o aplicativo.

“A função `main()` é o ponto de entrada principal do aplicativo Contact Manager, coordenando todas as operações de gerenciamento de contatos.”

