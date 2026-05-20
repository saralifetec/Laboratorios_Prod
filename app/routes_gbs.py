
from flask import app, jsonify
import app
from app import db
from services.gbs_service import get_gbs_customers
from .models import ClienteGBS


@app.route('/clientes/sync-gbs', methods=['POST'])
def sync_clientes_gbs():
    try:
        clientes_gbs = get_gbs_customers()

        inseridos = 0
        existentes = 0

        for c in clientes_gbs:
            nome = c.name  

            if not nome:
                continue

            cliente_existente = ClienteGBS.query.filter_by(cliente=nome).first()

            if cliente_existente:
                existentes += 1
                continue

            novo = ClienteGBS(
                cliente=nome,
                obsoleto=False
            )

            db.session.add(novo)
            inseridos += 1

        db.session.commit()

        return jsonify({
            "success": True,
            "inseridos": inseridos,
            "ignorados": existentes
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500