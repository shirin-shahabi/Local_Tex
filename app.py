#!/usr/bin/env python3
"""
Offline LaTeX Compiler - Flask Application
A local LaTeX to PDF compiler similar to Overleaf, running entirely offline.
"""

import os
import subprocess
import shutil
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Directories
TEX_DIR = Path('tex_files')
PDF_DIR = Path('pdf_output')
TEX_DIR.mkdir(exist_ok=True)
PDF_DIR.mkdir(exist_ok=True)

# LaTeX engines
LATEX_ENGINES = {
    'pdflatex': 'pdflatex',
    'xelatex': 'xelatex',
    'lualatex': 'lualatex'
}


def find_latex_engine(engine_name='pdflatex'):
    """Find LaTeX engine in PATH"""
    engine = LATEX_ENGINES.get(engine_name, 'pdflatex')
    
    # Check common locations
    common_paths = [
        '/Library/TeX/texbin',
        '/usr/local/texlive/2024/bin/universal-darwin',
        '/usr/local/texlive/2023/bin/universal-darwin',
    ]
    
    for path in common_paths:
        full_path = os.path.join(path, engine)
        if os.path.exists(full_path):
            return full_path
    
    # Try system PATH
    which_result = shutil.which(engine)
    if which_result:
        return which_result
    
    return None


@app.route('/')
def index():
    """Main editor interface"""
    return render_template('index.html')


@app.route('/api/files', methods=['GET'])
def list_files():
    """List all .tex files"""
    files = [f.name for f in TEX_DIR.glob('*.tex')]
    return jsonify({'files': sorted(files)})


@app.route('/api/file/<filename>', methods=['GET'])
def get_file(filename):
    """Get .tex file content"""
    filepath = TEX_DIR / secure_filename(filename)
    if filepath.exists() and filepath.suffix == '.tex':
        with open(filepath, 'r', encoding='utf-8') as f:
            return jsonify({'content': f.read()})
    return jsonify({'error': 'File not found'}), 404


@app.route('/api/file', methods=['POST'])
def save_file():
    """Save/create .tex file"""
    data = request.json
    filename = secure_filename(data.get('filename', 'document.tex'))
    content = data.get('content', '')
    
    if not filename.endswith('.tex'):
        filename += '.tex'
    
    filepath = TEX_DIR / filename
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return jsonify({'message': 'File saved', 'filename': filename})


@app.route('/api/compile', methods=['POST'])
def compile_latex():
    """Compile LaTeX to PDF"""
    data = request.json
    filename = secure_filename(data.get('filename', 'document.tex'))
    engine_name = data.get('engine', 'pdflatex')
    
    if not filename.endswith('.tex'):
        filename += '.tex'
    
    tex_file = TEX_DIR / filename
    if not tex_file.exists():
        return jsonify({'error': 'File not found'}), 404
    
    # Find LaTeX engine
    latex_engine = find_latex_engine(engine_name)
    if not latex_engine:
        return jsonify({
            'error': 'LaTeX engine not found',
            'message': f'Please install LaTeX. {engine_name} not found in PATH.'
        }), 500
    
    # Compile
    pdf_name = filename.replace('.tex', '.pdf')
    pdf_file = PDF_DIR / pdf_name
    
    try:
        # Change to tex_files directory for compilation
        original_dir = os.getcwd()
        os.chdir(TEX_DIR)
        
        # Run LaTeX compilation
        cmd = [
            latex_engine,
            '-interaction=nonstopmode',
            '-output-directory=' + str(PDF_DIR.absolute()),
            filename
        ]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        os.chdir(original_dir)
        
        if result.returncode != 0:
            return jsonify({
                'error': 'Compilation failed',
                'output': result.stderr
            }), 500
        
        if pdf_file.exists():
            return jsonify({
                'success': True,
                'pdf': pdf_name,
                'message': 'Compilation successful'
            })
        else:
            return jsonify({
                'error': 'PDF not generated',
                'output': result.stdout
            }), 500
            
    except subprocess.TimeoutExpired:
        return jsonify({'error': 'Compilation timeout'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/pdf/<filename>', methods=['GET'])
def get_pdf(filename):
    """Get compiled PDF"""
    pdf_file = PDF_DIR / secure_filename(filename)
    if pdf_file.exists() and pdf_file.suffix == '.pdf':
        return send_file(pdf_file, mimetype='application/pdf')
    return jsonify({'error': 'PDF not found'}), 404


@app.route('/api/delete/<filename>', methods=['DELETE'])
def delete_file(filename):
    """Delete .tex file"""
    filepath = TEX_DIR / secure_filename(filename)
    if filepath.exists() and filepath.suffix == '.tex':
        filepath.unlink()
        return jsonify({'message': 'File deleted'})
    return jsonify({'error': 'File not found'}), 404


if __name__ == '__main__':
    # Check if LaTeX is available
    if not find_latex_engine():
        print("Warning: LaTeX engine not found. Please install LaTeX.")
        print("macOS: brew install --cask mactex")
        print("Linux: sudo apt-get install texlive-full")
    
    app.run(host='127.0.0.1', port=5000, debug=True)
