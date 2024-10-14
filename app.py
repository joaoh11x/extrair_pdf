import os
from flask import Flask, request, render_template, jsonify
import pdfplumber

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def upload_form():
    return render_template('upload.html')

@app.route('/', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'nao enviou nada'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'nao selecionou nada'})
    
    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        extracted_text = extract_domains(file_path)
        
        return jsonify({'extracted_text': extracted_text})

def extract_domains(file_path):
    result = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            table = page.extract_table()
            if table:
                for row in table:
                    novos_dominios = row[2]  # índice da coluna que contém os dados
                    if novos_dominios:
                        result += novos_dominios + "\n"
    
    linhas = result.splitlines()  
    if len(linhas) >= 2:  
        del linhas[0:2] 
    return "\n".join(linhas)

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
