from flask import Flask, request, jsonify, render_template
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
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
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa o banco de dados
db = SQLAlchemy(app)

# Configuração do Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

# Modelo de Usuário
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(100), nullable=False)

# Modelo de Animal
class Animal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    raca = db.Column(db.String(100), nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    saude = db.Column(db.String(200), nullable=True)
    status = db.Column(db.String(50), default='Disponível')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

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
    user = User.query.filter_by(email=data['email']).first()  # Verifique se o usuário existe
    if user and user.senha == data['senha']:  # Verifique a senha
        login_user(user)  # Loga o usuário
        return jsonify({"message": "Login bem-sucedido!"}), 200
    return jsonify({"message": "Login falhou!"}), 401

# Rota para cadastrar uma nova ONG
@app.route('/cadastrar_ong', methods=['POST'])
def cadastrar_ong():
    data = request.json
    new_user = User(nome=data['nome'], email=data['email'], senha=data['senha'])
    db.session.add(new_user)
    db.session.commit()
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

# Rota para adicionar um novo animal
@app.route('/adicionar_animal', methods=['GET', 'POST'])
@login_required
def adicionar_animal():
    if request.method == 'POST':
        data = request.form
        new_animal = Animal(
            nome=data['nome'],
            raca=data['raca'],
            idade=data['idade'],
            saude=data['saude'],
            status=data['status']
        )
        db.session.add(new_animal)
        db.session.commit()
        return jsonify({'message': 'Animal adicionado com sucesso!'}), 201
    return render_template('adicionar_animal.html')  # Renderiza o formulário para adicionar animais

# Rota para listar todos os animais
@app.route('/animais', methods=['GET'])
@login_required
def listar_animais():
    todos_animais = Animal.query.all()  # Recupera todos os animais do banco de dados
    return render_template('animais.html', animais=todos_animais)  # Renderiza a página com a lista de animais

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Cria as tabelas do banco de dados
    app.run(host=os.getenv('HOST', '0.0.0.0'), port=int(os.getenv('PORT', 5000)), debug=os.getenv('DEBUG', 'False') == 'True')
