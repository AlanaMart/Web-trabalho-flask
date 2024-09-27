from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db, Formulario, Pergunta, Alternativa


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost/trabalhoflask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


migrate = Migrate(app, db)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit_form():
    data = request.get_json()
    if data is None:
        data = request.form

    nome = data.get('nome')
    descricao = data.get('descricao')
    perguntas = data.get('perguntas', [])

    if not nome or not descricao:
        return jsonify({"error": "Nome e Descrição são obrigatórios"}), 400
    
    novo_form = Formulario(nome=nome, descricao=descricao)
    db.session.add(novo_form)
    db.session.commit()

    for p in perguntas:
        nova_pergunta = Pergunta(texto=p['texto'], tipo=p['tipo'], formulario_id=novo_form.id)
        db.session.add(nova_pergunta)
        db.session.commit()

        for alt in p.get('alternativas', []):
            nova_alternativa = Alternativa(texto=alt, pergunta_id=nova_pergunta.id)
            db.session.add(nova_alternativa)

    db.session.commit()

    return jsonify({"success": True, "message": "Formulário e perguntas salvos", "form_id": novo_form.id})

@app.route('/formulario/<int:form_id>', methods=['GET'])
def ver_formulario(form_id):
    formulario = Formulario.query.get_or_404(form_id)
    return render_template('visualizar_formulario.html', formulario=formulario)

@app.route('/formularios', methods=['GET'])
def ver_formularios():
    formularios = Formulario.query.all()
    return render_template('visualizar_form.html', formularios=formularios)


@app.route('/formulario/<int:id>/editar', methods=['GET', 'POST'])
def editar_formulario(id):
    formulario = Formulario.query.get_or_404(id)

    if request.method == 'POST':
        data = request.get_json()
        nome = data.get('nome')
        descricao = data.get('descricao')
        perguntas = data.get('perguntas', [])

        if not nome or not descricao:
            return jsonify({"error": "Nome e Descrição são obrigatórios"}), 400


        formulario.nome = nome
        formulario.descricao = descricao


        Alternativa.query.filter(Alternativa.pergunta_id.in_([p.id for p in Pergunta.query.filter_by(formulario_id=formulario.id).all()])).delete(synchronize_session=False)
        Pergunta.query.filter_by(formulario_id=formulario.id).delete(synchronize_session=False)

        for p in perguntas:
            nova_pergunta = Pergunta(texto=p['texto'], tipo=p['tipo'], formulario_id=formulario.id)
            db.session.add(nova_pergunta)
            db.session.commit()

            for alt in p.get('alternativas', []):
                nova_alternativa = Alternativa(texto=alt, pergunta_id=nova_pergunta.id)
                db.session.add(nova_alternativa)

        db.session.commit()

        return jsonify({"success": True, "message": "Formulário editado com sucesso"})

    return render_template('editar_formulario.html', formulario=formulario)


        
        
if __name__ == '__main__':
    app.run(debug=True)
