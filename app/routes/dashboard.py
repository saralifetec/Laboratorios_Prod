from datetime import datetime
import json
from app import db
from flask import Blueprint, render_template, session, jsonify, request
from app.models import DashboardPerfil, User
from app.routes.geral import login_required
from services.horasauto_services import verificar_alerta_horas_auto
from services.dashboard_service import WIDGETS_DASHBOARD, get_default_dashboard_config 

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

@dashboard_bp.route('/dashboardconfig')
@login_required
def dashboardconfig():

    user = User.query.get( session['user_id'] )

    perfis = ( DashboardPerfil.query .order_by( DashboardPerfil.nome ) .all() )

    perfil_selecionado = ( perfis[0] if perfis else None )

    return render_template(
        'dashboardconfig.html',
        user=user,
        perfis=perfis,
        perfil_selecionado=perfil_selecionado,
        widgets=WIDGETS_DASHBOARD
    )

@dashboard_bp.route( '/dashboardconfig/guardar/<int:perfil_id>', methods=['POST'] )
def dashboardconfig_guardar(perfil_id):

    perfil = DashboardPerfil.query.get_or_404(
        perfil_id
    )

    data = request.get_json()

    perfil.configuracao = json.dumps(
        data,
        ensure_ascii=False
    )

    db.session.commit()

    return jsonify({
        'success': True
    })


@dashboard_bp.route( '/dashboardconfig/perfil/<int:perfil_id>' )
def dashboardconfig_perfil( perfil_id ):

    perfil = DashboardPerfil.query.get_or_404( perfil_id )

    try:

        configuracao = (
            json.loads(
                perfil.configuracao
            )
            if perfil.configuracao
            else get_default_dashboard_config()
        )

    except Exception:

        configuracao = (
            get_default_dashboard_config()
        )

    return jsonify({
        'id': perfil.id,
        'nome': perfil.nome,
        'descricao': perfil.descricao,
        'configuracao': configuracao
    })

@dashboard_bp.route( '/dashboardconfig/novo', methods=['POST'] )
def dashboardconfig_novo():

    data = request.get_json()

    perfil = DashboardPerfil(

        nome=data['nome'],

        descricao=data['descricao'],

        configuracao=json.dumps( get_default_dashboard_config() ),

        criado_por=session['user_id']
    )

    db.session.add(perfil)

    db.session.commit()

    return jsonify({
        'success': True,
        'id': perfil.id
    })

@dashboard_bp.route( '/dashboardconfig/utilizadores' )
def dashboardconfig_utilizadores():

    users = ( User.query .filter( User.obsoleto == 0 ) .order_by( User.full_name ) .all() )
    return jsonify([
        {
            'id': u.id,
            'nome': u.full_name,
            'perfil_id': u.dashboard_perfil_id
        }
        for u in users
    ])

@dashboard_bp.route(
    '/dashboardconfig/utilizador/<int:user_id>',
    methods=['POST']
)
def dashboardconfig_utilizador(user_id):

    user = User.query.get_or_404(user_id)

    data = request.get_json()

    perfil_id = data.get(
        'dashboard_perfil_id'
    )

    user.dashboard_perfil_id = (
        int(perfil_id)
        if perfil_id
        else None
    )

    db.session.commit()

    return jsonify({
        'success': True
    })