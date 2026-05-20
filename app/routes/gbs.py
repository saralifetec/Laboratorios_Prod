from flask import Blueprint, app, jsonify, request
from gbs3api.exceptions import ApiException, NotFoundException
from services.gbs_service import find_project, get_test_series

gbs_bp = Blueprint('gbs', __name__)


@gbs_bp.route("/gbs/project", methods=["POST"])
def get_project_gbs():

    data = request.get_json()
    function_number = data.get("function_number")

    if not function_number:
        return jsonify({"error": "Parâmetros inválidos"}), 400

    try:
        projeto = find_project(function_number)

        return jsonify({
            "cliente": projeto.get("customer_name")
        })

    except Exception as e:


        return jsonify({
            "error": "Erro ao comunicar com o GBS",
            "detail": str(e)
        }), 502




@gbs_bp.route("/gbs/test-series", methods=["POST"])
def get_test_series_gbs():
    data = request.get_json()

    function_number = data.get("function_number")
    series_number = data.get("series_number")

    if not function_number or not series_number:
        return jsonify({"error": "Parâmetros inválidos"}), 400

    try:
        serie = get_test_series(
            function_number=function_number,
            series_number=series_number,
            include_definition=False
        )

        return jsonify({
            "remark": serie.remark
        })

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
    

