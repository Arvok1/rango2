
from flask import Flask, request, render_template, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager ###probleminha####
from flask_migrate import Migrate, MigrateCommand
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, RadioField, IntegerField, DecimalField
from wtforms.validators import DataRequired
from flask_login import LoginManager, login_user, UserMixin

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
###### implementar csrf ######
app.config.update(dict(
    SECRET_KEY="voce precisa mudar isso",
    WTF_CSRF_SECRET_KEY="isso aqui tbm"
))
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return Cliente.query.get(int(user_id))



''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''




class Cliente(UserMixin, db.Model):
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
    pedidos = db.relationship('Pedido', backref='fornecedor')
    bebidas = db.relationship('Bebida', backref='fornecedor')
    #formas de pagamento
    cartao_de_credito = db.Column(db.Boolean)
    dinheiro = db.Column(db.Boolean)





class Pedido(db.Model):
    __tablename__= 'pedido'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_cliente = db.Column(db.Integer, db.ForeignKey('cliente.id'))
    id_prato = db.Column(db.Integer, db.ForeignKey('prato.id'))
    id_fornecedor = db.Column(db.Integer, db.ForeignKey('fornecedor.id'))
    id_bebida = db.Column(db.Integer, db.ForeignKey('bebida.id'))
    quantidade_maxima = db.Column(db.Integer)





#1 prato -> N pedidos <- N máximo é definido pelo Fornecedor
class Prato(db.Model):
    __tablename__= 'prato'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_fornecedor = db.Column(db.Integer, db.ForeignKey('fornecedor.id'))
    nome = db.Column(db.String)
    descricao = db.Column(db.String(100))
    preco = db.Column(db.Integer)
    quantidade_disponivel = db.Column(db.Integer)
    pedidos = db.relationship('Pedido', backref='prato')



class Bebida(db.Model):
    __tablename__='bebida'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_fornecedor = db.Column(db.Integer, db.ForeignKey('fornecedor.id'))
    nome = db.Column(db.String(20))
    pedidos = db.relationship('Pedido', backref='bebida')


db.create_all()



''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


'''
########################################
#  ABAIXO PRECISAM DE PRIMARY_KEY #
########################################
class Formas_entrega_fornecedores(db.Model):
    __tablename__='formas_entrega_fornecedores'
    id_fornecedor = db.Column(db.Integer, db.ForeignKey('fornecedor._id'))

 
class Formas_entrega_clientes(db.Model):
    __tablename__='formas_entrega_clientes'


'''

#criador de database






##### FORMULÁRIOS
class Form_login(FlaskForm):
    email = StringField("email", validators=[DataRequired()])
    senha = PasswordField("senha", validators=[DataRequired()])
    lembrar_me = BooleanField("lembrar_me")

class Form_registro_empresa(FlaskForm):
    nome = StringField("nome", validators=[DataRequired()])
    email = StringField("email", validators=[DataRequired()])
    cpf = IntegerField("cpf", validators=[DataRequired()])
    senha = PasswordField("senha", validators=[DataRequired()])
    cartao_de_credito = BooleanField("cartao_de_credito")
    dinheiro = BooleanField("dinheiro")

class Form_registro_cliente(FlaskForm):
    nome = StringField("nome", validators=[DataRequired()])
    email = StringField("email", validators=[DataRequired()])
    cpf = IntegerField("cpf", validators=[DataRequired()])
    senha = PasswordField("senha", validators=[DataRequired()])
    cartao_de_credito = BooleanField("cartao_de_credito")
    dinheiro = BooleanField("dinheiro")

class Form_prato(FlaskForm):
    nome_prato = StringField("nome_prato", validators=[DataRequired()])
    descricao_prato = StringField("descricao_prato", validators=[DataRequired()])
    preco = DecimalField("preco_prato", validators=[DataRequired()])
    quantidade_disponivel = IntegerField("quantidademax_prato")








## username = email

#homepage
@app.route("/") 
def hello():
    return render_template('index.html')

#cadastro de clientes
@app.route("/arrumar_a_mesa", methods=['GET','POST']) 
def cadastrar_cliente():
    form = Form_registro_cliente()
    if form.validate_on_submit():
        nome = form.nome.data
        email = form.email.data
        cpf = form.cpf.data
        senha = form.senha.data
        escravo = Cliente(nome=nome, email=email, cpf=cpf, senha=senha)
        db.session.add(escravo)
        db.session.commit()
        flash("Registro feito!")
        return render_template('index.html')
    return render_template('arrumar_a_mesa.html', form=form)
    

###login
@app.route("/login_cliente", methods=['GET','POST']) 
def login_cliente():
    form = Form_login()
    if form.validate_on_submit():
            email = form.email.data
            cliente = Cliente.query.filter_by( email = email ).first()
            if cliente and cliente.senha == form.senha.data:
                login_user(cliente)
                flash("Login realizado")

            else:
                flash("Login inválido")
    return render_template('login.html', form = form )
    
@app.route("/login")
def login():
    form = Form_login()
    return render_template('login.html', form = form )
    



@app.route("/homepage", methods=['GET','POST'])
def sei_la():
    return render_template('index.html')

@app.route("/criar_prato", methods=['GET','POST'])
def criar_prato():
    if form.validate_on_submit:
        nome_prato = form.nome_prato.data
        descricao_prato = form.descricao_prato.data
        preco = form.preco.data
        quantidade_disponivel = form.quantidade_disponivel.data
        escravo = Prato(nome=nome_prato, descricao=descricao_prato, preco=preco, quantidade_disponivel=quantidade_disponivel)
        db.session.add(escravo)
        db.session.commit()
        flash("Prato Registrado")
    return render_template('prato.html')

@app.route("/lista_pratos", methods=['GET', 'POST'])
def lista_pratos():
    pratos = Prato.query.all()
    return render_template("lista_pratos.html", pratos=prato)

