
from flask import Flask, request, render_template, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, RadioField, IntegerField, DecimalField
from wtforms.validators import DataRequired
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db = SQLAlchemy(app)
app.config.update(dict(
    SECRET_KEY="voce precisa mudar isso",
    WTF_CSRF_SECRET_KEY="isso aqui tbm"
))

login_manager = LoginManager() 
login_manager.init_app(app)


def handle_404(e):
    flash ("A página não foi encontrada, aí te devolvemos pra cá")
    return render_template('putz.html'), 404
def handle_500(e):
    flash ("Eita, acho que o estagiário fez besteira")
    return render_template('putz.html'), 500
def handle_403(e):
    flash ("Hmmmmmm, Safadinho")
    return render_template('putz.html'), 403
def handle_409(e):
    flash ("É GUERRA! É GUERRA!")
    return render_template('putz.html'), 409

app.register_error_handler(404, handle_404)
app.register_error_handler(500, handle_500)
app.register_error_handler(403, handle_403)
app.register_error_handler(409, handle_409)


class User(UserMixin, db.Model):
   __tablename__= 'user'
   id = db.Column(db.Integer, primary_key=True, autoincrement=True)
   nome = db.Column(db.String(20), nullable=False)
   cpf = db.Column(db.String, unique=True)
   email = db.Column(db.String, unique=True)
   senha = db.Column(db.String, nullable=False)
   pedidos = db.relationship('Pedido', backref='cliente')
   pratos = db.relationship('Prato', backref='user')
   bebidas_fornecedor = db.relationship('Bebida', backref='user')
   role = db.Column(db.Integer)








''' class Cliente(UserMixin, db.Model):
    __tablename__= 'cliente'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(20), nullable=False)
    cpf = db.Column(db.String, unique=True)
    sobrenome = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    senha = db.Column(db.String, nullable=False)
    pedidos = db.relationship('Pedido', backref='cliente')
    #formas de pagamento
    cartao_de_credito = db.Column(db.Boolean)
    dinheiro = db.Column(db.Boolean)

 # Fornecedor não precisa carregar pedido diretamente, prato carrega a id do fornecedor, podendo redirecionar
 #1 Fornecedor -> N pratos
class Fornecedor(UserMixin, db.Model):
    __tablename__= 'fornecedor'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_empresa = db.Column(db.String)
    cpf = db.Column(db.String, unique=True)
    email = db.Column(db.String)
    senha = db.Column(db.String)
    pratos = db.relationship('Prato', backref='fornecedor')
    #entregas = db.relationship('Formas_entrega_fornecedores', backref='fornecedor')
    pedidos_fornecedor = db.relationship('Pedido', backref='fornecedor')
    bebidas_fornecedor = db.relationship('Bebida', backref='fornecedor')
    #formas de pagamento
    cartao_de_credito = db.Column(db.Boolean)
    dinheiro = db.Column(db.Boolean)'''
    





class Pedido(db.Model):
    __tablename__= 'pedido'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_cliente = db.Column(db.Integer, db.ForeignKey('user.id'))
    id_prato = db.Column(db.Integer, db.ForeignKey('prato.id'))
    id_bebida = db.Column(db.Integer, db.ForeignKey('bebida.id'))

class Prato(db.Model):
    __tablename__= 'prato'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_fornecedor = db.Column(db.Integer, db.ForeignKey('user.id'))
    nome = db.Column(db.String)
    descricao = db.Column(db.String)
    preco = db.Column(db.Integer)
    quantidade_disponivel = db.Column(db.Integer )
    pedidos = db.relationship('Pedido', backref='prato')



class Bebida(db.Model):
    __tablename__='bebida'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_fornecedor = db.Column(db.Integer, db.ForeignKey('user.id'))
    nome = db.Column(db.String(20))
    pedidos = db.relationship('Pedido', backref='bebida')


db.create_all()
db.session.commit()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


##### FORMULÁRIOS
class Form_login(FlaskForm):
    email = StringField("email", validators=[DataRequired()])
    senha = PasswordField("senha", validators=[DataRequired()])
    lembrar_me = BooleanField("lembrar_me")


class Form_registro(FlaskForm):
    nome = StringField("nome", validators=[DataRequired()])
    email = StringField("email", validators=[DataRequired()])
    cpf = IntegerField("cpf", validators=[DataRequired()])
    senha = PasswordField("senha", validators=[DataRequired()])
    cartao_de_credito = BooleanField("cartao_de_credito")
    dinheiro = BooleanField("dinheiro")
    role = RadioField('Você é?', validators=[DataRequired()], choices=[('cliente', 'Cliente'),('fornecedor', 'Fornecedor')], default='cliente')

class Form_prato(FlaskForm):
    nome_prato = StringField("nome_prato", validators=[DataRequired()])
    descricao_prato = StringField("descricao_prato", validators=[DataRequired()])
    preco = IntegerField("preco", validators=[DataRequired()])
    quantidademax = IntegerField("quantidademax")










#homepage
@app.route("/")
@app.route("/home", methods=['GET','POST']) 
def home():
    return render_template('index.html')

#cadastro
@app.route("/registrar", methods=['GET','POST']) 
def registrar():
    form = Form_registro()
    if form.validate_on_submit():
        nome = form.nome.data
        email = form.email.data
        cpf = form.cpf.data
        senha = form.senha.data
        role = form.role.data
        escravo = User(nome=nome, email=email, cpf=cpf, senha=senha, role=role)
        db.session.add(escravo)
        db.session.commit()
        flash("Registro feito!")
        return render_template('index.html')
    return render_template('arrumar_a_mesa.html', form=form)


    

###login
@app.route("/login", methods=['GET','POST']) 
def login():
    form = Form_login()
    if form.validate_on_submit():
            email = form.email.data
            user = User.query.filter_by( email = email ).first()
            if user and user.senha == form.senha.data:
                login_user(user)
                flash("Login realizado, seja bem vindo")
            else:
                flash("Login inválido")
    return render_template("login.html", form = form )
    

    




@app.route("/criar_prato", methods=['GET','POST'])
@login_required
def criar_prato():
    form = Form_prato()
    if current_user.role == "fornecedor":
        if form.validate_on_submit():
            nome_prato = form.nome_prato.data
            descricao_prato = form.descricao_prato.data
            preco = form.preco.data
            quantidademax = form.quantidademax.data
            id_fornecedor = current_user.id
            escravo = Prato(nome=nome_prato, descricao=descricao_prato, preco=preco, quantidade_disponivel=quantidademax, id_fornecedor=id_fornecedor)
            db.session.add(escravo)
            db.session.commit()
            flash("Prato Registrado")
    else:
        flash("Opa, você não tem acesso a essa página:(")
        return render_template('index.html')
    return render_template('prato.html', form=form)



@app.route("/lista_pratos", methods=['GET', 'POST'])
def lista_pratos():
    pratos = Prato.query.all()
    return render_template("lista_pratos.html", pratos=pratos)

@app.route("/logout")
def logout():
    if current_user:
        logout_user()
        flash("você foi deslogado")
    else:
        flash("você não está logado")
    return render_template("index.html")

@app.route("/pedir/<id>", methods=['GET', 'POST'])
def pedir(id):
    if current_user.role == "cliente":
        id_cliente = current_user.id
        id_prato = id
        escravo = Pedido(id_cliente=id_cliente, id_prato = id_prato)
        db.session.add(escravo)
        db.session.commit()
        flash("Pedido feito")
        return render_template("index.html")
    else:
        flash("não foi possível realizar a ação")
        return render_template("index.html")

@app.route("/pedidos")
def lista_pedidos():
    if current_user.role == "cliente":
        pedidos = Pedido.query.filter_by(id_cliente = current_user.id)
        return render_template("lista_cliente.html", pedidos=pedidos)
    if current_user.role == "fornecedor":
        pratos = Prato.query.filter_by( id_fornecedor = current_user.id )
        pedidos = pratos.pedidos
        return render_template("lista_forn.html", pedidos=pedidos)

        
    

