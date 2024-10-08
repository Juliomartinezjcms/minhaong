from flask import Flask, request, jsonify, render_template
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import sqlite3
from dotenv import load_dotenv
import os

# Carrega as variáveis do arquivo .env
load_dotenv()

# Obtém as variáveis de ambiente
DATABASE_URL = os.getenv('DATABASE_URL')
SECRET_KEY = os.getenv('SECRET_KEY')
FLASK_ENV = os.getenv('FLASK_ENV')

app = Flask(__name__)
app.secret_key = SECRET_KEY



# Configuração do Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

# Classe de Usuário
class User(UserMixin):
    def __init__(self, id, nome):
        self.id = id
        self.nome = nome

# Simulação de um banco de dados de usuários
users = {}

@login_manager.user_loader
def load_user(user_id):
    return users.get(user_id)

# Conexão com o banco de dados
def get_db_connection():
    conn = sqlite3.connect(DATABASE_URL)
    conn.row_factory = sqlite3.Row
    return conn

# Rota para verificar se a aplicação está funcionando
@app.route('/')
def home():
    return render_template('index.html')  # Renderiza a página inicial

# Rota para a página de login
@app.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')

# Rota para a página de cadastro
@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')



# Rota para login
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    usuario = users.get(data['email'])  # Verifique se o usuário existe
    if usuario and usuario['senha'] == data['senha']:  # Verifique a senha
        user = User(id=usuario['id'], nome=usuario['nome'])
        login_user(user)  # Loga o usuário
        return jsonify({"message": "Login bem-sucedido!"}), 200
    return jsonify({"message": "Login falhou!"}), 401

# Rota para cadastrar uma nova ONG
@app.route('/cadastrar_ong', methods=['POST'])
def cadastrar_ong():
    data = request.json
    # Adicione a lógica para inserir a ONG no banco de dados
    # Exemplo:
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''
        INSERT INTO ongs (nome, email, senha, data_criacao, status)
        VALUES (?, ?, ?, CURRENT_TIMESTAMP, ?)
    ''', (data['nome'], data['email'], data['senha'], 'ativa'))  # O status padrão pode ser 'ativa'
    conn.commit()
    conn.close()
    return jsonify({'message': 'ONG cadastrada com sucesso!'}), 201


# Rota para o perfil
@app.route('/perfil', methods=['GET'])
@login_required
def perfil():
    return jsonify({"nome": current_user.nome}), 200

# Rota de logout
@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logout realizado com sucesso!"}), 200

# Rota para cadastrar um novo animal
@app.route('/adicionar_animal', methods=['POST'])
def adicionar_animal():
    data = request.json
    conn = get_db_connection()
    c = conn.cursor()
    c.execute(''' 
        INSERT INTO animais (nome, raca, idade, saude, status) 
        VALUES (?, ?, ?, ?, ?) 
    ''', (data['nome'], data['raca'], data['idade'], data['saude'], data['status']))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Animal adicionado com sucesso!'}), 201

if __name__ == '__main__':
   app.run(host=os.getenv('HOST', '167.88.33.66:8000'), port=int(os.getenv('PORT', 8000)), debug=True)

