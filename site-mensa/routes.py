from flask import render_template, redirect, url_for,flash,request, abort
from comunidademensa import app, database, bcrypt
from comunidademensa.forms import FormLogin, FormCriarConta, FormEditarPerfil, FormCriar_Post
from comunidademensa.models import Usuario, Post
from flask_login import login_user, logout_user, current_user, login_required
import secrets
import os
from PIL import Image



@app.route("/")
def home():
    posts = Post.query.order_by(Post.id.desc())
    return render_template('home.html', posts=posts)  #puxando o teste html


@app.route('/contato') #cada route é um novo link ou uma nova pagina
def contato():
    return render_template('contato.html')


@app.route('/usuarios')
@login_required
def usuarios():
    lista_usuarios = Usuario.query.all()
    return render_template('usuarios.html', lista_usuarios=lista_usuarios) #pegando a variavel lista usuarios e levando para o codigo em html


@app.route('/login', methods=['GET','POST']) #sempre que tiver um formulário na pagina deve-se liberar o metodo post
def login():
    formlogin = FormLogin()
    formcriarconta = FormCriarConta()
    if formlogin.validate_on_submit() and 'botao_submit_login' in request.form:
        usuario = Usuario.query.filter_by(email=formlogin.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, formlogin.senha.data):
            login_user(usuario, remember=formlogin.lembrar_dados.data)
            flash(f'Login feito com sucesso no e-mail: { formlogin.email.data }', 'alert-success')
            par_next = request.args.get('next')
            if par_next:
                return redirect(par_next)
            else:
                return redirect(url_for('home'))
        else:
            flash(f'Não foi possivel fazer o login. E-mail ou senha incorretos' , 'alert-danger')

        #fez login

    if formcriarconta.validate_on_submit() and 'botao_submit_criar_conta' in request.form:
        senha_crypt = bcrypt.generate_password_hash(formcriarconta.senha.data)
        usuario = Usuario(username=formcriarconta.username.data, email= formcriarconta.email.data, senha=senha_crypt)
        database.session.add(usuario)
        database.session.commit()
        flash(f'E-mail criado com sucesso para o e-mail:  {formcriarconta.email.data}', 'alert-success')
        return redirect(url_for('home'))
    return render_template('login.html',formlogin=formlogin, formcriarconta=formcriarconta)

@app.route('/sair')
@login_required
def sair():
    email_logado = current_user.email
    logout_user()
    flash(f'{email_logado} saiu ', 'alert-success')
    return redirect(url_for('home'))

@app.route('/perfil')
@login_required
def perfil():
    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template('perfil.html', foto_perfil=foto_perfil)

@app.route('/post/criar',  methods=['GET','POST'])
@login_required #o usuario só poderá acessar esta pagina se estiver logado.
def criar_post():
    form = FormCriar_Post()
    if form.validate_on_submit():
        post = Post(titulo=form.titulo.data, corpo=form.corpo.data, autor=current_user)
        database.session.add(post)
        database.session.commit()
        flash('Post criado com sucesso','alert-success')
        return redirect(url_for('home'))
    return render_template('criarpost.html', form=form)


def salvar_imagem(imagem):    #função que salva a imagem com um codigo para diferenciar a imagem, reduz a imagem do perfil para ser salva
    codigo = secrets.token_hex(8)
    nome, extensao = os.path.splitext(imagem.filename)
    nome_arquivo = nome + codigo + extensao
    caminho_completo = os.path.join(app.root_path, 'static/fotos_perfil', nome_arquivo)
    tamanho = (200,200)
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida.thumbnail(tamanho)
    imagem_reduzida.save(caminho_completo)
    return nome_arquivo


def atualizar_interesses(form):
    lista_interesses = []
    for campo in form:
        if 'interesse_' in campo.name:
            if campo.data:
                lista_interesses.append(campo.label.text)
    return ";".join(lista_interesses) #join está transformando a lista num texto porque a variavel cursos é uma string

@app.route('/perfil/editar',methods=['GET','POST'])
@login_required
def editar_perfil():
    form = FormEditarPerfil()
    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.username = form.username.data
        if form.foto_perfil.data:
            nome_imagem = salvar_imagem(form.foto_perfil.data)
            current_user.foto_perfil = nome_imagem
        current_user.interesses = atualizar_interesses(form)
        database.session.commit()
        flash('Perfil atualizado com sucesso!', 'alert-success')
        return redirect(url_for('perfil'))
    elif request.method == 'GET':
        form.email.data = current_user.email
        form.username.data = current_user.username
    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template('editarperfil.html', foto_perfil=foto_perfil, form=form)


@app.route('/post/<post_id>', methods=['GET','POST'])
@login_required
def exibir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        form = FormCriar_Post()
        if request.method == 'GET':
            form.titulo.data = post.titulo
            form.corpo.data = post.corpo
        elif form.validate_on_submit():
            post.titulo = form.titulo.data
            post.corpo = form.corpo.data
            database.session.commit()
            flash('Post atualizado com sucesso!','alert-success')
            return redirect(url_for('home',))
    else:
        form = None
    return render_template('post.html', post=post, form=form)


@app.route('/post/<post_id>/excluir', methods=['GET','POST'])
@login_required
def excluir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        database.session.delete(post)
        database.session.commit()
        flash('Post excluido', 'alert-danger')
        return redirect(url_for('home'))
    else:
        abort(403)