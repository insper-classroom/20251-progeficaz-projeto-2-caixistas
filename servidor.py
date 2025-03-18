from flask import Flask, request, jsonify
import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
# Carrega as variáveis de ambiente do arquivo .cred (se disponível)
load_dotenv('.env')

# Configurações para conexão com o banco de dados usando variáveis de ambiente
config = {
    'host': os.getenv('DB_HOST'),  # Obtém o host do banco de dados da variável de ambiente
    'user': os.getenv('DB_USER'),  # Obtém o usuário do banco de dados da variável de ambiente
    'password': os.getenv('DB_PASSWORD'),  # Obtém a senha do banco de dados da variável de ambiente
    'database': os.getenv('DB_NAME'),  # Obtém o nome do banco de dados da variável de ambiente
    'port': int(os.getenv('DB_PORT')),  # Obtém a porta do banco de dados da variável de ambiente
    'ssl_ca': os.getenv('SSL_CA_PATH')  # Caminho para o certificado SSL
}

# Função para conectar ao banco de dados
def connect_db():
    """Estabelece a conexão com o banco de dados usando as configurações fornecidas."""
    try:
        # Tenta estabelecer a conexão com o banco de dados usando mysql-connector-python
        conn = mysql.connector.connect(**config)
        if conn.is_connected():
            return conn
    except Error as err:
        # Em caso de erro, imprime a mensagem de erro
        print(f"Erro: {err}")
        return None


app = Flask(__name__)

@app.route('/imoveis', methods=['GET'])
def get_imoveis():

    # Conecta o banco de dados
    conn = connect_db()

    # Se não conseguiu conectar, retorna um erro 500
    if conn is None:
        resp = {"erro": "Erro ao conectar ao banco de dados"}
        return resp, 500

    cursor = conn.cursor()

    # Executa a query para buscar todos os imóveis
    sql = "SELECT * from imoveis"
    cursor.execute(sql)

    # Obtém os resultados da query
    results = cursor.fetchall()

    if not results:
        resp = {"erro": "Nenhum imóvel encontrado"}
        return resp, 404
    else:
        imoveis = []
        for imovel in results:
            imovel_dict = {
                "id": imovel[0],
                "logradouro": imovel[1],
                "tipo_logradouro": imovel[2],
                "bairro": imovel[3],
                "cidade": imovel[4],
                "cep": imovel[5],
                "tipo": imovel[6],
                "valor": imovel[7],
                "data_aquisicao": imovel[8],
            }
            imoveis.append(imovel_dict)
        resp = {"imovel": imoveis}
        return resp, 200

@app.route('/imoveis/delete/<int:id>', methods=['DELETE'])
def delete_imovel(id):

    # Conecta o banco de dados
    conn = connect_db()

    # Se não conseguiu conectar, retorna um erro 500
    if conn is None:
        resp = {"erro": "Erro ao conectar ao banco de dados"}
        return resp, 500

    cursor = conn.cursor()

    # Deletar o imóvel
    cursor.execute("DELETE FROM imoveis WHERE id = %s", (id,))
    conn.commit()

    if conn.is_connected():
            cursor.close()
            conn.close()

    resp = {'mensagem': 'Imóvel removido com sucesso.'}

    return resp, 200

@app.route('/imoveis/<int:id>', methods=['GET']) #devemos passar o que queremos acessar na rota, nesse caso o id 
def get_imoveis_id(id):

    conn = connect_db()

    cursor = conn.cursor()

    # Executa a query para buscar o id do imovel
    sql = f"SELECT * from imoveis where id = {id}"
    cursor.execute(sql)

    # Obtém os resultados da query
    results = cursor.fetchall()

    if not results:
        resp = {"erro": "Nenhum imóvel encontrado"}
        return resp, 404
    else:
        imoveis = []
        for imovel in results:
            if imovel[0] == id:
                imovel_dict = {
                    "id": imovel[0],
                    "logradouro": imovel[1],
                    "tipo_logradouro": imovel[2],
                    "bairro": imovel[3],
                    "cidade": imovel[4],
                    "cep": imovel[5],
                    "tipo": imovel[6],
                    "valor": imovel[7],
                    "data_aquisicao": imovel[8],
                }
                imoveis.append(imovel_dict)
        if not imoveis:
            resp = {'erro': 'imóvel não encontrado'}
            return resp, 404
        else:
            resp = {"imovel": imoveis}
            return resp, 200
        
@app.route('/imoveis/tipo/<string:tipo>', methods=['GET']) #precisa passar o que queremos na rota, que nesse caso é o tipo do imovel
def get_imoveis_tipo(tipo):

    # Conecta o banco de dados
    conn = connect_db()

    # Se não conseguiu conectar, retorna um erro 500
    if conn is None:
        resp = {"erro": "Erro ao conectar ao banco de dados"}
        return resp, 500

    cursor = conn.cursor()

    # Executa a query para buscar o tipo do imovel
    sql = f"SELECT * from imoveis where tipo = '{tipo}'"
    cursor.execute(sql)

    # Obtém os resultados da query
    results = cursor.fetchall()

    if not results:
        resp = {"erro": "Nenhum imóvel encontrado"}
        return resp, 404
    else:
        imoveis = []
        for imovel in results:
            if imovel[6] == tipo:
                imovel_dict = {
                    "id": imovel[0],
                    "logradouro": imovel[1],
                    "tipo_logradouro": imovel[2],
                    "bairro": imovel[3],
                    "cidade": imovel[4],
                    "cep": imovel[5],
                    "tipo": imovel[6],
                    "valor": imovel[7],
                    "data_aquisicao": imovel[8],
                }
                imoveis.append(imovel_dict)
        if not imoveis:
            resp = {'erro': 'imóvel não encontrado'}
            return resp, 404
        else:
            resp = {"imovel": imoveis}
            return resp, 200
        
@app.route('/imoveis/atualiza/<int:id>/<string:coluna>/<string:alteracao>', methods=['PUT'])
def atualiza_imovel(id, coluna, alteracao):

    # Conecta o banco de dados
    conn = connect_db()

    # Se não conseguiu conectar, retorna um erro 500
    if conn is None:
        resp = {"erro": "Erro ao conectar ao banco de dados"}
        return resp, 500

    cursor = conn.cursor()

    # Executa a query para verificar se este imóvel realmente existe
    sql= "SELECT * from imoveis.imoveis where id = %s"
    cursor.execute(sql, (id,))

    # Obtém os resultados da query
    results = cursor.fetchall()

        # Erro 404 para caso o imóvel não seja encontrado
    if not results:
        resp = {"erro": "Nenhum imóvel encontrado"}
        return resp, 404
    else:
        # Verifica se a coluna existe no banco de dados
        cursor.execute("SHOW COLUMNS FROM imoveis")
        columns = [column[0] for column in cursor.fetchall()]
        # if coluna not in columns:
        #     resp = {"erro": f"Coluna '{coluna}' não encontrada no banco de dados"}
        #     return resp, 400

        # Atualiza o imóvel
        sql = f"UPDATE imoveis.imoveis SET {coluna} = %s WHERE id = %s"
        cursor.execute(sql, (alteracao, id))
        conn.commit()

        if conn.is_connected():
            cursor.close()
            conn.close()

        resp = {'mensagem': 'Imóvel atualizado com sucesso.'}

    return resp, 200

@app.route('/imoveis/cidade/<string:cidade>', methods=['GET']) #precisa passar o que queremos na rota, que nesse caso é a cidade do imovel
def get_imoveis_cidade(cidade):

    # Conecta o banco de dados
    conn = connect_db()

    # Se não conseguiu conectar, retorna um erro 500
    if conn is None:
        resp = {"erro": "Erro ao conectar ao banco de dados"}
        return resp, 500

    cursor = conn.cursor()

    # Executa a query para buscar o tipo do imovel
    sql = f"SELECT * from imoveis.imoveis where cidade = %s"
    cursor.execute(sql, (cidade,))

    # Obtém os resultados da query
    results = cursor.fetchall()

    if not results:
        resp = {"erro": "Nenhum imóvel encontrado"}
        return resp, 404
    
    imoveis = []
    for imovel in results:
        imovel_dict = {
            "id": imovel[0],
            "logradouro": imovel[1],
            "tipo_logradouro": imovel[2],
            "bairro": imovel[3],
            "cidade": imovel[4],
            "cep": imovel[5],
            "tipo": imovel[6],
            "valor": imovel[7],
            "data_aquisicao": imovel[8],
        }
        imoveis.append(imovel_dict)
    if not imoveis:
        resp = {'erro': 'imóvel não encontrado'}
        return resp, 404
    else:
        resp = {"imovel": imoveis}
        return resp, 200
    


if __name__ == '__main__':
    app.run(debug=True)