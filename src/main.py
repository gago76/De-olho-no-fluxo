# Importações básicas do sistema e manipulação de dados
import os
import sys
import json
from datetime import datetime

# Configuração do path para possíveis imports de módulos em diretórios pais
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Importações do Flask para criação da aplicação web
from flask import Flask, send_from_directory, request, jsonify

# Configuração inicial da aplicação Flask
app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'  # Chave secreta para sessões (deve ser mais segura em produção)

# Caminho do arquivo para armazenamento simples das localizações
LOCATION_DATA_FILE = os.path.join(os.path.dirname(__file__), 'location_data.txt')

# Endpoint para receber dados de localização via POST
@app.route('/api/location', methods=['POST'])
def receive_location():
    try:
        # Extrai dados JSON da requisição
        data = request.get_json()
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        timestamp = data.get('timestamp')  # Timestamp formatado pelo cliente

        # Validação dos dados recebidos
        if latitude is None or longitude is None or timestamp is None:
            return jsonify({'status': 'error', 'message': 'Dados incompletos'}), 400

        # Armazena os dados no arquivo de texto
        with open(LOCATION_DATA_FILE, 'a') as f:
            f.write(f"{datetime.now().isoformat()} - Lat: {latitude}, Lon: {longitude}, Client Timestamp: {timestamp}\n")
        
        # Log de depuração no servidor
        print(f"Received data: Lat: {latitude}, Lon: {longitude}, Timestamp: {timestamp}")
        return jsonify({'status': 'success', 'message': 'Dados recebidos'}), 200
    
    except Exception as e:
        # Tratamento de erros genéricos
        print(f"Error receiving location: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Rota principal para servir arquivos estáticos e o SPA (Single Page Application)
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    
    # Verificação de segurança do caminho estático
    if static_folder_path is None:
        return "Static folder not configured", 404

    # Serve arquivos estáticos se existirem
    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        # Fallback para index.html (SPA)
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404

# Ponto de entrada principal da aplicação
if __name__ == '__main__':
    # Garante que o arquivo de dados exista
    if not os.path.exists(LOCATION_DATA_FILE):
        with open(LOCATION_DATA_FILE, 'w') as f:
            f.write("Location Data Log\n")
            f.write("--------------------\n")
    
    # Inicia o servidor Flask
    app.run(host='0.0.0.0', port=5000, debug=True)  # Debug=True só para ambiente de desenvolvimento