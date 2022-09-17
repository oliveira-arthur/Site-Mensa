from flask_wtf import FlaskForm  #importando formularios
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField,TextAreaField  #importando os campos que deseja estar no formulario: texto, senha e submit que é entar
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError #, ValidationError #importando os validadores das informaçoes de login e criar conta: 1 campo obrigatorio, 2 tamanho, 3 3mail, 4 campo igual a outro
from comunidademensa.models import Usuario
from flask_login import current_user


class FormCriarConta(FlaskForm): #não precisa de init pois criar conta esta pegando a herança do flaskform
    username = StringField('Nome de Usuário', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(),Length(6,20)])
    confirmacao = PasswordField('Confirmar senha', validators=[DataRequired(), EqualTo('senha')])
    botao_submit_criar_conta = SubmitField('Criar Conta')


    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('E-mail já cadastrado. Insira um novo e-mail ou faça login')


class FormLogin(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(),Length(6,20)])
    lembrar_dados = BooleanField('Lembrar dados de acesso')
    botao_submit_login = SubmitField('Entrar')



class FormEditarPerfil(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    foto_perfil = FileField('Atualizar foto de perfil', validators=[FileAllowed(['jpg', 'png'])])
    # local onde vou colocar as áreas de interesses da mensa.  Precisa coloca-los no html para funcionar
    interesse_filosofia = BooleanField('Filosofia')
    interesse_escritores = BooleanField('Escritores')
    interesse_jogos = BooleanField('Jogos')
    interrese_puzze = BooleanField('Puzzes')
    interesse_xadrez = BooleanField('Xadrez')
    interesse_psicologia = BooleanField('Psicologia')
    interesse_neurociencia = BooleanField('Neurociência')
    interesse_artes = BooleanField('Artes')
    interesse_programacao = BooleanField('Programação')
    interesse_desenho = BooleanField('Desenho')
    interesse_esportes = BooleanField('Esportes')
    interesse_fotografia = BooleanField('Fotografia')
    interesse_artes_marciais = BooleanField('Artes Marciais')
    interesse_matematica = BooleanField('Matemática')
    botao_submit_editarperfil = SubmitField('Atualizar Edição')

    def validate_email(self, email):
        if current_user.email != email.data:
            usuario = Usuario.query.filter_by(email=email.data).first()
            if usuario:
                raise ValidationError('Já existe um usuário com este e-mail. Por favor, cadastre um novo e-mail')


class FormCriar_Post(FlaskForm):
    titulo = StringField('Titulo do Post', validators=[DataRequired(), Length(2,140)])
    corpo = TextAreaField('Digite aqui seu Post', validators=[DataRequired()])
    submit = SubmitField('Criar Post')