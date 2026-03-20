# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import gspread
# from google.oauth2.service_account import Credentials
# from dotenv import load_dotenv
# import os
# from datetime import datetime

# load_dotenv()

# app = Flask(__name__, static_folder='../frontend', static_url_path='')
# CORS(app)

# SCOPES = [
#     'https://www.googleapis.com/auth/spreadsheets',
#     'https://www.googleapis.com/auth/drive'
# ]

# def conectar_sheets():
#     creds = Credentials.from_service_account_file('credentials.json', scopes=SCOPES)
#     client = gspread.authorize(creds)
#     spreadsheet = client.open_by_key(os.getenv('SPREADSHEET_ID'))
#     return spreadsheet

# def proxima_linha_vazia(sheet):
#     coluna_id = sheet.col_values(1)
#     for i in range(len(coluna_id) - 1, 0, -1):
#         if coluna_id[i].strip() != '':
#             return i + 2
#     return 2

# def registrar_movimentacao_estoque(spreadsheet, id_produto, produto, quantidade, tipo):
#     sheet_estoque = spreadsheet.worksheet('ESTOQUE')
#     coluna_id = sheet_estoque.col_values(1)
#     proxima = len([x for x in coluna_id if x.strip() != '']) + 1
#     data_atual = datetime.now().strftime('%Y-%m-%d')
#     sheet_estoque.batch_update([
#         {'range': f'A{proxima}', 'values': [[id_produto]]},
#         {'range': f'B{proxima}', 'values': [[produto]]},
#         {'range': f'C{proxima}', 'values': [[tipo]]},
#         {'range': f'D{proxima}', 'values': [[quantidade]]},
#         {'range': f'E{proxima}', 'values': [[data_atual]]}
#     ])

# # Rotas para servir os HTMLs
# @app.route('/')
# def index():
#     return app.send_static_file('menu.html')

# @app.route('/menu')
# def menu():
#     return app.send_static_file('menu.html')

# @app.route('/vendas')
# def vendas():
#     return app.send_static_file('index.html')

# @app.route('/clientes')
# def clientes():
#     return app.send_static_file('clientes.html')

# @app.route('/cadastro-produto')
# def produtos_page():
#     return app.send_static_file('produtos.html')

# @app.route('/cadastro-estoque')
# def estoque_page():
#     return app.send_static_file('estoque.html')

# # Rota API para buscar produtos
# @app.route('/produtos', methods=['GET'])
# def get_produtos():
#     try:
#         spreadsheet = conectar_sheets()
#         sheet = spreadsheet.worksheet('PRODUTO')
#         dados = sheet.get_all_records()
#         produtos = [
#             {
#                 'id': p['ID_ITEM'],
#                 'nome': p['PRODUTO'],
#                 'preco': str(p['PRECO_VENDA']).replace('R$', '').replace('.', '').replace(',', '.').strip()
#             }
#             for p in dados if p['PRODUTO']
#         ]
#         return jsonify({'sucesso': True, 'produtos': produtos})
#     except Exception as e:
#         return jsonify({'sucesso': False, 'erro': str(e)}), 500

# # Rota para registrar venda
# @app.route('/venda', methods=['POST'])
# def registrar_venda():
#     try:
#         dados = request.json
#         spreadsheet = conectar_sheets()
#         sheet_vendas = spreadsheet.worksheet('VENDAS')

#         quantidade = float(dados['quantidade'])
#         preco_unitario = float(dados['preco_unitario'])

#         proxima = proxima_linha_vazia(sheet_vendas)

#         sheet_vendas.batch_update([
#             {'range': f'C{proxima}', 'values': [[dados['produto']]]},
#             {'range': f'D{proxima}', 'values': [[quantidade]]},
#             {'range': f'F{proxima}', 'values': [[preco_unitario]]},
#             {'range': f'H{proxima}', 'values': [[dados['data_venda']]]},
#             {'range': f'I{proxima}', 'values': [[dados['cliente']]]},
#             {'range': f'J{proxima}', 'values': [[dados['status_pagamento']]]},
#             {'range': f'K{proxima}', 'values': [[dados['condicao']]]}
#         ])

#         registrar_movimentacao_estoque(
#             spreadsheet,
#             dados['id_produto'],
#             dados['produto'],
#             quantidade,
#             'SAIDA'
#         )

#         return jsonify({'sucesso': True, 'mensagem': 'Venda registrada com sucesso!'})
#     except Exception as e:
#         return jsonify({'sucesso': False, 'erro': str(e)}), 500

# # Rota para cadastrar cliente
# @app.route('/cliente', methods=['POST'])
# def cadastrar_cliente():
#     try:
#         dados = request.json
#         spreadsheet = conectar_sheets()
#         sheet_clientes = spreadsheet.worksheet('CLIENTE')

#         coluna_nome = sheet_clientes.col_values(2)
#         proxima = len([x for x in coluna_nome if x.strip() != '']) + 1

#         data_cadastro = datetime.now().strftime('%Y-%m-%d')

#         sheet_clientes.batch_update([
#             {'range': f'B{proxima}', 'values': [[dados['nome_cliente']]]},
#             {'range': f'C{proxima}', 'values': [[dados['cpf']]]},
#             {'range': f'D{proxima}', 'values': [[dados['telefone']]]},
#             {'range': f'E{proxima}', 'values': [[dados['email']]]},
#             {'range': f'F{proxima}', 'values': [[dados['endereco']]]},
#             {'range': f'G{proxima}', 'values': [[data_cadastro]]},
#             {'range': f'H{proxima}', 'values': [[dados['tipo_cliente']]]},
#             {'range': f'I{proxima}', 'values': [[dados['observacao']]]}
#         ])

#         return jsonify({'sucesso': True, 'mensagem': 'Cliente cadastrado com sucesso!'})
#     except Exception as e:
#         return jsonify({'sucesso': False, 'erro': str(e)}), 500

# # Rota para cadastrar produto
# @app.route('/produto', methods=['POST'])
# def cadastrar_produto():
#     try:
#         dados = request.json
#         spreadsheet = conectar_sheets()
#         sheet_produto = spreadsheet.worksheet('PRODUTO')

#         coluna_nome = sheet_produto.col_values(2)
#         proxima = len([x for x in coluna_nome if x.strip() != '']) + 1

#         sheet_produto.batch_update([
#             {'range': f'B{proxima}', 'values': [[dados['produto']]]},
#             {'range': f'C{proxima}', 'values': [[dados['preco_compra']]]},
#             {'range': f'D{proxima}', 'values': [[dados['preco_venda']]]}
#         ])

#         import time
#         time.sleep(1)
#         id_produto = sheet_produto.cell(proxima, 1).value

#         if float(dados.get('quantidade_inicial', 0)) > 0:
#             registrar_movimentacao_estoque(
#                 spreadsheet,
#                 id_produto,
#                 dados['produto'],
#                 float(dados['quantidade_inicial']),
#                 'ENTRADA'
#             )

#         return jsonify({'sucesso': True, 'mensagem': 'Produto cadastrado com sucesso!'})
#     except Exception as e:
#         return jsonify({'sucesso': False, 'erro': str(e)}), 500

# # Rota para entrada de estoque
# @app.route('/estoque/entrada', methods=['POST'])
# def entrada_estoque():
#     try:
#         dados = request.json
#         spreadsheet = conectar_sheets()

#         quantidade = float(dados['quantidade'])

#         registrar_movimentacao_estoque(
#             spreadsheet,
#             dados['id_produto'],
#             dados['produto'],
#             quantidade,
#             'ENTRADA'
#         )

#         return jsonify({'sucesso': True, 'mensagem': 'Entrada de estoque registrada com sucesso!'})
#     except Exception as e:
#         return jsonify({'sucesso': False, 'erro': str(e)}), 500

# # Rota para consultar estoque atual
# @app.route('/estoque', methods=['GET'])
# def consultar_estoque():
#     try:
#         spreadsheet = conectar_sheets()
#         sheet_estoque = spreadsheet.worksheet('ESTOQUE')
#         sheet_produto = spreadsheet.worksheet('PRODUTO')

#         produtos = sheet_produto.get_all_records()
#         movimentacoes = sheet_estoque.get_all_records()

#         estoque = []
#         for p in produtos:
#             if not p['PRODUTO']:
#                 continue
#             nome = p['PRODUTO']
#             entradas = sum(float(m['QUANTIDADE']) for m in movimentacoes if m['PRODUTO'] == nome and m['MOVIMENTACAO'] == 'ENTRADA')
#             saidas = sum(float(m['QUANTIDADE']) for m in movimentacoes if m['PRODUTO'] == nome and m['MOVIMENTACAO'] == 'SAIDA')
#             saldo = entradas - saidas
#             estoque.append({
#                 'id': p['ID_ITEM'],
#                 'produto': nome,
#                 'entradas': entradas,
#                 'saidas': saidas,
#                 'saldo': saldo
#             })

#         return jsonify({'sucesso': True, 'estoque': estoque})
#     except Exception as e:
#         return jsonify({'sucesso': False, 'erro': str(e)}), 500

# if __name__ == '__main__':
#     app.run(debug=True, port=5000)
#----------------------------------------------------------------------------

from flask import Flask, request, jsonify
from flask_cors import CORS
import gspread
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

def conectar_sheets():
    creds = Credentials.from_service_account_file('credentials.json', scopes=SCOPES)
    client = gspread.authorize(creds)
    spreadsheet = client.open_by_key(os.getenv('SPREADSHEET_ID'))
    return spreadsheet

def proxima_linha_vazia(sheet):
    coluna_id = sheet.col_values(1)
    for i in range(len(coluna_id) - 1, 0, -1):
        if coluna_id[i].strip() != '':
            return i + 2
    return 2

def registrar_movimentacao_estoque(spreadsheet, id_produto, produto, quantidade, tipo):
    sheet_estoque = spreadsheet.worksheet('ESTOQUE')
    coluna_id = sheet_estoque.col_values(1)
    proxima = len([x for x in coluna_id if x.strip() != '']) + 1
    data_atual = datetime.now().strftime('%Y-%m-%d')
    sheet_estoque.batch_update([
        {'range': f'A{proxima}', 'values': [[id_produto]]},
        {'range': f'B{proxima}', 'values': [[produto]]},
        {'range': f'C{proxima}', 'values': [[tipo]]},
        {'range': f'D{proxima}', 'values': [[quantidade]]},
        {'range': f'E{proxima}', 'values': [[data_atual]]}
    ])

# Rotas para servir os HTMLs
@app.route('/')
def index():
    return app.send_static_file('menu.html')

@app.route('/menu')
def menu():
    return app.send_static_file('menu.html')

@app.route('/vendas')
def vendas():
    return app.send_static_file('index.html')

@app.route('/clientes')
def clientes():
    return app.send_static_file('clientes.html')

@app.route('/cadastro-produto')
def produtos_page():
    return app.send_static_file('produtos.html')

@app.route('/cadastro-estoque')
def estoque_page():
    return app.send_static_file('estoque.html')

# Rota API para buscar produtos
@app.route('/produtos', methods=['GET'])
def get_produtos():
    try:
        spreadsheet = conectar_sheets()
        sheet = spreadsheet.worksheet('PRODUTO')
        dados = sheet.get_all_records()
        produtos = [
            {
                'id': p['ID_ITEM'],
                'nome': p['PRODUTO'],
                'preco': str(p['PRECO_VENDA']).replace('R$', '').replace('.', '').replace(',', '.').strip()
            }
            for p in dados if p['PRODUTO']
        ]
        return jsonify({'sucesso': True, 'produtos': produtos})
    except Exception as e:
        return jsonify({'sucesso': False, 'erro': str(e)}), 500

# Rota API para buscar clientes
@app.route('/api/clientes', methods=['GET'])
def get_clientes():
    try:
        spreadsheet = conectar_sheets()
        sheet = spreadsheet.worksheet('CLIENTE')
        dados = sheet.get_all_records()
        clientes = [
            {
                'id': c['ID_CLIENTE'],
                'nome': c['NOME_CLIENTE'],
                'telefone': c['TELEFONE'],
                'tipo': c['TIPO_CLIENTE']
            }
            for c in dados if c['NOME_CLIENTE']
        ]
        return jsonify({'sucesso': True, 'clientes': clientes})
    except Exception as e:
        return jsonify({'sucesso': False, 'erro': str(e)}), 500

# Rota para registrar venda
@app.route('/venda', methods=['POST'])
def registrar_venda():
    try:
        dados = request.json
        spreadsheet = conectar_sheets()
        sheet_vendas = spreadsheet.worksheet('VENDAS')

        quantidade = float(dados['quantidade'])
        preco_unitario = float(dados['preco_unitario'])

        proxima = proxima_linha_vazia(sheet_vendas)

        sheet_vendas.batch_update([
            {'range': f'C{proxima}', 'values': [[dados['produto']]]},
            {'range': f'D{proxima}', 'values': [[quantidade]]},
            {'range': f'F{proxima}', 'values': [[preco_unitario]]},
            {'range': f'H{proxima}', 'values': [[dados['data_venda']]]},
            {'range': f'I{proxima}', 'values': [[dados['cliente']]]},
            {'range': f'J{proxima}', 'values': [[dados['status_pagamento']]]},
            {'range': f'K{proxima}', 'values': [[dados['condicao']]]}
        ])

        registrar_movimentacao_estoque(
            spreadsheet,
            dados['id_produto'],
            dados['produto'],
            quantidade,
            'SAIDA'
        )

        return jsonify({'sucesso': True, 'mensagem': 'Venda registrada com sucesso!'})
    except Exception as e:
        return jsonify({'sucesso': False, 'erro': str(e)}), 500

# Rota para cadastrar cliente
@app.route('/cliente', methods=['POST'])
def cadastrar_cliente():
    try:
        dados = request.json
        spreadsheet = conectar_sheets()
        sheet_clientes = spreadsheet.worksheet('CLIENTE')

        coluna_nome = sheet_clientes.col_values(2)
        proxima = len([x for x in coluna_nome if x.strip() != '']) + 1

        data_cadastro = datetime.now().strftime('%Y-%m-%d')

        sheet_clientes.batch_update([
            {'range': f'B{proxima}', 'values': [[dados['nome_cliente']]]},
            {'range': f'C{proxima}', 'values': [[dados['cpf']]]},
            {'range': f'D{proxima}', 'values': [[dados['telefone']]]},
            {'range': f'E{proxima}', 'values': [[dados['email']]]},
            {'range': f'F{proxima}', 'values': [[dados['endereco']]]},
            {'range': f'G{proxima}', 'values': [[data_cadastro]]},
            {'range': f'H{proxima}', 'values': [[dados['tipo_cliente']]]},
            {'range': f'I{proxima}', 'values': [[dados['observacao']]]}
        ])

        return jsonify({'sucesso': True, 'mensagem': 'Cliente cadastrado com sucesso!'})
    except Exception as e:
        return jsonify({'sucesso': False, 'erro': str(e)}), 500

# Rota para cadastrar produto
@app.route('/produto', methods=['POST'])
def cadastrar_produto():
    try:
        dados = request.json
        spreadsheet = conectar_sheets()
        sheet_produto = spreadsheet.worksheet('PRODUTO')

        coluna_nome = sheet_produto.col_values(2)
        proxima = len([x for x in coluna_nome if x.strip() != '']) + 1

        sheet_produto.batch_update([
            {'range': f'B{proxima}', 'values': [[dados['produto']]]},
            {'range': f'C{proxima}', 'values': [[dados['preco_compra']]]},
            {'range': f'D{proxima}', 'values': [[dados['preco_venda']]]}
        ])

        import time
        time.sleep(1)
        id_produto = sheet_produto.cell(proxima, 1).value

        if float(dados.get('quantidade_inicial', 0)) > 0:
            registrar_movimentacao_estoque(
                spreadsheet,
                id_produto,
                dados['produto'],
                float(dados['quantidade_inicial']),
                'ENTRADA'
            )

        return jsonify({'sucesso': True, 'mensagem': 'Produto cadastrado com sucesso!'})
    except Exception as e:
        return jsonify({'sucesso': False, 'erro': str(e)}), 500

# Rota para entrada de estoque
@app.route('/estoque/entrada', methods=['POST'])
def entrada_estoque():
    try:
        dados = request.json
        spreadsheet = conectar_sheets()

        quantidade = float(dados['quantidade'])

        registrar_movimentacao_estoque(
            spreadsheet,
            dados['id_produto'],
            dados['produto'],
            quantidade,
            'ENTRADA'
        )

        return jsonify({'sucesso': True, 'mensagem': 'Entrada de estoque registrada com sucesso!'})
    except Exception as e:
        return jsonify({'sucesso': False, 'erro': str(e)}), 500

# Rota para consultar estoque atual
@app.route('/estoque', methods=['GET'])
def consultar_estoque():
    try:
        spreadsheet = conectar_sheets()
        sheet_estoque = spreadsheet.worksheet('ESTOQUE')
        sheet_produto = spreadsheet.worksheet('PRODUTO')

        produtos = sheet_produto.get_all_records()
        movimentacoes = sheet_estoque.get_all_records()

        estoque = []
        for p in produtos:
            if not p['PRODUTO']:
                continue
            nome = p['PRODUTO']
            entradas = sum(float(m['QUANTIDADE']) for m in movimentacoes if m['PRODUTO'] == nome and m['MOVIMENTACAO'] == 'ENTRADA')
            saidas = sum(float(m['QUANTIDADE']) for m in movimentacoes if m['PRODUTO'] == nome and m['MOVIMENTACAO'] == 'SAIDA')
            saldo = entradas - saidas
            estoque.append({
                'id': p['ID_ITEM'],
                'produto': nome,
                'entradas': entradas,
                'saidas': saidas,
                'saldo': saldo
            })

        return jsonify({'sucesso': True, 'estoque': estoque})
    except Exception as e:
        return jsonify({'sucesso': False, 'erro': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)