from flask import Flask, request, jsonify
from flask_cors import CORS
import gspread
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuração Google Sheets
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

def conectar_sheets():
    creds = Credentials.from_service_account_file('credentials.json', scopes=SCOPES)
    client = gspread.authorize(creds)
    spreadsheet = client.open_by_key(os.getenv('SPREADSHEET_ID'))
    return spreadsheet

# Rota para buscar produtos
@app.route('/produtos', methods=['GET'])
def get_produtos():
    try:
        spreadsheet = conectar_sheets()
        sheet = spreadsheet.worksheet('PRODUTO')
        dados = sheet.get_all_records()
        produtos = [{'id': p['ID_ITEM'], 'nome': p['PRODUTO'], 'preco': p['PRECO_VENDA']} for p in dados if p['PRODUTO']]
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

        # Pega o próximo ID
        todas_vendas = sheet_vendas.get_all_records()
        proximo_id = len(todas_vendas) + 1

        # Calcula valores
        quantidade = float(dados['quantidade'])
        preco_unitario = float(dados['preco_unitario'])
        preco_compra = float(dados.get('preco_compra', 0))
        valor_total = quantidade * preco_unitario
        lucro = valor_total - (quantidade * preco_compra)

        # Nova linha
        nova_linha = [
            proximo_id,
            dados.get('id_produto', ''),
            dados['produto'],
            quantidade,
            preco_compra,
            preco_unitario,
            valor_total,
            dados['data_venda'],
            dados['cliente'],
            dados['status_pagamento'],
            dados['condicao'],
            lucro
        ]

        sheet_vendas.append_row(nova_linha)
        return jsonify({'sucesso': True, 'mensagem': 'Venda registrada com sucesso!'})
    except Exception as e:
        return jsonify({'sucesso': False, 'erro': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)