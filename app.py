from flask import Flask, request, jsonify, send_file, render_template
from PyPDF2 import PdfReader
import pdfplumber
import os
from docx import Document
from werkzeug.utils import secure_filename
import tempfile

app = Flask(__name__, static_url_path='', static_folder='static')
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB max file size
app.config['UPLOAD_FOLDER'] = tempfile.gettempdir()

def convert_pdf_to_word(pdf_path):
    try:
        # Read PDF using PyPDF2
        reader = PdfReader(pdf_path)
        text_content = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
        
        # Create Word document
        doc = Document()
        doc.add_paragraph(text_content)
        
        # Save to temporary file
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'converted.docx')
        doc.save(output_path)
        return output_path, text_content
    except Exception as e:
        return str(e), None

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if not file.filename.lower().endswith('.pdf'):
        return jsonify({'error': 'File must be a PDF'}), 400
    
    try:
        # Save uploaded file
        filename = secure_filename(file.filename)
        pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(pdf_path)
        
        # Convert PDF to Word and get preview text
        output_path, text_content = convert_pdf_to_word(pdf_path)
        
        # Get preview text (first 1000 characters)
        preview_text = text_content[:1000] if text_content else ""
        
        # Clean up the PDF file
        os.remove(pdf_path)
        
        return jsonify({
            'message': 'File converted successfully',
            'preview': preview_text
        })
    except Exception as e:
        # Clean up in case of error
        if os.path.exists(pdf_path):
            os.remove(pdf_path)
        return jsonify({'error': str(e)}), 500

@app.route('/download')
def download_file():
    try:
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'converted.docx')
        return send_file(
            output_path,
            as_attachment=True,
            download_name='converted.docx'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True) 