from datetime import datetime
from flask import Blueprint, render_template, session
from app.models import User
from app.routes.geral import login_required
from services.horasauto_services import verificar_alerta_horas_auto

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
@login_required
def index():
    ano_atual = datetime.now().year
    mes_atual = datetime.now().month

    user = User.query.get(session['user_id'])
    alerta_horas_auto = verificar_alerta_horas_auto(user)

    return render_template(
        'index.html',
        user=user,
        ano_atual=ano_atual,
        mes_atual=mes_atual,
        alerta_horas_auto=alerta_horas_auto
    )