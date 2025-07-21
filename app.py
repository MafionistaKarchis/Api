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
        player_api_key = data.get('api_key') # Chave de API do jogador

        # Validação básica
        if not player_message or not player_api_key:
            return jsonify({"error": "Mensagem ou chave de API do jogador faltando."}), 400

        # Configura o Gemini com a CHAVE DE API DO JOGADOR
        genai.configure(api_key=player_api_key)
        model = genai.GenerativeModel('gemini-pro')

        # Geração de conteúdo com tratamento de erro básico
        try:
            response = model.generate_content(player_message)
            gemini_response_text = response.text
        except Exception as e:
            print(f"Erro ao chamar a API Gemini: {e}")
            # Retorna um erro amigável se a chave do jogador for inválida ou houver outro problema na API
            return jsonify({"error": "Não foi possível obter resposta do Gemini. Verifique sua chave de API ou tente novamente mais tarde."}), 500

        # Retorna a resposta do Gemini para o Roblox
        return jsonify({"gemini_response": gemini_response_text})

    except Exception as e:
        # Captura erros gerais do servidor
        print(f"Erro interno no servidor: {e}")
        return jsonify({"error": "Erro interno do servidor. Por favor, tente novamente."}), 500
          # Configura o Gemini com a CHAVE DE API DO JOGADOR
        genai.configure(api_key=player_api_key)

        # Mude esta linha para garantir que o modelo correto seja acessado
        # O "gemini-pro" é o nome do modelo. O "generateContent" é o método.
        # A biblioteca geralmente cuida do mapping.
        # O erro 404 sugere que o endpoint para gemini-pro/generateContent não está disponível.
        # Vamos garantir que a biblioteca esteja usando a versão correta.
        # Se você ainda tiver problemas, podemos tentar um ajuste na região do Render.
        model = genai.GenerativeModel('gemini-pro') # Manter assim, pois é o nome do modelo.

        # Geração de conteúdo com tratamento de erro básico
        try:
            # A chamada para generateContent é o que importa
            response = model.generate_content(player_message)
            gemini_response_text = response.text
        except Exception as e:
            # ... (seu tratamento de erro) ...

# O Render vai rodar seu aplicativo. Localmente, você usaria:
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=os.environ.get('PORT', 5000))
