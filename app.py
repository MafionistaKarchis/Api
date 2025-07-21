# app.py
from flask import Flask, request, jsonify
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env (útil para desenvolvimento local)
load_dotenv()

app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def handle_chat():
    try:
        # Pega os dados enviados pelo Roblox
        data = request.get_json()
        player_message = data.get('message')
        # A chave de API é esperada NO PAYLOAD da requisição
        player_api_key = data.get('api_key') 

        # Validação básica: verifica se a mensagem ou a chave de API do jogador estão faltando
        if not player_message or not player_api_key:
            return jsonify({"error": "Mensagem ou chave de API do jogador faltando."}), 400

        # Tenta configurar o Gemini e gerar o conteúdo
        try:
            # Configura o Gemini com a CHAVE DE API DO JOGADOR (recebida no payload)
            genai.configure(api_key=player_api_key)
            
            # --- MUDANÇA AQUI: Usando 'gemini-2.0-flash' ---
            model = genai.GenerativeModel('gemini-2.0-flash') 

            # Chama a API do Gemini para gerar a resposta
            response = model.generate_content(player_message)
            gemini_response_text = response.text

            # Retorna a resposta do Gemini para o Roblox
            return jsonify({"gemini_response": gemini_response_text})

        except Exception as e:
            # Captura erros específicos da chamada à API Gemini
            print(f"Erro ao chamar a API Gemini: {e}")
            # Se for um erro 404 (modelo não encontrado ou acesso negado), retorna 403
            if "404 models/gemini-pro is not found" in str(e) or "404 models/gemini-2.0-flash is not found" in str(e):
                return jsonify({"error": "Erro do Gemini: O modelo não pode ser acessado com sua chave de API. Verifique a chave ou permissões."}), 403
            # Para outros erros da API Gemini, retorna 400
            else:
                return jsonify({"error": f"Erro do Gemini: {str(e)}. Verifique sua chave de API ou tente novamente."}), 400

    except Exception as e:
        # Captura erros gerais do servidor (ex: JSON inválido na requisição do Roblox)
        print(f"Erro interno no servidor: {e}")
        return jsonify({"error": "Erro interno do servidor. Por favor, tente novamente."}), 500
