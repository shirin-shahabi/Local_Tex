# LaTeX Compilation Template

A clean template for compiling LaTeX documents locally with a web-based interface, similar to Overleaf but running entirely offline.

## Features

- **Local LaTeX Compilation**: Compile `.tex` files to PDF using pdflatex, xelatex, or lualatex
- **Web-based Editor**: Clean, modern interface for editing LaTeX documents
- **File Management**: Create, save, load, and compile `.tex` files
- **PDF Preview**: View compiled PDFs directly in the browser
- **Bibliography Support**: Includes `references.bib` with IEEE citation style
- **Offline Operation**: Works completely offline once LaTeX is installed

## Project Structure

```
.
├── app.py                 # Flask application for LaTeX compilation
├── run.sh                 # Startup script
├── requirements.txt       # Python dependencies
├── main.tex              # Main LaTeX document template
├── references.bib        # Bibliography file
├── truthtensor_whitepaper.sty  # LaTeX style file
├── plots/                # Directory for figures/images
├── templates/            # HTML templates
│   ├── index.html        # Main editor interface
│   └── error.html        # Error page
├── tex_files/            # Directory for .tex files (auto-created)
└── pdf_output/           # Directory for compiled PDFs (auto-created)
```

## Requirements

- Python 3.7+
- A LaTeX distribution:
  - **macOS**: MacTeX (`brew install --cask mactex`)
  - **Linux**: TeX Live (`sudo apt-get install texlive-full`)
  - **Windows**: MiKTeX (download from [miktex.org](https://miktex.org/download))

## Installation

1. **Set up virtual environment**:
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. **Install Python dependencies**:
```bash
pip install -r requirements.txt
```

3. **Verify LaTeX installation**:
```bash
pdflatex --version
```

## Usage

1. **Activate virtual environment** (if not already active):
```bash
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. **Start the server**:
```bash
./run.sh
# Or directly: python app.py
```

3. **Open your browser** and navigate to:
```
http://127.0.0.1:5000
```

4. **Use the interface**:
   - Edit `main.tex` or create new `.tex` files
   - Edit LaTeX code in the editor
   - Click "Compile" to generate PDF
   - View the PDF preview in the right pane
   - Save files using "Save" button or Ctrl+S

## LaTeX Document Structure

The template includes:
- `main.tex`: Main LaTeX document with IEEE citation style
- `references.bib`: Bibliography database
- `truthtensor_whitepaper.sty`: Custom style package
- `plots/`: Directory for figures (include images here)

## API Endpoints

- `GET /` - Main editor interface
- `GET /api/files` - List all .tex files
- `GET /api/file/<filename>` - Get .tex file content
- `POST /api/file` - Save/create .tex file
- `POST /api/compile` - Compile LaTeX to PDF
- `GET /api/pdf/<filename>` - Get compiled PDF
- `DELETE /api/delete/<filename>` - Delete .tex file

## Troubleshooting

**"No LaTeX engine found" error:**
- Make sure LaTeX is installed and available in your PATH
- On macOS, you may need to add `/Library/TeX/texbin` to your PATH
- Restart the terminal after installing LaTeX

**Compilation errors:**
- Check the status bar for error messages
- Review the LaTeX syntax in your document
- Some packages may require additional LaTeX packages to be installed

## Notes

- All `.tex` files are stored in the `tex_files/` directory
- Compiled PDFs are stored in the `pdf_output/` directory
- The application runs on `127.0.0.1:5000` by default
- Maximum file size is 16MB

## License

This template is provided as-is for local use.
