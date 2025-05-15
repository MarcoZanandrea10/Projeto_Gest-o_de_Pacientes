from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

#conexao com o banco de dados
conn = sqlite3.connect('gestao_hospitalar.db')
cursor = conn.cursor()

#criacao de tabelas caso nao exista
cursor.execute('''
    CREATE TABLE IF NOT EXISTS pacientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        idade INTEGER,
        sexo TEXT,     
        cpf TEXT UNIQUE,
        endereco TEXT,
        telefone TEXT    
    )
''')

conn.commit()  #salvar
conn.close()   #fechar

@app.route('/')
def index():
    conn = sqlite3.connect('gestao_hospitalar.db') #conecta com a gestao hospitalar
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM pacientes')      #seleciona tudo da tabalas "pacientes"
    pacientes = cursor.fetchall()                  #alinha as informacoes
    conn.close()                                   #apenas fechar pois nao foi feito alteracoes
    return render_template('index.html', pacientes=pacientes) #retornar informacoes no template


@app.route('/novo_paciente', methods=['GET', 'POST']) #sincroniza com html
def novo_paciente():
    if request.method == 'POST':        #resquest nao deixa enviar em branco
        nome = request.form['nome']
        idade = request.form['idade']
        sexo = request.form['sexo']
        cpf = request.form['cpf']
        endereco = request.form['endereco']
        telefone = request.form['telefone']

        conn = sqlite3.connect('gestao_hospitalar.db')  #entrar no banco de dados 
        cursor = conn.cursor()
        cursor.execute('''                              
            INSERT INTO pacientes (nome, idade, sexo, cpf, endereco, telefone)
            VALUES (?, ?, ?, ?, ?, ?)              
        ''', (nome, idade, sexo, cpf, endereco, telefone))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))           #caso de problema, retorna ao index
    return render_template('novo_paciente.html')


@app.route('/limpar_pacientes')      #botao limpar pacientes
def limpar_pacientes():
    conn = sqlite3.connect('gestao_hospitalar.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM pacientes')       #deletar todos os pacientes
    conn.commit()                                 #salvar mudancas
    conn.close()                                  #fechar
    return redirect(url_for('index'))             #redireciona pro index


if __name__ == ("__main__"):
    app.run(debug=True)