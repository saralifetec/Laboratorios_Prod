from pathlib import Path
import re
import unicodedata
from PIL import Image
from pathlib import Path
import tempfile
import csv
import win32com.client

def prepare_image_for_report(original_path, max_px=1000):

    img = Image.open(original_path)
    img.thumbnail((max_px, max_px))

    tmp_dir = Path(tempfile.gettempdir()) / "report_images"
    tmp_dir.mkdir(exist_ok=True)

    tmp_path = tmp_dir / original_path.name
    img.save(tmp_path, quality=85)

    return tmp_path


# =================================================
# NORMALIZAÇÃO
# =================================================
def norm(text: str) -> str:
    if not text:
        return ""
    text = unicodedata.normalize("NFKC", text)
    text = text.replace("&nbsp;", " ")
    text = text.replace("\u00A0", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip().upper()


# =================================================
# ENCONTRAR SUBPASTA
# =================================================
def find_child_dir(parent: Path, expected: str):
    for d in parent.iterdir():
        if d.is_dir() and norm(d.name) == norm(expected):
            return d
    return None


# =================================================
# RESOLVER BASE PATH DO ENSAIO
# =================================================
def resolver_base_path(ensaio):

    base = Path(ensaio.laboratorio.pastatestes)

    cliente_nome = (
        getattr(ensaio.cliente, "cliente", None)
        or getattr(ensaio.cliente, "nome", None)
        or getattr(ensaio.cliente, "designacao", None)
    )

    projeto_desc = (
        getattr(ensaio.projeto, "descricao", None)
        or getattr(ensaio.projeto, "denominacao", None)
        or getattr(ensaio.projeto, "nome", None)
    )

    tipopeca = ensaio.tipopeca.tipopeca if ensaio.tipopeca else ""

    projeto_folder = (
        f"{ensaio.projeto.codigo}_{projeto_desc}_{tipopeca}"
        if tipopeca else f"{ensaio.projeto.codigo}_{projeto_desc}"
    )

    for esperado in [
        ensaio.laboratorio.laboratorio,
        str(ensaio.datapedido.year),
        ensaio.corecustomer,
        cliente_nome,
        projeto_folder,
        ensaio.ensaio,
    ]:
        base = find_child_dir(base, esperado)
        if not base:
            return None

    return base


# =================================================
# OBTER PEÇAS
# =================================================
def obter_pecas(before_test_base):
    return sorted(p for p in before_test_base.iterdir() if p.is_dir())


# =================================================
# LABEL DA PEÇA
# =================================================
def extract_peca_label(nome):
    m = re.search(r"(P\d{2,3}|V\d+)$", nome, re.IGNORECASE)
    return m.group(1) if m else nome


# =================================================
# BEFORE / AFTER IMAGENS
# =================================================
def get_before_after_images(peca, before_base, previous_after, after_base):

    if previous_after is None:
        before = sorted((before_base / peca.name).glob("*.*"))[:3]
    else:
        before = sorted((previous_after / peca.name).glob("*.*"))[:3]

    after = []
    if after_base:
        p = after_base / peca.name
        if p.exists():
            after = sorted(p.glob("*.*"))[:3]

    return before, after

# ================================================
# PASSAR PARA PDF
# ================================================
import pythoncom
import win32com.client

def docx_to_pdf(docx_path, pdf_path):

    pythoncom.CoInitialize()

    try:

        word = win32com.client.Dispatch("Word.Application")
        word.Visible = False

        doc = word.Documents.Open(str(docx_path))

        doc.SaveAs(str(pdf_path), FileFormat=17)

        doc.Close(False)
        word.Quit()

    finally:

        pythoncom.CoUninitialize()

# =======================================
# Nº Peças
import re

def obter_numero_peca(texto):

    match = re.search(r'(\d+)', texto)

    if match:
        return int(match.group(1))

    return 999999


from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls




# ===============================================
# FORMATAÇÃO
# =================================================

from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls
from docx.shared import Pt


def formatar_celula(
    cell,
    header=False,
    bold=False,
    center=False
):

    if header:

        shading = parse_xml(
            f'<w:shd {nsdecls("w")} w:fill="C9C9C9"/>'
        )

        cell._tc.get_or_add_tcPr().append(shading)

    for paragraph in cell.paragraphs:

        if center:

            cell.vertical_alignment = (
                WD_CELL_VERTICAL_ALIGNMENT.CENTER
            )

            for paragraph in cell.paragraphs:

                paragraph.alignment = (
                    WD_ALIGN_PARAGRAPH.CENTER
                )

        for run in paragraph.runs:

            if bold:
                run.bold = True

            run.font.name = "Titillium Web"

            if header:
                run.font.size = Pt(10)
            else:
                run.font.size = Pt(8)



# ===============================================
# RESISTÊNCIAS
# =================================================
import csv


def ler_resistencias(csv_path):

    ignitores = {}

    ignitor_num = 0
    ignitor_atual = None
    tem_cores = False

    with open(csv_path, encoding="latin1") as f:

        reader = csv.reader(f, delimiter=';')

        for row in reader:

            if not row:
                continue

            primeira_coluna = row[0].strip()

            if not primeira_coluna:
                continue

            # cabeçalho
            if primeira_coluna.lower().startswith("probeta"):
                continue

            # linha de cor (PINK, PURPLE, GREEN...)
            if primeira_coluna.isalpha():

                tem_cores = True

                ignitor_num += 1
                ignitor_atual = ignitor_num

                ignitores[ignitor_atual] = {
                    "cor": primeira_coluna.strip().lower(),
                    "pecas": {}
                }

                continue

            # linha de peça
            try:
                int(primeira_coluna)
            except ValueError:
                continue

            peca = primeira_coluna

            try:
                valor = float(
                    row[2].strip().replace(",", ".")
                )
            except Exception:
                continue

            # ficheiros sem secções de cor
            if not tem_cores:

                ignitor_atual = "1"

                if ignitor_atual not in ignitores:

                    ignitores[ignitor_atual] = {
                        "cor": None,
                        "pecas": {}
                    }

            ignitores[ignitor_atual]["pecas"][peca] = round(valor, 2)

    return ignitores