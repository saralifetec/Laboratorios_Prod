from copy import deepcopy
from pathlib import Path
import re
from PIL import Image
import tempfile
import unicodedata
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx import Document
from flask import Blueprint, current_app, jsonify, request, send_file
from docx.shared import Cm

from app.models import Ensaio, Testes

relatorios_bp = Blueprint('relatorios', __name__)

def prepare_image_for_report(original_path, max_px=1000):
    img = Image.open(original_path)
    img.thumbnail((max_px, max_px))  # mantém proporção

    tmp_dir = Path(tempfile.gettempdir()) / "report_images"
    tmp_dir.mkdir(exist_ok=True)

    tmp_path = tmp_dir / original_path.name
    img.save(tmp_path, quality=85)

    return tmp_path

@relatorios_bp.route('/relatorio_fotos', methods=['POST'])
def relatorio_fotos():

    # =================================================
    # TEMPLATE
    # =================================================
    TEMPLATE_PATH = Path(
        r"W:\DEPARTMENTS\LAB\PROCESS\01 QUALITY\01.01 DOCUMENTATION"
        r"\01.01.05 TEMPLATES\ALL\REPORTS\Reports_Fotos_2.docx"
    )

    if not TEMPLATE_PATH.exists():
        return jsonify({"error_key": "msg.template_reports_fotos_nao_encontrado"}), 500

    # =================================================
    # FUNÇÕES AUXILIARES
    # =================================================
    def norm(text: str) -> str:
        """Normalização tolerante para comparar nomes de pastas"""
        if not text:
            return ""
        text = unicodedata.normalize("NFKC", text)
        text = text.replace("&nbsp;", " ")
        text = text.replace("\u00A0", " ")
        text = re.sub(r"\s+", " ", text)
        return text.strip().upper()

    def find_child_dir(parent: Path, expected: str) -> Path | None:
        expected_norm = norm(expected)
        for d in parent.iterdir():
            if d.is_dir() and norm(d.name) == expected_norm:
                return d
        return None

    def extract_peca_label(folder_name: str) -> str:
        m = re.search(r"(P\d{2,3}|V\d+)$", folder_name, re.IGNORECASE)
        return m.group(1) if m else folder_name

    def insert_table_after_paragraph(paragraph, table):
        new_tbl = deepcopy(table._tbl)
        paragraph._p.addnext(new_tbl)
        return new_tbl

    # =================================================
    # INPUT
    # =================================================
    ensaio_numero = request.json.get("ensaio")
    if not ensaio_numero:
        return jsonify({"error_key": "msg.preencha_ensaio"}), 400

    ensaio = Ensaio.query.filter_by(ensaio=ensaio_numero).first()
    if not ensaio:
        return jsonify({"error_key": "msg.ensaio_nao_encontrado"}), 404

    # =================================================
    # RESOLVER BASE PATH REAL (FS = VERDADE)
    # =================================================
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

    for nivel, esperado in [
        ("Laboratório", ensaio.laboratorio.laboratorio),
        ("Ano", str(ensaio.datapedido.year)),
        ("Fase", ensaio.corecustomer),
        ("Cliente", cliente_nome),
        ("Projeto", projeto_folder),
        ("Ensaio", ensaio.ensaio),
    ]:
        nxt = find_child_dir(base, esperado)
        if not nxt:
            current_app.logger.error(
                f"[Relatório Fotos] Pasta não encontrada ({nivel}): '{esperado}' em '{base}'"
            )
            return jsonify({"error_key": "msg.pasta_nao_encontrada","params": { "nivel": nivel }}), 400
        base = nxt

    base_path = base
    current_app.logger.info(f"[Relatório Fotos] BASE_PATH = {base_path}")

    # =================================================
    # BEFORE TEST E PEÇAS
    # =================================================
    before_test_base = base_path / "BEFORE TEST"
    if not before_test_base.exists():
        return jsonify({"error_key": "msg.pasta_before_test_nao_existe"}), 400

    pecas = sorted(p for p in before_test_base.iterdir() if p.is_dir())
    if not pecas:
        return jsonify({"error_key": "msg.nao_existem_pecas"}), 400

    # =================================================
    # TESTES VÁLIDOS
    # =================================================
    testes = Testes.query.filter_by(ensaio_id=ensaio.id).all()
    testes_validos = [
        t for t in sorted(testes, key=lambda x: x.ordem or 0)
        if t.teste and t.teste.criarpasta]
    

    # =================================================
    # DOCUMENTO WORD (TEMPLATE)
    # =================================================
    doc = Document(TEMPLATE_PATH)
    template_table = doc.tables[0]

    # remover todos os parágrafos iniciais do template
    for para in doc.paragraphs:
        p = para._element
        p.getparent().remove(p)


    previous_after_test_path = None
    last_paragraph = doc.add_paragraph()

    # =================================================
    # GERAÇÃO DO DOCUMENTO
    # =================================================
    for idx, teste in enumerate(testes_validos):

        

        # --- TÍTULO 
        last_paragraph = doc.add_paragraph(teste.teste.teste.upper())
        last_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        last_paragraph = doc.add_paragraph("")

        # --- Pasta real do teste (COM número)
        numero_pasta = idx + 1
        nome_pasta_teste = f"{numero_pasta} - {teste.teste.teste.upper()}"
        pasta_teste = find_child_dir(base_path, nome_pasta_teste)
        

        teste_after_base = (
            pasta_teste / "AFTER TEST"
            if pasta_teste and (pasta_teste / "AFTER TEST").exists()
            else None
        )
        

        for peca in pecas:
            label_peca = extract_peca_label(peca.name)

            # BEFORE
            if previous_after_test_path is None:
                before_imgs = sorted(
                    (before_test_base / peca.name).glob("*.*")
                )[:3]
            else:
                before_imgs = sorted(
                    (previous_after_test_path / peca.name).glob("*.*")
                )[:3]

            
            # AFTER (sempre do teste atual)
            after_imgs = []
            if teste_after_base:
                after_piece = teste_after_base / peca.name
                if after_piece.exists():
                    after_imgs = sorted(after_piece.glob("*.*"))[:3]
                    

            # Inserir tabela
            insert_table_after_paragraph(last_paragraph, template_table)
            tbl = doc.tables[-1]

            cell_left = tbl.rows[0].cells[0]
            cell_right = tbl.rows[0].cells[1]

            cell_left.text = f"{label_peca} Before Test"
            cell_left.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

            cell_right.text = f"{label_peca} After Test"
            cell_right.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

            for i in range(3):

                if i < len(before_imgs):
                    img_before = prepare_image_for_report(before_imgs[i])
                    tbl.rows[i+1].cells[0].paragraphs[0] \
                        .add_run().add_picture(str(img_before), width=Cm(8))

                if i < len(after_imgs):
                    img_after = prepare_image_for_report(after_imgs[i])
                    tbl.rows[i+1].cells[1].paragraphs[0] \
                        .add_run().add_picture(str(img_after), width=Cm(8))


            doc.add_page_break()
            last_paragraph = doc.paragraphs[-1]


        # --- atualizar AFTER para o próximo teste
        previous_after_test_path = teste_after_base

    # =================================================
    # REMOVER TABELA MODELO INICIAL
    # =================================================
    doc._body._body.remove(template_table._tbl)

    # =================================================
    # GUARDAR NA PASTA DO ENSAIO
    # =================================================
    #output_path = base_path / f"Relatorio_Fotos_{ensaio_numero}.docx"
    base_path = Path("C:/temp")
    output_path = base_path / f"Relatorio_Fotos_{ensaio_numero}.docx"

    doc.save(output_path)

    return send_file(
        output_path,
        as_attachment=True,
        download_name=f"Relatorio_Fotos_{ensaio_numero}.docx"
    )



@relatorios_bp.route('/relatorio_fotos_por_teste', methods=['POST'])
def relatorio_fotos_por_teste():

    TEMPLATE_PATH = Path(
        r"W:\DEPARTMENTS\LAB\PROCESS\01 QUALITY\01.01 DOCUMENTATION"
        r"\01.01.05 TEMPLATES\ALL\REPORTS\Reports_Fotos_2.docx"
    )

    if not TEMPLATE_PATH.exists():
        return jsonify({"error_key": "msg.template_reports_fotos_nao_encontrado"}), 500

    data = request.get_json()
    ensaio_numero = data.get("ensaio")

    if not ensaio_numero:
        return jsonify({"error_key": "msg.preencha_ensaio"}), 400

    ensaio = Ensaio.query.filter_by(ensaio=ensaio_numero).first()
    if not ensaio:
        return jsonify({"error_key": "msg.ensaio_nao_encontrado"}), 404

    base = Path(ensaio.laboratorio.pastatestes)

    def norm(text):
        text = unicodedata.normalize("NFKC", text)
        text = text.replace("&nbsp;", " ").replace("\u00A0", " ")
        return re.sub(r"\s+", " ", text).strip().upper()

    def find_child_dir(parent, expected):
        for d in parent.iterdir():
            if d.is_dir() and norm(d.name) == norm(expected):
                return d
        return None

    # construir base_path
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

    for nivel, esperado in [
        ("Laboratório", ensaio.laboratorio.laboratorio),
        ("Ano", str(ensaio.datapedido.year)),
        ("Fase", ensaio.corecustomer),
        ("Cliente", cliente_nome),
        ("Projeto", projeto_folder), 
        ("Ensaio", ensaio.ensaio),
    ]:
        nxt = find_child_dir(base, esperado)
        if not nxt:
            return jsonify({"error_key": "msg.pasta_nao_encontrada"}), 400
        base = nxt

    base_path = base
    before_test_base = base_path / "BEFORE TEST"

    pecas = sorted(p for p in before_test_base.iterdir() if p.is_dir())

    testes = Testes.query.filter_by(ensaio_id=ensaio.id).all()
    testes_validos = [
        t for t in sorted(testes, key=lambda x: x.ordem or 0)
        if t.teste and t.teste.criarpasta
    ]

    # pasta de saída
    output_dir = Path("C:/temp")
    output_dir.mkdir(exist_ok=True)

    previous_after_test_path = None

    for idx, teste in enumerate(testes_validos):

        doc = Document(TEMPLATE_PATH)
        template_table = doc.tables[0]
        last_paragraph = doc.paragraphs[-1]

        # remover todos os parágrafos iniciais do template
        for para in doc.paragraphs:
            p = para._element
            p.getparent().remove(p)


        # Título
        last_paragraph = doc.add_paragraph(teste.teste.teste.upper())
        last_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        last_paragraph = doc.add_paragraph("")

        numero_pasta = idx + 1
        nome_pasta_teste = f"{numero_pasta} - {teste.teste.teste.upper()}"

        pasta_teste = find_child_dir(base_path, nome_pasta_teste)

        teste_after_base = (
            pasta_teste / "AFTER TEST"
            if pasta_teste and (pasta_teste / "AFTER TEST").exists()
            else None
        )

        for peca in pecas:

            # BEFORE
            if previous_after_test_path is None:
                before_imgs = sorted((before_test_base / peca.name).glob("*.*"))[:3]
            else:
                before_imgs = sorted((previous_after_test_path / peca.name).glob("*.*"))[:3]

            # AFTER
            after_imgs = []
            if teste_after_base:
                after_piece = teste_after_base / peca.name
                if after_piece.exists():
                    after_imgs = sorted(after_piece.glob("*.*"))[:3]

            # tabela
            new_tbl = deepcopy(template_table._tbl)
            last_paragraph._p.addnext(new_tbl)
            tbl = doc.tables[-1]

            lbl = peca.name

            
            cell_left = tbl.rows[0].cells[0]
            cell_right = tbl.rows[0].cells[1]

            cell_left.text = f"{lbl} Before Test"
            cell_left.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

            cell_right.text = f"{lbl} After Test"
            cell_right.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER


            for i in range(3):
                if i < len(before_imgs):
                    img = prepare_image_for_report(before_imgs[i])
                    tbl.rows[i+1].cells[0].paragraphs[0].add_run().add_picture(str(img), width=Cm(8))

                if i < len(after_imgs):
                    img = prepare_image_for_report(after_imgs[i])
                    tbl.rows[i+1].cells[1].paragraphs[0].add_run().add_picture(str(img), width=Cm(8))

            doc.add_page_break()
            last_paragraph = doc.paragraphs[-1]

        doc._body._body.remove(template_table._tbl)

        nome_clean = teste.teste.teste.upper().replace(" ", "_")
        output_path = output_dir / f"{ensaio_numero}_{numero_pasta}_{nome_clean}.docx"

        doc.save(output_path)

        previous_after_test_path = teste_after_base

    return jsonify({
        "success": True,
        "message_key": "msg.relatorios_criados_sucesso",
        "params": {"path": str(output_dir)}
    })