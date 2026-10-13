from datetime import datetime

from flask import Blueprint, app, jsonify, request
from app import db
from app.models import Maquina, Projeto, Solicitante, Cliente, Laboratorio, Normas, Templatenormas, Testes, Tipopeca, Fase, Tipotestes
from gbs3api.exceptions import ApiException, NotFoundException
from services.gbs_service import find_test_series_details, find_test_step_details, get_person_gbs
from sqlalchemy import func

gbs_bp = Blueprint('gbs', __name__)


@gbs_bp.route("/gbs/test-series", methods=["POST"])
def get_test_series_gbs():

    data = request.get_json()

    full_series_number = data.get(
        "full_series_number"
    )

    if not full_series_number:

        return jsonify({
            "error": "Parâmetros inválidos"
        }), 400

    try:

        serie = find_test_series_details(
            full_series_number
        )

        return jsonify(serie)


    except NotFoundException:

        return jsonify({
            "error": "A série não existe no GBS"
        }), 404

    except ApiException as e:

        return jsonify({
            "error": "Erro ao comunicar com o GBS",
            "detail": str(e)
        }), 502

    except Exception as e:

        return jsonify({
            "error": "Erro inesperado no servidor",
            "detail": str(e)
        }), 500

@gbs_bp.route("/gbs/test-step-details", methods=["POST"])
def get_test_step_details():

    data = request.get_json()

    test_series_id = data.get(
        "test_series_id"
    )

    if not test_series_id:

        return jsonify({
            "error":
            "Test Series ID em falta"
        }), 400

    try:

        resultado = find_test_step_details(
            test_series_id
        )

        if hasattr(
            resultado,
            "to_dict"
        ):
            resultado = resultado.to_dict()

        return jsonify(
            resultado
        )

    except Exception as e:

        return jsonify({
            "error":
            "Erro ao consultar os passos do ensaio",
            "detail":
            str(e)
        }), 500

def normalizar_texto_projeto(texto):

    if not texto:
        return ""

    return " ".join(
        texto.strip().upper().split()
    )

@gbs_bp.route("/gbs/verificar_projeto", methods=["POST"])
def verificar_projeto():

    data = request.get_json()

    codigo = normalizar_texto_projeto(data.get("codigo"))

    descricao = normalizar_texto_projeto(data.get("descricao"))

    cliente_id = data.get("cliente_id")

    projeto = Projeto.query.filter_by(
        codigo=codigo,
        descricao=descricao,
        cliente_id=cliente_id
    ).first()

    return jsonify({
        "existe": projeto is not None,
        "id": projeto.id if projeto else None,
        "tipopeca_id": projeto.tipopeca_id if projeto else None
    })


@gbs_bp.route("/projetos/criar_gbs", methods=["POST"])
def criar_projeto_gbs():

    data = request.get_json()

    codigo = data.get("codigo")
    descricao = data.get("descricao")

    projeto = Projeto(
        codigo=codigo,
        descricao=descricao,
        cliente_id=int(data["cliente_id"]),
        tipopeca_id=int(data["tipopeca_id"]),
        obsoleto=False
    )

    db.session.add(projeto)
    db.session.commit()

    return jsonify({
        "success": True,
        "id": projeto.id,
        "texto": f"{projeto.codigo} - {projeto.descricao}"
    })

"""
VERIFICAR E CRIAR LABORATÓRIO
"""
@gbs_bp.route("/gbs/verificar_laboratorio", methods=["POST"])
def verificar_laboratorio():

    data = request.get_json()

    laboratorio = data.get("laboratorio")

    if not laboratorio:

        return jsonify({
            "error": "Laboratório não fornecido"
        }), 400

    registo = Laboratorio.query.filter(
        db.func.upper(Laboratorio.laboratorio)
        == laboratorio.upper()
    ).first()

    return jsonify({
        "existe": registo is not None,
        "id": registo.id if registo else None
    })

@gbs_bp.route("/laboratorios/criar_gbs", methods=["POST"])
def criar_laboratorio_gbs():

    data = request.get_json()

    nome = data.get("laboratorio")

    laboratorio = Laboratorio(
        laboratorio=nome,
        pastatestes="",
        obsoleto=False
    )

    db.session.add(laboratorio)
    db.session.commit()

    return jsonify({
        "success": True,
        "id": laboratorio.id,
        "texto": laboratorio.laboratorio
    })
    

"""
VERIFICAR E CRIAR NORMA
"""
@gbs_bp.route("/gbs/verificar_norma", methods=["POST"])
def verificar_norma():

    data = request.get_json()

    norma = data.get("norma")
    laboratorio_id = data.get("laboratorio_id")

    registo = Normas.query.filter_by(
        norma=norma,
        laboratorio_id=laboratorio_id
    ).first()

    return jsonify({
        "existe": registo is not None,
        "id": registo.id if registo else None
    })

@gbs_bp.route("/normas/criar_gbs", methods=["POST"])
def criar_norma_gbs():

    data = request.get_json()

    norma = Normas(
        norma=data["norma"],
        laboratorio_id=data["laboratorio_id"],
        obsoleto=False
    )

    db.session.add(norma)
    db.session.commit()



    return jsonify({
        "success": True,
        "id": norma.id,
        "texto": norma.norma
    })

"""
VERIFICAR E CRIAR SOLICITANTE
"""
@gbs_bp.route("/gbs/verificar_solicitante", methods=["POST"])
def verificar_solicitante():

    data = request.get_json()

    email = data.get("email")

    if not email:
        return jsonify({
            "error": "Email não fornecido"
        }), 400

    solicitante = Solicitante.query.filter_by(
        email=email
    ).first()

    return jsonify({
        "existe": solicitante is not None,
        "id": solicitante.id if solicitante else None
    })

@gbs_bp.route("/solicitantes/criar_gbs", methods=["POST"])
def criar_solicitante_gbs():

    data = request.get_json()
    nome = data.get("nome")
    email = data.get("email")

    solicitante = Solicitante.query.filter_by(
        email=email
    ).first()

    if solicitante:
        return jsonify({
            "success": True,
            "id": solicitante.id,
            "texto": (
                f"{solicitante.nome} - "
                f"{solicitante.email}"
            )
        })

    solicitante = Solicitante(
        nome=nome,
        email=email,
        obsoleto=False
    )

    db.session.add(solicitante)
    db.session.commit()

    return jsonify({
        "success": True,
        "id": solicitante.id,
        "texto": (
            f"{solicitante.nome} - "
            f"{solicitante.email}"
        )
    })

"""
VERIFICAR E CRIAR CLIENTE
"""
@gbs_bp.route("/gbs/verificar_cliente", methods=["POST"])
def verificar_cliente():

    data = request.get_json()

    cliente = data.get("cliente")

    if not cliente:

        return jsonify({
            "error": "Cliente não fornecido"
        }), 400

    registo = Cliente.query.filter(
        Cliente.cliente.ilike(cliente)
    ).first()

    return jsonify({
        "existe": registo is not None,
        "id": registo.id if registo else None
    })

@gbs_bp.route("/clientes/criar_gbs", methods=["POST"])
def criar_cliente_gbs():

    data = request.get_json()

    nome = data.get("cliente")

    novo_cliente = Cliente(
        cliente=nome,
        obsoleto=False
    )

    db.session.add(novo_cliente)
    db.session.commit()

    return jsonify({
        "success": True,
        "id": novo_cliente.id,
        "texto": novo_cliente.cliente
    })


"""
VERIFICAR E CRIAR TIPO DE PEÇA
"""
@gbs_bp.route("/gbs/tipospeca")
def get_tipospeca():

    tipos = Tipopeca.query.filter_by(
        obsoleto=False
    ).order_by(
        Tipopeca.tipopeca
    ).all()

    return jsonify([
        {
            "id": t.id,
            "text": t.tipopeca
        }
        for t in tipos
    ])

@gbs_bp.route("/tipopeca/criar_gbs", methods=["POST"])
def criar_tipopeca_gbs():

    data = request.get_json()

    tipo = data.get("tipopeca")

    novo = Tipopeca(
        tipopeca=tipo,
        obsoleto=False
    )

    db.session.add(novo)
    db.session.commit()

    return jsonify({
        "success": True,
        "id": novo.id,
        "texto": novo.tipopeca
    })

"""
VERIFICAR E CRIAR FASE
"""
@gbs_bp.route("/gbs/verificar_fase", methods=["POST"])
def verificar_fase():

    data = request.get_json()

    fase = data.get("fase")

    registo = Fase.query.filter_by(
        fase=fase
    ).first()

    return jsonify({
        "existe": registo is not None,
        "id": registo.id if registo else None
    })

@gbs_bp.route("/fases/criar_gbs", methods=["POST"])
def criar_fase_gbs():

    data = request.get_json()

    fase = Fase(
        fase=data["fase"],
        sucatearmod=None,
        sucateartrims=None,
        obsoleto=False
    )

    db.session.add(fase)
    db.session.commit()

    return jsonify({
        "success": True,
        "id": fase.id,
        "texto": fase.fase
    })

"""
TEST STEPS
"""
@gbs_bp.route( '/gbs/test-steps/<int:test_series_id>', methods=['GET'] )
def get_test_steps_gbs( test_series_id ):

    try:
        test_steps = find_test_step_details(
            test_series_id
        )

        return jsonify(
            test_steps
        )

    except Exception as e:

        return jsonify({
            'error': str(e)
        }), 500

"""
TIPOS DE TESTES
"""    
@gbs_bp.route( '/gbs/tipotestes/<int:laboratorio_id>', methods=['GET'] )
def obter_tipotestes_laboratorio( laboratorio_id ):

    tipotestes = Tipotestes.query.filter(
        Tipotestes.laboratorio_id == laboratorio_id,
        Tipotestes.obsoleto == False
    ).order_by(
        Tipotestes.teste
    ).all()

    return jsonify([
        {
            'id': t.id,
            'teste': t.teste
        }
        for t in tipotestes
    ])



@gbs_bp.route( '/gbs/maquinas/<int:laboratorio_id>', methods=['GET'] )
def obter_maquinas_laboratorio( laboratorio_id ):
    maquinas = Maquina.query.filter(
        Maquina.laboratorio_id == laboratorio_id,
        Maquina.obsoleto == False
    ).order_by(
        Maquina.codigo
    ).all()

    return jsonify([
        {
            'id': m.id,
            'codigo': m.codigo,
            'nome': m.nome
        }
        for m in maquinas
    ])


def guardar_teststeps_gbs_service( ensaio_id, laboratorio_id, norma_id, linhas ):

    testes_criados = []

    for linha in linhas:

        # TIPO DE TESTE
        tipoteste = Tipotestes.query.filter(
            func.lower(
                Tipotestes.teste
            ) == linha['tipo_teste'].lower(),
            Tipotestes.laboratorio_id
            == laboratorio_id
        ).first()

        if not tipoteste:

            tipoteste = Tipotestes(
                teste= linha['tipo_teste'],
                laboratorio_id= laboratorio_id,
                criarpasta=True,
                mediveis=True,
                obsoleto=False
            )

            db.session.add( tipoteste )

            db.session.flush()

        # TEMPLATE DA NORMA

        if norma_id:

            template = Templatenormas.query.filter(
                Templatenormas.norma_id == norma_id,
                Templatenormas.teste_id == tipoteste.id
            ).first()

            if not template:

                ultima_ordem = db.session.query(
                    func.max(
                        Templatenormas.ordem
                    )
                ).filter(
                    Templatenormas.norma_id == norma_id
                ).scalar()

                template = Templatenormas(
                    norma_id=norma_id,
                    teste_id=tipoteste.id,
                    ordem=(ultima_ordem or 0) + 1,
                    obsoleto=False
                )

                db.session.add(template)

        # MAQUINA
        maquina = None

        if linha['codigo_maquina']:

            maquina = Maquina.query.filter(
                func.lower(
                    Maquina.codigo
                ) == linha['codigo_maquina'].lower(),
                Maquina.laboratorio_id
                == laboratorio_id
            ).first()

            if not maquina:

                maquina = Maquina(
                    codigo= linha['codigo_maquina'],
                    nome= linha['nome_maquina'],
                    laboratorio_id= laboratorio_id,
                    obsoleto=False
                )

                db.session.add( maquina )

                db.session.flush()

        # DATAS
        datainicio = None
        datafim = None

        if linha['datainicio']:

            datainicio = datetime.fromisoformat(
                linha['datainicio']
            )

        if linha['datafim']:

            datafim = datetime.fromisoformat(
                linha['datafim']
            )

        # TESTE
        teste = Testes(
            ensaio_id= ensaio_id,
            teste_id= tipoteste.id,
            ordem= linha['ordem'],
            qtd= linha['qtd'],
            datainicio= datainicio,
            datafim= datafim,
            maquina_id= maquina.id if maquina else None,
            fator=1,
            motivofalhaensaio_id=1
        )

        db.session.add( teste )

        testes_criados.append( teste )

    db.session.commit()

    return {
        'criados':
            len(testes_criados)
    }

@gbs_bp.route( '/gbs/guardar_teststeps', methods=['POST'] )
def guardar_teststeps_gbs():

    try:

        data = request.get_json()

        resultado = guardar_teststeps_gbs_service(
            ensaio_id=data['ensaio_id'],
            laboratorio_id=data['laboratorio_id'],
            norma_id=data['norma_id'],
            linhas=data['linhas']
        )

        return jsonify({
            'success': True,
            'resultado': resultado
        })

    except Exception as e:

        db.session.rollback()

        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

    
"""
Dados dos utilizadores
"""
@gbs_bp.route( '/gbs/person/<username>' )
def obter_pessoa_gbs(username):
    try:
        pessoa = get_person_gbs( username )

        if not pessoa:
            return jsonify({
                'success': False,
                'message': 'Utilizador não encontrado.'
            })

        return jsonify({
            'success': True,
            'username': pessoa['username'],
            'nome': pessoa['nome'],
            'email': pessoa['email']
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

