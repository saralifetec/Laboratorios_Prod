from flask import Blueprint, app, jsonify, request
from gbs3api.exceptions import ApiException, NotFoundException
from services.gbs_service import find_project, find_test_series_details, find_test_step_details

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


#teste - apagar
@gbs_bp.route("/teste_project")
def teste_project():

    resultado = find_project("TAVA123456")

    return str(resultado)
