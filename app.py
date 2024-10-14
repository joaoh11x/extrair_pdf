import os
from flask import Flask, request, render_template, send_file
import pdfplumber

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def upload_form():
    return render_template('upload.html')

@app.route('/', methods=['POST'])

#validar se tem arquivo e se nao ta vazio
def upload_file():
    if 'file' not in request.files:
        return 'nao tem nada'
    
    file = request.files['file']
    if file.filename == '':
        return 'nao selecionou nada'
    
    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        extracted_text = extract_domains(file_path)
        
        result_file = os.path.join(app.config['UPLOAD_FOLDER'], 'dominios_bloqueios.txt')
        with open(result_file, 'w') as f:
            f.write(extracted_text)
        
        return send_file(result_file, as_attachment=True)

def extract_domains(file_path):
    result = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            table = page.extract_table()
            if table:
                for row in table:
                    novos_dominios = row[2]  #indice da coluna que contem os dados para bloquear
                    if novos_dominios:
                        result += novos_dominios + "\n"
    return result

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
