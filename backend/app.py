# from flask import Flask, request, jsonify, send_from_directory
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

# def proxima_linha_vazia(sheet_vendas):
#     coluna_id = sheet_vendas.col_values(1)
#     for i in range(len(coluna_id) - 1, 0, -1):
#         if coluna_id[i].strip() != '':
#             return i + 2
#     return 2

# # Rotas para servir os HTMLs
# @app.route('/')
# def index():
#     return app.send_static_file('index.html')

# @app.route('/clientes')
# def clientes():
#     return app.send_static_file('clientes.html')

# # Rota para buscar produtos
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

# # Rota para buscar o menu
# @app.route('/menu')
# def menu():
#     return app.send_static_file('menu.html')

# @app.route('/vendas')
# def vendas():
#     return app.send_static_file('index.html')


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

# if __name__ == '__main__':
#     app.run(debug=True, port=5000)

#---------------------------------------------------------------------------------

from flask import Flask, request, jsonify, send_from_directory
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

def proxima_linha_vazia(sheet_vendas):
    coluna_id = sheet_vendas.col_values(1)
    for i in range(len(coluna_id) - 1, 0, -1):
        if coluna_id[i].strip() != '':
            return i + 2
    return 2

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

# Rota para buscar produtos
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

if __name__ == '__main__':
    app.run(debug=True, port=5000)