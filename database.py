import sqlite3

def init_db():
    # Conectar ao banco de dados (ou criar se não existir)
    conn = sqlite3.connect('refugio.db')
    c = conn.cursor()

    # Criar tabela de animais
    c.execute('''
        CREATE TABLE IF NOT EXISTS animais (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            raca TEXT NOT NULL,
            idade INTEGER NOT NULL,
            saude TEXT NOT NULL,
            status TEXT NOT NULL
        )
    ''')

    # Criar tabela de adoções
    c.execute('''
        CREATE TABLE IF NOT EXISTS adocao (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            animal_id INTEGER NOT NULL,
            adotante_nome TEXT NOT NULL,
            adotante_contato TEXT NOT NULL,
            data_adocao TEXT NOT NULL,
            FOREIGN KEY (animal_id) REFERENCES animais (id)
        )
    ''')

    # Salvar (commit) as mudanças e fechar a conexão
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Banco de dados e tabelas criados com sucesso!")
