import sqlite3
import csv
import re

def create_connection():
    conn = None
    try:
        conn = sqlite3.connect('contacts.db')
    except sqlite3.Error as e:
        print(e)
    return conn

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


def add_contact(conn, contact):
    sql = '''INSERT INTO contacts(name, email, phone, address)
             VALUES(?, ?, ?, ?)'''
    cur = conn.cursor()
    cur.execute(sql, contact)
    conn.commit()
    return cur.lastrowid

def view_contacts(conn):
    sql = 'SELECT * FROM contacts'
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    for row in rows:
        print(row)

def update_contact(conn, contact_id, fields):
    set_clause = ', '.join(f"{field} = ?" for field in fields.keys())
    sql = f"UPDATE contacts SET {set_clause} WHERE id = ?"
    cur = conn.cursor()
    cur.execute(sql, list(fields.values()) + [contact_id])
    conn.commit()

def delete_contact(conn, id):
    sql = 'DELETE FROM contacts WHERE id=?'
    cur = conn.cursor()
    cur.execute(sql, (id,))
    conn.commit()

def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email)

def is_valid_phone(phone):
    pattern = r'^[\d\+\-\(\) ]+$'
    return re.match(pattern, phone)

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

def contact_exists(conn, contact_id):
    sql = 'SELECT 1 FROM contacts WHERE id = ?'
    cur = conn.cursor()
    cur.execute(sql, (contact_id,))
    return cur.fetchone() is not None

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
            name = get_validated_input("Nome (deve incluir sobrenome): ", lambda x: ' ' in x)
            email = get_validated_input("Email: ", is_valid_email)
            phone = get_validated_input("Telefone: ", is_valid_phone)
            address = get_validated_input("Endereço: ")
            if name and email and phone and address:
                contact = (name, email, phone, address)
                add_contact(conn, contact)
            else:
                print("Todos os campos são obrigatórios.")
        elif choice == '2':
            view_contacts(conn)
        elif choice == '3':
            contact_id = get_validated_input("ID do Contato: ", lambda x: x.isdigit() and contact_exists(conn, int(x)))
            contact_id = int(contact_id)
            fields = {}
            if input("Atualizar nome? (s/n): ").lower() == 's':
                fields['name'] = get_validated_input("Nome (deve incluir sobrenome): ", lambda x: ' ' in x)
            if input("Atualizar email? (s/n): ").lower() == 's':
                fields['email'] = get_validated_input("Email: ", is_valid_email)
            if input("Atualizar telefone? (s/n): ").lower() == 's':
                fields['phone'] = get_validated_input("Telefone: ", is_valid_phone)
            if input("Atualizar endereço? (s/n): ").lower() == 's':
                fields['address'] = get_validated_input("Endereço: ")
            if fields:
                update_contact(conn, contact_id, fields)
            else:
                print("Nenhum campo selecionado para atualização.")
        elif choice == '4':
            contact_id = get_validated_input("ID do Contato: ", lambda x: x.isdigit() and contact_exists(conn, int(x)))
            contact_id = int(contact_id)
            delete_contact(conn, contact_id)
        elif choice == '5':
            conn.close()
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == '__main__':
    import_from_csv('contacts_with_errors.csv')
    main()
