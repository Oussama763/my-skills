import os
import re
import subprocess
from pdf2image import convert_from_path  # Requires: pip install pdf2image pypdf

def audit_pdf_compilation(tex_path):
    output_dir = os.path.dirname(tex_path) or "."
    base_name = os.path.splitext(tex_path)[0]
    pdf_path = f"{base_name}.pdf"
    log_path = f"{base_name}.log"
    
    # 1. Execute pdflatex
    cmd = ["pdflatex", "-interaction=nonstopmode", f"-output-directory={output_dir}", tex_path]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    # 2. Parse Log for Errors & Overflows
    errors, overflow_warnings = [], []
    if os.path.exists(log_path):
        with open(log_path, "r", encoding="utf-8", errors="ignore") as f:
            log_lines = f.readlines()
            for i, line in enumerate(log_lines):
                if line.startswith("!"):
                    errors.append("".join(log_lines[i:i+3]).strip())
                elif "Overfull \\hbox" in line:
                    overflow_warnings.append(line.strip())
                    
    if res.returncode != 0 or errors:
        return {"status": "COMPILATION_FAILED", "errors": errors[:3]}

    # 3. Render PDF Pages to PNG for Visual Verification
    page_images = []
    if os.path.exists(pdf_path):
        images = convert_from_path(pdf_path, dpi=150)
        for i, img in enumerate(images):
            img_path = f"{base_name}_page_{i+1}.png"
            img.save(img_path, "PNG")
            page_images.append(img_path)

    return {
        "status": "COMPILED_WITH_WARNINGS" if overflow_warnings else "SUCCESS",
        "pdf_path": pdf_path,
        "page_count": len(page_images),
        "page_images": page_images,
        "overflow_warnings": overflow_warnings
    }