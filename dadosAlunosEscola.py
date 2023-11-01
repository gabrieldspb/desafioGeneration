from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/dbname'
db = SQLAlchemy(app)
ma = Marshmallow(app)

# Modelo de dados para Aluno
class Aluno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    idade = db.Column(db.Integer)
    nota_primeiro_semestre = db.Column(db.Float)
    nota_segundo_semestre = db.Column(db.Float)
    nome_professor = db.Column(db.String(100))
    numero_sala = db.Column(db.String(10))

# Schema do Aluno para serialização
class AlunoSchema(ma.Schema):
    class Meta:
        fields = ('id', 'nome', 'idade', 'nota_primeiro_semestre', 'nota_segundo_semestre', 'nome_professor', 'numero_sala')

aluno_schema = AlunoSchema()
alunos_schema = AlunoSchema(many=True)

# Rota para criar um novo aluno
@app.route('/alunos', methods=['POST'])
def add_aluno():
    nome = request.json['nome']
    idade = request.json['idade']
    nota_primeiro_semestre = request.json['nota_primeiro_semestre']
    nota_segundo_semestre = request.json['nota_segundo_semestre']
    nome_professor = request.json['nome_professor']
    numero_sala = request.json['numero_sala']

    novo_aluno = Aluno(nome, idade, nota_primeiro_semestre, nota_segundo_semestre, nome_professor, numero_sala)

    db.session.add(novo_aluno)
    db.session.commit()

    return aluno_schema.jsonify(novo_aluno)

# Rota para obter todos os alunos
@app.route('/alunos', methods=['GET'])
def get_alunos():
    alunos = Aluno.query.all()
    return alunos_schema.jsonify(alunos)

# Rota para obter um aluno por ID
@app.route('/alunos/<id>', methods=['GET'])
def get_aluno(id):
    aluno = Aluno.query.get(id)
    return aluno_schema.jsonify(aluno)

# Rota para atualizar um aluno por ID
@app.route('/alunos/<id>', methods=['PUT'])
def update_aluno(id):
    aluno = Aluno.query.get(id)

    # Atualize os campos conforme necessário
    aluno.nome = request.json['nome']
    aluno.idade = request.json['idade']
    aluno.nota_primeiro_semestre = request.json['nota_primeiro_semestre']
    aluno.nota_segundo_semestre = request.json['nota_segundo_semestre']
    aluno.nome_professor = request.json['nome_professor']
    aluno.numero_sala = request.json['numero_sala']

    db.session.commit()

    return aluno_schema.jsonify(aluno)

# Rota para excluir um aluno por ID
@app.route('/alunos/<id>', methods=['DELETE'])
def delete_aluno(id):
    aluno = Aluno.query.get(id)
    db.session.delete(aluno)
    db.session.commit()

    return aluno_schema.jsonify(aluno)

# Swagger
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Escola Alunos CRUD"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

if __name__ == '__main__':
    app.run(debug=True)
