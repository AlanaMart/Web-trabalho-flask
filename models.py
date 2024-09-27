from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Formulario(db.Model):
    __tablename__ = 'formularios'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    perguntas = db.relationship('Pergunta', backref='formulario', lazy=True)

class Pergunta(db.Model):
    __tablename__ = 'perguntas'
    id = db.Column(db.Integer, primary_key=True)
    texto = db.Column(db.String(200), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    formulario_id = db.Column(db.Integer, db.ForeignKey('formularios.id'), nullable=False)
    alternativas = db.relationship('Alternativa', backref='pergunta', lazy=True)

class Alternativa(db.Model):
    __tablename__ = 'alternativas'
    id = db.Column(db.Integer, primary_key=True)
    texto = db.Column(db.String(200), nullable=False)
    pergunta_id = db.Column(db.Integer, db.ForeignKey('perguntas.id'), nullable=False)
