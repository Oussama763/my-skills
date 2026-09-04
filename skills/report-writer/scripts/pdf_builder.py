import os
import subprocess
import sys

def compile_tex_to_pdf(tex_filepath):
    if not os.path.exists(tex_filepath):
        print(f"Error: {tex_filepath} not found.")
        sys.exit(1)

    output_dir = os.path.dirname(tex_filepath) or "."

    # Execute pdflatex command in non-interactive batch mode
    cmd = [
        "pdflatex",
        "-interaction=nonstopmode",
        f"-output-directory={output_dir}",
        tex_filepath
    ]

    # Run twice to resolve references and page numbers accurately
    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    pdf_filepath = os.path.splitext(tex_filepath)[0] + ".pdf"
    if result.returncode == 0 and os.path.exists(pdf_filepath):
        print(f"Successfully compiled: {pdf_filepath}")
        return pdf_filepath
    else:
        print("PDF compilation failed. Check the .log file for details.")
        return None

if __name__ == "__main__":
    if len(sys.argv) > 1:
        compile_tex_to_pdf(sys.argv[1])
    else:
        print("Usage: python build_pdf.py path/to/document.tex")