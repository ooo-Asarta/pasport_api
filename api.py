from flask import Flask, request, jsonify
import requests
import pytesseract
from PIL import Image
from io import BytesIO

app = Flask(__name__)

@app.route('/extract_text', methods=['POST'])
def extract_text():
    try:
        # Получаем URL-адрес изображения из запроса
        url = request.json['url']
        
        # Загружаем изображение с помощью requests
        response = requests.get(url)
        image = Image.open(BytesIO(response.content))
        
        # Применяем OCR для извлечения текста
        extracted_text = pytesseract.image_to_string(image, lang='eng')
        
        # Возвращаем результат в формате JSON
        return jsonify({'text': extracted_text})
    
    except Exception as e:
        # Если произошла ошибка, возвращаем соответствующий статус и сообщение об ошибке
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run()