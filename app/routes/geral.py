from calendar import monthrange
from decimal import ROUND_HALF_UP, Decimal
import subprocess
import os
from flask import current_app, flash, render_template, jsonify, request, url_for, redirect, session, render_template_string, send_file
from services.horasauto_services import verificar_alerta_horas_auto
from ..models import Cliente, Codigosg, ConfEmailAuto, ConfHorasAuto, ConsultaLayout, ConsultaLayoutUser, Fase, Horas, Laboratorio, Localizacao, Localizacao_ae, Maquina, Motivosatraso, Normas, Normasdocumentos, Projeto, Solicitante, Templatenormas, Testes, Tipotestes, User, ReferenciaAE, DadosGerais
from ..models import Tipopeca, ConfValidacaoManual, Ensaio, Funcao, Motivosfalhaensaios, Componente, Referencia, MovimentoStock, ConfHorasAuto, ConfHorasAutoCodg, ConfHorasAutoLab, Report, ConfEmailAutoLab, PedidoHorasExtra, Componentesae, Tipovolumeae, Codificacaoae, MovimentoAE
from .. import db
from functools import wraps
from sqlalchemy import Integer, case, extract, or_, func, cast, Date
from datetime import date, datetime, timedelta
from werkzeug.security import check_password_hash, generate_password_hash
import re
import json
from collections import deque, defaultdict, Counter
from pathlib import Path
from io import BytesIO
from openpyxl import Workbook
from shutil import copy2
from sqlalchemy.orm import joinedload, aliased







def login_required(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                return redirect(url_for('login'))
            return f(*args, **kwargs)
        return decorated_function

def _get_current_user():
    user_id = session.get('user_id')
    if not user_id:
        return None
    return User.query.get(user_id)

def _can_edit_consulta(layout, user):
    if not user or not layout:
        return False
    return layout.owner_id == user.id or user.funcao_id == 3

def _can_view_consulta(layout, user):
    if not user or not layout:
        return False

    if layout.owner_id == user.id:
        return True

    if user.funcao_id == 3:
        return True

    vis = (layout.visibilidade or 'private').strip().lower()

    if vis == 'private':
        return False

    if vis == 'all':
        return True

    if vis == 'role_tecnicos':
        return user.funcao_id == 1

    if vis == 'role_coordenadores':
        return user.funcao_id in (2, 3)

    if vis == 'selected_users':
        return any(rel.user_id == user.id for rel in layout.utilizadores_especificos)

    return False




def init_routes(app):

    def _qb_neighbors(table_name):
        meta = QUERY_BUILDER_TABLES.get((table_name or '').strip().lower(), {})
        return list((meta.get('joins') or {}).keys())

    def _qb_find_path(base, target, max_depth=2):
        base = (base or '').strip().lower()
        target = (target or '').strip().lower()

        if not base or not target:
            return None
        if base == target:
            return [base]

        queue = deque([(base, [base])])
        visited = set([base])

        while queue:
            node, path = queue.popleft()
            depth = len(path) - 1
            if depth >= max_depth:
                continue

            for nxt in _qb_neighbors(node):
                if nxt in path:
                    continue
                new_path = path + [nxt]
                if nxt == target:
                    return new_path
                if nxt not in visited:
                    visited.add(nxt)
                    queue.append((nxt, new_path))

        return None

    def _qb_validate_related_tables(base, related_tables, max_depth=2):
        clean = []
        for t in (related_tables or []):
            tt = (t or '').strip().lower()
            if tt:
                clean.append(tt)

        seen = set()
        valid = []
        paths = {}
        invalid = []

        for t in clean:
            if t == base or t in seen:
                continue

            path = _qb_find_path(base, t, max_depth=max_depth)
            if not path:
                invalid.append(t)
                continue

            seen.add(t)
            valid.append(t)
            paths[t] = path

        return valid, paths, invalid

    def _qb_apply_join_paths(q, paths):
        applied_edges = set()
        ordered_paths = sorted(paths.values(), key=len)

        for path in ordered_paths:
            for i in range(len(path) - 1):
                left = path[i]
                right = path[i + 1]
                edge = (left, right)
                if edge in applied_edges:
                    continue

                join_fn = QUERY_BUILDER_TABLES.get(left, {}).get('joins', {}).get(right)
                if not join_fn:
                    continue

                q = join_fn(q)
                applied_edges.add(edge)

        return q

    
    
    FILTER_OPS = {
        'eq', 'neq', 'gt', 'gte', 'lt', 'lte',
        'contains', 'starts_with', 'ends_with',
        'in', 'between',
        'is_null', 'is_not_null'
    }
    
    def _qb_apply_filters(q, filters, allowed_tables):
        if not isinstance(filters, list):
            return q, 'filters inválido'
    
        for f in filters:
            table = (f.get('table') or '').strip().lower()
            field = (f.get('field') or '').strip()
            op = (f.get('op') or 'eq').strip().lower()
            v1 = f.get('value')
            v2 = f.get('value2')
    
            if table not in allowed_tables:
                return None, f'Tabela não permitida no filtro: {table}'
            if op not in FILTER_OPS:
                return None, f'Operador de filtro inválido: {op}'
    
            col = _qb_get_column(table, field)
            if col is None:
                return None, f'Campo inválido no filtro: {table}.{field}'
    
            if op == 'eq':
                q = q.filter(col == v1)
            elif op == 'neq':
                q = q.filter(col != v1)
            elif op == 'gt':
                q = q.filter(col > v1)
            elif op == 'gte':
                q = q.filter(col >= v1)
            elif op == 'lt':
                q = q.filter(col < v1)
            elif op == 'lte':
                q = q.filter(col <= v1)
            elif op == 'contains':
                q = q.filter(col.ilike(f'%{v1}%'))
            elif op == 'starts_with':
                q = q.filter(col.ilike(f'{v1}%'))
            elif op == 'ends_with':
                q = q.filter(col.ilike(f'%{v1}'))
            elif op == 'in':
                vals = v1 if isinstance(v1, list) else []
                q = q.filter(col.in_(vals))
            elif op == 'between':
                if v1 is None or v2 is None:
                    return None, 'Filtro between requer value e value2'
                q = q.filter(col.between(v1, v2))
            elif op == 'is_null':
                q = q.filter(col.is_(None))
            elif op == 'is_not_null':
                q = q.filter(col.is_not(None))
    
        return q, None

####################################################################
#LOGIN
    @app.route('/login')
    def login():
        remote_user = request.environ.get('REMOTE_USER')
        print('REMOTE_USER:', remote_user)  # Debug
        if remote_user:
            username = remote_user.split('\\')[-1]
            print('Username extraído:', username)  # Debug
            user = User.query.filter_by(username=username).first()
            print('User encontrado:', user)  # Debug
            if user:
                session['user_id'] = user.id
                session['funcao_id'] = user.funcao_id
                session['laboratorio_id'] = user.laboratorio_id
                return redirect(url_for('index'))
        return redirect(url_for('manual_login'))

    
        
    
    @app.route('/manual_login', methods=['GET', 'POST'])
    def manual_login():
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            user = User.query.filter(func.lower(User.username) == username.lower()).first()
            if user and check_password_hash(user.password_hash, password):
                session['user_id'] = user.id
                session['funcao_id'] = user.funcao_id
                session['laboratorio_id'] = user.laboratorio_id
                if request.form.get('remember'):
                    session.permanent = True
                else:
                    session.permanent = False
                return redirect(url_for('index'))
            else:
                return render_template('manual_login.html', error='Utilizador ou password incorretos!')
        return render_template('manual_login.html')

    @app.route('/logout')
    def logout():
        session.clear()
        return redirect(url_for('login'))


    ########################################################################
    #PAGES

    @app.route('/')
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

    @app.route('/home')
    @login_required
    def home():

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
    
    @app.route('/plme')
    @login_required
    def plme():
        user = User.query.get(session['user_id'])
        return render_template('plme.html', user=user)

    @app.route('/ae_consultas')
    @login_required
    def ae_consultas():
        user = User.query.get(session['user_id'])
    
        localizacoes_externas = (
            Localizacao_ae.query
            .filter(
                Localizacao_ae.obsoleto == False,
                Localizacao_ae.interno == False
            )
            .order_by(Localizacao_ae.nome.asc())
            .all()
        )
    
        return render_template(
            'ae_consultas.html',
            user=user,
            localizacoes_externas=localizacoes_externas
        )
    
    @app.route('/ae_envios')
    @login_required
    def ae_envios():
        user = User.query.get(session['user_id'])
        localizacoes_rows = (
            Localizacao_ae.query
            .filter(Localizacao_ae.obsoleto == False)
            .order_by(Localizacao_ae.nome.asc())
            .all()
        )
        
        localizacoes = [
            {'id': l.id, 'nome': l.nome}
            for l in localizacoes_rows
        ]
        
        return render_template('ae_envios.html', user=user, localizacoes=localizacoes)

    

    @app.route('/armazem_externo')
    @login_required
    def armazem_externo():
        user = User.query.get(session['user_id'])
        projetos=(
            Projeto.query
            .filter(Projeto.obsoleto == False)
            .order_by(Projeto.codigo.asc())
            .all()
        )
        solicitantes=(
            Solicitante.query
            .filter(Solicitante.obsoleto == False)
            .order_by(Solicitante.nome.asc())
            .all()
        )
        tipopecas=(
            Tipopeca.query
            .filter(Tipopeca.obsoleto == False)
            .order_by(Tipopeca.tipopeca.asc())
            .all()
        )
        tipovolume=(
            Tipovolumeae.query
            .filter(Tipovolumeae.obsoleto == False)
            .order_by(Tipovolumeae.nome.asc())
            .all()
        )
        componentes_ae=(
            Componentesae.query
            .filter(Componentesae.obsoleto == False)
            .order_by(Componentesae.codigo.asc())
            .all()
        )
        codificacao_ae=(
            Codificacaoae.query
            .filter(Codificacaoae.obsoleto == False)
            .order_by(Codificacaoae.nome.asc())
            .all()
        )
        localizacoes=(
            Localizacao_ae.query
            .filter(Localizacao_ae.obsoleto == False)
            .order_by(Localizacao_ae.nome.asc())
            .all()
        )
        laboratorios = (
            Laboratorio.query
            .filter(Laboratorio.obsoleto == False)
            .order_by(Laboratorio.laboratorio.asc())
            .all()
        )
        return render_template('armazemexterno.html', user=user, laboratorios=laboratorios, projetos=projetos, tipopecas=tipopecas, componentes_ae=componentes_ae, tipovolume=tipovolume, solicitantes=solicitantes, localizacoes=localizacoes, codificacao_ae=codificacao_ae)


    
    @app.route('/consultaspersonalizadas')
    @login_required
    def consultaspersonalizadas():
        user = User.query.get(session['user_id'])
        return render_template('consultaspersonalizadas.html', user=user)

    @app.route('/resumo_horas')
    @login_required
    def resumo_horas():
        user = User.query.get(session['user_id'])
        laboratorios = (
            Laboratorio.query
            .filter(Laboratorio.obsoleto == False)
            .order_by(Laboratorio.laboratorio.asc())
            .all()
        )
        return render_template(
            'resumo_horas.html',
            user=user,
            laboratorios=laboratorios,
            ano_atual=datetime.now().year
        )

    @app.route('/construtorconsultas')
    @login_required
    def construtorconsultas():
        user = User.query.get(session['user_id'])
        return render_template('construtor_consultas.html', user=user)
    
    @app.route('/dadosgerais')
    @login_required
    def dadosgerais():
        user = User.query.get(session['user_id'])
        return render_template('dados_gerais.html', user=user)
    
    @app.route('/emailsauto')
    @login_required
    def emailsauto():
        user = User.query.get(session['user_id'])
        return render_template('emails_auto.html', user=user)

    @app.route('/referencias')
    @login_required
    def referencias():
        user = User.query.get(session['user_id'])
        laboratorios=Laboratorio.query.all()
        componentes=Componente.query.all()
        projetos=Projeto.query.all()
        solicitantes=Solicitante.query.all()
        return render_template('referencias.html', user=user, laboratorios=laboratorios, componentes=componentes, projetos=projetos, solicitantes=solicitantes)
    
    @app.route('/ensaioshistorico')
    @login_required
    def ensaioshistorico():
        user = User.query.get(session['user_id'])
        return render_template('ensaios_historico.html', user=user)
    
    @app.route('/horas_maquina')
    @login_required
    def horas_maquina():
        user = User.query.get(session['user_id'])
        ano_atual = datetime.now().year
        mes_atual = datetime.now().month
        return render_template('horas_maquina.html', user=user, ano_atual=ano_atual, mes_atual=mes_atual)
    
    @app.route('/ensaiosconsultas')
    @login_required
    def ensaiosconsultas():
        user = User.query.get(session['user_id'])
        ano_atual = datetime.now().year
        mes_atual = datetime.now().month
        return render_template('ensaiosconsultas.html', user=user, ano_atual=ano_atual, mes_atual=mes_atual)
    

    ################################################################
    ##construtor de consultas

    @app.route('/api/consultas/users', methods=['GET'])
    @login_required
    def consultas_users():
        users = (
            User.query
            .filter(User.obsoleto == False)
            .order_by(User.full_name.asc())
            .all()
        )

        return jsonify([
            {
                'id': u.id,
                'nome': u.full_name,
                'username': u.username,
                'funcao_id': u.funcao_id,
                'laboratorio_id': u.laboratorio_id
            }
            for u in users
        ])

    @app.route('/api/consultas/layouts', methods=['GET'])
    @login_required
    def listar_consultas_layout():
        user = _get_current_user()
        if not user:
            return jsonify({'error': 'Utilizador não autenticado'}), 401

        layouts = (
            ConsultaLayout.query
            .options(joinedload(ConsultaLayout.owner), joinedload(ConsultaLayout.utilizadores_especificos))
            .order_by(ConsultaLayout.nome.asc(), ConsultaLayout.id.desc())
            .all()
        )

        out = []
        for layout in layouts:
            if not _can_view_consulta(layout, user):
                continue

            out.append({
                'id': layout.id,
                'nome': layout.nome,
                'descricao': layout.descricao,
                'tabela_principal': layout.tabela_principal,
                'visibilidade': layout.visibilidade,
                'obsoleto': bool(layout.obsoleto),
                'owner_id': layout.owner_id,
                'owner_nome': layout.owner.full_name if layout.owner else '',
                'can_edit': _can_edit_consulta(layout, user),
                'created_at': layout.created_at.isoformat() if layout.created_at else None,
                'updated_at': layout.updated_at.isoformat() if layout.updated_at else None
            })

        return jsonify(out)

    @app.route('/api/consultas/layouts/<int:layout_id>', methods=['GET'])
    @login_required
    def obter_consulta_layout(layout_id):
        user = _get_current_user()
        if not user:
            return jsonify({'error': 'Utilizador não autenticado'}), 401

        layout = (
            ConsultaLayout.query
            .options(joinedload(ConsultaLayout.utilizadores_especificos))
            .get_or_404(layout_id)
        )

        if not _can_view_consulta(layout, user):
            return jsonify({'error': 'Sem permissão'}), 403

        try:
            definicao = json.loads(layout.definicao_json or '{}')
        except Exception:
            definicao = {}

        return jsonify({
            'id': layout.id,
            'nome': layout.nome,
            'descricao': layout.descricao,
            'tabela_principal': layout.tabela_principal,
            'visibilidade': layout.visibilidade,
            'obsoleto': bool(layout.obsoleto),
            'owner_id': layout.owner_id,
            'selected_user_ids': [rel.user_id for rel in layout.utilizadores_especificos],
            'definicao': definicao
        })
    
    @app.route('/api/consultas/layouts', methods=['POST'])
    @login_required
    def criar_consulta_layout():
        user = _get_current_user()
        if not user:
            return jsonify({'error': 'Utilizador não autenticado'}), 401

        data = request.get_json(silent=True) or {}

        nome = (data.get('nome') or '').strip()
        descricao = (data.get('descricao') or '').strip() or None
        tabela_principal = (data.get('tabela_principal') or '').strip()
        visibilidade = (data.get('visibilidade') or 'private').strip()
        obsoleto = bool(data.get('obsoleto', False))
        definicao = data.get('definicao') or {}
        selected_user_ids = data.get('selected_user_ids') or []

        if not nome:
            return jsonify({'error': 'Nome é obrigatório'}), 400

        if not tabela_principal:
            return jsonify({'error': 'Tabela principal é obrigatória'}), 400

        if visibilidade not in ('private', 'all', 'role_tecnicos', 'role_coordenadores', 'selected_users'):
            return jsonify({'error': 'Visibilidade inválida'}), 400

        novo = ConsultaLayout(
            nome=nome,
            descricao=descricao,
            owner_id=user.id,
            tabela_principal=tabela_principal,
            definicao_json=json.dumps(definicao, ensure_ascii=False),
            visibilidade=visibilidade,
            obsoleto=obsoleto
        )
        db.session.add(novo)
        db.session.flush()

        if visibilidade == 'selected_users':
            users_validos = (
                User.query
                .filter(User.id.in_(selected_user_ids))
                .all()
                if selected_user_ids else []
            )
            for u in users_validos:
                db.session.add(ConsultaLayoutUser(consulta_id=novo.id, user_id=u.id))

        db.session.commit()

        return jsonify({'success': True, 'id': novo.id})

    @app.route('/api/consultas/layouts/<int:layout_id>', methods=['PUT'])
    @login_required
    def atualizar_consulta_layout(layout_id):
        user = _get_current_user()
        if not user:
            return jsonify({'error': 'Utilizador não autenticado'}), 401

        layout = ConsultaLayout.query.get_or_404(layout_id)

        if not _can_edit_consulta(layout, user):
            return jsonify({'error': 'Sem permissão'}), 403

        data = request.get_json(silent=True) or {}

        nome = (data.get('nome') or '').strip()
        descricao = (data.get('descricao') or '').strip() or None
        tabela_principal = (data.get('tabela_principal') or '').strip()
        visibilidade = (data.get('visibilidade') or 'private').strip()
        obsoleto = bool(data.get('obsoleto', False))
        definicao = data.get('definicao') or {}
        selected_user_ids = data.get('selected_user_ids') or []

        if not nome:
            return jsonify({'error': 'Nome é obrigatório'}), 400

        if not tabela_principal:
            return jsonify({'error': 'Tabela principal é obrigatória'}), 400

        if visibilidade not in ('private', 'all', 'role_tecnicos', 'role_coordenadores', 'selected_users'):
            return jsonify({'error': 'Visibilidade inválida'}), 400

        layout.nome = nome
        layout.descricao = descricao
        layout.tabela_principal = tabela_principal
        layout.visibilidade = visibilidade
        layout.obsoleto = obsoleto
        layout.definicao_json = json.dumps(definicao, ensure_ascii=False)

        ConsultaLayoutUser.query.filter_by(consulta_id=layout.id).delete()

        if visibilidade == 'selected_users':
            users_validos = (
                User.query
                .filter(User.id.in_(selected_user_ids))
                .all()
                if selected_user_ids else []
            )
            for u in users_validos:
                db.session.add(ConsultaLayoutUser(consulta_id=layout.id, user_id=u.id))

        db.session.commit()

        return jsonify({'success': True})
    
    @app.route('/api/consultas/layouts/<int:layout_id>', methods=['DELETE'])
    @login_required
    def eliminar_consulta_layout(layout_id):
        user = _get_current_user()
        if not user:
            return jsonify({'error': 'Utilizador não autenticado'}), 401

        layout = ConsultaLayout.query.get_or_404(layout_id)

        if not _can_edit_consulta(layout, user):
            return jsonify({'error': 'Sem permissão'}), 403

        db.session.delete(layout)
        db.session.commit()

        return jsonify({'success': True})

   
    QUERY_BUILDER_TABLES = {
        'ensaios': {
            'label': 'Ensaios',
            'model': Ensaio,
            'joins': {
                'testes': lambda q: q.outerjoin(Testes, Testes.ensaio_id == Ensaio.id),
                'horas': lambda q: q.outerjoin(Horas, Horas.ensaio_id == Ensaio.id),
                'projetos': lambda q: q.outerjoin(Projeto, Ensaio.projeto_id == Projeto.id),
                'laboratorios': lambda q: q.outerjoin(Laboratorio, Ensaio.laboratorio_id == Laboratorio.id),
                'solicitantes': lambda q: q.outerjoin(Solicitante, Ensaio.solicitante_id == Solicitante.id),
                'users': lambda q: q.outerjoin(User, Ensaio.user_id == User.id),
                'normas': lambda q: q.outerjoin(Normas, Ensaio.norma_id == Normas.id),
            }
        },
        'testes': {
            'label': 'Testes',
            'model': Testes,
            'joins': {
                'ensaios': lambda q: q.outerjoin(Ensaio, Testes.ensaio_id == Ensaio.id),
                'tipotestes': lambda q: q.outerjoin(Tipotestes, Testes.teste_id == Tipotestes.id),
                'horas': lambda q: q.outerjoin(Horas, Horas.teste_id == Testes.id),
                'users': lambda q: q.outerjoin(User, Testes.user_id == User.id),
                'maquinas': lambda q: q.outerjoin(Maquina, Testes.maquina_id == Maquina.id),
            }
        },
        'horas': {
            'label': 'Horas',
            'model': Horas,
            'joins': {
                'ensaios': lambda q: q.outerjoin(Ensaio, Horas.ensaio_id == Ensaio.id),
                'testes': lambda q: q.outerjoin(Testes, Horas.teste_id == Testes.id),
                'users': lambda q: q.outerjoin(User, Horas.tecnico_id == User.id),
                'codigosg': lambda q: q.outerjoin(Codigosg, Horas.codigog_id == Codigosg.id),
            }
        },
        'referencias': {
            'label': 'Referências',
            'model': Referencia,
            'joins': {
                'movimentostock': lambda q: q.outerjoin(MovimentoStock, MovimentoStock.referencia_id == Referencia.id),
                'projetos': lambda q: q.outerjoin(Projeto, Referencia.projeto_id == Projeto.id),
                'laboratorios': lambda q: q.outerjoin(Laboratorio, Referencia.laboratorio_id == Laboratorio.id),
                'solicitantes': lambda q: q.outerjoin(Solicitante, Referencia.solicitante_id == Solicitante.id),
            }
        },
        'movimentostock': {
            'label': 'Movimentos de Stock',
            'model': MovimentoStock,
            'joins': {
                'referencias': lambda q: q.outerjoin(Referencia, MovimentoStock.referencia_id == Referencia.id),
                'ensaios': lambda q: q.outerjoin(Ensaio, MovimentoStock.ensaio_id == Ensaio.id),
                'localizacao': lambda q: q.outerjoin(Localizacao, MovimentoStock.localizacao_id == Localizacao.id),
            }
        },
        'users': {
            'label': 'Utilizadores',
            'model': User,
            'exclude_columns': {'password_hash'},
            'joins': {
                'ensaios':            lambda q: q.outerjoin(Ensaio, Ensaio.user_id == User.id),
                'testes':             lambda q: q.outerjoin(Testes, Testes.user_id == User.id),
                'horas':              lambda q: q.outerjoin(Horas, Horas.tecnico_id == User.id),
                'pedidos_horas_extra': lambda q: q.outerjoin(PedidoHorasExtra, PedidoHorasExtra.tecnico_id == User.id),
            }
        },
        'pedidos_horas_extra': {
            'label': 'Pedidos Horas Extra',
            'model': PedidoHorasExtra,
            'joins': {
                'users': lambda q: q.outerjoin(User, PedidoHorasExtra.tecnico_id == User.id),
                'testes': lambda q: q.outerjoin(Testes, PedidoHorasExtra.teste_id == Testes.id),
                'ensaios': lambda q: q.outerjoin(Ensaio, Testes.ensaio_id == Ensaio.id),
                'tipotestes': lambda q: q.outerjoin(Tipotestes, Testes.teste_id == Tipotestes.id),
            }
        }
    }

    TABLE_NAME_TO_MODEL = {
        'ensaios': Ensaio,
        'testes': Testes,
        'horas': Horas,
        'projetos': Projeto,
        'laboratorios': Laboratorio,
        'solicitantes': Solicitante,
        'users': User,
        'normas': Normas,
        'tipotestes': Tipotestes,
        'maquinas': Maquina,
        'referencias': Referencia,
        'movimentostock': MovimentoStock,
        'localizacao': Localizacao,
        'codigosg': Codigosg,
        'pedidos_horas_extra': PedidoHorasExtra,
    }

    AGGREGATES = {'sum', 'count', 'count_distinct', 'avg', 'min', 'max'}

    def _qb_get_model(table_name):
        return TABLE_NAME_TO_MODEL.get((table_name or '').strip().lower())

    def _qb_get_column(table_name, field_name):
        model = _qb_get_model(table_name)
        if not model:
            return None
        return getattr(model, field_name, None)

    def _qb_columns_for_table(table_name):
        model = _qb_get_model(table_name)
        if not model:
            return []
        meta = QUERY_BUILDER_TABLES.get(table_name, {})
        excluded = meta.get('exclude_columns', set())
        cols = []
        for c in model.__table__.columns:
            if c.name in excluded:
                continue
            col_type = c.type.__class__.__name__.lower()
            cols.append({'name': c.name, 'type': col_type})
        return cols

    @app.route('/api/consultas/meta/tabelas', methods=['GET'])
    @login_required
    def consultas_meta_tabelas():
        return jsonify([
            {'key': key, 'label': meta['label']}
            for key, meta in QUERY_BUILDER_TABLES.items()
        ])

    @app.route('/api/consultas/meta/tabelas_relacionadas', methods=['GET'])
    @login_required
    def consultas_meta_tabelas_relacionadas():
        base = (request.args.get('base') or '').strip().lower()
        if base not in QUERY_BUILDER_TABLES:
            return jsonify([])
    
        selecionadas_raw = (request.args.get('selecionadas') or '').strip()
        selecionadas = [s.strip().lower() for s in selecionadas_raw.split(',') if s.strip()]
    
        out_map = {}
    
        # Nível 1: diretas da base
        n1 = _qb_neighbors(base)
        for t in n1:
            out_map[t] = {
                'key': t,
                'label': QUERY_BUILDER_TABLES.get(t, {}).get('label', t),
                'level': 1
            }
    
        # Nível 2: diretas das selecionadas de nível 1
        selecionadas_n1 = [s for s in selecionadas if s in n1]
        out_n2 = {}
        for parent in selecionadas_n1:
            for t in _qb_neighbors(parent):
                if t == base:
                    continue
                if _qb_get_model(t) is None:
                    continue
                if t in out_n2:
                    continue
                out_n2[t] = {
                    'key': t,
                    'label': QUERY_BUILDER_TABLES.get(t, {}).get('label', t),
                    'level': 2,
                    'via': parent
                }
    
        out = list(out_map.values()) + list(out_n2.values())
        out.sort(key=lambda x: (x.get('level', 99), x.get('label', '').lower()))
        return jsonify(out)

    @app.route('/api/consultas/meta/campos', methods=['GET'])
    @login_required
    def consultas_meta_campos():
        base = (request.args.get('base') or '').strip().lower()
        if base not in QUERY_BUILDER_TABLES:
            return jsonify({'error': 'Tabela base inválida'}), 400

        related = (request.args.get('tabelas') or '').strip()
        related_tables = [t.strip().lower() for t in related.split(',') if t.strip()]
        
        related_valid, _, _ = _qb_validate_related_tables(base, related_tables, max_depth=2)
        tables = [base] + related_valid

        tables = [base] + related_tables
        out = []
        for t in tables:
            out.append({
                'table': t,
                'label': QUERY_BUILDER_TABLES.get(t, {}).get('label', t),
                'columns': _qb_columns_for_table(t)
            })

        return jsonify({
            'tables': out,
            'aggregates': ['sum', 'count', 'count_distinct', 'avg', 'min', 'max'],
            'calculated': [
                {'type': 'datediff_days', 'label': 'Dias entre datas'}
            ]
        })

    @app.route('/api/consultas/preview', methods=['POST'])
    @login_required
    def consultas_preview():
        try:
            payload = request.get_json(silent=True) or {}
    
            base = (payload.get('tabela_principal') or '').strip().lower()
            if base not in QUERY_BUILDER_TABLES:
                return jsonify({'error': 'Tabela principal inválida'}), 400
    
            related_tables = payload.get('tabelas_relacionadas') or []
            if not isinstance(related_tables, list):
                return jsonify({'error': 'tabelas_relacionadas deve ser lista'}), 400
    
            related_valid, related_paths, invalid_related = _qb_validate_related_tables(
                base, related_tables, max_depth=2
            )
            if invalid_related:
                return jsonify({'error': f'Tabelas relacionadas inválidas: {", ".join(invalid_related)}'}), 400
    
            allowed_tables = set([base] + related_valid)

            filters = payload.get('filters')
            if filters is None:
                filters = (payload.get('definicao') or {}).get('filters') or []
            q_filters = db.session.query(QUERY_BUILDER_TABLES[base]['model']).select_from(QUERY_BUILDER_TABLES[base]['model'])
            q_filters = _qb_apply_join_paths(q_filters, related_paths)
            q_filters, ferr = _qb_apply_filters(q_filters, filters, allowed_tables)
            if ferr:
                return jsonify({'error': ferr}), 400
    
            campos = payload.get('campos') or []
            if not isinstance(campos, list) or not campos:
                return jsonify({'error': 'Selecione pelo menos um campo'}), 400
    
            calculated_fields = payload.get('calculated_fields') or []
            if not isinstance(calculated_fields, list):
                return jsonify({'error': 'calculated_fields inválido'}), 400
    
            select_exprs = []
            group_exprs = []
            col_names = []
    
            # campos normais
            for idx, c in enumerate(campos):
                table = (c.get('table') or '').strip().lower()
                field = (c.get('field') or '').strip()
                label = (c.get('label') or f'{table}.{field}' or f'col_{idx+1}').strip()
                agg = (c.get('aggregate') or '').strip().lower() or None
                group_by = bool(c.get('group_by', False))
    
                if table not in allowed_tables:
                    return jsonify({'error': f'Tabela não permitida no campo: {table}.{field}'}), 400
    
                col = _qb_get_column(table, field)
                if col is None:
                    return jsonify({'error': f'Campo inválido: {table}.{field}'}), 400
    
                if agg:
                    if agg not in AGGREGATES:
                        return jsonify({'error': f'Agregação inválida: {agg}'}), 400
    
                    if agg == 'sum':
                        expr = func.sum(col).label(label)
                    elif agg == 'count':
                        expr = func.count(col).label(label)
                    elif agg == 'count_distinct':
                        expr = func.count(func.distinct(col)).label(label)
                    elif agg == 'avg':
                        expr = func.avg(col).label(label)
                    elif agg == 'min':
                        expr = func.min(col).label(label)
                    elif agg == 'max':
                        expr = func.max(col).label(label)
                else:
                    expr = col.label(label)
                    if group_by:
                        group_exprs.append(col)
    
                select_exprs.append(expr)
                col_names.append(label)
    
            # campos calculados
            for i, cf in enumerate(calculated_fields):
                ctype = (cf.get('type') or '').strip().lower()
                label = (cf.get('label') or f'calc_{i+1}').strip()
    
                if ctype == 'datediff_days':
                    t1 = (cf.get('start_table') or '').strip().lower()
                    f1 = (cf.get('start_field') or '').strip()
                    t2 = (cf.get('end_table') or '').strip().lower()
                    f2 = (cf.get('end_field') or '').strip()
    
                    if t1 not in allowed_tables or t2 not in allowed_tables:
                        return jsonify({
                            'error': 'Campos calculados só podem usar a tabela principal e relacionadas selecionadas.'
                        }), 400
    
                    cstart = _qb_get_column(t1, f1)
                    cend = _qb_get_column(t2, f2)
                    if cstart is None or cend is None:
                        return jsonify({'error': 'datediff_days com campos inválidos'}), 400
    
                    expr = func.datediff(cend, cstart).label(label)
                    select_exprs.append(expr)
                    col_names.append(label)
                else:
                    return jsonify({'error': f'Campo calculado não suportado: {ctype}'}), 400
    
            if not select_exprs:
                return jsonify({'error': 'Sem colunas para mostrar'}), 400
    
            q = db.session.query(*select_exprs).select_from(QUERY_BUILDER_TABLES[base]['model'])
            
            # IMPORTANTE: só joins por caminho (2 níveis)
            q = _qb_apply_join_paths(q, related_paths)
            
            q, ferr = _qb_apply_filters(q, filters, allowed_tables)
            if ferr:
                return jsonify({'error': ferr}), 400
            
            has_agg = any((c.get('aggregate') or '').strip().lower() in AGGREGATES for c in campos)
            if has_agg and group_exprs:
                q = q.group_by(*group_exprs)
    
            sort = payload.get('sort') or []
            if isinstance(sort, list):
                for s in sort:
                    t = (s.get('table') or '').strip().lower()
                    f = (s.get('field') or '').strip()
                    d = (s.get('direction') or 'asc').strip().lower()
    
                    if t not in allowed_tables:
                        continue
    
                    col = _qb_get_column(t, f)
                    if col is not None:
                        q = q.order_by(col.desc() if d == 'desc' else col.asc())
    
            rows = q.limit(5).all()
    
            data = []
            for r in rows:
                row_dict = {}
                mapping = r._mapping if hasattr(r, '_mapping') else {}
                for col_name in col_names:
                    val = mapping.get(col_name)
                    if isinstance(val, (date, datetime)):
                        val = val.isoformat()
                    row_dict[col_name] = val
                data.append(row_dict)
    
            return jsonify({
                'columns': col_names,
                'rows': data,
                'total_preview': len(data),
                'preview_limit': 5
            })
        except Exception as e:
            current_app.logger.exception('Erro em /api/consultas/preview')
            return jsonify({'error': str(e)}), 500


    @app.route('/api/consultas/layouts/<int:layout_id>/run', methods=['POST'])
    @login_required
    def consultas_run_layout(layout_id):
        try:
            user = _get_current_user()
            if not user:
                return jsonify({'error': 'Utilizador não autenticado'}), 401
    
            layout = ConsultaLayout.query.get_or_404(layout_id)
            if not _can_view_consulta(layout, user):
                return jsonify({'error': 'Sem permissão para executar esta consulta'}), 403
    
            try:
                definicao = json.loads(layout.definicao_json or '{}')
            except Exception:
                definicao = {}
    
            body = request.get_json(silent=True) or {}
    
            base = (layout.tabela_principal or definicao.get('base_table') or '').strip().lower()
            if base not in QUERY_BUILDER_TABLES:
                return jsonify({'error': 'Tabela principal inválida'}), 400
    
            related_tables = definicao.get('joins') or []
            if not isinstance(related_tables, list):
                return jsonify({'error': 'joins inválido'}), 400
    
            related_valid, related_paths, invalid_related = _qb_validate_related_tables(
                base, related_tables, max_depth=2
            )
            if invalid_related:
                return jsonify({'error': f'Tabelas relacionadas inválidas: {", ".join(invalid_related)}'}), 400
    
            allowed_tables = set([base] + related_valid)
    
            campos = definicao.get('fields') or []
            if not isinstance(campos, list) or not campos:
                return jsonify({'error': 'Layout sem campos configurados'}), 400
    
            calculated_fields = definicao.get('calculated_fields') or []
            if not isinstance(calculated_fields, list):
                return jsonify({'error': 'calculated_fields inválido'}), 400
    
            # filtros: runtime (body) sobrepõem os do layout
            filters_runtime = body.get('filters')
            if filters_runtime is None:
                filters = definicao.get('filters') or []
            else:
                filters = filters_runtime
    
            sort_runtime = body.get('sort')
            sort = sort_runtime if isinstance(sort_runtime, list) else (definicao.get('sort') or [])
    
            select_exprs = []
            group_exprs = []
            col_names = []
    
            for idx, c in enumerate(campos):
                table = (c.get('table') or '').strip().lower()
                field = (c.get('field') or '').strip()
                label = (c.get('label') or f'{table}.{field}' or f'col_{idx+1}').strip()
                agg = (c.get('aggregate') or '').strip().lower() or None
                group_by = bool(c.get('group_by', False))
    
                if table not in allowed_tables:
                    return jsonify({'error': f'Tabela não permitida no campo: {table}.{field}'}), 400
    
                col = _qb_get_column(table, field)
                if col is None:
                    return jsonify({'error': f'Campo inválido: {table}.{field}'}), 400
    
                if agg:
                    if agg not in AGGREGATES:
                        return jsonify({'error': f'Agregação inválida: {agg}'}), 400
    
                    if agg == 'sum':
                        expr = func.sum(col).label(label)
                    elif agg == 'count':
                        expr = func.count(col).label(label)
                    elif agg == 'count_distinct':
                        expr = func.count(func.distinct(col)).label(label)
                    elif agg == 'avg':
                        expr = func.avg(col).label(label)
                    elif agg == 'min':
                        expr = func.min(col).label(label)
                    elif agg == 'max':
                        expr = func.max(col).label(label)
                else:
                    expr = col.label(label)
                    if group_by:
                        group_exprs.append(col)
    
                select_exprs.append(expr)
                col_names.append(label)
    
            for i, cf in enumerate(calculated_fields):
                ctype = (cf.get('type') or '').strip().lower()
                label = (cf.get('label') or f'calc_{i+1}').strip()
    
                if ctype == 'datediff_days':
                    t1 = (cf.get('start_table') or '').strip().lower()
                    f1 = (cf.get('start_field') or '').strip()
                    t2 = (cf.get('end_table') or '').strip().lower()
                    f2 = (cf.get('end_field') or '').strip()
    
                    if t1 not in allowed_tables or t2 not in allowed_tables:
                        return jsonify({
                            'error': 'Campos calculados só podem usar a tabela principal e relacionadas selecionadas.'
                        }), 400
    
                    cstart = _qb_get_column(t1, f1)
                    cend = _qb_get_column(t2, f2)
                    if cstart is None or cend is None:
                        return jsonify({'error': 'datediff_days com campos inválidos'}), 400
    
                    expr = func.datediff(cend, cstart).label(label)
                    select_exprs.append(expr)
                    col_names.append(label)
                else:
                    return jsonify({'error': f'Campo calculado não suportado: {ctype}'}), 400
    
            if not select_exprs:
                return jsonify({'error': 'Sem colunas para mostrar'}), 400
    
            q = db.session.query(*select_exprs).select_from(QUERY_BUILDER_TABLES[base]['model'])
            q = _qb_apply_join_paths(q, related_paths)
    
            q, ferr = _qb_apply_filters(q, filters, allowed_tables)
            if ferr:
                return jsonify({'error': ferr}), 400
    
            has_agg = any((c.get('aggregate') or '').strip().lower() in AGGREGATES for c in campos)
            if has_agg and group_exprs:
                q = q.group_by(*group_exprs)
    
            if isinstance(sort, list):
                for s in sort:
                    t = (s.get('table') or '').strip().lower()
                    f = (s.get('field') or '').strip()
                    d = (s.get('direction') or 'asc').strip().lower()
    
                    if t not in allowed_tables:
                        continue
    
                    col = _qb_get_column(t, f)
                    if col is not None:
                        q = q.order_by(col.desc() if d == 'desc' else col.asc())
    
            rows = q.all()
            try:
                limit = int(limit)
            except Exception:
                limit = 1000
            limit = max(1, min(limit, 5000))
    
            rows = q.limit(limit).all()
    
            data = []
            for r in rows:
                row_dict = {}
                mapping = r._mapping if hasattr(r, '_mapping') else {}
                for col_name in col_names:
                    val = mapping.get(col_name)
                    if isinstance(val, (date, datetime)):
                        val = val.isoformat()
                    row_dict[col_name] = val
                data.append(row_dict)
    
            return jsonify({
                'layout_id': layout.id,
                'layout_nome': layout.nome,
                'columns': col_names,
                'rows': data,
                'total': len(data)
            })
        except Exception as e:
            current_app.logger.exception('Erro em /api/consultas/layouts/<id>/run')
            return jsonify({'error': str(e)}), 500

    #################################################################
    #Resumo Horas
    @app.route('/ensaios/todos')
    @login_required
    def ensaios_todos():
        ano = request.args.get('ano', type=int)
        laboratorio_id = request.args.get('laboratorio_id', type=int)
    
        query = db.session.query(Ensaio)
    
        # Filtro por ano (usa datapedido)
        if ano:
            query = query.filter(db.extract('year', Ensaio.datapedido) == ano)
    
        # Filtro por laboratório (0 = Todos)
        if laboratorio_id and laboratorio_id != 0:
            query = query.filter(Ensaio.laboratorio_id == laboratorio_id)
    
        ensaios = query.order_by(Ensaio.id.desc()).all()
    
        result = []
        for e in ensaios:
            projeto = Projeto.query.get(e.projeto_id)
            solicitante = Solicitante.query.get(e.solicitante_id)
            tipopeca = Tipopeca.query.get(e.tipopeca_id)
            laboratorio = Laboratorio.query.get(e.laboratorio_id)
            result.append({
                'ensaio': e.ensaio,
                'codigo_projeto': projeto.codigo if projeto else '',
                'denominacao_projeto': projeto.descricao if projeto else '',
                'tipo_peca': tipopeca.tipopeca if tipopeca else '',
                'solicitante': solicitante.nome if solicitante else '',
                'laboratorio': laboratorio.laboratorio if laboratorio else ''
            })
    
        return jsonify(result)

    @app.route('/api/resumo_horas_ensaio/<ensaio_numero>')
    @login_required
    def api_resumo_horas_ensaio(ensaio_numero):
    
        ensaio = Ensaio.query.filter_by(ensaio=ensaio_numero).first()
        if not ensaio:
            return jsonify({'error': 'Ensaio não encontrado'}), 404
    
        if ensaio.norma_id:
            templates = Templatenormas.query.filter_by(norma_id=ensaio.norma_id).all()
            template_map = {t.teste_id: t for t in templates}
        else:
            template_map = {}
    
        def build_detalhes(horas_list):
            grupos = defaultdict(float)
            grupo_meta = {}
            for h in horas_list:
                key = (h.tecnico_id, str(h.data), bool(h.extra), bool(h.auto or False), h.tipo)
                grupos[key] += float(h.horas)
                grupo_meta[key] = {
                    'tecnico': h.tecnico.full_name if h.tecnico else '',
                    'data': str(h.data),
                    'extra': bool(h.extra),
                    'auto': bool(h.auto or False),
                    'tipo': h.tipo
                }
            result = []
            for key, total_h in grupos.items():
                meta = grupo_meta[key]
                result.append({
                    'tecnico': meta['tecnico'],
                    'data': meta['data'],
                    'horas': round(total_h, 2),
                    'extra': meta['extra'],
                    'auto': meta['auto'],
                    'tipo': meta['tipo']
                })
            result.sort(key=lambda x: (x['data'], x['tecnico']))
            return result
    
        rows = []
        testes = Testes.query.filter_by(ensaio_id=ensaio.id).order_by(Testes.ordem).all()
        for teste in testes:
            tpl = template_map.get(teste.teste_id)
            num_pecas = teste.qtd or 0
            horas_max = round((tpl.duracaomontagem or 0) + ((tpl.tempopp or 0) * num_pecas), 2) if tpl else None
    
            horas_list = Horas.query.filter_by(ensaio_id=ensaio.id, teste_id=teste.id).all()
            horas_colocadas = round(sum(float(h.horas) for h in horas_list), 2)
            horas_disponiveis = round(horas_max - horas_colocadas, 2) if horas_max is not None else None
    
            rows.append({
                'teste_id': teste.id,
                'teste_nome': teste.teste.teste if teste.teste else '',
                'horas_max': horas_max,
                'horas_colocadas': horas_colocadas,
                'horas_disponiveis': horas_disponiveis,
                'detalhes': build_detalhes(horas_list)
            })
    
        # Horas linked to the ensaio but with no teste_id
        horas_sem_teste = Horas.query.filter(
            Horas.ensaio_id == ensaio.id,
            Horas.teste_id.is_(None)
        ).all()
        if horas_sem_teste:
            horas_colocadas_sem = round(sum(float(h.horas) for h in horas_sem_teste), 2)
            rows.append({
                'teste_id': None,
                'teste_nome': '(sem teste)',
                'horas_max': None,
                'horas_colocadas': horas_colocadas_sem,
                'horas_disponiveis': None,
                'detalhes': build_detalhes(horas_sem_teste)
            })
    
        return jsonify({'ensaio': ensaio_numero, 'rows': rows})

    ##################################################################
    #HORAS PESSOA

    @app.route('/horas_pessoa')
    @login_required
    def horas_pessoa():
        user = User.query.get(session['user_id'])
        tecnicos = User.query.all()
        import datetime
        current_date = datetime.date.today().isoformat()
        return render_template('horas_pessoa.html', user=user, tecnicos=tecnicos, current_date=current_date)
    
    @app.route('/ensaios/disponiveis')
    @login_required
    def ensaios_disponiveis():
        """
        Retorna os ensaios disponíveis para um laboratório específico ou para todos,
        filtrando apenas os que têm horas disponíveis relevantes.
        """
    
        # Aceita lab_id como int, string "todos" ou None
        lab_id_raw = request.args.get("lab_id")
        try:
            lab_id = int(lab_id_raw) if lab_id_raw not in (None, '', 'todos') else None
        except (ValueError, TypeError):
            lab_id = None
    
        # Se não houver filtro de laboratório, retorna todos
        if lab_id is None:
            ensaios = Ensaio.query.filter_by(anulado=False).all()
        else:
            ensaios = Ensaio.query.filter_by(laboratorio_id=lab_id, anulado=False).all()
    
        resultados = []
    
        def to_iso(val):
            if not val:
                return ''
            if isinstance(val, datetime):
                return val.strftime('%Y-%m-%d %H:%M:%S')
            if isinstance(val, date):
                return val.strftime('%Y-%m-%d')
            if isinstance(val, str) and 'T' in val:
                return val.replace('T', ' ')
            return str(val)
    
        data_limite = date(2026, 3, 1)
    
        for ensaio in ensaios:
            if not ensaio.norma_id:
                continue
    
            templates = Templatenormas.query.filter_by(norma_id=ensaio.norma_id).all()
            template_map = {t.teste_id: t for t in templates}
            testes = Testes.query.filter_by(ensaio_id=ensaio.id).all()
    
            for teste in testes:
                tpl = template_map.get(teste.teste_id)
                if not tpl:
                    continue
    
                num_pecas = teste.qtd or 0
                horas_max = (tpl.duracaomontagem or 0) + ((tpl.tempopp or 0) * num_pecas)
                horas_colocadas = (
                    db.session.query(db.func.sum(Horas.horas))
                    .filter(Horas.teste_id == teste.id)
                    .filter(or_(Horas.extra.is_(False), Horas.extra.is_(None)))
                    .scalar()
                ) or 0
                horas_disp_raw = horas_max - horas_colocadas
    
                # Tolerância: ignora valores muito pequenos
                if horas_disp_raw <= 1e-6:
                    continue
                horas_disp = round(horas_disp_raw, 2)
                if horas_disp <= 0:
                    continue
    
                # Só inclui se datafim for None ou >= data_limite
                incluir = False
                if teste.datafim is None:
                    incluir = True
                else:
                    datafim_val = teste.datafim
                    if isinstance(datafim_val, str):
                        try:
                            datafim_val = datetime.fromisoformat(datafim_val).date()
                        except Exception:
                            datafim_val = None
                    elif isinstance(datafim_val, datetime):
                        datafim_val = datafim_val.date()
                    if datafim_val and datafim_val >= data_limite:
                        incluir = True
    
                if incluir:
                    resultados.append({
                        "ensaio": ensaio.ensaio,
                        "link": f"/ensaios?ensaio={ensaio.ensaio}",
                        "teste": teste.teste.teste,
                        "datainicio": to_iso(teste.datainicio),
                        "datafim": to_iso(teste.datafim),
                        "ensaio_id": ensaio.id,
                        "teste_id": teste.id,
                        "horas_max": round(horas_max, 2),
                        "horas_colocadas": round(horas_colocadas, 2),
                        "horas_disponiveis": horas_disp,
                        "inserir": "<i class='far fa-clock inserir-horas' style='cursor:pointer' title='Inserir Horas'></i>"
                    })
    
        return jsonify(resultados)

    @app.route('/historico_horas')
    @login_required
    def historico_horas():
        user = User.query.get(session['user_id'])
        tecnicos = User.query.all()
        import datetime
        current_date = datetime.date.today().isoformat()
        return render_template('historico_horas.html', user=user, tecnicos=tecnicos, current_date=current_date)
    


   
    @app.route('/api/ensaios_concluidos', methods=['GET'])
    @login_required
    def api_ensaios_concluidos():
        tipo = (request.args.get('tipo') or 'todos').strip().lower()
    
        query = Ensaio.query

        laboratorio_id = (request.args.get('laboratorio_id') or '').strip()
        if laboratorio_id and laboratorio_id != 'todos':
            try:
                query = query.filter(Ensaio.laboratorio_id == int(laboratorio_id))
            except ValueError:
                return jsonify({'error': 'laboratorio_id inválido'}), 400
    
        if tipo == 'concluidos':
            query = query.filter(
                Ensaio.anulado.is_(False),
                Ensaio.concluido.isnot(None),
                Ensaio.concluido != ''
            )
        elif tipo == 'pendentes':
            query = query.filter(
                Ensaio.anulado.is_(False),
                or_(Ensaio.concluido.is_(None), Ensaio.concluido == '')
            )
        elif tipo == 'anulados':
            query = query.filter(Ensaio.anulado.is_(True))
        else:  # todos
            pass
    
        ensaios = query.order_by(Ensaio.id.desc()).all()
    
        resultado = []
        for e in ensaios:
            resultado.append({
                "ensaio": e.ensaio,
                "laboratorio": e.laboratorio.laboratorio if e.laboratorio else '',
                "norma": e.norma.norma if e.norma else '',
                "npecasrecebidas": e.npecasrecebidas,
                "destinopecas": e.destinopecas,
                "datapedido": safe_iso(e.datapedido),
                "datasolicitada": safe_iso(e.datasolicitada),
                "pep": e.pep,
                "network": e.network,
                "partnzf": e.partnzf,
                "partncliente": e.partncliente,
                "dataentregapecas": safe_iso(e.dataentregapecas),
                "dataacordada": safe_iso(e.dataacordada),
                "concluido": safe_iso(e.concluido),
                "cliente": e.cliente.cliente if e.cliente else '',
                "projeto": e.projeto.codigo if e.projeto else '',
                "projeto_descricao": e.projeto.descricao if e.projeto else '',
                "tipopeca": e.tipopeca.tipopeca if e.tipopeca else '',
                "fase": e.fase.fase if e.fase else '',
                "solicitante": e.solicitante.nome if e.solicitante else '',
                "user": e.user.full_name if e.user else '',
                "obs": e.obs,
                "anulado": e.anulado,
                "motivoanulacao": e.motivoanulacao
            })
        return jsonify(resultado)


    @app.route('/api/horas_maquina', methods=['GET'])
    @login_required
    def api_horas_maquina():
        ano = int(request.args.get('ano'))
        mes = int(request.args.get('mes'))
        lab_id = request.args.get('laboratorio')
        if lab_id == "" or lab_id is None:
            lab_id = None
    
        query = Testes.query.join(Ensaio).filter(
            extract('year', Testes.datafim) == ano,
            extract('month', Testes.datafim) == mes,
            or_(Testes.horasmaqexp == None, Testes.horasmaqexp == '0000-00-00 00:00:00'),
            Testes.maquina_id != None
        )
        if lab_id:
            query = query.filter(Ensaio.laboratorio_id == int(lab_id))
    
        results = []
        for t in query.all():
            ensaio = t.ensaio
            maquina = t.maquina
            datafim = t.datafim
            laboratorio = ensaio.laboratorio
            laboratoriomaq = maquina.laboratorio if maquina else None
            norma_id = ensaio.norma_id
            # Buscar duracao e tempomp do templatenormas
            temp = Templatenormas.query.filter_by(norma_id=norma_id, teste_id=t.teste_id).first()
            duracao = t.duracao if t and t.duracao else 0
            tempomp = temp.tempomp if temp and temp.tempomp else 0
            fator = t.fator if t.fator else 1
            qtd = t.qtd if t.qtd else 0
            horas = (duracao / fator) + (tempomp * qtd)
            results.append({
                'ensaio': ensaio.ensaio,
                'network': ensaio.network,
                'datafim': datafim.strftime('%d-%m-%Y') if datafim else '',
                'laboratorio': laboratorio.laboratorio if laboratorio else '',
                'elmact': laboratoriomaq.elmact if laboratoriomaq else '',
                'act': laboratoriomaq.act if laboratoriomaq else '',
                'maquina_nome': maquina.nome if maquina else '',
                'codsaphoras': maquina.codsaphoras if maquina else '',
                'codsappecas': maquina.codsappecas if maquina else '',
                'fator': fator,
                'qtd': qtd,
                'duracao': duracao,
                'tempomp': tempomp,
                'horas': round(horas, 2),
                'id': t.id,
            })
        return jsonify(results)
    
    @app.route('/api/exportar_horas_maquina_por_data', methods=['GET'])
    @login_required
    def exportar_horas_maquina_por_data():
        

        data_param = request.args.get('data')
        if not data_param:
            return jsonify({'error': 'Parâmetro data não fornecido.'}), 400

        try:
            data_dt = datetime.strptime(data_param, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return jsonify({'error': 'Formato de data inválido.'}), 400

        query = (
            Testes.query
            .join(Ensaio)
            .filter(
                Testes.maquina_id.isnot(None),
                Testes.horasmaqexp == data_dt
            )
        )

        results = []

        for t in query.all():
            ensaio = t.ensaio
            maquina = t.maquina
            laboratorio = ensaio.laboratorio
            norma_id = ensaio.norma_id

            temp = Templatenormas.query.filter_by(
                norma_id=norma_id,
                teste_id=t.teste_id
            ).first()

            duracao = temp.duracao if temp and temp.duracao else 0
            tempomp = temp.tempomp if temp and temp.tempomp else 0
            fator = t.fator or 1
            qtd = t.qtd or 0
            horas = (duracao / fator) + (tempomp * qtd)

            results.append({
                'ensaio': ensaio.ensaio,
                'network': ensaio.network,
                'datafim': t.datafim.strftime('%d-%m-%Y') if t.datafim else '',
                'laboratorio': laboratorio.laboratorio if laboratorio else '',
                'elmact': laboratorio.elmact if laboratorio else '',
                'act': laboratorio.act if laboratorio else '',
                'maquina_nome': maquina.nome if maquina else '',
                'codsaphoras': maquina.codsaphoras if maquina else '',
                'codsappecas': maquina.codsappecas if maquina else '',
                'fator': fator,
                'qtd': qtd,
                'duracao': duracao,
                'tempomp': tempomp,
                'horas': round(horas, 2),
                'id': t.id,
            })

        return jsonify(results)

    

    @app.route('/api/datas_exportacao_maquina')
    @login_required
    def datas_exportacao_maquina():
        rows = (
            db.session.query(
                Testes.horasmaqexp,
                Laboratorio.laboratorio
            )
            .join(Ensaio, Ensaio.id == Testes.ensaio_id)
            .join(Laboratorio, Laboratorio.id == Ensaio.laboratorio_id)
            .filter(Testes.horasmaqexp.isnot(None))
            .distinct()
            .order_by(Testes.horasmaqexp.desc())
            .all()
        )

        resultado = []
        for data, laboratorio in rows:
            resultado.append({
                'data': data.strftime('%Y-%m-%d %H:%M:%S') if hasattr(data, 'strftime') else str(data),
                'laboratorio': laboratorio
            })

        return jsonify(resultado)
    
    @app.route('/api/anular_exportacao_maquina_data', methods=['POST'])
    def anular_exportacao_maquina_data():
        data = request.get_json()
        data_export = data.get('data')
        if not data_export:
            return jsonify({'success': False, 'error': 'Data não fornecida.'}), 400
        try:
            linhas = Testes.query.filter(Testes.horasmaqexp == data_export).all()
            for linha in linhas:
                linha.horasmaqexp = None
            db.session.commit()
            return jsonify({'success': True, 'removidos': len(linhas)})
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'error': str(e)}), 500

    @app.route('/horas_maquina/marcar_exportados', methods=['POST'])
    def marcar_exportados():
        data = request.get_json()
        ids = data.get('ids', [])
        data_export = data.get('data')
        atualizar_horasmaqexp = data.get('atualizar_horasmaqexp', False)
        if ids and data_export and atualizar_horasmaqexp:
            Testes.query.filter(Testes.id.in_(ids)).update(
                {Testes.horasmaqexp: data_export}, synchronize_session=False
            )
            db.session.commit()
            return jsonify(success=True)
        return jsonify(success=False)

    
    
    @app.route('/horas_mensal')
    def horas_mensal():
        try:
        
            ano = int(request.args.get('ano'))
            mes = int(request.args.get('mes'))
            tecnico_id = int(request.args.get('tecnico_id'))
    
            data_inicio = date(ano, mes, 1)
            if mes == 12:
                data_fim = date(ano + 1, 1, 1)
            else:
                data_fim = date(ano, mes + 1, 1)
    
            # Carrega também o código G associado a cada registo de horas
            registros = (
                db.session.query(Horas)
                .options(joinedload(Horas.codigog))
                .filter(
                    Horas.tecnico_id == tecnico_id,
                    Horas.data >= data_inicio,
                    Horas.data < data_fim
                )
                .all()
            )
    
            resultado = {}
    
            for reg in registros:
                if not reg.data:
                    continue
    
                dia = reg.data.day
                dia_key = str(dia)
                horas_val = float(reg.horas or 0)
    
                # Total diário (todas as horas)
                resultado[dia_key] = resultado.get(dia_key, 0) + horas_val
    
                # Total diário de "gerais" só para códigos E.G7%
                codigog_txt = ((reg.codigog.codigog if reg.codigog else '') or '').strip().upper()
                if codigog_txt.startswith('E.G7'):
                    chave_g = f"{dia}_g"
                    resultado[chave_g] = resultado.get(chave_g, 0) + horas_val
    
            return jsonify(resultado)
    
        except Exception as e:
            current_app.logger.exception("Erro em /horas_mensal")
            return jsonify({
                "error": str(e),
                "args": {
                    "ano": request.args.get('ano'),
                    "mes": request.args.get('mes'),
                    "tecnico_id": request.args.get('tecnico_id')
                }
            }), 500
  
    def safe_iso(val):
        """Convert datetime to ISO format, handling null and zero-dates safely."""
        if not val:
            return ''
        if hasattr(val, 'isoformat'):
            s = val.isoformat()
            return '' if s.startswith('0000') else s
        s = str(val)
        return '' if s.startswith('0000') else s
    
    @app.route('/api/ensaios')
    def api_ensaios():
        print('>>> [LOG] Entrou no endpoint /api/ensaios', flush=True)

        tecnico_id = request.args.get('tecnico_id', type=int)

        # sopendentes: 1 (default) => só pendentes; 0 => todos
        try:
            sopendentes = int(request.args.get('sopendentes', 1))
        except (TypeError, ValueError):
            sopendentes = 1

        # Base query: Ensaio + Projeto (LEFT OUTER JOIN) e ordenação por datapedido desc
        # Usando joinedload para evitar N+1 quando acedemos a Projeto
        query = (
            Ensaio.query
            .options(joinedload(Ensaio.projeto))   # assumindo relationship Ensaio.projeto existe
            .order_by(Ensaio.datapedido.desc())
        )

        # Filtro de pendentes usando apenas 'concluido'
        # - Pendente: concluido IS NULL  (e opcionalmente casos legados "0000-00-00")
        if sopendentes == 1:
            query = query.filter(
                or_(
                    Ensaio.concluido.is_(None),
                    # Caso exista lixo legado na BD; se a coluna for Date real, este or não terá efeito.
                    # Mantemos por segurança de dados antigos (não causa erro; apenas ignora se for Date).
                    (getattr(Ensaio, 'concluido', None) == '0000-00-00')
                )
            )

        ensaios = query.all()

        resultado = []
        for e in ensaios:
            try:
                projeto = getattr(e, 'projeto', None)  # via joinedload
                projeto_codigo = getattr(projeto, 'codigo', '') if projeto else ''
                projeto_descricao = getattr(projeto, 'descricao', '') if projeto else ''

                resultado.append({
                    'id': e.id,
                    'ensaio': e.ensaio,
                    'projeto_codigo': projeto_codigo or '',
                    'projeto_descricao': projeto_descricao or ''
                })
            except Exception as ex:
                print(f"[ERRO ao processar ensaio {getattr(e, 'id', '?')}]: {ex}", flush=True)

        print(f"[LOG] Total de ensaios retornados: {len(resultado)}", flush=True)
        return jsonify(resultado)

    


    @app.route('/api/datas_exportacao_tecnico')
    def datas_exportacao_tecnico():
        tecnico_id = request.args.get('tecnico_id', type=int)
        if not tecnico_id:
            return jsonify({'error': 'tecnico_id não fornecido'}), 400
        datas = db.session.query(Horas.exportado).filter(
            Horas.tecnico_id == tecnico_id,
            Horas.exportado != None,
            Horas.exportado != '0000-00-00'
        ).distinct().order_by(Horas.exportado.desc()).all()
        datas_unicas = sorted({d[0] for d in datas if d[0]}, reverse=True)
        return jsonify([d.strftime('%Y-%m-%d') for d in datas_unicas])


    @app.route('/api/anular_exportacao_data', methods=['POST'])
    def anular_exportacao_data():
        data = request.get_json()
        tecnico_id = data.get('tecnico_id')
        data_export = data.get('data')
        if not tecnico_id or not data_export:
            return jsonify({'success': False, 'error': 'Parâmetros obrigatórios não fornecidos.'}), 400
        try:
            data_dt = datetime.strptime(data_export, '%Y-%m-%d').date()
            linhas = Horas.query.filter(
                Horas.tecnico_id == int(tecnico_id),
                db.func.date(Horas.exportado) == data_dt
            ).all()
            for linha in linhas:
                linha.exportado = None
            db.session.commit()
            return jsonify({'success': True, 'removidos': len(linhas)})
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'error': str(e)}), 500

    @app.route('/api/ensaio_by_id')
    def get_ensaio_by_id():
        ensaio_id = request.args.get('id', type=int)
        if not ensaio_id:
            return jsonify({'error': 'ID não fornecido'}), 400
        ensaio = Ensaio.query.get(ensaio_id)
        if ensaio:
            return jsonify({'id': ensaio.id, 'ensaio': ensaio.ensaio})
        else:
            return jsonify({'error': 'Ensaio não encontrado'}), 404

    @app.route('/api/ensaio_by_numero')
    def get_ensaio_by_numero():
        numero = request.args.get('numero')
        if not numero:
            return jsonify({'error': 'Número não fornecido'}), 400
        ensaio = Ensaio.query.filter_by(ensaio=numero).first()
        if ensaio:
            return jsonify({'id': ensaio.id, 'ensaio': ensaio.ensaio})
        else:
            return jsonify({'error': 'Ensaio não encontrado'}), 404

    @app.route('/horas_dia')
    def horas_dia():
    
        id_param = request.args.get('id')
        if id_param:
            reg = Horas.query.get(int(id_param))
            if not reg:
                return jsonify({'error': 'Registo não encontrado'}), 404
            linha = {
                'id': reg.id,
                'data': reg.data.isoformat() if reg.data else '',
                'tecnico_id': reg.tecnico_id,
                'horas': reg.horas,
                'observacoes': reg.obs if hasattr(reg, 'obs') else '',
                'ensaio_id': reg.ensaio_id,
                'codigog_id': reg.codigog_id,
                'teste_id': reg.teste_id if hasattr(reg, 'teste_id') else None,
                'tipo': 'ensaio' if reg.ensaio_id else ('codigog' if reg.codigog_id else 'manual'),
                'manual': reg.manual,
            }
            return jsonify(linha)
    
        tecnico_id = request.args.get('tecnico_id')
        data_str = request.args.get('data')
        if not tecnico_id or not data_str:
            return jsonify({'error': 'Parâmetros obrigatórios não fornecidos'}), 400
    
        tecnico_id = int(tecnico_id)
        data = datetime.strptime(data_str, '%Y-%m-%d').date()
        registros = db.session.query(Horas).filter(
            Horas.tecnico_id == tecnico_id,
            Horas.data == data
        ).all()
        resultado = []
        for reg in registros:
            linha = {
                'ensaio': '',
                'network': '',
                'projeto': '',
                'teste': ''
            }
        
            if reg.ensaio_id is not None:
                ensaio = Ensaio.query.get(reg.ensaio_id)
                linha['ensaio'] = ensaio.ensaio if ensaio else ''
                linha['network'] = ensaio.network if ensaio and hasattr(ensaio, 'network') else ''
                linha['projeto'] = ensaio.projeto.descricao if ensaio and ensaio.projeto else ''
                if hasattr(reg, 'teste_id') and reg.teste_id and reg.teste_id > 0:
                    teste_obj = Testes.query.get(reg.teste_id)
                    if teste_obj and teste_obj.teste_id:
                        tipoteste_obj = Tipotestes.query.get(teste_obj.teste_id)
                        linha['teste'] = tipoteste_obj.teste if tipoteste_obj else ''
                    else:
                        linha['teste'] = ''
        
            elif reg.codigog_id is not None:
                codigog = Codigosg.query.get(reg.codigog_id) if reg.codigog_id else None
                linha['network'] = codigog.codigog if codigog else ''
                linha['projeto'] = codigog.descricao if codigog else ''
                linha['teste'] = reg.teste if hasattr(reg, 'teste') else ''
        
            else:
                linha['network'] = reg.manual or ''
        
            linha['horas'] = reg.horas
            linha['observacoes'] = reg.obs if hasattr(reg, 'obs') else ''
            linha['id'] = reg.id
            resultado.append(linha)
        return jsonify(resultado)
    
    

    @app.route('/api/exportar_horas', methods=['POST'])
    def exportar_horas():
        tecnico_id = request.json.get('tecnico_id')

        # Ver a configuração do técnico para saber se exporta por PEP ou por Network
        conf = ConfHorasAuto.query.filter_by(tecnico_id=tecnico_id).first()
        usar_pep = (conf and (conf.pepnet or '').lower() == "pep")

        horas = Horas.query.filter(
            Horas.tecnico_id == tecnico_id,
            or_(Horas.exportado == None, Horas.exportado == '0000-00-00')
        ).all()

        export_data = []
        ids_exportados = []

        for h in horas:
            ens = h.ensaio
            codg = h.codigog.codigog if h.codigog else None
            manual_val = (h.manual or '').strip()

            # Determinar tipo base
            if ens:
                tipo_base = "ensaio"
            elif codg:
                tipo_base = "codigog"
            elif manual_val:
                if manual_val.startswith('8'):
                    tipo_base = "manual_ensaio"
                elif manual_val.upper().startswith('E'):
                    tipo_base = "manual_codigog"
            else:
                continue  # sem ensaio e sem codigog, ignora

            laboratorio_elmact = ""
            laboratorio_act = ""
            if ens and ens.laboratorio_id:
                lab = Laboratorio.query.get(ens.laboratorio_id)
                if lab:
                    laboratorio_elmact = str(lab.elmact) if lab.elmact is not None else ""
                    laboratorio_act   = str(lab.act)   if lab.act   is not None else ""

            # =============================
            # Regras pedidas
            # =============================
            if tipo_base == "manual_ensaio":
                # Registo manual: ignora usar_pep, sempre usa manual_val como network
                network_val = manual_val
                if not (
                    network_val
                    and (network_val.startswith("84") or network_val.startswith("88"))
                    and network_val.isdigit()
                    and len(network_val) == 10
                ):
                    continue
                tipo_export = "ensaio"
                export_key = network_val

            elif tipo_base == "ensaio":
                if usar_pep:
                    pep_val = (ens.pep or "").strip() if ens else ""
                    if not pep_val:
                        continue
                    tipo_export = "codigog-pep"
                    export_key = pep_val
                else:
                    network_val = (ens.network or "").strip() if ens else ""
                    if not (
                        network_val
                        and (network_val.startswith("84") or network_val.startswith("88"))
                        and network_val.isdigit()
                        and len(network_val) == 10
                    ):
                        continue
                    tipo_export = "ensaio"
                    export_key = network_val

            elif tipo_base in ("codigog", "manual_codigog"):
                tipo_export = "codigog"
                export_key = None
                if tipo_base == "manual_codigog":
                    codg = manual_val
            else:
                continue

            export_data.append({
                "id": h.id,
                "tipo": tipo_export,
                "data": h.data.strftime('%Y-%m-%d'),
                "mes": h.data.strftime('%m'),
                "dia": int(h.data.strftime('%d')),
                "network": export_key,
                "ensaio": ens.ensaio if ens else None,
                "codigog": codg,
                "laboratorio_elmact": laboratorio_elmact,
                "laboratorio_act": laboratorio_act,
                "horas": float(h.horas),
                "obs": h.obs or ""
            })

            ids_exportados.append(h.id)

        # Marcar como exportado
        now = datetime.now()
        if ids_exportados:
            Horas.query.filter(Horas.id.in_(ids_exportados)).update(
                {'exportado': now}, synchronize_session=False
            )
            db.session.commit()

        return jsonify(export_data)

    @app.route('/api/exportar_horas_por_data', methods=['POST'])
    def exportar_horas_por_data():
        tecnico_id = request.json.get('tecnico_id')
        data_export = request.json.get('data')

        if not tecnico_id or not data_export:
            return jsonify({'error': 'Parâmetros obrigatórios não fornecidos.'}), 400

        data_dt = datetime.strptime(data_export, '%Y-%m-%d').date()

        # Buscar configuração para ver se é network ou pep
        conf = ConfHorasAuto.query.filter_by(tecnico_id=tecnico_id).first()
        usar_pep = conf and (conf.pepnet or "").lower() == "pep"

        horas = Horas.query.filter(
            Horas.tecnico_id == tecnico_id,
            db.func.date(Horas.exportado) == data_dt
        ).all()

        export_data = []

        for h in horas:
            ens = h.ensaio
            codg = h.codigog.codigog if h.codigog else None
            manual_val = (h.manual or '').strip()

            if ens:
                tipo_base = "ensaio"
            elif codg:
                tipo_base = "codigog"
            elif manual_val:
                if manual_val.startswith('8'):
                    tipo_base = "manual_ensaio"
                elif manual_val.upper().startswith('E'):
                    tipo_base = "manual_codigog"
                else:
                    continue
            else:
                continue

            laboratorio_elmact = ""
            laboratorio_act = ""
            if ens and ens.laboratorio_id:
                lab = Laboratorio.query.get(ens.laboratorio_id)
                if lab:
                    laboratorio_elmact = lab.elmact or ""
                    laboratorio_act = lab.act or ""

            if tipo_base == "manual_ensaio":
                # Registo manual: ignora usar_pep, sempre usa manual_val como network
                network_val = manual_val
                if not (
                    network_val
                    and (network_val.startswith("84") or network_val.startswith("88"))
                    and network_val.isdigit()
                    and len(network_val) == 10
                ):
                    continue
                tipo_export = "ensaio"
                export_key = network_val

            elif tipo_base == "ensaio":
                if usar_pep:
                    pep_val = (ens.pep or "").strip()
                    if not pep_val:
                        continue
                    tipo_export = "codigog-pep"
                    export_key = pep_val
                else:
                    network_val = (ens.network or "").strip()
                    if not (network_val and (network_val.startswith("84") or network_val.startswith("88"))
                            and network_val.isdigit() and len(network_val) == 10):
                        continue
                    tipo_export = "ensaio"
                    export_key = network_val

            elif tipo_base in ("codigog", "manual_codigog"):
                tipo_export = "codigog"
                export_key = None
                if tipo_base == "manual_codigog":
                    codg = manual_val
            else:
                continue

            export_data.append({
                'id': h.id,
                'tipo': tipo_export,
                'data': h.data.strftime('%Y-%m-%d'),
                'mes': h.data.strftime('%m'),
                'dia': int(h.data.strftime('%d')),
                'network': export_key,
                'ensaio': ens.ensaio if ens else None,
                'codigog': codg,
                'laboratorio_elmact': laboratorio_elmact,
                'laboratorio_act': laboratorio_act,
                'horas': float(h.horas),
                'exportado': h.exportado.strftime('%Y-%m-%d') if h.exportado else None,
            })

        return jsonify(export_data)

    #######################################################################
    #TABELAS
    @app.route('/tabelas')
    @login_required
    def tabelas():
        user = User.query.get(session['user_id'])
        codigosg = Codigosg.query.all()
        
        ano_atual = datetime.now().year
        mes_atual = datetime.now().month

      
        anos_permitidos = [ano_atual]
        if mes_atual == 12:
                anos_permitidos.append(ano_atual + 1)


        projetos = Projeto.query.all()
        tipotestes = Tipotestes.query.all()
        clientes_todos = Cliente.query.order_by(Cliente.cliente).all()
        clientes_ativos = Cliente.query.filter_by(obsoleto=False).order_by(Cliente.cliente).all()
        solicitantes_todos = Solicitante.query.order_by(Solicitante.nome).all()
        solicitantes_ativos = Solicitante.query.filter_by(obsoleto=False).order_by(Solicitante.nome).all()
        tipopecas_ativos = Tipopeca.query.filter_by(obsoleto=False).order_by(Tipopeca.tipopeca).all()
        tipopecas_todos = Tipopeca.query.order_by(Tipopeca.tipopeca).all()
        current_app.logger.debug('DEBUG /tabelas: tipopecas ativos=%d, todos=%d', len(tipopecas_ativos), len(tipopecas_todos))
        return render_template('tabelas.html', projetos=projetos, tipotestes=tipotestes, clientes=clientes_todos, clientes_ativos=clientes_ativos, solicitantes=solicitantes_todos, solicitantes_ativos=solicitantes_ativos, tipopecas=tipopecas_todos, tipopecas_ativos=tipopecas_ativos, codigosg=codigosg, anos_permitidos=anos_permitidos, user=user)

    
    #######################################################################
    #PROJETOS
    #OBTER PROJETOS
    @app.route('/projetos', methods=['GET'])
    def get_projetos():
        projetos = Projeto.query.all()
        return jsonify({
            'data': [
                {
                    'id': p.id,
                    'codigo': p.codigo,
                    'descricao': p.descricao,
                    'tipopeca_id': p.tipopeca_id,
                    'tipopeca': p.tipopeca.tipopeca,
                    'cliente_id': p.cliente_id,
                    'cliente': p.cliente.cliente,
                    'torque': p.torque,
                    'testfixture': p.testfixture,
                    'obsoleto': p.obsoleto
                }
                for p in projetos
            ]
        })


    
    @app.route('/projetos', methods=['POST'])
    def add_projeto():
        try:
            current_app.logger.info("=== INICIANDO ADD_PROJETO ===")
            data = request.json
            current_app.logger.info(f"Dados recebidos: {data}")
            
            codigo = data.get('codigo')
            descricao = data.get('descricao')
            cliente_id = data.get('cliente_id')
            tipopeca_id = data.get('tipopeca_id')
            obsoleto = data.get('obsoleto')
            torque = data.get('torque')
            testfixture = data.get('testfixture')

            # Validar TODOS os campos obrigatórios
            if not codigo or not descricao:
                current_app.logger.warning("Código ou descrição vazios")
                return jsonify({'error': 'Código e descrição são obrigatórios'}), 400
            
            if not tipopeca_id:
                current_app.logger.warning("Tipo de peça vazio")
                return jsonify({'error': 'Tipo de peça é obrigatório'}), 400
                
            if not cliente_id:
                current_app.logger.warning("Cliente vazio")
                return jsonify({'error': 'Cliente é obrigatório'}), 400
            
            # Verificar duplicado composto (os 4 campos em conjunto)
            existente = Projeto.query.filter_by(
                codigo=codigo,
                descricao=descricao,
                tipopeca_id=int(tipopeca_id),
                cliente_id=int(cliente_id)
            ).first()
            if existente:
                return jsonify({'error': 'Já existe um projeto com o mesmo código, descrição, tipo de peça e cliente'}), 409
    
            novo = Projeto(
                codigo=codigo, 
                descricao=descricao,
                cliente_id=int(cliente_id),
                tipopeca_id=int(tipopeca_id),
                obsoleto=False,
                torque=torque,
                testfixture=testfixture
            )
            db.session.add(novo)
            db.session.commit()
            
            current_app.logger.info(f"Projeto criado com sucesso: ID={novo.id}")
            return jsonify({'success': True, 'message': 'Projeto adicionado com sucesso'})
        
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"ERRO ao adicionar projeto: {str(e)}")
            import traceback
            current_app.logger.error(traceback.format_exc())
            return jsonify({'error': f'Erro ao adicionar projeto: {str(e)}'}), 500
    
  

    @app.route('/projetos/update/<int:id>', methods=['POST'])
    def update_projeto(id):

        projeto = Projeto.query.get_or_404(id)
        data = request.json

        # Calcular os valores finais e verificar duplicado
        chk_codigo    = data.get('codigo') or projeto.codigo
        chk_descricao = data.get('descricao') if 'descricao' in data else projeto.descricao
        chk_tipopeca_id = int(data['tipopeca_id']) if 'tipopeca_id' in data else projeto.tipopeca_id
        chk_cliente_id  = int(data['cliente_id'])  if 'cliente_id'  in data else projeto.cliente_id
        
        existente = Projeto.query.filter(
            Projeto.id != id,
            Projeto.codigo == chk_codigo,
            Projeto.descricao == chk_descricao,
            Projeto.tipopeca_id == chk_tipopeca_id,
            Projeto.cliente_id == chk_cliente_id
        ).first()
        if existente:
            return jsonify({'error': 'Já existe um projeto com o mesmo código, descrição, tipo de peça e cliente'}), 409


        novo_codigo = data.get('codigo')
        if novo_codigo and novo_codigo != projeto.codigo:
            projeto.codigo = novo_codigo

        if 'descricao' in data:
            projeto.descricao = data['descricao']
        if 'cliente_id' in data:
            projeto.cliente_id = data['cliente_id']
        if 'tipopeca_id' in data:
            projeto.tipopeca_id = data['tipopeca_id']
        if 'obsoleto' in data:
            projeto.obsoleto = data['obsoleto']
        if 'torque' in data:
            projeto.torque = data['torque']
        if 'testfixture' in data:
            projeto.testfixture = data['testfixture']

        db.session.commit()
        return jsonify({'success': True, 'message': 'Projeto atualizado com sucesso'})

    @app.route('/projetos/check/<int:id>', methods=['GET'])
    def check_projeto(id):
        usado_em_ensaios = db.session.query(Ensaio.id).filter(Ensaio.projeto_id == id).first()
        return jsonify({'temEnsaios': usado_em_ensaios is not None})



    @app.route('/projetos/<int:id>', methods=['DELETE'])
    def delete_projeto(id):
        projeto = Projeto.query.get_or_404(id)
    
        usado_em_ensaios = db.session.query(Ensaio.id).filter(Ensaio.projeto_id == id).first()
        usado_em_referencias = db.session.query(Referencia.id).filter(Referencia.projeto_id == id).first()
    
        if usado_em_ensaios or usado_em_referencias:
            return jsonify({'error': 'Este projeto não pode ser eliminado porque está a ser usado em ensaios ou referências. Marque como obsoleto em vez de eliminar.'}), 400
        else:
            db.session.delete(projeto)
            db.session.commit()
            return jsonify({'success': True, 'message': 'Projeto eliminado.'})


    @app.route('/clientes/ativos', methods=['GET'])
    def get_clientes_ativos():
        clientes = Cliente.query.filter_by(obsoleto=False).order_by(Cliente.cliente).all()
        return jsonify([
            {'id': c.id, 'cliente': c.cliente}
            for c in clientes
        ])


    @app.route('/tipopecas/ativos', methods=['GET'])
    def get_tipopecas_ativos():
        tipopecas = Tipopeca.query.filter_by(obsoleto=False).order_by(Tipopeca.tipopeca).all()
        return jsonify([
            {'id': t.id, 'tipopeca': t.tipopeca}
            for t in tipopecas
        ])
    
    #####################################################################
    #LOCALIZAÇÕES
    @app.route('/localizacoes', methods=['GET'])
    def get_localizacoes():
        localizacoes = Localizacao.query.all()
        return jsonify({
            'data': [
                {
                    'id': loc.id,
                    'nome': loc.nome or '',
                    'morada': loc.morada or '',
                    'morada2': loc.morada2 or '',
                    'contactonome': loc.contactonome or '',
                    'contactoemail': loc.contactoemail or '',
                    'contactotlf': loc.contactotlf or '',
                    'interno': bool(loc.interno),
                    'obsoleto': bool(loc.obsoleto)
                }
                for loc in localizacoes
            ]
        })

    @app.route('/api/localizacoes_stock')
    def api_localizacoes_stock():
        referencia_id = request.args.get('referencia_id', type=int)

        stock_por_localizacao = (
            db.session.query(
                Localizacao.id,
                Localizacao.nome,
                func.sum(
                    case(
                        (MovimentoStock.movimento == '+', 1),
                        (MovimentoStock.movimento == '-', -1),
                        else_=0
                    ) * MovimentoStock.quantidade
                ).label('stock')
            )
            .join(MovimentoStock, MovimentoStock.localizacao_id == Localizacao.id)
            .filter(MovimentoStock.referencia_id == referencia_id)
            .filter(MovimentoStock.localizacao_id.isnot(None))  # 👈 obrigatório
            .group_by(Localizacao.id, Localizacao.nome)
            .having(func.sum(
                case(
                    (MovimentoStock.movimento == '+', 1),
                    (MovimentoStock.movimento == '-', -1),
                    else_=0
                ) * MovimentoStock.quantidade
            ) > 0)
            .all()
        )

        print(stock_por_localizacao)
        for l in stock_por_localizacao:
            print("ID:", l.id, "NOME:", l.nome, "STOCK:", l.stock)

        return jsonify([
            {'id': l.id, 'nome': l.nome, 'stock': int(l.stock) if l.stock is not None else 0}
            for l in stock_por_localizacao
        ])

    @app.route('/api/saida_stock/resumo', methods=['GET'])
    @login_required
    def resumo_saidas_stock():
        ensaio_id = request.args.get('ensaio_id', type=int)
        if not ensaio_id:
            return jsonify([])
        
        rows = (
            db.session.query(
                Referencia.id,
                Referencia.referencia,
                Referencia.descricao,
                func.sum(MovimentoStock.quantidade).label('total')
            )
            .join(Referencia, MovimentoStock.referencia_id == Referencia.id)
            .filter(
                MovimentoStock.ensaio_id == ensaio_id,
                MovimentoStock.movimento == '-'
            )
            .group_by(Referencia.id, Referencia.referencia, Referencia.descricao)
            .all()
        )
        return jsonify([{
            'id': r.id,
            'referencia': r.referencia,
            'descricao': r.descricao or '',
            'total': float(r.total)
        } for r in rows])

    @app.route('/api/localizacoes')
    def api_localizacoes():
        obsoleto = request.args.get('obsoleto', '0')
        # Ajuste o nome da sua tabela/model conforme necessário
        localizacoes = Localizacao.query.filter_by(obsoleto=int(obsoleto)).order_by(Localizacao.nome).all()
        return jsonify([{'id': l.id, 'nome': l.nome} for l in localizacoes])

    # Criar nova Localização
    @app.route('/localizacoes', methods=['POST'])
    def add_localizacao():
        data = request.get_json() or {}
        nome = (data.get('nome') or '').strip()

        if not nome:
            return jsonify({'error': 'Nome da localização é obrigatório'}), 400

        # Verificar duplicado (podes remover se não precisa ser único)
        if Localizacao.query.filter_by(nome=nome).first():
            return jsonify({'error': 'Já existe uma localização com esse nome'}), 409

        nova = Localizacao(
            nome=nome,
            morada=(data.get('morada') or '').strip() or None,
            morada2=(data.get('morada2') or '').strip() or None,
            contactonome=(data.get('contactonome') or '').strip() or None,
            contactoemail=(data.get('contactoemail') or '').strip() or None,
            contactotlf=(data.get('contactotlf') or '').strip() or None,
            interno=bool(data.get('interno')) if data.get('interno') is not None else True,
            obsoleto=bool(data.get('obsoleto')) if data.get('obsoleto') is not None else False
        )

        db.session.add(nova)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Localização adicionada com sucesso',
            'id': nova.id
        })

    # Atualizar Localização existente (parcial)
    @app.route('/localizacoes/update/<int:id>', methods=['POST'])
    def update_localizacao(id):
        loc = Localizacao.query.get_or_404(id)
        data = request.get_json() or {}

        # Nome (com verificação de duplicado)
        if 'nome' in data:
            novo_nome = (data.get('nome') or '').strip()
            if not novo_nome:
                return jsonify({'error': 'O nome não pode estar vazio.'}), 400
            if novo_nome != loc.nome:
                if Localizacao.query.filter(Localizacao.nome == novo_nome, Localizacao.id != id).first():
                    return jsonify({'error': 'Já existe outra localização com esse nome'}), 409
                loc.nome = novo_nome

        # Restantes campos (atualização parcial)
        if 'morada' in data:
            loc.morada = (data.get('morada') or '').strip() or None
        if 'morada2' in data:
            loc.morada2 = (data.get('morada2') or '').strip() or None
        if 'contactonome' in data:
            loc.contactonome = (data.get('contactonome') or '').strip() or None
        if 'contactoemail' in data:
            loc.contactoemail = (data.get('contactoemail') or '').strip() or None
        if 'contactotlf' in data:
            loc.contactotlf = (data.get('contactotlf') or '').strip() or None
        if 'interno' in data:
            loc.interno = bool(data.get('interno'))
        if 'obsoleto' in data:
            loc.obsoleto = bool(data.get('obsoleto'))

        db.session.commit()
        return jsonify({'success': True, 'message': 'Localização atualizada com sucesso'})



    #####################################################################
    #LOCALIZAÇÕES ae
    @app.route('/localizacoesae', methods=['GET'])
    def get_localizacoesae():
        localizacoes = Localizacao_ae.query.all()
        return jsonify({
            'data': [
                {
                    'id': loc.id,
                    'nome': loc.nome or '',
                    'morada': loc.morada or '',
                    'morada2': loc.morada2 or '',
                    'contactonome': loc.contactonome or '',
                    'contactoemail': loc.contactoemail or '',
                    'contactotlf': loc.contactotlf or '',
                    'interno': bool(loc.interno),
                    'obsoleto': bool(loc.obsoleto)
                }
                for loc in localizacoes
            ]
        })


    @app.route('/api/localizacoesae')
    def api_localizacoesae():
        obsoleto = request.args.get('obsoleto', '0')
        # Ajuste o nome da sua tabela/model conforme necessário
        localizacoes = Localizacao_ae.query.filter_by(obsoleto=int(obsoleto)).order_by(Localizacao_ae.nome).all()
        return jsonify([{'id': l.id, 'nome': l.nome} for l in localizacoes])

    # Criar nova Localização
    @app.route('/localizacoesae', methods=['POST'])
    def add_localizacaoae():
        data = request.get_json() or {}
        nome = (data.get('nome') or '').strip()

        if not nome:
            return jsonify({'error': 'Nome da localização é obrigatório'}), 400

        # Verificar duplicado (podes remover se não precisa ser único)
        if Localizacao_ae.query.filter_by(nome=nome).first():
            return jsonify({'error': 'Já existe uma localização com esse nome'}), 409

        nova = Localizacao_ae(
            nome=nome,
            morada=(data.get('morada') or '').strip() or None,
            morada2=(data.get('morada2') or '').strip() or None,
            contactonome=(data.get('contactonome') or '').strip() or None,
            contactoemail=(data.get('contactoemail') or '').strip() or None,
            contactotlf=(data.get('contactotlf') or '').strip() or None,
            interno=bool(data.get('interno')) if data.get('interno') is not None else True,
            obsoleto=bool(data.get('obsoleto')) if data.get('obsoleto') is not None else False
        )

        db.session.add(nova)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Localização adicionada com sucesso',
            'id': nova.id
        })

    # Atualizar Localização existente (parcial)
    @app.route('/localizacoesae/update/<int:id>', methods=['POST'])
    def update_localizacaoae(id):
        loc = Localizacao_ae.query.get_or_404(id)
        data = request.get_json() or {}

        # Nome (com verificação de duplicado)
        if 'nome' in data:
            novo_nome = (data.get('nome') or '').strip()
            if not novo_nome:
                return jsonify({'error': 'O nome não pode estar vazio.'}), 400
            if novo_nome != loc.nome:
                if Localizacao_ae.query.filter(Localizacao_ae.nome == novo_nome, Localizacao_ae.id != id).first():
                    return jsonify({'error': 'Já existe outra localização com esse nome'}), 409
                loc.nome = novo_nome

        # Restantes campos (atualização parcial)
        if 'morada' in data:
            loc.morada = (data.get('morada') or '').strip() or None
        if 'morada2' in data:
            loc.morada2 = (data.get('morada2') or '').strip() or None
        if 'contactonome' in data:
            loc.contactonome = (data.get('contactonome') or '').strip() or None
        if 'contactoemail' in data:
            loc.contactoemail = (data.get('contactoemail') or '').strip() or None
        if 'contactotlf' in data:
            loc.contactotlf = (data.get('contactotlf') or '').strip() or None
        if 'interno' in data:
            loc.interno = bool(data.get('interno'))
        if 'obsoleto' in data:
            loc.obsoleto = bool(data.get('obsoleto'))

        db.session.commit()
        return jsonify({'success': True, 'message': 'Localização atualizada com sucesso'})

    @app.route('/localizacoesae/<int:id>', methods=['DELETE'])
    def delete_localizacaoae(id):
        loc = Localizacao_ae.query.get_or_404(id)

        # Pode eliminar
        db.session.delete(loc)
        db.session.commit()
        return jsonify({
            'success': True,
            'message': 'Localização eliminada.'
        })



    ########################################################################
    #CLIENTES
    

    @app.route('/clientes', methods=['GET'])
    def get_clientes():
        clientes = Cliente.query.all()
        return jsonify({
            'data': [
                {'id': c.id, 'cliente': c.cliente or '', 'obsoleto': c.obsoleto}
                for c in clientes
            ]
        })

    @app.route('/clientes', methods=['POST'])
    def add_cliente():
        data = request.json
        nome = data.get('cliente')
        if not nome:
            return jsonify({'error': 'Nome do cliente é obrigatório'}), 400

        # Verificar duplicado
        if Cliente.query.filter_by(cliente=nome).first():
            return jsonify({'error': 'Já existe um cliente com esse nome'}), 409

        novo = Cliente(cliente=nome, obsoleto=False)
        db.session.add(novo)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Cliente adicionado com sucesso'})

    @app.route('/clientes/update/<int:id>', methods=['POST'])
    def update_cliente(id):
        cliente = Cliente.query.get_or_404(id)
        data = request.json
        novo_nome = data.get('cliente')

        if novo_nome and novo_nome != cliente.cliente:
            # Verificar duplicado
            if Cliente.query.filter(Cliente.cliente == novo_nome, Cliente.id != id).first():
                return jsonify({'error': 'Já existe outro cliente com esse nome'}), 409
            cliente.cliente = novo_nome

        cliente.obsoleto = data.get('obsoleto', cliente.obsoleto)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Cliente atualizado com sucesso'})

    @app.route('/clientes/<int:id>', methods=['DELETE'])
    def delete_cliente(id):
        cliente = Cliente.query.get_or_404(id)
        usado_em_projetos = db.session.query(Projeto.id).filter(Projeto.cliente_id == id).exists()
        if db.session.query(usado_em_projetos).scalar():
            cliente.obsoleto = True
            db.session.commit()
            return jsonify({'success': True, 'message': 'Cliente marcado como obsoleto.'})
        else:
            db.session.delete(cliente)
            db.session.commit()
            return jsonify({'success': True, 'message': 'Cliente eliminado.'})

    @app.route('/localizacoes/<int:id>', methods=['DELETE'])
    def delete_localizacao(id):
        loc = Localizacao.query.get_or_404(id)

        # Pode eliminar
        db.session.delete(loc)
        db.session.commit()
        return jsonify({
            'success': True,
            'message': 'Localização eliminada.'
        })


    #######################################################################
    #SOLICITANTES
    @app.route('/solicitantes', methods=['GET'])
    def get_solicitantes():
        solicitantes = Solicitante.query.all()
        return jsonify({
            'data': [
                {
                    'id': s.id,
                    'nome': s.nome,
                    'email': s.email,
                    'obsoleto': s.obsoleto
                }
                for s in solicitantes
            ]
        })
    
    @app.route('/solicitantes', methods=['POST'])
    def add_solicitante():
        try:
            data = request.json
            nome = data.get('nome')
            email = data.get('email')
    
            # Validar campo obrigatório
            if not nome or not email:
                return jsonify({'error': 'Nome e email são obrigatórios'}), 400

            # Verificar duplicado
            if Solicitante.query.filter_by(nome=nome).first():
                return jsonify({'error': 'Já existe um solicitante com esse nome'}), 409
            
            # Verificar duplicado
            if Solicitante.query.filter_by(email=email).first():
                return jsonify({'error': 'Já existe um solicitante com esse email'}), 409

            novo = Solicitante(
                nome=nome,
                email=email,
                obsoleto=False
            )
            db.session.add(novo)
            db.session.commit()
            return jsonify({'success': True, 'message': 'Solicitante adicionado com sucesso'})
        
        except Exception as e:
            db.session.rollback()
            current_app.logger.error("Erro ao adicionar solicitante: %s", e)
            return jsonify({'error': f'Erro ao adicionar solicitante: {str(e)}'}), 500
    
    @app.route('/solicitantes/update/<int:id>', methods=['POST'])
    def update_solicitante(id):
        solicitante = Solicitante.query.get_or_404(id)
        data = request.json
    
        novo_nome = data.get('nome')
        if novo_nome and novo_nome != solicitante.nome:
            # Verificar duplicado
            if Solicitante.query.filter(Solicitante.nome == novo_nome, Solicitante.id != id).first():
                return jsonify({'error': 'Já existe outro solicitante com esse nome'}), 409
            solicitante.nome = novo_nome
    
        if 'email' in data:
            solicitante.email = data['email'] if data['email'] else None
        if 'obsoleto' in data:
            solicitante.obsoleto = data['obsoleto']
    
        db.session.commit()
        return jsonify({'success': True, 'message': 'Solicitante atualizado com sucesso'})
    
    @app.route('/solicitantes/<int:id>', methods=['DELETE'])
    def delete_solicitante(id):
        solicitante = Solicitante.query.get_or_404(id)
        
        # Aqui pode adicionar verificação se está a ser usado em ensaios
        # usado_em_ensaios = db.session.query(Ensaio.id).filter(Ensaio.solicitante_id == id).first()
        
        db.session.delete(solicitante)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Solicitante eliminado.'})
    

    
    #######################################################################
    #CÓDIGOS G
    @app.route('/codigosg', methods=['GET'])
    def get_codigosg():
        codigosg = Codigosg.query.all()
        return jsonify({
            'data': [
                {
                    'id': c.id,
                    'codigog': c.codigog,
                    'descricao': c.descricao,
                    'ano': c.ano,
                    'obsoleto': c.obsoleto
                }
                for c in codigosg
            ]
        })
    
    @app.route('/codigosg', methods=['POST'])
    def add_codigosg():
        try:
            data = request.json
            codigog = data.get('codigog')
            descricao = data.get('descricao')
            ano = data.get('ano')
    
            # Validar campo obrigatório
            if not codigog or not descricao:
                return jsonify({'error': 'Código G e descrição são obrigatórios'}), 400

            # Verificar duplicado
            if Codigosg.query.filter_by(codigog=codigog).first():
                return jsonify({'error': 'Já existe um código G com esse valor'}), 409
    
            novo = Codigosg(
                codigog=codigog,
                descricao=descricao,
                ano=int(ano) if ano else None,
                obsoleto=False
            )
            db.session.add(novo)
            db.session.commit()
            return jsonify({'success': True, 'message': 'Código G adicionado com sucesso'})
        
        except Exception as e:
            db.session.rollback()
            current_app.logger.error("Erro ao adicionar código G: %s", e)
            return jsonify({'error': f'Erro ao adicionar código G: {str(e)}'}), 500
    
    @app.route('/codigosg/update/<int:id>', methods=['POST'])
    def update_codigosg(id):
        codigosg = Codigosg.query.get_or_404(id)
        data = request.json
    
        novo_codigog = data.get('codigog')
        if novo_codigog and novo_codigog != codigosg.codigog:
            # Verificar duplicado
            if Codigosg.query.filter(Codigosg.codigog == novo_codigog, Codigosg.id != id).first():
                return jsonify({'error': 'Já existe outro código G com esse valor'}), 409
            codigosg.codigog = novo_codigog

        if 'descricao' in data:
            codigosg.descricao = data['descricao']
        if 'ano' in data:
            codigosg.ano = int(data['ano']) if data['ano'] else None
        if 'obsoleto' in data:
            codigosg.obsoleto = data['obsoleto']
    
        db.session.commit()
        return jsonify({'success': True, 'message': 'Código G atualizado com sucesso'})
    
    @app.route('/codigosg/<int:id>', methods=['DELETE'])
    def delete_codigosg(id):
        codigosg = Codigosg.query.get_or_404(id)
        
        # Aqui pode adicionar verificação se está a ser usado em ensaios
        # usado_em_ensaios = db.session.query(Ensaio.id).filter(Ensaio.codigosg_id == id).first()
        
        db.session.delete(codigosg)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Código G eliminado.'})


 
    
    #######################################################################
    #TESTES
    @app.route('/tipotestes', methods=['GET'])
    def get_tipotestes():
        tipotestes = Tipotestes.query.all()
        return jsonify({
            'data': [
                {
                    'id': t.id,
                    'teste': t.teste,
                    'laboratorio_id': t.laboratorio_id,
                    'laboratorio': t.laboratorio.laboratorio if t.laboratorio else '',
                    'criarpasta': t.criarpasta,
                    'mediveis': t.mediveis,
                    'obsoleto': t.obsoleto
                }
                for t in tipotestes
            ]
        })

    @app.route('/tipotestes', methods=['POST'])
    def add_tipoteste():
        try:
            data = request.json
            teste = data.get('teste')
            laboratorio_id = data.get('laboratorio_id')
            criarpasta = data.get('criarpasta')
            mediveis = data.get('mediveis')
            # Validar campos obrigatórios
            if not teste:
                return jsonify({'error': 'Teste é obrigatório'}), 400
            
            if not laboratorio_id:
                return jsonify({'error': 'Laboratório é obrigatório'}), 400
    
            # Verificar duplicado
            if Tipotestes.query.filter_by(teste=teste).first():
                return jsonify({'error': 'Já existe um teste com esse nome'}), 409

            novo = Tipotestes(
                teste=teste,
                laboratorio_id=int(laboratorio_id),
                criarpasta=criarpasta,
                mediveis=mediveis,
                obsoleto=False
            )
            db.session.add(novo)
            db.session.commit()
            return jsonify({'success': True, 'message': 'Teste adicionado com sucesso'})
        
        except Exception as e:
            db.session.rollback()
            current_app.logger.error("Erro ao adicionar teste: %s", e)
            return jsonify({'error': f'Erro ao adicionar teste: {str(e)}'}), 500

    @app.route('/testes/<int:id>', methods=['DELETE'])
    def delete_teste(id):
        teste = Testes.query.get_or_404(id)
    
        # 1) Bloqueia se já existe uso em horas
        existe_horas = db.session.query(Horas.id).filter(Horas.teste_id == id).first() is not None
        if existe_horas:
            return jsonify({
                'error': 'Não é possível eliminar: este teste já existe na tabela horas.'
            }), 409
    
        # 2) Bloqueia se já existe uso em reports
        existe_report = db.session.query(Report.id).filter(Report.teste_id == id).first() is not None
        if existe_report:
            return jsonify({
                'error': 'Não é possível eliminar: este teste já existe na tabela reports.'
            }), 409
    
        # 3) Se só houver pedidos, recusa automaticamente os pedidos pendentes
        pedidos_pendentes = PedidoHorasExtra.query.filter(
            PedidoHorasExtra.teste_id == id,
            PedidoHorasExtra.estado == 'Pendente'
        ).all()
    
        for p in pedidos_pendentes:
            p.estado = 'Recusado'
    
        db.session.delete(teste)
        db.session.commit()
    
        if pedidos_pendentes:
            return jsonify({
                'success': True,
                'message': f'Teste eliminado e {len(pedidos_pendentes)} pedido(s) marcado(s) como Recusado.'
            })
    
        return jsonify({'success': True, 'message': 'Teste eliminado.'})

    @app.route('/tipotestes/update/<int:id>', methods=['POST'])
    def update_tipoteste(id):
        tipoteste = Tipotestes.query.get_or_404(id)
        data = request.json
    
        novo_teste = data.get('teste')
        if novo_teste and novo_teste != tipoteste.teste:
            # Verificar duplicado
            if Tipotestes.query.filter(Tipotestes.teste == novo_teste, Tipotestes.id != id).first():
                return jsonify({'error': 'Já existe outro teste com esse nome'}), 409
            tipoteste.teste = novo_teste
        
        if 'laboratorio_id' in data:
            tipoteste.laboratorio_id = int(data['laboratorio_id'])
        if 'obsoleto' in data:
            tipoteste.obsoleto = data['obsoleto']
        if 'criarpasta' in data:
            tipoteste.criarpasta = data['criarpasta']
        if 'mediveis' in data:
            tipoteste.mediveis = data['mediveis']

        db.session.commit()
        return jsonify({'success': True, 'message': 'Teste atualizado com sucesso'})

    @app.route('/tipotestes/<int:id>', methods=['DELETE'])
    def delete_tipoteste(id):
        tipoteste = Tipotestes.query.get_or_404(id)
    
        # Verificar se está a ser usado em ensaios
        usado_em_ensaios = db.session.query(Ensaio.id).filter(Ensaio.tipoteste_id == id).first()
        if usado_em_ensaios:
            return jsonify({'error': 'Este tipo de teste está a ser usado em ensaios. Marque como obsoleto em vez de eliminar.'}), 400
    
        db.session.delete(tipoteste)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Teste eliminado.'})
    
    @app.route('/laboratorios/ativos')
    def get_laboratorios_ativos():
        laboratorios = Laboratorio.query.filter_by(obsoleto=False).all()
        return jsonify([{'id': lab.id, 'laboratorio': lab.laboratorio, 'elmact': lab.elmact, 'act': lab.act, 'pastatestes': lab.pastatestes, 'email': lab.email} for lab in laboratorios])
    


    #######################################################################
    #TIPOS DE PEÇA
    @app.route('/tipopecas', methods=['GET'])
    def get_tipopecas():
        tipopecas = Tipopeca.query.all()
        return jsonify({
            'data': [
                {
                    'id': t.id,
                    'tipopeca': t.tipopeca,
                    'obsoleto': t.obsoleto
                }
                for t in tipopecas
            ]
        })

    @app.route('/tipopecas', methods=['POST'])
    def add_tipopeca():
        try:
            data = request.json
            tipopeca = data.get('tipopeca')

            # Validar campo obrigatório
            if not tipopeca:
                return jsonify({'error': 'Tipo de peça é obrigatório'}), 400

            # Verificar duplicado
            if Tipopeca.query.filter_by(tipopeca=tipopeca).first():
                return jsonify({'error': 'Já existe um tipo de peça com esse nome'}), 409

            novo = Tipopeca(
                tipopeca=tipopeca,
                obsoleto=False
            )
            db.session.add(novo)
            db.session.commit()
            return jsonify({'success': True, 'message': 'Tipo de peça adicionado com sucesso'})
        
        except Exception as e:
            db.session.rollback()
            current_app.logger.error("Erro ao adicionar tipo de peça: %s", e)
            return jsonify({'error': f'Erro ao adicionar tipo de peça: {str(e)}'}), 500

    @app.route('/tipopecas/update/<int:id>', methods=['POST'])
    def update_tipopeca(id):
        tipopeca = Tipopeca.query.get_or_404(id)
        data = request.json

        novo_tipopeca = data.get('tipopeca')
        if novo_tipopeca and novo_tipopeca != tipopeca.tipopeca:
            # Verificar duplicado
            if Tipopeca.query.filter(Tipopeca.tipopeca == novo_tipopeca, Tipopeca.id != id).first():
                return jsonify({'error': 'Já existe outro tipo de peça com esse nome'}), 409
            tipopeca.tipopeca = novo_tipopeca

        if 'obsoleto' in data:
            tipopeca.obsoleto = data['obsoleto']

        db.session.commit()
        return jsonify({'success': True, 'message': 'Tipo de peça atualizado com sucesso'})

    @app.route('/tipopecas/<int:id>', methods=['DELETE'])
    def delete_tipopeca(id):
        tipopeca = Tipopeca.query.get_or_404(id)
        
        # Verificar se está a ser usado em projetos
        usado_em_projetos = db.session.query(Projeto.id).filter(Projeto.tipopeca_id == id).first()
        
        if usado_em_projetos:
            return jsonify({'error': 'Este tipo de peça está a ser usado em projetos. Marque como obsoleto em vez de eliminar.'}), 400
        
        db.session.delete(tipopeca)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Tipo de peça eliminado.'})

   
    #######################################################################
    #COMPONENTES
    @app.route('/componentes', methods=['GET'])
    def get_componentes():
        componentes = Componente.query.all()
        return jsonify({
            'data': [
                {
                    'id': t.id,
                    'componente': t.componente,
                    'obsoleto': t.obsoleto
                }
                for t in componentes
            ]
        })

    @app.route('/componentes', methods=['POST'])
    def add_componente():
        try:
            data = request.json
            componente = data.get('componente')

            # Validar campo obrigatório
            if not componente:
                return jsonify({'error': 'Componente é obrigatório'}), 400

            # Verificar duplicado
            if Componente.query.filter_by(componente=componente).first():
                return jsonify({'error': 'Já existe um componente com esse nome'}), 409

            novo = Componente(
                componente=componente,
                obsoleto=False
            )
            db.session.add(novo)
            db.session.commit()
            return jsonify({'success': True, 'message': 'Componente adicionado com sucesso'})
        
        except Exception as e:
            db.session.rollback()
            current_app.logger.error("Erro ao adicionar componente: %s", e)
            return jsonify({'error': f'Erro ao adicionar componente: {str(e)}'}), 500

    @app.route('/componentes/update/<int:id>', methods=['POST'])
    def update_componente(id):
        componente = Componente.query.get_or_404(id)
        data = request.json

        novo_componente = data.get('componente')
        if novo_componente and novo_componente != componente.componente:
            # Verificar duplicado
            if Componente.query.filter(Componente.componente == novo_componente, Componente.id != id).first():
                return jsonify({'error': 'Já existe outro componente com esse nome'}), 409
            componente.componente = novo_componente

        if 'obsoleto' in data:
            componente.obsoleto = data['obsoleto']

        db.session.commit()
        return jsonify({'success': True, 'message': 'Componente atualizado com sucesso'})

    @app.route('/componentes/<int:id>', methods=['DELETE'])
    def delete_componente(id):
        componente = Componente.query.get_or_404(id)
        
        db.session.delete(componente)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Componente eliminado.'})

    #######################################################################
    #COMPONENTES AE
    @app.route('/componentesae', methods=['GET'])
    def get_componentes_ae():
        componentesae = Componentesae.query.all()
        return jsonify({
            'data': [
                {
                    'id': t.id,
                    'codigo': t.codigo,
                    'nome': t.nome,
                    'obsoleto': t.obsoleto
                }
                for t in componentesae
            ]
        })

    @app.route('/componentesae', methods=['POST'])
    def add_componente_ae():
        try:
            data = request.json
            codigo = data.get('codigo')
            nome = data.get('nome')

            # Validar campo obrigatório
            if not codigo or not nome:
                return jsonify({'error': 'Código e Nome são obrigatórios'}), 400

            # Verificar duplicado
            if Componentesae.query.filter_by(codigo=codigo).first():
                return jsonify({'error': 'Já existe um componente com esse código'}), 409

            novo = Componentesae(
                codigo=codigo,
                nome=nome,
                obsoleto=False
            )
            db.session.add(novo)
            db.session.commit()
            return jsonify({'success': True, 'message': 'Componente adicionado com sucesso'})
        
        except Exception as e:
            db.session.rollback()
            current_app.logger.error("Erro ao adicionar componente: %s", e)
            return jsonify({'error': f'Erro ao adicionar componente: {str(e)}'}), 500

    @app.route('/componentesae/update/<int:id>', methods=['POST'])
    def update_componente_ae(id):
        componente = Componentesae.query.get_or_404(id)
        data = request.json

        novo_componente = data.get('componente')
        if novo_componente and novo_componente != componente.nome:
            # Verificar duplicado
            if Componentesae.query.filter(Componentesae.nome == novo_componente, Componentesae.id != id).first():
                return jsonify({'error': 'Já existe outro componente com esse nome'}), 409
            componente.nome = novo_componente

        if 'obsoleto' in data:
            componente.obsoleto = data['obsoleto']

        db.session.commit()
        return jsonify({'success': True, 'message': 'Componente atualizado com sucesso'})

    @app.route('/componentesae/<int:id>', methods=['DELETE'])
    def delete_componente_ae(id):
        componente = Componentesae.query.get_or_404(id)
        
        db.session.delete(componente)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Componente eliminado.'})
  
    #######################################################################
    #TIPO VOLUME AE
    @app.route('/tipovolumeae', methods=['GET'])
    def get_tipovolume_ae():
        tipovolumeae = Tipovolumeae.query.all()
        return jsonify({
            'data': [
                {
                    'id': t.id,
                    'nome': t.nome,
                    'obsoleto': t.obsoleto
                }
                for t in tipovolumeae
            ]
        })

    @app.route('/tipovolumeae', methods=['POST'])
    def add_tipovolume_ae():
        try:
            data = request.json
            nome = data.get('nome')

            # Validar campo obrigatório
            if not nome:
                return jsonify({'error': 'Nome é obrigatório'}), 400

            # Verificar duplicado
            if Tipovolumeae.query.filter_by(nome=nome).first():
                return jsonify({'error': 'Já existe um tipo de volume com esse nome'}), 409

            novo = Tipovolumeae(
                nome=nome,
                obsoleto=False
            )
            db.session.add(novo)
            db.session.commit()
            return jsonify({'success': True, 'message': 'Tipo de volume adicionado com sucesso'})
        
        except Exception as e:
            db.session.rollback()
            current_app.logger.error("Erro ao adicionar tipo de volume: %s", e)
            return jsonify({'error': f'Erro ao adicionar tipo de volume: {str(e)}'}), 500

    @app.route('/tipovolumeae/update/<int:id>', methods=['POST'])
    def update_tipovolume_ae(id):
        tipovolume = Tipovolumeae.query.get_or_404(id)
        data = request.json

        novo_nome = data.get('nome')
        if novo_nome and novo_nome != tipovolume.nome:
            # Verificar duplicado
            if Tipovolumeae.query.filter(Tipovolumeae.nome == novo_nome, Tipovolumeae.id != id).first():
                return jsonify({'error': 'Já existe outro tipo de volume com esse nome'}), 409
            tipovolume.nome = novo_nome

        if 'obsoleto' in data:
            tipovolume.obsoleto = data['obsoleto']

        db.session.commit()
        return jsonify({'success': True, 'message': 'Tipo de volume atualizado com sucesso'})

    @app.route('/tipovolumeae/<int:id>', methods=['DELETE'])
    def delete_tipovolume_ae(id):
        tipovolume = Tipovolumeae.query.get_or_404(id)
        
        db.session.delete(tipovolume)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Tipo de volume eliminado.'})

    #######################################################################
    #CODIFICACAO AE
    @app.route('/codificacaoae', methods=['GET'])
    def get_codificacao_ae():
        codificacaoae = Codificacaoae.query.all()
        return jsonify({
            'data': [
                {
                    'id': t.id,
                    'nome': t.nome,
                    'obsoleto': t.obsoleto
                }
                for t in codificacaoae
            ]
        })

    @app.route('/codificacaoae', methods=['POST'])
    def add_codificacao_ae():
        try:
            data = request.json
            nome = data.get('nome')

            # Validar campo obrigatório
            if not nome:
                return jsonify({'error': 'Nome é obrigatório'}), 400

            # Verificar duplicado
            if Codificacaoae.query.filter_by(nome=nome).first():
                return jsonify({'error': 'Já existe uma codificação com esse nome'}), 409

            novo = Codificacaoae(
                nome=nome,
                obsoleto=False
            )
            db.session.add(novo)
            db.session.commit()
            return jsonify({'success': True, 'message': 'Codificação adicionada com sucesso'})
        
        except Exception as e:
            db.session.rollback()
            current_app.logger.error("Erro ao adicionar codificação: %s", e)
            return jsonify({'error': f'Erro ao adicionar codificação: {str(e)}'}), 500

    @app.route('/codificacaoae/update/<int:id>', methods=['POST'])
    def update_codificacao_ae(id):
        codificacao = Codificacaoae.query.get_or_404(id)
        data = request.json

        novo_nome = data.get('nome')
        if novo_nome and novo_nome != codificacao.nome:
            # Verificar duplicado
            if Codificacaoae.query.filter(Codificacaoae.nome == novo_nome, Codificacaoae.id != id).first():
                return jsonify({'error': 'Já existe outra codificação com esse nome'}), 409
            codificacao.nome = novo_nome

        if 'obsoleto' in data:
            codificacao.obsoleto = data['obsoleto']

        db.session.commit()
        return jsonify({'success': True, 'message': 'Codificação atualizada com sucesso'})

    @app.route('/codificacaoae/<int:id>', methods=['DELETE'])
    def delete_codificacao_ae(id):
        codificacao = Codificacaoae.query.get_or_404(id)
        
        db.session.delete(codificacao)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Codificação eliminada.'})


    #######################################################################
    #MOTIVOS DE FALHA EM ENSAIOS
    @app.route('/motivosfalhaensaios', methods=['GET'])
    def get_motivos_falha_ensaios():
        """Retorna todos os motivos de falha em ensaios"""
        try:
            motivos = Motivosfalhaensaios.query.all()
            return jsonify({
                'data': [
                    {
                        'id': m.id,
                        'motivo': m.motivo,
                        'obsoleto': m.obsoleto
                    }
                    for m in motivos
                ]
            })
        except Exception as e:
            current_app.logger.error("Erro ao buscar motivos: %s", e)
            return jsonify({'error': str(e)}), 500
    
    @app.route('/motivosfalhaensaios', methods=['POST'])
    def add_motivo_falha_ensaios():
        """Adiciona um novo motivo de falha"""
        try:
            data = request.json
            motivo = data.get('motivo')
    
            # Validar campo obrigatório
            if not motivo:
                return jsonify({'error': 'Motivo é obrigatório'}), 400
    
            # Verificar duplicado
            if Motivosfalhaensaios.query.filter_by(motivo=motivo).first():
                return jsonify({'error': 'Já existe um motivo com esse nome'}), 409
    
            novo = Motivosfalhaensaios(
                motivo=motivo,
                obsoleto=data.get('obsoleto', False)
            )
            db.session.add(novo)
            db.session.commit()
            return jsonify({'success': True, 'message': 'Motivo adicionado com sucesso'})
        
        except Exception as e:
            db.session.rollback()
            current_app.logger.error("Erro ao adicionar motivo: %s", e)
            return jsonify({'error': f'Erro ao adicionar motivo: {str(e)}'}), 500
    
    @app.route('/motivosfalhaensaios/update/<int:id>', methods=['POST'])
    def update_motivo_falha_ensaios(id):
        """Atualiza um motivo de falha existente"""
        try:
            motivo = Motivosfalhaensaios.query.get_or_404(id)
            data = request.json
    
            novo_motivo = data.get('motivo')
            if novo_motivo and novo_motivo != motivo.motivo:
                # Verificar duplicado
                if Motivosfalhaensaios.query.filter(
                    Motivosfalhaensaios.motivo == novo_motivo, 
                    Motivosfalhaensaios.id != id
                ).first():
                    return jsonify({'error': 'Já existe outro motivo com esse nome'}), 409
                motivo.motivo = novo_motivo
    
            if 'obsoleto' in data:
                motivo.obsoleto = data['obsoleto']
    
            db.session.commit()
            return jsonify({'success': True, 'message': 'Motivo atualizado com sucesso'})
        
        except Exception as e:
            db.session.rollback()
            current_app.logger.error("Erro ao atualizar motivo: %s", e)
            return jsonify({'error': f'Erro ao atualizar: {str(e)}'}), 500
    
    @app.route('/motivosfalhaensaios/<int:id>', methods=['DELETE'])
    def delete_motivo_falha_ensaios(id):
        """Elimina um motivo de falha"""
        try:
            motivo = Motivosfalhaensaios.query.get_or_404(id)
    
            # Verificar se está a ser usado em ensaios (adapte conforme sua model Ensaio)
            # usado_em_ensaios = db.session.query(Ensaio.id).filter(Ensaio.motivo_falha_id == id).first()
            # 
            # if usado_em_ensaios:
            #     return jsonify({'error': 'Este motivo está a ser usado em ensaios. Marque como obsoleto em vez de eliminar.'}), 400
    
            db.session.delete(motivo)
            db.session.commit()
            return jsonify({'success': True, 'message': 'Motivo eliminado com sucesso'})
        
        except Exception as e:
            db.session.rollback()
            current_app.logger.error("Erro ao eliminar motivo: %s", e)
            return jsonify({'error': f'Erro ao eliminar: {str(e)}'}), 500
    
    #######################################################################
    #MOTIVOS DE ATRASO
    @app.route('/motivosatraso', methods=['GET'])
    def get_motivos_atraso():
        try:
            motivos = Motivosatraso.query.all()
            return jsonify({
                'data': [
                    {
                        'id': m.id,
                        'motivo': m.motivo,
                        'obsoleto': m.obsoleto
                    }
                    for m in motivos
                ]
            })
        except Exception as e:
            current_app.logger.error("Erro ao buscar motivos de atraso: %s", e)
            return jsonify({'error': str(e)}), 500
    
    @app.route('/motivosatraso', methods=['POST'])
    def add_motivo_atraso():
        try:
            data = request.json
            motivo = data.get('motivo')
    
            # Validar campo obrigatório
            if not motivo:
                return jsonify({'error': 'Motivo é obrigatório'}), 400
    
            # Verificar duplicado
            if Motivosatraso.query.filter_by(motivo=motivo).first():
                return jsonify({'error': 'Já existe um motivo com esse nome'}), 409
    
            novo = Motivosatraso(
                motivo=motivo,
                obsoleto=data.get('obsoleto', False)
            )
            db.session.add(novo)
            db.session.commit()
            return jsonify({'success': True, 'message': 'Motivo adicionado com sucesso'})
        
        except Exception as e:
            db.session.rollback()
            current_app.logger.error("Erro ao adicionar motivo de atraso: %s", e)
            return jsonify({'error': f'Erro ao adicionar motivo: {str(e)}'}), 500
    
    @app.route('/motivosatraso/update/<int:id>', methods=['POST'])
    def update_motivo_atraso(id):
        try:
            motivo = Motivosatraso.query.get_or_404(id)
            data = request.json
    
            novo_motivo = data.get('motivo')
            if novo_motivo and novo_motivo != motivo.motivo:
                # Verificar duplicado
                if Motivosatraso.query.filter(
                    Motivosatraso.motivo == novo_motivo, 
                    Motivosatraso.id != id
                ).first():
                    return jsonify({'error': 'Já existe outro motivo com esse nome'}), 409
                motivo.motivo = novo_motivo
    
            if 'obsoleto' in data:
                motivo.obsoleto = data['obsoleto']
    
            db.session.commit()
            return jsonify({'success': True, 'message': 'Motivo atualizado com sucesso'})
        
        except Exception as e:
            db.session.rollback()
            current_app.logger.error("Erro ao atualizar motivo de atraso: %s", e)
            return jsonify({'error': f'Erro ao atualizar: {str(e)}'}), 500
    
    @app.route('/motivosatraso/<int:id>', methods=['DELETE'])
    def delete_motivo_atraso(id):
        """Elimina um motivo de atraso"""
        try:
            motivo = Motivosatraso.query.get_or_404(id)
    
            db.session.delete(motivo)
            db.session.commit()
            return jsonify({'success': True, 'message': 'Motivo eliminado com sucesso'})
        
        except Exception as e:
            db.session.rollback()
            current_app.logger.error("Erro ao eliminar motivo de atraso: %s", e)
            return jsonify({'error': f'Erro ao eliminar: {str(e)}'}), 500
    

    #######################################################################
    #FASES
    @app.route('/fases', methods=['GET'])
    def get_fases():
        fases = Fase.query.all()
        return jsonify({
            'data': [
                {
                    'id': f.id,
                    'fase': f.fase,
                    'sucatearmod': f.sucatearmod,
                    'sucateartrims': f.sucateartrims,
                    'obsoleto': f.obsoleto
                }
                for f in fases
            ]
        })
    
    @app.route('/fases', methods=['POST'])
    def add_fase():
        try:
            data = request.json
            fase = data.get('fase')
    
            # Validar campo obrigatório
            if not fase:
                return jsonify({'error': 'Fase é obrigatória'}), 400
    
            # Verificar duplicado
            if Fase.query.filter_by(fase=fase).first():
                return jsonify({'error': 'Já existe uma fase com esse nome'}), 409
    
            novo = Fase(
                fase=fase,
                sucatearmod=data.get('sucatearmod'),
                sucateartrims=data.get('sucateartrims'),
                obsoleto=False
            )
            db.session.add(novo)
            db.session.commit()
            return jsonify({'success': True, 'message': 'Fase adicionada com sucesso'})
        
        except Exception as e:
            db.session.rollback()
            current_app.logger.error("Erro ao adicionar fase: %s", e)
            return jsonify({'error': f'Erro ao adicionar fase: {str(e)}'}), 500
    
    @app.route('/fases/update/<int:id>', methods=['POST'])
    def update_fase(id):
        fase = Fase.query.get_or_404(id)
        data = request.json
    
        nova_fase = data.get('fase')
        if nova_fase and nova_fase != fase.fase:
            # Verificar duplicado
            if Fase.query.filter(Fase.fase == nova_fase, Fase.id != id).first():
                return jsonify({'error': 'Já existe outra fase com esse nome'}), 409
            fase.fase = nova_fase
    
        if 'sucatearmod' in data:
            fase.sucatearmod = data['sucatearmod']
        if 'sucateartrims' in data:
            fase.sucateartrims = data['sucateartrims']
        if 'obsoleto' in data:
            fase.obsoleto = data['obsoleto']
    
        db.session.commit()
        return jsonify({'success': True, 'message': 'Fase atualizada com sucesso'})
    
    @app.route('/fases/<int:id>', methods=['DELETE'])
    def delete_fase(id):
        fase = Fase.query.get_or_404(id)
    
        usado_em_ensaios = db.session.query(Ensaio.id).filter(Ensaio.fase_id == id).first()
        if usado_em_ensaios:
            return jsonify({
                'error': 'Esta fase não pode ser eliminada porque está a ser usada em ensaios.'
            }), 409
    
        db.session.delete(fase)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Fase eliminada.'})
    
     
    #######################################################################
    #LABORATÓRIOS - CRUD para a tabela laboratorios

    @app.route('/laboratorios', methods=['GET'])
    def get_laboratorios():
        try:
            labs = Laboratorio.query.all()
            return jsonify({
                'data': [
                    {
                        'id': l.id,
                        'laboratorio': l.laboratorio,
                        'elmact': l.elmact,
                        'act': l.act,
                        'pastatestes': l.pastatestes,
                        'email': l.email,
                        'obsoleto': bool(l.obsoleto)
                    } for l in labs
                ]
            })
        except Exception as e:
            current_app.logger.error("Erro ao buscar laboratórios: %s", e)
            return jsonify({'error': str(e)}), 500

    @app.route('/laboratorios', methods=['POST'])
    def add_laboratorio():
        try:
            data = request.get_json(silent=True) or {}
            nome = (data.get('laboratorio') or '').strip()
            elmact = data.get('elmact')
            act = data.get('act')
            pastatestes = (data.get('pastatestes') or '').strip()
            email = data.get('email')
            obsoleto = bool(data.get('obsoleto', False))

            if not nome:
                return jsonify({'error': 'Nome do laboratório é obrigatório'}), 400

            # duplicado
            if Laboratorio.query.filter(Laboratorio.laboratorio == nome).first():
                return jsonify({'error': 'Já existe um laboratório com esse nome'}), 409

            novo = Laboratorio(
                laboratorio=nome,
                elmact=int(elmact) if elmact not in (None, '') else None,
                act=int(act) if act not in (None, '') else None,
                pastatestes=pastatestes,
                email=email,
                obsoleto=obsoleto
            )
            db.session.add(novo)
            db.session.commit()
            return jsonify({'success': True, 'message': 'Laboratório adicionado com sucesso', 'id': novo.id})
        except Exception as e:
            db.session.rollback()
            current_app.logger.error("Erro ao adicionar laboratório: %s", e)
            return jsonify({'error': str(e)}), 500

    @app.route('/laboratorios/update/<int:id>', methods=['POST'])
    def update_laboratorio(id):
        try:
            lab = Laboratorio.query.get_or_404(id)
            data = request.get_json(silent=True) or {}

            # atualizar nome (verificar duplicado)
            if 'laboratorio' in data:
                novo_nome = (data.get('laboratorio') or '').strip()
                if not novo_nome:
                    return jsonify({'error': 'Nome do laboratório não pode ficar vazio'}), 400
                if novo_nome != lab.laboratorio and Laboratorio.query.filter(Laboratorio.laboratorio == novo_nome, Laboratorio.id != id).first():
                    return jsonify({'error': 'Já existe outro laboratório com esse nome'}), 409
                lab.laboratorio = novo_nome

            if 'elmact' in data:
                lab.elmact = int(data['elmact']) if data['elmact'] not in (None, '') else None

            if 'act' in data:
                lab.act = int(data['act']) if data['act'] not in (None, '') else None
            
            if 'pastatestes' in data:
                lab.pastatestes = (data.get('pastatestes') or '').strip()

            if 'email' in data:
                lab.email = (data.get('email') or '').strip()

            if 'obsoleto' in data:
                lab.obsoleto = bool(data['obsoleto'])

            db.session.commit()
            return jsonify({'success': True, 'message': 'Laboratório atualizado com sucesso'})
        except Exception as e:
            db.session.rollback()
            current_app.logger.error("Erro ao atualizar laboratório: %s", e)
            return jsonify({'error': str(e)}), 500

    @app.route('/laboratorios/<int:id>', methods=['DELETE'])
    def delete_laboratorio(id):
        try:
            lab = Laboratorio.query.get_or_404(id)

            # Se estiver a ser usado noutras tabelas, marcar obsoleto em vez de eliminar
            usado = False
            if Tipotestes.query.filter_by(laboratorio_id=id).first():
                usado = True
            if Maquina.query.filter_by(laboratorio_id=id).first():
                usado = True
            if User.query.filter_by(laboratorio_id=id).first():
                usado = True

            if usado:
                lab.obsoleto = True
                db.session.commit()
                return jsonify({'success': True, 'message': 'Laboratório marcado como obsoleto (está em uso).'})
            else:
                db.session.delete(lab)
                db.session.commit()
                return jsonify({'success': True, 'message': 'Laboratório eliminado.'})
        except Exception as e:
            db.session.rollback()
            current_app.logger.error("Erro ao eliminar laboratório: %s", e)
            return jsonify({'error': str(e)}), 500

 
    #######################################################################
    #USERS
    @app.route('/users', methods=['GET'])
    def get_users():
        users = User.query.all()
        return jsonify({'data': [
            {
                'id': u.id,
                'username': u.username,
                'full_name': u.full_name,
                'email': u.email,
                'funcao_id': u.funcao_id,
                'funcao': u.funcao.funcao if u.funcao else '',
                'laboratorio_id': u.laboratorio_id,
                'laboratorio': u.laboratorio.laboratorio if u.laboratorio else '',
                'obsoleto': u.obsoleto
            } for u in users
        ]})
    
    @app.route('/users', methods=['POST'])
    def add_user():
        try:
            data = request.json
            required = ['username','full_name','email','funcao_id','laboratorio_id']
            if any(not data.get(f) for f in required):
                return jsonify({'error':'Todos os campos são obrigatórios'}), 400
            # opcional: validar duplicado username/email
            if User.query.filter_by(username=data['username']).first():
                return jsonify({'error':'Username já existe'}), 409
            if User.query.filter_by(email=data['email']).first():
                return jsonify({'error':'Email já existe'}), 409
            novo = User(
                username=data['username'],
                full_name=data['full_name'],
                email=data['email'],
                funcao_id=int(data['funcao_id']),
                laboratorio_id=int(data['laboratorio_id']),
                obsoleto=data.get('obsoleto', False)
            )
            db.session.add(novo)
            db.session.commit()
            return jsonify({'message':'Utilizador criado com sucesso'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'error':f'Erro ao criar: {e}'}), 500
    
    @app.route('/users/update/<int:id>', methods=['POST'])
    def update_user(id):
        user = User.query.get_or_404(id)
        data = request.json
        if 'username' in data and data['username'] and data['username'] != user.username:
            if User.query.filter(User.username==data['username'], User.id!=id).first():
                return jsonify({'error':'Username duplicado'}), 409
            user.username = data['username']
        if 'full_name' in data:
            user.full_name = data['full_name'] or ''
        if 'email' in data and data['email'] and data['email'] != user.email:
            if User.query.filter(User.email==data['email'], User.id!=id).first():
                return jsonify({'error':'Email duplicado'}), 409
            user.email = data['email']
        if 'funcao_id' in data and data['funcao_id']:
            user.funcao_id = int(data['funcao_id'])
        if 'laboratorio_id' in data and data['laboratorio_id']:
            user.laboratorio_id = int(data['laboratorio_id'])
        if 'obsoleto' in data:
            user.obsoleto = data['obsoleto']
        db.session.commit()
        return jsonify({'message':'Utilizador atualizado'})
    
    @app.route('/users/<int:id>', methods=['DELETE'])
    def delete_user(id):
        user = User.query.get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message':'Utilizador eliminado'})
    
    @app.route('/funcoes/ativos')
    def get_funcoes_ativos():
        funcoes = Funcao.query.filter_by(obsoleto=False).all()
        return jsonify([{'id': f.id, 'funcao': f.funcao} for f in funcoes])
    

    #######################################################################
    #NORMAS
    @app.route('/normas', methods=['GET'])
    def get_normas():
        normas = Normas.query.all()
        return jsonify({
            'data': [
                {
                    'id': n.id,
                    'norma': n.norma,
                    'laboratorio_id': n.laboratorio_id,
                    'laboratorio': n.laboratorio.laboratorio if n.laboratorio else '',
                    'obsoleto': n.obsoleto
                }
                for n in normas
            ]
        })

    @app.route('/api/normas_todas', methods=['GET'])
    def api_normas_todas():
        normas = Normas.query.all()
        return jsonify([
            {
                'id': n.id,
                'norma': n.norma,
                'laboratorio_id': n.laboratorio_id,
                'laboratorio': n.laboratorio.laboratorio if n.laboratorio else '',
                'obsoleto': n.obsoleto
            }
            for n in normas
        ])
    
    @app.route('/normas', methods=['POST'])
    def add_norma():
        try:
            data = request.json
            norma = data.get('norma')
            laboratorio_id = data.get('laboratorio_id')
    
            # Validar campo obrigatório
            if not norma:
                return jsonify({'error': 'Norma é obrigatória'}), 400
    
            # Verificar duplicado
            if Normas.query.filter_by(norma=norma).first():
                return jsonify({'error': 'Já existe uma norma com esse nome'}), 409
    
            nova = Normas(
                norma=norma,
                laboratorio_id=int(laboratorio_id) if laboratorio_id else None,
                obsoleto=False
            )
            db.session.add(nova)
            db.session.commit()
            return jsonify({'success': True, 'message': 'Norma adicionada com sucesso'})
        
        except Exception as e:
            db.session.rollback()
            current_app.logger.error("Erro ao adicionar norma: %s", e)
            return jsonify({'error': f'Erro ao adicionar norma: {str(e)}'}), 500
    
    @app.route('/normas/update/<int:id>', methods=['POST'])
    def update_norma(id):
        norma = Normas.query.get_or_404(id)
        data = request.json
    
        nova_norma = data.get('norma')
        if nova_norma and nova_norma != norma.norma:
            # Verificar duplicado
            if Normas.query.filter(Normas.norma == nova_norma, Normas.id != id).first():
                return jsonify({'error': 'Já existe outra norma com esse nome'}), 409
            norma.norma = nova_norma

        if 'laboratorio_id' in data:
            try:
                norma.laboratorio_id = int(data['laboratorio_id']) if data['laboratorio_id'] else None
            except Exception:
                norma.laboratorio_id = None
    
        if 'obsoleto' in data:
            norma.obsoleto = data['obsoleto']
    
        db.session.commit()
        return jsonify({'success': True, 'message': 'Norma atualizada com sucesso'})
    
    @app.route('/normas/<int:id>', methods=['DELETE'])
    def delete_norma(id):
        norma = Normas.query.get_or_404(id)
        
        # Aqui pode adicionar verificação se está a ser usado em ensaios
        
        db.session.delete(norma)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Norma eliminada.'})
    
#######################################################################
# TEMPLATE NORMAS

    @app.route('/templatenormas/<int:norma_id>', methods=['GET'])
    def get_templatenormas_by_norma(norma_id):

        try:
            
            templates = Templatenormas.query.filter_by(norma_id=norma_id)\
                .order_by(Templatenormas.ordem).all()
            
            return jsonify([
                {
                    'id': t.id,
                    'norma_id': t.norma_id,
                    'teste_id': t.teste_id,
                    'teste': t.teste.teste if t.teste else '',
                    'ordem': t.ordem,
                    'duracao': t.duracao,
                    'duracaomontagem': t.duracaomontagem,
                    'tempopp': t.tempopp,
                    'tempomp': t.tempomp,
                    'obsoleto': t.obsoleto
                }
                for t in templates
            ])
        except Exception as e:
            current_app.logger.error("Erro ao buscar template normas: %s", e)
            return jsonify({'error': str(e)}), 500

    @app.route('/templatenormas', methods=['POST'])
    def add_templatenorma():
        try:
            data = request.json
            
            norma_id = data.get('norma_id')
            teste_id = data.get('teste_id')
            ordem = data.get('ordem')
            
            # Validar campos obrigatórios
            if not norma_id or not teste_id:
                return jsonify({'error': 'Norma e teste são obrigatórios'}), 400
            
            # Se não veio ordem, calcular a próxima
            if not ordem:
                max_ordem = db.session.query(db.func.max(Templatenormas.ordem))\
                    .filter_by(norma_id=norma_id).scalar()
                ordem = (max_ordem or 0) + 1
            
            novo = Templatenormas(
                norma_id=norma_id,
                teste_id=teste_id,
                ordem=ordem,
                duracao=data.get('duracao'),
                duracaomontagem=data.get('duracaomontagem'),
                tempopp=data.get('tempopp'),
                tempomp=data.get('tempomp'),
                obsoleto=False
            )
            
            db.session.add(novo)
            db.session.commit()
            
            return jsonify({
                'success': True, 
                'message': 'Teste adicionado à norma com sucesso',
                'id': novo.id
            })
        
        except Exception as e:
            db.session.rollback()
            current_app.logger.error("Erro ao adicionar template norma: %s", e)
            return jsonify({'error': f'Erro ao adicionar: {str(e)}'}), 500

    @app.route('/templatenormas/update/<int:id>', methods=['POST'])
    def update_templatenorma(id):
        try:
            template = Templatenormas.query.get_or_404(id)
            data = request.json
            
            # Atualizar teste
            if 'teste_id' in data:
                novo_teste_id = data['teste_id']
                
                
                
                template.teste_id = novo_teste_id
            
            # Atualizar campos numéricos
            if 'duracao' in data:
                template.duracao = data['duracao']
            
            if 'duracaomontagem' in data:
                template.duracaomontagem = data['duracaomontagem']
            
            if 'tempopp' in data:
                template.tempopp = data['tempopp']

            if 'tempomp' in data:
                template.tempomp = data['tempomp']
            
            if 'ordem' in data:
                template.ordem = data['ordem']
            
            if 'obsoleto' in data:
                template.obsoleto = data['obsoleto']
            
            db.session.commit()
            return jsonify({'success': True, 'message': 'Template atualizado com sucesso'})
        
        except Exception as e:
            db.session.rollback()
            current_app.logger.error("Erro ao atualizar template norma: %s", e)
            return jsonify({'error': f'Erro ao atualizar: {str(e)}'}), 500

    @app.route('/templatenormas/ordem', methods=['POST'])
    def update_ordem_templates():

        try:
        
            data = request.json
            testes = data.get('testes', [])
            
            # Atualizar ordem de cada teste
            for item in testes:
                template_id = item.get('id')
                nova_ordem = item.get('ordem')
                
                if template_id and nova_ordem:
                    template = Templatenormas.query.get(template_id)
                    if template:
                        template.ordem = nova_ordem
            
            db.session.commit()
            return jsonify({'success': True, 'message': 'Ordem atualizada com sucesso'})
        
        except Exception as e:
            db.session.rollback()
            current_app.logger.error("Erro ao atualizar ordem: %s", e)
            return jsonify({'error': f'Erro ao atualizar ordem: {str(e)}'}), 500

    @app.route('/templatenormas/<int:id>', methods=['DELETE'])
    def delete_templatenorma(id):

        try:

            template = Templatenormas.query.get_or_404(id)
            
            norma_id = template.norma_id
            ordem_deletada = template.ordem
            
            # Deletar o registro
            db.session.delete(template)
            
            # Reorganizar ordem dos testes restantes
            templates_restantes = Templatenormas.query.filter(
                Templatenormas.norma_id == norma_id,
                Templatenormas.ordem > ordem_deletada
            ).all()
            
            for t in templates_restantes:
                t.ordem -= 1
            
            db.session.commit()
            return jsonify({'success': True, 'message': 'Teste removido da norma'})
        
        except Exception as e:
            db.session.rollback()
            current_app.logger.error("Erro ao deletar template norma: %s", e)
            return jsonify({'error': f'Erro ao deletar: {str(e)}'}), 500

    @app.route('/normas/ativos', methods=['GET'])
    def get_normas_ativos():

        try:
            normas = Normas.query.filter_by(obsoleto=False).order_by(Normas.norma).all()
            return jsonify([
                {
                    'id': n.id,
                    'norma': n.norma
                }
                for n in normas
            ])
        except Exception as e:
            current_app.logger.error("Erro ao buscar normas ativas: %s", e)
            return jsonify({'error': str(e)}), 500

    @app.route('/tipotestes/ativos', methods=['GET'])
    def get_tipotestes_ativos():

        try:
            testes = Tipotestes.query.filter_by(obsoleto=False).order_by(Tipotestes.teste).all()
            return jsonify([
                {
                    'id': t.id,
                    'teste': t.teste,
                    'laboratorio_id': t.laboratorio_id
                }
                for t in testes
            ])
        except Exception as e:
            current_app.logger.error("Erro ao buscar testes ativos: %s", e)
            return jsonify({'error': str(e)}), 500

        
    @app.route('/templatenormas/import', methods=['POST'])
    def import_templatenormas():
        try:
            data = request.get_json(silent=True) or {}
            source_id = data.get('source_norma_id')
            target_id = data.get('target_norma_id')
    
            if not source_id or not target_id:
                return jsonify({'error': 'Source e target são obrigatórios.'}), 400
            if int(source_id) == int(target_id):
                return jsonify({'error': 'Source e target não podem ser a mesma norma.'}), 400
    
            source_norma = Normas.query.get(int(source_id))
            target_norma = Normas.query.get(int(target_id))
            if not source_norma or not target_norma:
                return jsonify({'error': 'Norma source ou target não encontrada.'}), 404
    
            source_entries = Templatenormas.query.filter_by(
                norma_id=int(source_id)
            ).order_by(Templatenormas.ordem).all()
    
            if not source_entries:
                return jsonify({'error': 'A norma de origem não tem testes para importar.'}), 400
    
            # Acrescenta ao fim da lista existente na norma de destino
            max_ordem = db.session.query(func.max(Templatenormas.ordem)).filter_by(
                norma_id=int(target_id)
            ).scalar()
            ordem_inicial = max_ordem or 0
    
            imported = 0
            for idx, s in enumerate(source_entries):
                novo = Templatenormas(
                    norma_id=int(target_id),
                    teste_id=s.teste_id,
                    ordem=ordem_inicial + idx + 1,
                    duracao=s.duracao,
                    duracaomontagem=getattr(s, 'duracaomontagem', None),
                    tempopp=getattr(s, 'tempopp', None),
                    tempomp=getattr(s, 'tempomp', None)
                )
                db.session.add(novo)
                imported += 1
    
            db.session.commit()
            msg = f'Importados {imported} testes da norma {source_id} para {target_id}. (Os testes existentes foram mantidos)'
            return jsonify({'success': True, 'message': msg})
    
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Erro ao importar template normas: {e}")
            return jsonify({'error': str(e)}), 500
    

#######################################################################
# MAQUINAS
    @app.route('/maquinas', methods=['GET'])
    def get_maquinas():
        try:
            maquinas = Maquina.query.all()
            return jsonify({
                'data': [
                    {
                        'id': m.id,
                        'codigo': m.codigo,
                        'nome': m.nome,
                        'codsaphoras': m.codsaphoras,
                        'codsappecas': m.codsappecas,
                        'laboratorio_id': m.laboratorio_id,
                        'custo': m.custo,
                        'obsoleto': m.obsoleto
                    } for m in maquinas
                ]
            })
        except Exception as e:
            current_app.logger.error("Erro ao buscar máquinas: %s", e)
            return jsonify({'error': str(e)}), 500

    @app.route('/maquinas', methods=['POST'])
    def add_maquina():
        try:
            data = request.json or {}
            codigo = data.get('codigo')
            nome = data.get('nome')

            if not codigo or not nome:
                return jsonify({'error': 'Código e Nome são obrigatórios'}), 400

            # opcional: evitar códigos duplicados
            if Maquina.query.filter_by(codigo=codigo).first():
                return jsonify({'error': 'Já existe uma máquina com esse código'}), 409

            nova = Maquina(
                codigo=codigo,
                nome=nome,
                codsaphoras=data.get('codsaphoras'),
                codsappecas=data.get('codsappecas'),
                laboratorio_id=data.get('laboratorio_id'),
                custo=data.get('custo'),
                obsoleto=data.get('obsoleto', False)
            )
            db.session.add(nova)
            db.session.commit()
            return jsonify({'success': True, 'message': 'Máquina adicionada com sucesso'})
        except Exception as e:
            db.session.rollback()
            current_app.logger.error("Erro ao adicionar máquina: %s", e)
            return jsonify({'error': f'Erro ao adicionar: {str(e)}'}), 500

    @app.route('/maquinas/update/<int:id>', methods=['POST'])
    def update_maquina(id):
        try:
            maq = Maquina.query.get_or_404(id)
            data = request.json or {}

            if 'codigo' in data and data['codigo'] and data['codigo'] != maq.codigo:
                if Maquina.query.filter(Maquina.codigo == data['codigo'], Maquina.id != id).first():
                    return jsonify({'error': 'Já existe outra máquina com esse código'}), 409
                maq.codigo = data['codigo']

            if 'nome' in data and data['nome']:
                maq.nome = data['nome']
            if 'codsaphoras' in data:
                maq.codsaphoras = data['codsaphoras']
            if 'codsappecas' in data:
                maq.codsappecas = data['codsappecas']
            if 'laboratorio_id' in data:
                maq.laboratorio_id = data['laboratorio_id']
            if 'custo' in data:
                maq.custo = data['custo']
            if 'obsoleto' in data:
                maq.obsoleto = bool(data['obsoleto'])

            db.session.commit()
            return jsonify({'success': True, 'message': 'Máquina atualizada com sucesso'})
        except Exception as e:
            db.session.rollback()
            current_app.logger.error("Erro ao atualizar máquina: %s", e)
            return jsonify({'error': f'Erro ao atualizar: {str(e)}'}), 500

    @app.route('/maquinas/<int:id>', methods=['DELETE'])
    def delete_maquina(id):
        try:
            maq = Maquina.query.get_or_404(id)

            # Se existir relação futura (ex.: ensaios), validar uso antes de eliminar

            db.session.delete(maq)
            db.session.commit()
            return jsonify({'success': True, 'message': 'Máquina eliminada com sucesso'})
        except Exception as e:
            db.session.rollback()
            current_app.logger.error("Erro ao eliminar máquina: %s", e)
            return jsonify({'error': f'Erro ao eliminar: {str(e)}'}), 500



################################################################################
#COMBOS FORM ENSAIOS
  
    @app.route('/projetos/ativos', methods=['GET'])
    def get_projetos_ativos():
        """Retorna projetos ativos para as combos"""
        try:
            projetos = Projeto.query.filter_by(obsoleto=False).order_by(Projeto.codigo).all() 
            return jsonify([
                {
                    'id': p.id,
                    'projeto': p.codigo,  
                    'cliente_id': p.cliente_id,
                    'tipopeca_id': p.tipopeca_id,
                    'descricao': p.descricao,
                    'torque': p.torque,
                    'testfixture': p.testfixture
                } for p in projetos
            ])
        except Exception as e:
            current_app.logger.error(f"Erro ao buscar projetos ativos: {e}")
            return jsonify({'error': str(e)}), 500
    


    @app.route('/solicitantes/ativos', methods=['GET'])
    def get_solicitantes_ativos():
        """Retorna solicitantes ativos com email"""
        try:
            solicitantes = Solicitante.query.filter_by(obsoleto=False).order_by(Solicitante.nome).all()
            return jsonify([
                {
                    'id': s.id,
                    'nome': s.nome,
                    'email': s.email
                } for s in solicitantes
            ])
        except Exception as e:
            current_app.logger.error(f"Erro ao buscar solicitantes ativos: {e}")
            return jsonify({'error': str(e)}), 500

    @app.route('/normas/ativas', methods=['GET'])
    def get_normas_ativas():
        try:
            normas = Normas.query.filter_by(obsoleto=False).order_by(Normas.norma).all()
            return jsonify([
                {
                    'id': n.id,
                    'norma': n.norma
                }
                for n in normas
            ])
        except Exception as e:
            current_app.logger.error("Erro ao buscar normas ativas: %s", e)
            return jsonify({'error': str(e)}), 500


    @app.route('/ensaios', methods=['GET', 'POST'])
    @login_required  
    def ensaios():
        if request.method == 'POST':
            try:
                # Buscar dados do formulário
                ensaio_numero = request.form.get('ensaio')
                laboratorio_id = request.form.get('laboratorio_id')
                norma_id = request.form.get('norma_id') or None
                npecasrecebidas = request.form.get('npecasrecebidas') or None
                destinopecas = request.form.get('destino_pecas') or None
                destinodevol = request.form.get('destinodevol') or None
                moradadevol = request.form.get('moradadevol') or None
                datapedido = request.form.get('datapedido')
                datasolicitada = request.form.get('data_solicitada') or None
                dataentregapecas = request.form.get('data_entrega_pecas') or None
                dataacordada = request.form.get('data_acordada') or None
                pep = request.form.get('pep') or None
                network = request.form.get('network') or None
                partnzf = request.form.get('part_number') or None
                partncliente = request.form.get('partnumbercli') or None
                cliente_id = request.form.get('cliente_id') or None
                projeto_id = request.form.get('projecto_id') or None
                tipopeca_id = request.form.get('tipopeca_id') or None
                fase_id = request.form.get('fase_id') or None
                corecustomer = request.form.get('corecustomer') or "Customer"
                atrasado = request.form.get('atrasado') or None
                motivoatraso_id = request.form.get('motivoatraso_id') or None
                solicitante_id = request.form.get('solicitante_id') or None
                user_id = request.form.get('tecnico_id') or None
                prefixo = request.form.get('prefixo') or None
                primeirapeca = request.form.get('primeira_peca') or None
    
                # Validações obrigatórias
                if not ensaio_numero:
                    flash('Número de ensaio é obrigatório', 'error')
                    return redirect(url_for('ensaios'))
                if not laboratorio_id:
                    flash('Laboratório é obrigatório', 'error')
                    return redirect(url_for('ensaios'))
                if not datapedido:
                    flash('Data de pedido é obrigatória', 'error')
                    return redirect(url_for('ensaios'))
    
                # Verificar se já existe ensaio com este número
                ensaio_existe = Ensaio.query.filter_by(ensaio=ensaio_numero).first()
                if ensaio_existe:
                    flash('Já existe um ensaio com este número', 'error')
                    return redirect(url_for('ensaios'))
    
                # Converter strings vazias em None e números
                if npecasrecebidas:
                    npecasrecebidas = int(npecasrecebidas)
                if primeirapeca:
                    primeirapeca = int(primeirapeca)
    
                # Criar novo ensaio
                novo_ensaio = Ensaio(
                    ensaio=ensaio_numero,
                    laboratorio_id=int(laboratorio_id),
                    norma_id=int(norma_id) if norma_id else None,
                    npecasrecebidas=npecasrecebidas,
                    destinopecas=destinopecas,
                    destinodevol=destinodevol,
                    moradadevol=moradadevol,
                    datapedido=datapedido,
                    datasolicitada=datasolicitada,
                    dataentregapecas=dataentregapecas,
                    dataacordada=dataacordada,
                    pep=pep,
                    network=network,
                    partnzf=partnzf,
                    partncliente=partncliente,
                    cliente_id=int(cliente_id) if cliente_id else None,
                    projeto_id=int(projeto_id) if projeto_id else None,
                    tipopeca_id=int(tipopeca_id) if tipopeca_id else None,
                    fase_id=int(fase_id) if fase_id else None,
                    corecustomer=corecustomer,
                    atrasado=atrasado,
                    motivoatraso_id=int(motivoatraso_id) if motivoatraso_id else None,
                    solicitante_id=int(solicitante_id) if solicitante_id else None,
                    user_id=int(user_id) if user_id else None,
                    prefixo=prefixo,
                    primeirapeca=primeirapeca,
                    anulado=False
                )
    
                db.session.add(novo_ensaio)
                db.session.commit()
    
                flash('Ensaio criado com sucesso!', 'success')
                return redirect(url_for('ensaios'))
    
            except ValueError as ve:
                db.session.rollback()
                current_app.logger.error(f"Erro de validação ao criar ensaio: {ve}")
                flash('Erro nos dados fornecidos. Verifique os campos numéricos.', 'error')
                return redirect(url_for('ensaios'))
            
            except Exception as e:
                db.session.rollback()
                current_app.logger.error(f"Erro ao criar ensaio: {e}")
                flash(f'Erro ao criar ensaio: {str(e)}', 'error')
                return redirect(url_for('ensaios'))
    
        # GET - Carregar dados para o formulário (novo ou edição)
        try:
            user = User.query.get(session['user_id'])
            clientes = Cliente.query.filter_by(obsoleto=False).order_by(Cliente.cliente).all()
            solicitantes = Solicitante.query.filter_by(obsoleto=False).order_by(Solicitante.nome).all()
            tipopecas = Tipopeca.query.filter_by(obsoleto=False).order_by(Tipopeca.tipopeca).all()
            fases = Fase.query.filter_by(obsoleto=False).order_by(Fase.fase).all()
            tecnicos = User.query.join(Funcao).filter(
                User.obsoleto == False,
                Funcao.funcao != 'Sistema'
            ).order_by(User.full_name).all()
            laboratorios = Laboratorio.query.filter_by(obsoleto=False).order_by(Laboratorio.laboratorio).all()
            normas = Normas.query.filter_by(obsoleto=False).order_by(Normas.norma).all()
    
            # NOVO: buscar ensaio se vier na query string
            ensaio_numero = request.args.get('ensaio')
            ensaio_selecionado = None
            if ensaio_numero:
                ensaio_selecionado = Ensaio.query.filter_by(ensaio=ensaio_numero).first()
    
            return render_template(
                'ensaios.html',
                user=user,
                clientes=clientes,
                solicitantes=solicitantes,
                tipopecas=tipopecas,
                fases=fases,
                tecnicos=tecnicos,
                laboratorios=laboratorios,
                normas=normas,
                ensaio=ensaio_selecionado  # Passa o ensaio selecionado para o template
            )
        except Exception as e:
            current_app.logger.error(f"Erro ao carregar página ensaios: {e}")
            flash('Erro ao carregar dados.', 'error')
            return redirect(url_for('index'))
    
    @app.route('/normas/com_documentos')
    def normas_com_documentos():
        normas_ids = db.session.query(Normasdocumentos.norma_id).distinct().all()
        ids = [nid[0] for nid in normas_ids]
        normas = Normas.query.filter(Normas.id.in_(ids)).all()
        return jsonify([{'id': n.id, 'norma': n.norma} for n in normas])

    @app.route('/tipo_pecas/ativas', methods=['GET'])
    def get_tipo_pecas_ativas():
        try:
            tipopecas = Tipopeca.query.filter_by(obsoleto=False).order_by(Tipopeca.tipopeca).all()
            return jsonify([
                {
                    'id': t.id,
                    'tipopeca': t.tipopeca
                }
                for t in tipopecas
            ])
        except Exception as e:
            current_app.logger.error("Erro ao buscar tipo de peças ativas: %s", e)
            return jsonify({'error': str(e)}), 500

    @app.route('/fases/ativas', methods=['GET'])
    def get_fases_ativas():
        try:
            fases = Fase.query.filter_by(obsoleto=False).order_by(Fase.fase).all()
            return jsonify([
                {
                    'id': f.id,
                    'fase': f.fase
                }
                for f in fases
            ])
        except Exception as e:
            current_app.logger.error("Erro ao buscar fases ativas: %s", e)
            return jsonify({'error': str(e)}), 500

    @app.route('/normas/template/<int:norma_id>', methods=['GET'])
    @login_required
    def get_norma_template(norma_id):
        # Vai buscar todos os testes do template da norma
        template_testes = Templatenormas.query.filter_by(norma_id=norma_id, obsoleto=False).order_by(Templatenormas.ordem).all()
        testes = []
        for t in template_testes:
            testes.append({
                'teste_id': t.teste_id,
                'ordem': t.ordem,
                'duracao': t.duracao,
                'duracaomontagem': t.duracaomontagem,
                'tempopp': t.tempopp,
                'tempomp': t.tempomp
            })
        return jsonify({'testes': testes})

    @app.route('/testes/update/<int:id>', methods=['POST'])
    def update_teste(id):
        teste = Testes.query.get_or_404(id)
        data = request.json

        # Atualiza apenas os campos enviados no payload
        for field in [
            'ensaio_id', 'teste_id', 'ordem', 'qtd', 'prefixo', 'primeirapeca',
            'datainicio', 'duracao', 'datafim', 'maquina_id', 'obs', 'user_id', 'fator', 'bemprimeira', 'motivofalhaensaio_id'
        ]:
            if field in data:
                setattr(teste, field, data[field])

        db.session.commit()
        return jsonify({'success': True, 'message': 'Teste atualizado com sucesso'})
    
    @app.route('/testes', methods=['POST'])
    def criar_teste():
        data = request.json
        # Campos obrigatórios: ensaio (número ou id) e teste_id
        ensaio_numero = data.get('ensaio')
        ensaio_id = data.get('ensaio_id')
        if not ensaio_id:
            ensaio_obj = Ensaio.query.filter_by(ensaio=ensaio_numero).first()
            if not ensaio_obj:
                return jsonify({'error': 'Ensaio não encontrado'}), 400
            ensaio_id = ensaio_obj.id
    
        novo_teste = Testes(
            ensaio_id=ensaio_id,
            teste_id=data.get('teste_id'),
            ordem=data.get('ordem'),
            qtd=data.get('qtd'),
            prefixo=data.get('prefixo'),
            primeirapeca=data.get('primeirapeca'),
            datainicio=data.get('datainicio'),
            duracao=data.get('duracao'),
            datafim=data.get('datafim'),
            maquina_id=data.get('maquina_id'),
            obs=data.get('obs'),
            user_id=data.get('user_id'),
            fator=data.get('fator'),
            bemprimeira=data.get('bemprimeira'),
            motivofalhaensaio_id=data.get('motivofalhaensaio_id')
        )
        db.session.add(novo_teste)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Teste criado com sucesso', 'id': novo_teste.id})

    @app.route('/testes/<ensaio_numero>')
    def get_testes_by_ensaio(ensaio_numero):
        ensaio = Ensaio.query.filter_by(ensaio=ensaio_numero).first()
        if not ensaio:
            return jsonify([])  # or return an error message
        testes = Testes.query.filter_by(ensaio_id=ensaio.id).order_by(Testes.ordem).all()
        return jsonify([t.to_dict() for t in testes])
    
    @app.route('/testes/pdf_export/<ensaio_numero>')
    def get_testes_for_pdf_export(ensaio_numero):
        ensaio = Ensaio.query.filter_by(ensaio=ensaio_numero).first()
        if not ensaio:
            return jsonify([])
        testes = Testes.query.filter_by(ensaio_id=ensaio.id).order_by(Testes.ordem).all()
        result = []
        for t in testes:
            tipo = Tipotestes.query.get(t.teste_id)
            nome_teste = tipo.teste if tipo else ''
            maquina = Maquina.query.get(t.maquina_id) if t.maquina_id else None
            nome_maquina = maquina.nome if maquina else ''
            result.append({
                'teste': nome_teste,
                'datainicio': t.datainicio,
                'datafim': t.datafim,
                'maquina': nome_maquina,
                'obs': t.obs,
                'qtd': t.qtd,
                'prefixo': t.prefixo,
                'primeirapeca': t.primeirapeca
            })
        return jsonify(result)
    
    @app.route('/testes/tipo/<int:teste_id>')
    def get_nome_teste_by_teste_id(teste_id):
        tipo = Tipotestes.query.get(teste_id)
        if not tipo:
            return jsonify({'error': 'Tipo de teste não encontrado'}), 404
        return jsonify({'teste': tipo.teste})
      
    @app.route('/testes/gravar_template', methods=['POST'])
    def gravar_testes_template():
        data = request.json
        ensaio_id = data.get('ensaio_id')
        norma_id = data.get('norma_id')
        user_id = data.get('user_id')
        qtd = data.get('qtd')
        prefixo = data.get('prefixo')
        primeirapeca = data.get('primeirapeca')
    
        # Busca os testes do template da norma
        template_testes = Templatenormas.query.filter_by(norma_id=norma_id).all()
        novos_testes = []
        for t in template_testes:
            novo_teste = Testes(
                ensaio_id=ensaio_id,
                teste_id=t.teste_id,
                ordem=t.ordem,
                duracao=t.duracao,
                user_id=user_id,
                qtd=qtd,
                prefixo=prefixo,
                primeirapeca=primeirapeca
            )
            novos_testes.append(novo_teste)
            db.session.add(novo_teste)
        db.session.commit()
        return jsonify({'status': 'ok', 'testes_gravados': len(novos_testes)})
    

    @app.route('/ensaios/sem_data_fim')
    def ensaios_sem_data_fim():
        # Buscar todos os ensaios cujo campo concluido é NULL ou '0000-00-00'
        ensaios = (
            db.session.query(Ensaio)
            .filter((Ensaio.concluido == None) | (Ensaio.concluido == '0000-00-00'))
            .all()
        )
        result = []
        for e in ensaios:
            projeto = Projeto.query.get(e.projeto_id)
            solicitante = Solicitante.query.get(e.solicitante_id)
            tipopeca = Tipopeca.query.get(e.tipopeca_id)
            laboratorio = Laboratorio.query.get(e.laboratorio_id)
            result.append({
                'ensaio': e.ensaio,
                'codigo_projeto': projeto.codigo if projeto else '',
                'denominacao_projeto': projeto.descricao if projeto else '',
                'tipo_peca': tipopeca.tipopeca if tipopeca else '',
                'solicitante': solicitante.nome if solicitante else '',
                'laboratorio': laboratorio.laboratorio if laboratorio else ''
            })
        return jsonify(result)



    @app.route('/tecnicos/ativos', methods=['GET'])
    def get_tecnicos_ativos():
        try:
            tecnicos = User.query.join(Funcao).filter(
                User.obsoleto == False,
                Funcao.funcao != 'Sistema'
            ).order_by(User.full_name).all()
            
            return jsonify([
                {
                    'id': t.id,
                    'full_name': t.full_name
                } for t in tecnicos
            ])
        except Exception as e:
            current_app.logger.error(f"Erro ao buscar técnicos ativos: {e}")
            return jsonify({'error': str(e)}), 500
    


    @app.route('/maquinas/ativas', methods=['GET'])
    def get_maquinas_ativas():
        try:
            maquinas = Maquina.query.filter_by(obsoleto=False).order_by(Maquina.nome).all()
            return jsonify([
                {
                    'id': m.id,
                    'nome': m.nome,
                    'codigo': m.codigo
                } for m in maquinas
            ])
        except Exception as e:
            current_app.logger.error(f"Erro ao buscar máquinas ativas: {e}")
            return jsonify({'error': str(e)}), 500

    @app.route('/testes/reordenar', methods=['POST'])
    def reordenar_testes():
        data = request.get_json()
        ordens = data.get('ordens', [])
        try:
            for item in ordens:
                teste = Testes.query.get(item['id'])
                if teste:
                    teste.ordem = item['ordem']
            db.session.commit()
            return jsonify({'success': True, 'message': 'Ordem atualizada.'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500    
        
    @app.route('/ensaios/api', methods=['POST'])
    def criar_ensaio_api():
        try:
            data = request.get_json()
            # Validações obrigatórias
            if not data.get('ensaio') or not data.get('laboratorio_id') or not data.get('datapedido'):
                return jsonify({'error': 'Campos obrigatórios em falta'}), 400
    
            # Verificar duplicado
            if Ensaio.query.filter_by(ensaio=data['ensaio']).first():
                return jsonify({'error': 'Já existe um ensaio com este número'}), 409
    
            novo_ensaio = Ensaio(
                ensaio=data['ensaio'],
                laboratorio_id=data['laboratorio_id'],
                norma_id=data.get('norma_id'),
                npecasrecebidas=data.get('npecasrecebidas'),
                destinopecas=data.get('destinopecas'),
                destinodevol=data.get('destinodevol'),
                moradadevol=data.get('moradadevol'),
                datapedido=data.get('datapedido'),
                datasolicitada=data.get('datasolicitada'),
                dataentregapecas=data.get('dataentregapecas'),
                dataacordada=data.get('dataacordada'),
                pep=data.get('pep'),
                network=data.get('network'),
                partnzf=data.get('partnzf'),
                partncliente=data.get('partncliente'),
                cliente_id=data.get('cliente_id'),
                projeto_id=data.get('projeto_id'),
                tipopeca_id=data.get('tipopeca_id'),
                fase_id=data.get('fase_id'),
                corecustomer=data.get('corecustomer', 'Customer'),
                atrasado=data.get('atrasado'),
                motivoatraso_id=int(data.get('motivoatraso_id')) if data.get('motivoatraso_id') else None,
                solicitante_id=data.get('solicitante_id'),
                user_id=data.get('user_id'),
                prefixo=data.get('prefixo'),
                obs=data.get('obs'),
                primeirapeca=data.get('primeirapeca'),
                concluido=data.get('concluido'),
                anulado=False
            )
            db.session.add(novo_ensaio)
            db.session.commit()
            return jsonify({'message': 'Ensaio criado com sucesso!', 'id': novo_ensaio.id})
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Erro ao criar ensaio (API): {e}")
            return jsonify({'error': f'Erro ao criar ensaio: {str(e)}'}), 500
        
    @app.route('/ensaios/update/<int:id>', methods=['PUT'])
    def atualizar_ensaio(id):
        data = request.get_json()
        ensaio = Ensaio.query.get_or_404(id)
        if 'ensaio' in data and data['ensaio'] != ensaio.ensaio:
            if Ensaio.query.filter(Ensaio.ensaio == data['ensaio'], Ensaio.id != id).first():
                return jsonify({'error': 'Já existe um ensaio com este número'}), 409
        # Atualize os campos
        for field in [
            'ensaio', 'laboratorio_id', 'norma_id', 'npecasrecebidas', 'destinopecas', 'destinodevol', 'datapedido',
            'datasolicitada', 'pep', 'network', 'partnzf', 'partncliente', 'dataentregapecas',
            'dataacordada', 'cliente_id', 'projeto_id', 'projeto_descricao', 'tipopeca_id',
            'fase_id', 'atrasado', 'motivoatraso_id', 'solicitante_id', 'user_id', 'prefixo', 'obs', 'primeirapeca', 'concluido', 'moradadevol', 'corecustomer'
        ]:
            if field in data:
                setattr(ensaio, field, data[field])
        db.session.commit()
        return jsonify({'message': 'Ensaio atualizado com sucesso!', 'id': ensaio.id})
    
    @app.route('/anular_informe/<numero_informe>', methods=['POST'])
    def anular_informe(numero_informe):
        data = request.get_json()
        motivo = data.get('motivoanulacao', '').strip()
        if not motivo:
            return jsonify({'success': False, 'error': 'Motivo da anulação é obrigatório.'}), 400
    
        ensaio = Ensaio.query.filter_by(ensaio=numero_informe).first()
        if not ensaio:
            return jsonify({'success': False, 'error': 'Ensaio não encontrado.'}), 404
        ensaio.anulado = True
        ensaio.motivoanulacao = motivo
        db.session.commit()
        return jsonify({'success': True, 'message': 'Ensaio anulado com sucesso!'})

    @app.route('/reverter_anulacao/<numero_informe>', methods=['POST'])
    def reverter_anulacao(numero_informe):
        ensaio = Ensaio.query.filter_by(ensaio=numero_informe).first()
        if not ensaio:
            return jsonify({'success': False, 'error': 'Ensaio não encontrado.'}), 404
        if not ensaio.anulado:
            return jsonify({'success': False, 'error': 'Este ensaio não está anulado.'}), 400

        ensaio.anulado = False
        ensaio.motivoanulacao = None
        db.session.commit()
        return jsonify({'success': True, 'message': 'Anulação revertida com sucesso!'})
  

    @app.route('/criar_pastas', methods=['POST'])
    def criar_pastas():
        data = request.get_json()
        laboratorio = data.get('laboratorio')
        ano = data.get('ano')
        tipoFase = data.get('tipoFase')
        cliente = data.get('cliente')
        projetoFolder = data.get('projetoFolder')
        tipopeca = data.get('tipopeca')
        ensaio_numero = data.get('ensaio')
        prefixo = data.get('prefixo')
        primeira_peca = data.get('primeira_peca')
        npecasrecebidas = data.get('npecasrecebidas')

        # Buscar laboratório
        lab_obj = Laboratorio.query.filter_by(laboratorio=laboratorio).first()
        if not lab_obj or not lab_obj.pastatestes:
            return jsonify({'success': False, 'error': 'Laboratório ou pasta de testes não encontrada.'}), 400

        CAMINHO_BASE = lab_obj.pastatestes
        print("Dados recebidos:", data)

        # Verificação de obrigatórios
        for campo in ['laboratorio', 'ano', 'tipoFase', 'cliente', 'projetoFolder', 'ensaio']:
            if not data.get(campo):
                print(f"Campo obrigatório vazio: {campo}")
                return jsonify({'success': False, 'error': f'Campo obrigatório vazio: {campo}'}), 400

        # Paths
        projeto_path = f"{projetoFolder}_{tipopeca}"
        lab_path = os.path.join(CAMINHO_BASE, laboratorio)
        ano_path = os.path.join(lab_path, str(ano))
        os.makedirs(ano_path, exist_ok=True)
        base_path = os.path.join(ano_path, tipoFase, cliente, projeto_path, ensaio_numero)

        # Buscar ensaio
        ensaio_obj = Ensaio.query.filter_by(ensaio=ensaio_numero).first()
        if not ensaio_obj:
            return jsonify({'success': False, 'error': 'Ensaio não encontrado.'}), 400

        try:
            os.makedirs(base_path, exist_ok=True)

            # -----------------------------------------------------------
            #   COPIAR DOCUMENTOS DA NORMA 
            # -----------------------------------------------------------

            NORMAS_DOCS_BASE = r"W:\DEPARTMENTS\LAB\PROCESS\01 QUALITY\01.01 DOCUMENTATION\01.01.05 TEMPLATES\ALL\REPORTS"

            if ensaio_obj.norma_id:
                norma_docs = Normasdocumentos.query.filter_by(norma_id=ensaio_obj.norma_id).all()
            else:
                norma_docs = []

            documentos_a_copiar = []
            documentos_conflito = []

            for doc in norma_docs:
                origem = Path(NORMAS_DOCS_BASE) / doc.documento
                destino = Path(base_path) / doc.documento

                documentos_a_copiar.append({
                    "nome": doc.documento,
                    "origem": str(origem),
                    "destino": str(destino)
                })

                if destino.exists():
                    documentos_conflito.append(doc.documento)

            # Primeira chamada — existem conflitos e ainda não há decisão
            if documentos_conflito and not data.get("overwrite_list"):
                return jsonify({
                    "success": False,
                    "conflict": True,
                    "documents": documentos_conflito,
                    "message": "Existem documentos da norma que já estão na pasta. Substituir documento a documento?"
                }), 409

            # Segunda chamada — overwrite_list presente
            overwrite_list = data.get("overwrite_list", {})

            for doc in documentos_a_copiar:
                filename = doc["nome"]
                origem = Path(doc["origem"])
                destino = Path(doc["destino"])

                # Se não existe → copia sem perguntar
                if not destino.exists():
                    try:
                        copy2(origem, destino)
                    except Exception as e:
                        print("Erro ao copiar:", origem, "->", destino, str(e))
                    continue

                # Existe → ver a decisão individual
                if filename in overwrite_list:
                    if overwrite_list[filename] is True:
                        try:
                            copy2(origem, destino)
                            print(f"Substituído: {filename}")
                        except Exception as e:
                            print("Erro ao substituir:", filename, str(e))
                    else:
                        print(f"Ignorado (não substituir): {filename}")

         
            if laboratorio != 'STD':

                before_test_path = os.path.join(base_path, 'BEFORE TEST')
                os.makedirs(before_test_path, exist_ok=True)

                if primeira_peca and npecasrecebidas:
                    try:
                        npecas = int(npecasrecebidas)
                        primeira = int(primeira_peca)
                    except ValueError:
                        return jsonify({'success': False, 'error': 'Primeira peça e nº peças devem ser números.'})

                    for i in range(npecas):
                        num = str(primeira + i).zfill(3)
                        nome_peca = f"{ensaio_numero}_{prefixo}{num}" if prefixo else f"{ensaio_numero}_{num}"
                        os.makedirs(os.path.join(before_test_path, nome_peca), exist_ok=True)

                testes = Testes.query.filter_by(ensaio_id=ensaio_obj.id).all()
                testes_validos = sorted(
                    [t for t in testes if t.teste and t.teste.teste.upper() not in ['INCOMING', 'REPORT']],
                    key=lambda t: t.ordem if hasattr(t, 'ordem') and t.ordem is not None else 0
                )

                for idx, teste in enumerate(testes_validos, 1):
                    # Verificar se deve criar pasta para este tipo de teste
                    if not teste.teste.criarpasta:
                        continue
                    
                    nome_teste = f"{idx} - {teste.teste.teste.upper()}"
                    teste_path = os.path.join(base_path, nome_teste)
                    os.makedirs(teste_path, exist_ok=True)
                
                    after_test_path = os.path.join(teste_path, 'AFTER TEST')
                    charts_path = os.path.join(teste_path, 'CHARTS')
                    setup_path = os.path.join(teste_path, 'SETUP')
                    os.makedirs(after_test_path, exist_ok=True)
                    os.makedirs(charts_path, exist_ok=True)
                    os.makedirs(setup_path, exist_ok=True)
                
                    if teste.primeirapeca and teste.qtd:
                        try:
                            npecas_teste = int(teste.qtd)
                            primeira_teste = int(teste.primeirapeca)
                        except ValueError:
                            continue
                
                        for i in range(npecas_teste):
                            num = str(primeira_teste + i).zfill(3)
                            nome_peca = f"{ensaio_numero}_{prefixo}{num}" if prefixo else f"{ensaio_numero}_{num}"
                            os.makedirs(os.path.join(after_test_path, nome_peca), exist_ok=True)

            else:
                # STD — estrutura especial
                if primeira_peca and npecasrecebidas:
                    try:
                        npecas = int(npecasrecebidas)
                        primeira = int(primeira_peca)
                    except ValueError:
                        return jsonify({'success': False, 'error': 'Primeira peça e nº peças devem ser números.'})

                    for i in range(npecas):
                        num = str(primeira + i).zfill(3)
                        nome_pasta = f"{ensaio_numero}_{prefixo}{num}" if prefixo else f"{ensaio_numero}_{num}"
                        peca_path = os.path.join(base_path, nome_pasta)
                        os.makedirs(peca_path, exist_ok=True)
                        os.makedirs(os.path.join(peca_path, 'DOCUMENT'), exist_ok=True)
                        os.makedirs(os.path.join(peca_path, 'MOVIE'), exist_ok=True)
                        photo_path = os.path.join(peca_path, 'PHOTO')
                        os.makedirs(photo_path, exist_ok=True)
                        os.makedirs(os.path.join(photo_path, 'AFTER TEST'), exist_ok=True)
                        os.makedirs(os.path.join(photo_path, 'BEFORE TEST'), exist_ok=True)

            return jsonify({'success': True})

        except Exception as e:
            import traceback
            traceback.print_exc()
            return jsonify({'success': False, 'error': str(e)})

    @app.route('/abrir_pasta', methods=['POST'])
    def abrir_pasta():
        data = request.get_json()
        pasta = data.get('pasta')
        print(f'CAMINHO RECEBIDO PARA ABRIR: {pasta}')  # <-- Adicione isto
        if not pasta or not os.path.exists(pasta):
            return jsonify({'success': False, 'error': 'Pasta não encontrada.'})
        try:
            subprocess.Popen(f'explorer \"{pasta}\"')
            return jsonify({'success': True})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})
    
    @app.route('/laboratorios/pastatestes_nome/<laboratorio>', methods=['GET'])
    def get_pastatestes_nome(laboratorio):
        lab = Laboratorio.query.filter_by(laboratorio=laboratorio).first()
        if not lab or not lab.pastatestes:
            return jsonify({'error': 'Laboratório ou pasta de testes não encontrada.'}), 404
        return jsonify({'pastatestes': lab.pastatestes})

    def _get_regras_manuais_aplicaveis():
        """
        Regras ativas para o campo manual (atalho atual):
        nome contém 'network' ou 'pep' (case-insensitive).
        """
        return (
            ConfValidacaoManual.query
            .filter(ConfValidacaoManual.obsoleto == 0)
            .filter(
                or_(
                    func.lower(ConfValidacaoManual.nome).like('%network%'),
                    func.lower(ConfValidacaoManual.nome).like('%pep%')
                )
            )
            .order_by(ConfValidacaoManual.nome.asc(), ConfValidacaoManual.id.asc())
            .all()
        )


    def _validar_manual_por_regras(manual_valor):
        """
        Retorna (ok: bool, detalhe: str|None).
        detalhe pode ser a chave_i18n da regra ou mensagem de erro.
        """
        valor = (manual_valor or '').strip()
        if not valor:
            return False, 'manual_obrigatorio'

        regras = _get_regras_manuais_aplicaveis()
        if not regras:
            return False, 'Sem regras de validacao manual ativas (Network/PEP).'

        for r in regras:
            try:
                padrao = re.compile(r.regex or '')
            except re.error:
                # Ignora regras mal configuradas para nao quebrar o endpoint
                continue

            if padrao.fullmatch(valor):
                return True, (r.chave_i18n or 'manual_valido')

        return False, 'manual_invalido'


    @app.route('/horas', methods=['POST'])
    @login_required
    def add_horas():
        data = request.get_json(silent=True) or {}

        tipo = (data.get('tipo') or '').strip().lower()
        manual_val = (data.get('manual') or '').strip() or None

        # Backend enforcement da validacao manual
        if tipo == 'manual' or manual_val:
            ok, detalhe = _validar_manual_por_regras(manual_val)
            if not ok:
                return jsonify({
                    'success': False,
                    'error': 'Valor manual invalido.',
                    'code': detalhe
                }), 400

        try:
            nova_hora = Horas(
                tecnico_id=data.get('tecnico_id'),
                data=data.get('data'),
                horas=data.get('horas'),
                ensaio_id=data.get('ensaio_id'),
                codigog_id=data.get('codigog_id'),
                teste_id=data.get('teste_id'),
                manual=manual_val,
                obs=data.get('obs')
            )
            db.session.add(nova_hora)
            db.session.commit()
            return jsonify({'success': True, 'message': 'Horas registadas com sucesso!'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'error': f'Erro ao registar horas: {str(e)}'}), 500

    
    @app.route('/horas/<int:id>', methods=['DELETE'])
    @login_required
    def delete_horas(id):
        try:
            hora = Horas.query.get_or_404(id)
            db.session.delete(hora)
            db.session.commit()
            return jsonify({'success': True, 'message': 'Registo de horas eliminado com sucesso!'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'error': f'Erro ao eliminar registo: {str(e)}'}), 500


    @app.route('/horas/<int:id>', methods=['PUT'])
    @login_required
    def update_horas(id):
        data = request.get_json(silent=True) or {}

        tipo = (data.get('tipo') or '').strip().lower()
        manual_val = (data.get('manual') or '').strip() if 'manual' in data else None

        # So valida se manual veio no payload ou tipo manual
        if tipo == 'manual' or ('manual' in data):
            ok, detalhe = _validar_manual_por_regras(manual_val)
            if not ok:
                return jsonify({
                    'success': False,
                    'error': 'Valor manual invalido.',
                    'code': detalhe
                }), 400

        try:
            hora = Horas.query.get_or_404(id)

            for field in ['tecnico_id', 'data', 'horas', 'ensaio_id', 'codigog_id', 'teste_id', 'obs']:
                if field in data:
                    setattr(hora, field, data[field])

            if 'manual' in data:
                hora.manual = (manual_val or None)

            db.session.commit()
            return jsonify({'success': True, 'message': 'Horas atualizadas com sucesso!'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'error': f'Erro ao atualizar horas: {str(e)}'}), 500

        


    def _parse_horas(value):
        """
        Converte '2.5' -> 2.5, '2,5' -> 2.5, '02:30' -> 2.5
        Levanta ValueError se inválido.
        """
        if value is None:
            raise ValueError("Valor de horas vazio.")
        if isinstance(value, (int, float)):
            return float(value)
        s = str(value).strip()
        if not s:
            raise ValueError("Valor de horas vazio.")
        if ":" in s:
            try:
                h_str, m_str = s.split(":")
                h = int(h_str)
                m = int(m_str)
                if h < 0 or m < 0 or m >= 60:
                    raise ValueError
                return h + (m / 60.0)
            except Exception:
                raise ValueError("Formato de horas inválido. Use HH:MM (ex.: 02:30).")
        else:
            # suporta vírgula decimal
            s = s.replace(",", ".")
            try:
                v = float(s)
                return v
            except Exception:
                raise ValueError("Formato de horas inválido. Use número (ex.: 2.5) ou HH:MM (ex.: 02:30).")


    def _parse_data_iso(dstr):
        """
        Converte 'YYYY-MM-DD' em date. Levanta ValueError se inválido.
        """
        if not dstr:
            raise ValueError("Data é obrigatória.")
        try:
            return date.fromisoformat(dstr)
        except Exception:
            raise ValueError("Formato de data inválido. Use YYYY-MM-DD.")


    @app.route('/horas/inserir', methods=['POST'])
    @login_required
    def inserir_horas():
        """
        Insere horas num teste de um ensaio, garantindo que não excede as horas máximas
        definidas pelo template da norma: horas_max = duracaomontagem + (tempopp * qtd_do_teste).
        Verifica novamente no momento do commit (com lock) para evitar concorrência.
        """
        try:
            payload = request.get_json(silent=True) or {}
            user = User.query.get(session['user_id'])
            ensaio_id = payload.get('ensaio_id')
            teste_id  = payload.get('teste_id')
            horas_in  = payload.get('horas')
            data_str  = payload.get('data') or payload.get('dia') or payload.get('date')
            obs       = (payload.get('obs') or '').strip()

            # Validações básicas
            if not ensaio_id or not teste_id:
                return jsonify({'error': 'ensaio_id e teste_id são obrigatórios.'}), 400

            # Data é obrigatória no modelo
            try:
                dia = _parse_data_iso(data_str)
            except ValueError as ve:
                return jsonify({'error': str(ve)}), 400

            try:
                horas_val = _parse_horas(horas_in)
            except ValueError as ve:
                return jsonify({'error': str(ve)}), 400

            if horas_val <= 0:
                return jsonify({'error': 'As horas devem ser superiores a zero.'}), 400

            # 1) Bloquear a linha do teste para evitar corrida (precisa InnoDB e transação)
            teste = (db.session.query(Testes)
                    .filter(Testes.id == teste_id, Testes.ensaio_id == ensaio_id)
                    .with_for_update()
                    .first())

            if not teste:
                return jsonify({'error': 'Teste não encontrado para o ensaio indicado.'}), 404

            ensaio = teste.ensaio
            if not ensaio or not ensaio.norma_id:
                return jsonify({'error': 'O ensaio não tem norma associada. Não é possível calcular horas máximas.'}), 400

            # 2) Obter template desta norma para este tipo de teste
            tpl = (Templatenormas.query
                .filter_by(norma_id=ensaio.norma_id, teste_id=teste.teste_id)
                .first())
            if not tpl:
                return jsonify({'error': 'Teste não existe no template da norma do ensaio.'}), 400

            qtd_pecas = teste.qtd or 0
            horas_max = (tpl.duracaomontagem or 0.0) + ((tpl.tempopp or 0.0) * qtd_pecas)

            # 3) Recalcular horas já colocadas (no momento, dentro do lock/mesma transação)
            horas_colocadas = (
                db.session.query(func.sum(Horas.horas))
                .filter(Horas.teste_id == teste.id)
                .filter(or_(Horas.extra.is_(False), Horas.extra.is_(None)))
                .scalar()
            ) or 0.0

            restantes = round(horas_max - horas_colocadas, 4)

            if horas_val > restantes + 1e-9:
                # Conflito: alguém pode ter lançado horas entretanto
                return jsonify({
                    'error': 'Horas excedem as disponíveis para este teste.',
                    'horas_max': round(horas_max, 2),
                    'horas_colocadas': round(horas_colocadas, 2),
                    'horas_disponiveis': round(max(0.0, restantes), 2)
                }), 409

            # 4) Inserir horas — técnico é SEMPRE o utilizador autenticado
            reg = Horas(
                tecnico_id=user.id,
                data=dia,
                horas=float(horas_val),
                ensaio_id=int(ensaio_id),
                teste_id=int(teste_id),
                obs=obs if obs else None
            )
            db.session.add(reg)
            db.session.commit()

            # 5) Devolver totals atualizados
            novas_colocadas = horas_colocadas + float(horas_val)
            novas_disp = max(0.0, horas_max - novas_colocadas)

            return jsonify({
                'success': True,
                'message': 'Horas inseridas com sucesso.',
                'horas_max': round(horas_max, 2),
                'horas_colocadas': round(novas_colocadas, 2),
                'horas_disponiveis': round(novas_disp, 2)
            }), 201

        except Exception as e:
            db.session.rollback()
            # Opcional: current_app.logger.exception("Erro ao inserir horas")
            return jsonify({'error': f'Erro ao inserir horas: {str(e)}'}), 500







    @app.route('/upload_norma_documento', methods=['POST'])
    def upload_norma_documento():
        file = request.files.get('file')
        norma_id = request.form.get('norma_id')
        if not file or not norma_id:
            return jsonify({'success': False, 'error': 'Ficheiro e norma obrigatórios.'})
    
        # Diretório de destino (ajuste conforme necessário)
        upload_dir = os.path.join('uploads', 'normas', str(norma_id))
        os.makedirs(upload_dir, exist_ok=True)
        filepath = os.path.join(upload_dir, file.filename)
        file.save(filepath)
    
        # Gravar na base de dados
        doc = Normasdocumentos(norma_id=norma_id, documento=file.filename)
        db.session.add(doc)
        db.session.commit()
    
        return jsonify({'success': True, 'filename': file.filename, 'path': filepath})


    @app.route('/normas/<int:norma_id>/documentos', methods=['GET'])
    def get_norma_documentos(norma_id):
        docs = Normasdocumentos.query.filter_by(norma_id=norma_id).all()
        return jsonify({"data": [
            {'id': d.id, 'documento': d.documento}
            for d in docs
        ]})
    
    @app.route('/normasdocumentos/existe', methods=['GET'])
    def verifica_documento_existe():
        nome = request.args.get('nome')
        pasta = r"W:\DEPARTMENTS\LAB\PROCESS\01 QUALITY\01.01 DOCUMENTATION\01.01.05 TEMPLATES\ALL\REPORTS"
        caminho = os.path.join(pasta, nome)
        existe = os.path.exists(caminho)
        return jsonify({'existe': existe})
    
    @app.route('/normasdocumentos/<int:id>', methods=['DELETE'])
    def apagar_norma_documento(id):
        doc = Normasdocumentos.query.get_or_404(id)
        db.session.delete(doc)
        db.session.commit()
        return jsonify({'success': True})

    @app.route('/consultas/ensaiosatrasados')
    def consulta_ensaiosatrasados():
        """
        Retorna o total de ensaios concluídos (não anulados) por laboratório, ano e mês,
        o total desses ensaios com atrasado=1, e motivos do atraso agrupados.
        Parâmetros: ano (int), mes (int), laboratorio (id ou vazio para todos)
        """
        ano = request.args.get('ano', type=int)
        mes = request.args.get('mes', type=int)
        laboratorio_id = request.args.get('laboratorio', type=int)
        query = Ensaio.query.filter(
            Ensaio.anulado == False,
            Ensaio.concluido != None,
            db.extract('year', Ensaio.concluido) == ano,
            db.extract('month', Ensaio.concluido) == mes
        )
        if laboratorio_id:
            query = query.filter(Ensaio.laboratorio_id == laboratorio_id)
        ensaios = query.all()
        labs = {l.id: l.laboratorio for l in Laboratorio.query.all()}
        motivos_dict = {m.id: m.motivo for m in Motivosatraso.query.all()}
        total_por_lab = defaultdict(int)
        atrasados_por_lab = defaultdict(int)
        motivos_por_lab = defaultdict(list)
        for e in ensaios:
            total_por_lab[e.laboratorio_id] += 1
            if str(getattr(e, 'atrasado', '0')) == '1':
                atrasados_por_lab[e.laboratorio_id] += 1
                motivo_id = getattr(e, 'motivoatraso_id', None)
                if motivo_id:
                    motivos_por_lab[e.laboratorio_id].append(motivo_id)
        resultado = []
        def motivos_agrupados(lab_id):
            motivos = Counter(motivos_por_lab.get(lab_id, []))
            return [
                {'motivo': motivos_dict.get(m_id, 'Sem motivo'), 'qtd': qtd}
                for m_id, qtd in motivos.items()
            ]
        if laboratorio_id:
            resultado.append({
                'laboratorio': labs.get(laboratorio_id, 'Desconhecido'),
                'total_ensaios': total_por_lab.get(laboratorio_id, 0),
                'total_atrasados': atrasados_por_lab.get(laboratorio_id, 0),
                'motivos_atraso': motivos_agrupados(laboratorio_id)
            })
        else:
            for lab_id in set(list(total_por_lab.keys()) + list(atrasados_por_lab.keys())):
                resultado.append({
                    'laboratorio': labs.get(lab_id, 'Desconhecido'),
                    'total_ensaios': total_por_lab.get(lab_id, 0),
                    'total_atrasados': atrasados_por_lab.get(lab_id, 0),
                    'motivos_atraso': motivos_agrupados(lab_id)
                })
        return jsonify(resultado)

    @app.route('/consultas/bemaprimeira')
    def consulta_bem_a_primeira():

        ano = request.args.get('ano', type=int)
        mes = request.args.get('mes', type=int)
        laboratorio_id = request.args.get('laboratorio', type=int)

        # ---------------------------------------------------------
        # QUERY PRINCIPAL
        # ---------------------------------------------------------
        query = (
            db.session.query(Testes, Ensaio)
            .join(Ensaio, cast(Testes.ensaio_id, Integer) == Ensaio.id)
            .join(Tipotestes, Tipotestes.id == Testes.teste_id)  
            .filter(
                Testes.datafim != None,
                db.extract('year', Testes.datafim) == ano,
                db.extract('month', Testes.datafim) == mes,
                Ensaio.anulado == False,
                Tipotestes.mediveis == 1           
            )
        )

        if laboratorio_id:
            query = query.filter(Ensaio.laboratorio_id == laboratorio_id)

        resultados = query.all()

        # ---------------------------------------------------------
        # CONSTRUÇÃO DA RESPOSTA
        # ---------------------------------------------------------
        labs = {l.id: l.laboratorio for l in Laboratorio.query.all()}
        motivos_dict = {m.id: m.motivo for m in Motivosfalhaensaios.query.all()}

        dados = defaultdict(lambda: defaultdict(lambda: {
            'qtd': 0,
            'bemprimeira': 0
        }))
        total_pecas_lab = defaultdict(int)

        for teste, ensaio in resultados:
            lab_id = ensaio.laboratorio_id
            motivo_id = getattr(teste, 'motivofalhaensaio_id', None)

            qtd = int(teste.qtd or 0)
            bemprimeira = int(teste.bemprimeira or 0)

            total_pecas_lab[lab_id] += qtd

            motivo_nome = motivos_dict.get(motivo_id, 'Sem motivo')

            dados[lab_id][motivo_nome]['qtd'] += qtd
            dados[lab_id][motivo_nome]['bemprimeira'] += bemprimeira

        resposta = []
        for lab_id, motivos in dados.items():
            resposta.append({
                'laboratorio': labs.get(lab_id, 'Desconhecido'),
                'total_pecas': total_pecas_lab.get(lab_id, 0),
                'motivos': [
                    {
                        'motivo': motivo,
                        'total_pecas': info['qtd'],
                        'total_bemprimeira': info['bemprimeira'],
                        'total_nao_bemprimeira': info['qtd'] - info['bemprimeira']
                    }
                    for motivo, info in motivos.items()
                ]
            })

        return jsonify(resposta)


    @app.route('/consultas/ensaiosterminados')
    def consulta_ensaios_terminados():
        """
        Retorna ensaios terminados entre duas datas, com todos os campos detalhados.
        Parâmetros: dataDe, dataAte, laboratorio (id ou vazio para todos)
        """
        data_de = request.args.get('dataDe')
        data_ate = request.args.get('dataAte')
        laboratorio_id = request.args.get('laboratorio', type=int)
    
        # Converter datas
        data_de = datetime.strptime(data_de, '%Y-%m-%d')
        data_ate = datetime.strptime(data_ate, '%Y-%m-%d')
    
        query = (
            db.session.query(Testes, Ensaio)
            .join(Ensaio, Testes.ensaio_id == Ensaio.id)
            .filter(Testes.datafim != None)
            .filter(Testes.datafim >= data_de)
            .filter(Testes.datafim <= data_ate)
            .filter(Ensaio.anulado == False)
        )
        if laboratorio_id:
            query = query.filter(Ensaio.laboratorio_id == laboratorio_id)
    
        resultados = []
        for teste, ensaio in query.all():
            # Calcular horas estimadas
            tpl = Templatenormas.query.filter_by(norma_id=ensaio.norma_id, teste_id=teste.teste_id).first()
            if tpl:
                horas_estimadas = (tpl.duracaomontagem or 0.0) + ((tpl.tempopp or 0.0) * (teste.qtd or 0))
            else:
                horas_estimadas = 0.0
    
            # Calcular horas totais
            horas_totais = (
                db.session.query(func.sum(Horas.horas))
                .filter(Horas.teste_id == teste.id)
                .scalar()
            ) or 0.0
    
            resultados.append({
                'ensaio': ensaio.ensaio,
                'network': ensaio.network,
                'cliente': ensaio.cliente.cliente if ensaio.cliente else '',
                'projeto': ensaio.projeto.descricao if ensaio.projeto else '',
                'tipo_peca': ensaio.tipopeca.tipopeca if ensaio.tipopeca else '',
                'teste': teste.teste.teste if teste.teste else '',
                'num_pecas_teste': teste.qtd,
                'data_inicio': teste.datainicio.strftime('%Y-%m-%d') if teste.datainicio else '',
                'data_fim': teste.datafim.strftime('%Y-%m-%d') if teste.datafim else '',
                'fase': ensaio.fase.fase if ensaio.fase else '',
                'horas_estimadas': round(horas_estimadas, 2),
                'horas_totais': round(horas_totais, 2)
            })
        return jsonify(resultados)


    @app.route('/consultas/horasensaios')
    def consulta_horas_ensaios():
    
        data_de = request.args.get('dataDe')
        data_ate = request.args.get('dataAte')
        laboratorio_id = request.args.get('laboratorio', type=int)
    
        data_de = datetime.strptime(data_de, '%Y-%m-%d').date()
        data_ate = datetime.strptime(data_ate, '%Y-%m-%d').date()
    
        query = (
            db.session.query(
                Ensaio.ensaio.label('ensaio'),
                Tipotestes.teste.label('teste'),
                User.full_name.label('tecnico'),
                Horas.data.label('data'),
                func.sum(Horas.horas).label('horas')
            )
            .join(Ensaio, Horas.ensaio_id == Ensaio.id)
            .join(User, Horas.tecnico_id == User.id)
            .outerjoin(Testes, Horas.teste_id == Testes.id)
            .outerjoin(Tipotestes, Testes.teste_id == Tipotestes.id)
            .filter(Horas.data >= data_de)
            .filter(Horas.data <= data_ate)
            .filter(Horas.ensaio_id != None)
            .filter(Ensaio.anulado == False)
        )
    
        if laboratorio_id:
            query = query.filter(Ensaio.laboratorio_id == laboratorio_id)
    
        rows = (
            query
            .group_by(Ensaio.ensaio, Tipotestes.teste, User.full_name, Horas.data)
            .order_by(Ensaio.ensaio.asc(), Tipotestes.teste.asc(), User.full_name.asc(), Horas.data.asc())
            .all()
        )
    
        resultado = []
        for row in rows:
            resultado.append({
                'ensaio': row.ensaio or '',
                'teste': row.teste or '',
                'tecnico': row.tecnico or '',
                'data': row.data.strftime('%Y-%m-%d') if row.data else '',
                'horas': round(float(row.horas or 0), 2)
            })
    
        return jsonify(resultado)


    @app.route('/ensaios/<ensaio_numero>', methods=['GET'])
    @login_required
    def get_ensaio(ensaio_numero):
        def safe_iso(dt):
            try:
                if not dt or str(dt) in ("0000-00-00", "0000-00-00 00:00:00"):
                    return None
                return dt.isoformat()
            except Exception:
                return None
    
        ensaio = Ensaio.query.filter_by(ensaio=ensaio_numero).first()
        if ensaio:
            projeto = Projeto.query.get(ensaio.projeto_id) if ensaio.projeto_id else None
            return jsonify({
                'id': ensaio.id,
                'ensaio': ensaio.ensaio,
                'laboratorio_id': ensaio.laboratorio_id,
                'norma_id': ensaio.norma_id,
                'npecasrecebidas': ensaio.npecasrecebidas,
                'destinopecas': ensaio.destinopecas,
                'destinodevol': ensaio.destinodevol,
                'moradadevol': ensaio.moradadevol,
                'pep': ensaio.pep,
                'network': ensaio.network,
                'partnzf': ensaio.partnzf,
                'partncliente': ensaio.partncliente,
                'cliente_id': ensaio.cliente_id,
                'projeto_id': ensaio.projeto_id,
                'projeto_descricao': projeto.descricao if projeto else '',
                'tipopeca_id': ensaio.tipopeca_id,
                'fase_id': ensaio.fase_id,
                'corecustomer':ensaio.corecustomer,
                'atrasado': ensaio.atrasado,
                'motivoatraso_id': ensaio.motivoatraso_id,
                'solicitante_id': ensaio.solicitante_id,
                'user_id': ensaio.user_id,
                'prefixo': ensaio.prefixo,
                'obs': ensaio.obs,
                'primeirapeca': ensaio.primeirapeca,
                'datapedido': safe_iso(ensaio.datapedido),
                'datasolicitada': safe_iso(ensaio.datasolicitada),
                'dataentregapecas': safe_iso(ensaio.dataentregapecas),
                'dataacordada': safe_iso(ensaio.dataacordada),
                'concluido': safe_iso(ensaio.concluido),
                'anulado': ensaio.anulado,
                'motivoanulacao': ensaio.motivoanulacao
            }), 200
        else:
            return jsonify({'error': 'Ensaio não encontrado.'}), 404
        

    
    
    @app.route('/users/update_password/<int:id>', methods=['POST'])
    def update_user_password(id):
        data = request.json
        new_password = data.get('new_password')
        if not new_password or len(new_password) < 4:
            return jsonify({'error': 'Password inválida'}), 400
    
        user = User.query.get_or_404(id)
        user.password_hash = generate_password_hash(new_password)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Password atualizada com sucesso'})
    


    #####################################################################
    #REFERENCIAS
    @app.route('/referencias', methods=['POST'])
    def add_referencia():
        try:
            data = request.json if request.is_json else request.form
            referencia = data.get('referencia')
            descricao= data.get('descricao')
            projeto_id = data.get('projeto_id')
            componente_id = data.get('componente_id')
            laboratorio_id = data.get('laboratorio_id')
            solicitante_id = data.get('solicitante_id')
            stockminimo = data.get('stockminimo') or 0
            obs = data.get('obs') or data.get('observacoes')
            estado = data.get('estado') or data.get('estado_id')
            plme = data.get('plme') or data.get('plme')
            obsoleto = data.get('obsoleto')
    
            if not referencia:
                return jsonify({'error': 'Referência é obrigatória'}), 400
    
            if Referencia.query.filter_by(referencia=referencia).first():
                return jsonify({'error': 'Já existe uma referência com esse nome'}), 409
    
            nova = Referencia(
                referencia=referencia,
                descricao=descricao,
                projeto_id=projeto_id,
                componente_id=componente_id,
                laboratorio_id=laboratorio_id,
                solicitante_id=solicitante_id,
                stockminimo=stockminimo,
                obs=obs,
                estado=estado,
                plme=bool(int(plme)) if plme is not None else False,
                obsoleto=bool(int(obsoleto)) if obsoleto is not None else False
            )
            db.session.add(nova)
            db.session.commit()
            return jsonify({'success': True, 'message': 'Referência adicionada com sucesso', 'id': nova.id})
        except Exception as e:
            db.session.rollback()
            current_app.logger.error("Erro ao adicionar referência: %s", e)
            return jsonify({'error': f'Erro ao adicionar referência: {str(e)}'}), 500
    
    @app.route('/referencias/update/<int:id>', methods=['POST'])
    def update_referencia(id):
        referencia = Referencia.query.get_or_404(id)
        data = request.json if request.is_json else request.form
    
        novo_referencia = data.get('referencia')
        if novo_referencia and novo_referencia != referencia.referencia:
            if Referencia.query.filter(Referencia.referencia == novo_referencia, Referencia.id != id).first():
                return jsonify({'error': 'Já existe outra referência com esse nome'}), 409
            referencia.referencia = novo_referencia
    
        referencia.descricao = data.get('descricao', referencia.descricao)
        referencia.projeto_id = data.get('projeto_id', referencia.projeto_id)
        referencia.componente_id = data.get('componente_id', referencia.componente_id)
        referencia.laboratorio_id = data.get('laboratorio_id', referencia.laboratorio_id)
        referencia.solicitante_id = data.get('solicitante_id', referencia.solicitante_id)
        referencia.stockminimo = data.get('stockminimo', referencia.stockminimo)
        referencia.obs = data.get('obs', referencia.obs) or data.get('observacoes', referencia.obs)
        referencia.estado = data.get('estado', referencia.estado) or data.get('estado_id', referencia.estado)
        plme = data.get('plme') or data.get('plme')
        if plme is not None:
            referencia.plme = bool(int(plme))
        obsoleto = data.get('obsoleto')
        if obsoleto is not None:
            referencia.obsoleto = bool(int(obsoleto))
    
        try:
            db.session.commit()
            return jsonify({'success': True, 'message': 'Referência atualizada com sucesso'})
        except Exception as e:
            db.session.rollback()
            current_app.logger.error("Erro ao atualizar referência: %s", e)
            return jsonify({'error': f'Erro ao atualizar referência: {str(e)}'}), 500
        
    @app.route('/api/referencia_by_nome')
    def api_referencia_by_nome():
        nome = request.args.get('referencia')
        if not nome:
            return jsonify({'error': 'Parâmetro "referencia" obrigatório'}), 400
        ref = Referencia.query.filter_by(referencia=nome).first()
        if not ref:
            return jsonify({'error': 'Referência não encontrada'}), 404
        return jsonify({
            'id': ref.id,
            'referencia': ref.referencia,
            'descricao': ref.descricao,
            'projeto_id': ref.projeto_id,
            'componente_id': ref.componente_id,
            'laboratorio_id': ref.laboratorio_id,
            'solicitante_id': ref.solicitante_id,
            'stockminimo': ref.stockminimo,
            'obs': ref.obs,
            'estado': ref.estado,
            'plme': ref.plme,
            'obsoleto': ref.obsoleto
        })
    
    @app.route('/api/referencias')
    def api_referencias():
        referencias = Referencia.query.all()
        result = []
        for r in referencias:
            # Calcular stock: somar movimentos +, subtrair movimentos -
            movimentos = r.saidas_stock  # relação MovimentoStock
            stock = 0
            for m in movimentos:
                if m.movimento == '+':
                    stock += m.quantidade or 0
                elif m.movimento == '-':
                    stock -= m.quantidade or 0
            # Obter denominação do projeto e tipo de peça
            projeto_descricao = r.projeto.descricao if r.projeto else ''
            tipopeca = r.projeto.tipopeca.tipopeca if r.projeto and r.projeto.tipopeca else ''
            result.append({
                'id': r.id,
                'referencia': r.referencia,
                'descricao': r.descricao,
                'projeto_codigo': r.projeto.codigo if r.projeto else '',
                'projeto_descricao': projeto_descricao,
                'tipopeca': tipopeca,
                'stock': stock,
                'laboratorio_nome': r.laboratorio.laboratorio if r.laboratorio else '',
                'componente_nome': r.componente.componente if r.componente else '',
                'solicitante_nome': r.solicitante.nome if r.solicitante else '',
                'estado': r.estado or ''
            })
        return jsonify(result)
    
    @app.route('/api/referencias_stock')
    def api_referencias_stock():
        projeto_id = request.args.get('projeto_id', type=int)
        obsoleta = request.args.get('obsoleta')
        query = Referencia.query
        if obsoleta is not None:
            if obsoleta == '0':
                query = query.filter((Referencia.obsoleto == False) | (Referencia.obsoleto == None))
            elif obsoleta == '1':
                query = query.filter(Referencia.obsoleto == True)
        if projeto_id:
            query = query.filter(Referencia.projeto_id == projeto_id)
        referencias = query.all()
        result = []
        for r in referencias:
            result.append({
                'id': r.id,
                'referencia': r.referencia,
                'descricao': r.descricao,
                'componente': r.componente.componente if r.componente else '',
                'projeto_id': r.projeto_id,
                'obsoleto': r.obsoleto
            })
        return jsonify(result)
    
    @app.route('/api/referencia_by_id')
    def api_referencia_by_id():
        rid = request.args.get('id')
        if not rid:
            return jsonify({'error': 'Parâmetro \"id\" obrigatório'}), 400
        ref = Referencia.query.get(rid)
        if not ref:
            return jsonify({'error': 'Referência não encontrada'}), 404
        movimentos = ref.saidas_stock if hasattr(ref, 'saidas_stock') else []
        stock = 0
        for m in movimentos:
            if m.movimento == '+':
                stock += m.quantidade or 0
            elif m.movimento == '-':
                stock -= m.quantidade or 0
        return jsonify({
            'id': ref.id,
            'referencia': ref.referencia,
            'descricao': ref.descricao,
            'projeto_id': ref.projeto_id,
            'componente_id': ref.componente_id,
            'laboratorio_id': ref.laboratorio_id,
            'solicitante_id': ref.solicitante_id,
            'stockminimo': ref.stockminimo,
            'obs': ref.obs,
            'estado': ref.estado,
            'plme': ref.plme,
            'obsoleto': ref.obsoleto,
            'stock': stock
        })
    
    ######################################
    #BAIXA STOCK
    @app.route('/api/saida_stock', methods=['POST'])
    @login_required
    def inserir_saida_stock():
        data = request.get_json()
        ensaio_id = data.get('ensaio_id')
        referencia_id = data.get('referencia_id')
        quantidade = data.get('quantidade')
        localizacao = data.get('localizacao_id')
        movimento = data.get('movimento')
        obs = data.get('obs')
        if not referencia_id or quantidade is None:
            return jsonify({'success': False, 'error': 'Campos obrigatórios em falta.'}), 400
        try:
            saida = MovimentoStock(
                ensaio_id=ensaio_id,
                referencia_id=referencia_id,
                quantidade=quantidade,
                localizacao_id=localizacao,
                obs=obs,
                movimento=movimento
            )
            db.session.add(saida)
            db.session.commit()
            return jsonify({'success': True, 'id': saida.id})
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'error': str(e)}), 500
    
    @app.route('/api/saida_stock', methods=['GET'])
    @login_required
    def listar_saidas_stock():
        ensaio_id = request.args.get('ensaio_id', type=int)
        query = MovimentoStock.query
        if ensaio_id:
            query = query.filter_by(ensaio_id=ensaio_id)
        saidas = query.all()
        result = []
        for s in saidas:
            result.append({
                'id': s.id,
                'ensaio_id': s.ensaio_id,
                'referencia_id': s.referencia_id,
                'quantidade': s.quantidade,
                'movimento': s.movimento,
                'localizacao_id': s.localizacao_id
            })
        return jsonify(result)
    
    @app.route('/api/movimentostock')
    def api_movimentostock():
        referencia_id = request.args.get('referencia_id', type=int)
        query = MovimentoStock.query
        if referencia_id:
            query = query.filter_by(referencia_id=referencia_id)
        movimentos = query.all()
        result = []
        for m in movimentos:
            ensaio_nome = ''
            localizacao_nome = ''
            if m.ensaio_id:
                ensaio_obj = Ensaio.query.get(m.ensaio_id)
                ensaio_nome = ensaio_obj.ensaio if ensaio_obj else m.ensaio_id
            if hasattr(m, 'localizacao_id') and m.localizacao_id:
                localizacao_obj = Localizacao.query.get(m.localizacao_id)
                localizacao_nome = localizacao_obj.nome if localizacao_obj else m.localizacao_id
            result.append({
                'id': m.id,
                'ensaio': ensaio_nome,
                'movimento': m.movimento,
                'quantidade': m.quantidade,
                'localizacao': localizacao_nome,
                'obs': m.obs or ''
            })
        return jsonify(result)
    
    @app.route('/api/movimentostock/delete/<int:id>', methods=['DELETE'])
    def delete_movimentostock(id):
        movimento = MovimentoStock.query.get(id)
        if not movimento:
            return jsonify({'success': False, 'error': 'Movimento não encontrado.'}), 404
        try:
            db.session.delete(movimento)
            db.session.commit()
            return jsonify({'success': True})
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'error': str(e)}), 500
    
    @app.route('/api/movimentostock/update/<int:id>', methods=['PUT'])
    def update_movimentostock(id):
        movimento = MovimentoStock.query.get(id)
        if not movimento:
            return jsonify({'success': False, 'error': 'Movimento não encontrado.'}), 404
        data = request.get_json()
        try:
            # Só permite atualizar campos editáveis
            if 'ensaio' in data:
                # Procurar o ensaio pelo nome (ou id, conforme o frontend envia)
                ensaio_obj = Ensaio.query.filter_by(ensaio=data['ensaio']).first()
                if ensaio_obj:
                    movimento.ensaio_id = ensaio_obj.id
                else:
                    return jsonify({'success': False, 'error': 'Ensaio não encontrado.'}), 400
            if 'movimento' in data:
                movimento.movimento = data['movimento']
            if 'quantidade' in data:
                movimento.quantidade = data['quantidade']
            if 'obs' in data:
                movimento.obs = data['obs']
            db.session.commit()
            return jsonify({'success': True})
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'error': str(e)}), 500
        
    #PLME
    @app.route('/api/plme_pendentes')
    def api_plme_pendentes():
        # Movimentos não exportados (exportado null ou 00-00-0000), movimento '-' e referencia com plme=1
        movimentos = (
            db.session.query(
                Referencia.referencia.label('referencia'),
                Referencia.descricao.label('descricao'),
                Ensaio.network.label('network'),
                func.sum(MovimentoStock.quantidade).label('quantidade')
            )
            .join(MovimentoStock.referencia)
            .join(MovimentoStock.ensaio)
            .filter(
                ((MovimentoStock.exportado == None) | (MovimentoStock.exportado == '00-00-0000')),
                MovimentoStock.movimento == '-',
                Referencia.plme == True
            )
            .group_by(Referencia.referencia, Referencia.descricao, Ensaio.network)
            .all()
        )
        result = []
        for m in movimentos:
            result.append({
                'referencia': m.referencia,
                'descricao': m.descricao,
                'network': m.network,
                'quantidade': m.quantidade
            })
        return jsonify(result)

    @app.route('/api/plme_exportar', methods=['POST'])
    def api_plme_exportar():
        data = request.get_json()
        referencia_ids = data.get('referencia_ids', [])
        timestamp = data.get('timestamp')
        if not referencia_ids or not timestamp:
            return jsonify({'success': False, 'error': 'Dados em falta.'}), 400
        try:
            # Atualiza todos os movimentos stock não exportados dessas referências e movimento '-'
            movimentos = MovimentoStock.query.join(MovimentoStock.referencia).filter(
                Referencia.referencia.in_(referencia_ids),
                (MovimentoStock.exportado == None) | (MovimentoStock.exportado == '00-00-0000'),
                MovimentoStock.movimento == '-'
            ).all()
            for m in movimentos:
                m.exportado = timestamp
            db.session.commit()
            return jsonify({'success': True})
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'error': str(e)}), 500
        
   
    
    @app.route('/api/movimentostock_exportados', methods=['GET'])
    def movimentostock_exportados():
        datas = (
            db.session.query(MovimentoStock.exportado)
            .filter(MovimentoStock.exportado.isnot(None))
            .distinct()
            .order_by(MovimentoStock.exportado.desc())
            .all()
        )
        # Filtrar datas válidas
        datas_validas = [d[0] for d in datas if d[0] and str(d[0]) not in ('0000-00-00 00:00:00', '00-00-0000', '0000-00-00')]
        if not datas_validas:
            return jsonify({'message': 'Sem registos'}), 200
        result = [{'exportado': d} for d in datas_validas]
        return jsonify(result)
   
    @app.route('/api/plme_anular_exportacao', methods=['POST'])
    def plme_anular_exportacao():
        data = request.get_json()
        exportado = data.get('exportado')
        if not exportado:
            return jsonify({'success': False, 'error': 'Data em falta.'}), 400
        try:
            # Tenta converter de string tipo 'Fri, 13 Feb 2026 11:04:38 GMT' para 'YYYY-MM-DD HH:MM:SS'
            try:
                dt = datetime.strptime(exportado, '%a, %d %b %Y %H:%M:%S GMT')
                exportado_bd = dt.strftime('%Y-%m-%d %H:%M:%S')
            except Exception:
                exportado_bd = exportado[:19]  # fallback: usa só os primeiros 19 chars
    
            movimentos = MovimentoStock.query.filter(
                MovimentoStock.exportado == exportado_bd
            ).all()
            for m in movimentos:
                m.exportado = None
            db.session.commit()
            return jsonify({'success': True})
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'error': str(e)}), 500
        
    @app.route('/api/plme_movimentos_exportados')
    def plme_movimentos_exportados():
        exportado = request.args.get('exportado')
        if not exportado:
            return jsonify([])
        try:
            if 'GMT' in exportado:
                dt = datetime.strptime(exportado, '%a, %d %b %Y %H:%M:%S GMT')
                exportado_bd = dt.strftime('%Y-%m-%d %H:%M:%S')
            else:
                exportado_bd = exportado[:19]
        except Exception:
            exportado_bd = exportado[:19]
        # Agrupar por referência, descrição, network e somar quantidades
        movimentos = (
            db.session.query(
                Referencia.referencia.label('referencia'),
                Referencia.descricao.label('descricao'),
                Ensaio.network.label('network'),
                db.func.sum(MovimentoStock.quantidade).label('quantidade')
            )
            .join(MovimentoStock.referencia)
            .join(MovimentoStock.ensaio)
            .filter(MovimentoStock.exportado.like(f'{exportado_bd}%'))
            .group_by(Referencia.referencia, Referencia.descricao, Ensaio.network)
            .all()
        )
        result = []
        for m in movimentos:
            result.append({
                'referencia': m.referencia,
                'descricao': m.descricao,
                'network': m.network,
                'quantidade': m.quantidade
            })
        return jsonify(result)
    
    #Entrada Stock
    @app.route('/api/entrada_stock', methods=['POST'])
    @login_required
    def inserir_entrada_stock():
        data = request.get_json()
        referencia_id = data.get('referencia_id')
        quantidade = data.get('quantidade')
        movimento = data.get('movimento')
        obs = data.get('obs')
        localizacao_id = data.get('localizacao_id')
        if not referencia_id or quantidade is None or not localizacao_id:
            return jsonify({'success': False, 'error': 'Campos obrigatórios em falta.'}), 400
        try:
            entrada = MovimentoStock(
                referencia_id=referencia_id,
                quantidade=quantidade,
                obs=obs,
                movimento=movimento,
                localizacao_id=localizacao_id
            )
            db.session.add(entrada)
            db.session.commit()
            return jsonify({'success': True, 'id': entrada.id})
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'error': str(e)}), 500


    ###############################################################
    #HORAS AUTO
    @app.route('/api/confhorasauto', methods=['POST'])
    def api_confhorasauto():
        data = request.get_json()
        tecnico_id = data.get('tecnico_id')
        horasdia = data.get('horasdia')
        auto = data.get('auto')
        tipo = data.get('tipo')
        pepnet = data.get('pepnet')
        laboratorios = data.get('laboratorios', [])
        peps_gerais = data.get('peps_gerais', [])
        horasgerais = data.get('horasgerais')

       
        if not tecnico_id:
            return jsonify({'success': False, 'error': 'Técnico não fornecido.'}), 400
        try:
            # Remove configuração anterior se existir
            conf = ConfHorasAuto.query.filter_by(tecnico_id=tecnico_id).first()
            if conf:
                ConfHorasAutoLab.query.filter_by(confhorasauto_id=conf.id).delete()
                ConfHorasAutoCodg.query.filter_by(confhorasauto_id=conf.id).delete()
                conf.horasdia = horasdia
                conf.auto = bool(int(auto)) if auto is not None else False
                conf.tipo = tipo
                conf.pepnet = pepnet
                conf.horasgerais = horasgerais
            else:
                conf = ConfHorasAuto(
                    tecnico_id=tecnico_id,
                    horasdia=horasdia,
                    auto=bool(int(auto)) if auto is not None else False,
                    tipo=tipo,
                    pepnet=pepnet,
                    horasgerais=horasgerais
                )
                db.session.add(conf)
                db.session.flush()  # Para obter conf.id

            # Adiciona laboratórios
            for lab_id in laboratorios:
                db.session.add(ConfHorasAutoLab(confhorasauto_id=conf.id, laboratorio_id=lab_id))
            # Adiciona códigos gerais
            for codg_id in peps_gerais:
                db.session.add(ConfHorasAutoCodg(confhorasauto_id=conf.id, codigog_id=codg_id))

            db.session.commit()
            return jsonify({'success': True})
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'error': str(e)}), 500

    @app.route('/api/confhorasauto', methods=['GET'])
    @login_required
    def get_all_confhorasauto():
        confs = (
            db.session.query(ConfHorasAuto, User)
            .join(User, User.id == ConfHorasAuto.tecnico_id)
            .order_by(User.full_name)
            .all()
        )

        return jsonify({
            'success': True,
            'data': [
                {
                    'tecnico_id': conf.tecnico_id,
                    'tecnico_nome': user.full_name,
                    'horasdia': conf.horasdia,
                    'horasgerais': conf.horasgerais,
                    'auto': int(conf.auto),
                    'tipo': conf.tipo,
                    'pepnet': conf.pepnet,
                    'laboratorios': [lab.laboratorio_id for lab in conf.laboratorios],
                    'peps_gerais': [cod.codigog_id for cod in conf.codigosg]
                }
                for conf, user in confs
            ]
        })

    @app.route('/api/confhorasauto/<int:tecnico_id>', methods=['GET'])
    def get_confhorasauto(tecnico_id):
        conf = ConfHorasAuto.query.filter_by(tecnico_id=tecnico_id).first()
        if not conf:
            return jsonify({'success': False, 'error': 'Configuração não encontrada.'}), 404
        return jsonify({
            'success': True,
            'tecnico_id': conf.tecnico_id,
            'horasdia': conf.horasdia,
            'auto': int(conf.auto),
            'tipo': conf.tipo,
            'pepnet': conf.pepnet,
            'horasgerais': conf.horasgerais,
            'laboratorios': [lab.laboratorio_id for lab in conf.laboratorios],
            'peps_gerais': [codg.codigog_id for codg in conf.codigosg]
        })
    
    @app.route('/api/gerar_horas_auto', methods=['POST'])
    def gerar_horas_auto():
        data = request.get_json()
        tecnico_id = data.get("tecnico_id")
        dias = data.get("dias", [])

        if not dias:
            return jsonify({"success": False, "error": "Nenhum dia recebido."}), 400

        # 1) Obter configuração
        conf = ConfHorasAuto.query.filter_by(tecnico_id=tecnico_id).first()
        if not conf:
            return jsonify({"success": False, "error": "Configuração não encontrada."}), 404

        # 2) Verificar tipo == "horas"
        if not conf.tipo or conf.tipo.lower() != "horas":
            return jsonify({
                "success": False,
                "error": "A criação de horas automáticas de acordo com o planeamento ainda não está configurada."
            }), 400

        horas_dia = conf.horasdia or 8

        # 3) Laboratórios permitidos para este técnico
        labs_permitidos = [lab.laboratorio_id for lab in conf.laboratorios]

        resultados = []

        for dia_str in dias:
            data_dia = datetime.strptime(dia_str, "%Y-%m-%d").date()

            # 4) Buscar registos da tabela 'horas' desse dia, com ensaio válido e lab permitido
            registos = (
                Horas.query
                .join(Ensaio, Horas.ensaio_id == Ensaio.id)
                .filter(
                    Horas.tecnico_id == tecnico_id,
                    Horas.data == data_dia,
                    Horas.ensaio_id.isnot(None),
                    Ensaio.laboratorio_id.in_(labs_permitidos)
                )
                .all()
            )

            # Total de horas já lançadas nestes ensaios
            total_horas = sum([float(r.horas) for r in registos])

            # Horas que faltam até o alvo
            falta = horas_dia - total_horas

            resultados.append({
                "dia": dia_str,
                "labs_permitidos": labs_permitidos,
                "total_existente": total_horas,
                "falta_lancar": max(falta, 0)
            })

            

        return jsonify({"success": True, "dias": resultados}), 200

    

    @app.route('/api/gerar_horas_auto_gerais', methods=['POST'])
    def gerar_horas_auto_gerais():
        data = request.get_json()
        tecnico_id = data.get("tecnico_id")
        dias = data.get("dias", [])

        conf = ConfHorasAuto.query.filter_by(tecnico_id=tecnico_id).first()
        horasdia = conf.horasdia or 8
        pct_gerais = (conf.horasgerais or 0) / 100.0
        horas_gerais_obj = horasdia * pct_gerais

        pepnet = (conf.pepnet or '').strip().lower()
        tipo_auto = 'pep' if pepnet == 'pep' else 'net'

        codigos = [c.codigog_id for c in conf.codigosg]
        n_codg = len(codigos)

        relatorio = []

        for dia_str in dias:
            data_dia = datetime.strptime(dia_str, "%Y-%m-%d").date()

            # 1. Total já lançado pelo próprio no dia
            total_dia = db.session.query(func.coalesce(func.sum(Horas.horas), 0.0)).filter(
                Horas.tecnico_id == tecnico_id,
                Horas.data == data_dia
            ).scalar()

            if total_dia >= horasdia:
                relatorio.append({"dia": dia_str, "status": "ignorado", "msg": "Já tem horas completas do dia."})
                continue

            # 2. Total de horas gerais já lançadas
            total_gerais = (
                db.session.query(func.coalesce(func.sum(Horas.horas), 0.0))
                .join(Codigosg, Horas.codigog_id == Codigosg.id)
                .filter(
                    Horas.tecnico_id == tecnico_id,
                    Horas.data == data_dia,
                    Codigosg.codigog.like('E.G7%')
                )
                .scalar()
            )

            if total_gerais >= horas_gerais_obj:
                relatorio.append({"dia": dia_str, "status": "ignorado", "msg": "Já tem todas as horas gerais permitidas."})
                continue

            # 3. Horas a gerar = diferença
            falta_gerais = horas_gerais_obj - total_gerais
            falta_gerais_por_codg = falta_gerais / n_codg

            gerados = []
            for codg in codigos:
                novo = Horas(
                    tecnico_id=tecnico_id,
                    data=data_dia,
                    horas=round(falta_gerais_por_codg, 2),
                    ensaio_id=None,
                    codigog_id=codg,
                    obs="Gerado de forma automática",
                    auto=True,
                    tipo=tipo_auto
                )
                db.session.add(novo)
                gerados.append({
                    "codigog_id": codg,
                    "horas": round(falta_gerais_por_codg, 2)
                })

            relatorio.append({
                "dia": dia_str,
                "status": "gerado",
                "total": round(falta_gerais, 2),
                "itens": gerados
            })

        db.session.commit()
        return jsonify({"success": True, "relatorio": relatorio})
    
    
    @app.route('/api/gerar_horas_auto_ensaios', methods=['POST'])
    def gerar_horas_auto_ensaios():
        """
        FASE 2: Gerar HORAS DE ENSAIO automaticamente (por dia selecionado).
        Regras:
        - Não ultrapassar 'horasdia' do técnico.
        - Usar apenas o 'restante' para atingir 'horasdia' (após o que já estiver lançado, incluindo gerais).
        - Distribuir proporcionalmente por ensaio, com base nas horas dos OUTROS técnicos no mesmo dia:
                * Apenas ensaios com laboratorio_id nos laboratórios configurados para este técnico.
                * Ignorar registos com obs = "Gerado de forma automática".
                * Ignorar horas do próprio técnico.
        - Upsert por (tecnico_id, data, ensaio_id): se existir, soma; senão cria.
        Corpo (JSON):
            {
            "tecnico_id": <int>,
            "dias": ["YYYY-MM-DD", ...]
            }
        Resposta (JSON):
            {
            "success": true,
            "relatorio": [
                {
                "dia": "YYYY-MM-DD",
                "status": "gerado" | "ignorado" | "erro",
                "msg": "...",                         # quando aplicável
                "total": <float>,                      # total gerado no dia (apenas se 'gerado')
                "itens": [{"ensaio_id": <int>, "horas": <float>}, ...]
                }, ...
            ]
            }
        """
        payload = request.get_json(silent=True) or {}
        tecnico_id = payload.get("tecnico_id")
        dias = payload.get("dias", [])

        # Validação de parâmetros
        if not tecnico_id or not isinstance(dias, list) or not dias:
            return jsonify({"success": False, "error": "Parâmetros inválidos (tecnico_id e dias são obrigatórios)."}), 400

        # Configuração do técnico
        conf = ConfHorasAuto.query.filter_by(tecnico_id=tecnico_id).first()
        if not conf:
            return jsonify({"success": False, "error": "Configuração não encontrada."}), 404

        # Apenas se tipo == "horas"
        if not conf.tipo or conf.tipo.lower() != "horas":
            return jsonify({
                "success": False,
                "error": "A criação de horas automáticas de acordo com o planeamento ainda não está configurada."
            }), 400

        # Alvo de horas por dia
        horasdia = float(conf.horasdia or 8.0)

        # logo após carregar conf em cada endpoint
        pepnet = (conf.pepnet or '').strip().lower()
        tipo_auto = 'pep' if pepnet == 'pep' else 'net'

        # Laboratórios permitidos
        labs_permitidos = [lab.laboratorio_id for lab in conf.laboratorios]
        if not labs_permitidos:
            return jsonify({"success": False, "error": "Sem laboratórios configurados nesta conta."}), 400

        relatorio = []

        for dia_str in dias:
            # Parse da data
            try:
                data_dia = datetime.strptime(dia_str, "%Y-%m-%d").date()
            except ValueError:
                relatorio.append({"dia": dia_str, "status": "erro", "msg": "Formato de data inválido (YYYY-MM-DD)."})
                continue

            # 1) Total de horas já lançadas PELO PRÓPRIO no dia (qualquer tipo)
            total_dia = (
                db.session.query(func.coalesce(func.sum(Horas.horas), 0.0))
                .filter(Horas.tecnico_id == tecnico_id, Horas.data == data_dia)
                .scalar()
            ) or 0.0

            # 2) Se já atingiu (ou ultrapassou) horasdia, não gerar nada
            if float(total_dia) >= horasdia - 1e-6:
                relatorio.append({
                    "dia": dia_str,
                    "status": "ignorado",
                    "msg": "Dia completo — já tem horas suficientes."
                })
                continue

            # 3) Restante para atingir horasdia
            restante = round(horasdia - float(total_dia), 2)
            if restante <= 0.0:
                relatorio.append({
                    "dia": dia_str,
                    "status": "ignorado",
                    "msg": "Não há tempo restante para ensaios."
                })
                continue

            # 4) Base de proporção: horas dos OUTROS técnicos (≠ tecnico_id) neste dia, por ensaio,
            #    ignorando registos 'Gerado de forma automática' e limitando aos laboratórios permitidos.
            outros = (
                db.session.query(
                    Horas.ensaio_id,
                    func.sum(Horas.horas).label("total")
                )
                .join(Ensaio, Horas.ensaio_id == Ensaio.id)
                .filter(
                    Horas.data == data_dia,
                    Horas.tecnico_id != tecnico_id,                   # apenas outros
                    Horas.ensaio_id.isnot(None),                      # só ensaio
                    ~or_(
                        func.coalesce(Horas.obs, '') == "Gerado de forma automática",
                        Horas.auto == True
                    ),
                    Ensaio.laboratorio_id.in_(labs_permitidos)
                )
                .group_by(Horas.ensaio_id)
                .all()
            )

            soma_outros = float(sum(float(r.total or 0.0) for r in outros))

            if soma_outros <= 1e-6:
                relatorio.append({
                    "dia": dia_str,
                    "status": "ignorado",
                    "msg": "Sem base de distribuição (outros técnicos = 0h em ensaios elegíveis)."
                })
                continue

            # 5) Distribuição proporcional do 'restante' por ensaio
            restante_ajuste = restante
            gerados = []

            for i, row in enumerate(outros):
                ensaio_id = int(row.ensaio_id)
                quota = float(row.total) / soma_outros
                horas_alocar = round(restante * quota, 2)

                # No último item, ajusta para fechar exatamente o 'restante'
                if i == len(outros) - 1:
                    horas_alocar = round(restante_ajuste, 2)

                restante_ajuste = round(restante_ajuste - horas_alocar, 2)

                if horas_alocar <= 0.0:
                    continue

                # 6) Upsert: se já existir do próprio em (dia, ensaio_id), soma; caso contrário, cria
                reg = (
                    Horas.query
                    .filter(
                        Horas.tecnico_id == tecnico_id,
                        Horas.data == data_dia,
                        Horas.ensaio_id == ensaio_id
                    )
                    .first()
                )

                if reg:
                    reg.horas = float(reg.horas) + horas_alocar
                    # Mantém 'obs' existente; se quiseres, força a nota automática:
                    # reg.obs = "Gerado de forma automática"
                else:
                    reg = Horas(
                        tecnico_id=tecnico_id,
                        data=data_dia,
                        horas=horas_alocar,
                        ensaio_id=ensaio_id,
                        codigog_id=None,
                        obs="Gerado de forma automática",
                        auto=True,
                        tipo=tipo_auto
                    )
                    db.session.add(reg)

                gerados.append({"ensaio_id": ensaio_id, "horas": horas_alocar})

            # (Opcional) commit por dia, para garantir persistência incremental
            # db.session.commit()

            total_gerado = round(sum(item["horas"] for item in gerados), 2)
            relatorio.append({
                "dia": dia_str,
                "status": "gerado" if total_gerado > 0 else "ignorado",
                "total": total_gerado,
                "itens": gerados
            })

        # Commit final
        db.session.commit()

        return jsonify({"success": True, "relatorio": relatorio}), 200

    ######################################################
    #home
    @app.route('/api/me')
    def api_me():
        user_id = session.get('user_id')
        funcao_id = session.get('funcao_id')
        laboratorio_id = session.get('laboratorio_id')

        if not user_id:
            return jsonify({"error": "not_authenticated"}), 401

        user = User.query.get(user_id)

        return jsonify({
            "id": user.id,
            "full_name": user.full_name,
            "funcao_id": funcao_id,
            "laboratorio_id": laboratorio_id,
        })
    

    @app.route('/home/ensaios_nao_concluidos')
    def home_ensaios_nao_concluidos():
        lab_id = request.args.get('laboratorio_id', type=int)
        if lab_id == 0:
            ensaios = (
                Ensaio.query
                .options(
                    joinedload(Ensaio.projeto),
                    joinedload(Ensaio.tipopeca),
                    joinedload(Ensaio.solicitante),
                    joinedload(Ensaio.laboratorio),
                )
                .filter(
                    or_(Ensaio.anulado.is_(False), Ensaio.anulado.is_(None)),
                    or_(Ensaio.concluido.is_(None), Ensaio.concluido == '0000-00-00')
                )
                .order_by(
                    (Ensaio.datasolicitada.is_(None)).asc(),
                    Ensaio.datasolicitada.asc()
                )
                .all()
            )
        else:
            ensaios = (
                Ensaio.query
                .options(
                    joinedload(Ensaio.projeto),
                    joinedload(Ensaio.tipopeca),
                    joinedload(Ensaio.solicitante),
                    joinedload(Ensaio.laboratorio),
                )
                .filter(
                    Ensaio.laboratorio_id == lab_id,
                    or_(Ensaio.anulado.is_(False), Ensaio.anulado.is_(None)),
                    or_(Ensaio.concluido.is_(None), Ensaio.concluido == '0000-00-00')
                )
                .order_by(
                    (Ensaio.datasolicitada.is_(None)).asc(),
                    Ensaio.datasolicitada.asc()
                )
                .all()
            )

        def fmt_date(dt):
            try:
                return dt.strftime('%Y-%m-%d') if dt else None
            except Exception:
                return None

        data = []
        for e in ensaios:
            data.append({
                "id": e.id,
                "ensaio": e.ensaio,                                         # número do ensaio
                "laboratorio": e.laboratorio.laboratorio if e.laboratorio else "",
                "codigo_projeto": e.projeto.codigo if e.projeto else "",
                "denominacao": e.projeto.descricao if e.projeto else "",
                "tipopeca": e.tipopeca.tipopeca if e.tipopeca else "",
                "solicitante": e.solicitante.nome if e.solicitante else "",
                "datasolicitada": fmt_date(e.datasolicitada),               # para ordenar e pintar
                "link": f"/ensaios?ensaio={e.ensaio}"               # ajusta: nome da tua rota de detalhe
            })
        return jsonify(data)

    @app.route('/home/avisos')
    def home_avisos():
        lab_id = request.args.get('laboratorio_id', type=int)
        if lab_id is None:
            return jsonify([])
        
        if lab_id == 0:
            ensaios = (
                Ensaio.query
                .options(
                    joinedload(Ensaio.projeto),
                    joinedload(Ensaio.tipopeca),
                    joinedload(Ensaio.solicitante),
                    joinedload(Ensaio.laboratorio),
                )
                .filter(
                    or_(Ensaio.concluido.is_(None), Ensaio.concluido == '0000-00-00')
                )
                .order_by(
                    (Ensaio.datasolicitada.is_(None)).asc(),
                    Ensaio.datasolicitada.asc()
                )
                .all()
            )
        else:
            ensaios = (
                Ensaio.query
                .options(
                    joinedload(Ensaio.projeto),
                    joinedload(Ensaio.tipopeca),
                    joinedload(Ensaio.solicitante),
                    joinedload(Ensaio.laboratorio),
                )
                .filter(
                    Ensaio.laboratorio_id == lab_id,
                    or_(Ensaio.concluido.is_(None), Ensaio.concluido == '0000-00-00')
                )
                .order_by(
                    (Ensaio.datasolicitada.is_(None)).asc(),
                    Ensaio.datasolicitada.asc()
                )
                .all()
            )

        avisos = []
        for e in ensaios:
            tem_horas = any(h.ensaio_id == e.id for h in e.horas)
            if not tem_horas:
                continue

            falta_network = not e.network or not e.network.strip()
            falta_pep     = not e.pep or not e.pep.strip()

            if falta_network or falta_pep:
                avisos.append({
                    "ensaio": e.ensaio,
                    "link": f"/ensaios?ensaio={e.ensaio}",
                    "falta_network": falta_network,
                    "falta_pep": falta_pep,
                })

        return jsonify(avisos)

    

    @app.route('/home/avisos_horas')
    def home_avisos_horas():
        tecnico_id = session.get('user_id')
        if not tecnico_id:
            return jsonify({"has_old_unexported": False})

        hoje = date.today()
        inicio_semana = hoje - timedelta(days=hoje.weekday())  # segunda-feira desta semana

        # Alguma hora não exportada antes desta semana?
        existe = (
            db.session.query(Horas.id)
            .filter(
                Horas.tecnico_id == tecnico_id,
                ((Horas.exportado.is_(None)) | (Horas.exportado == '0000-00-00')),
                Horas.data < inicio_semana
            )
            .first()
        )

        return jsonify({"has_old_unexported": bool(existe)})
    
    @app.route('/home/avisos_horas_percentagem')
    def home_avisos_horas_percentagem():
        tecnico_id = session.get('user_id')
        if not tecnico_id:
            return jsonify({"excedeu": False})


        hoje = date.today()

        # Primeiro dia do mês
        inicio_mes = hoje.replace(day=1)

        # Buscar configuração do técnico
        conf = ConfHorasAuto.query.filter_by(tecnico_id=tecnico_id).first()
        if not conf:
            return jsonify({"excedeu": False})

        

        # HORAS TOTAIS DO MÊS
        horas_totais = (
            db.session.query(db.func.coalesce(db.func.sum(Horas.horas), 0))
            .filter(
                Horas.tecnico_id == tecnico_id,
                Horas.data >= inicio_mes
            )
            .scalar()
        )

        if horas_totais == 0:
            return jsonify({"excedeu": False})

      # HORAS GERAIS para percentagem (apenas codigos E.G7*)
        horas_gerais = (
            db.session.query(db.func.coalesce(db.func.sum(Horas.horas), 0))
            .join(Codigosg, Horas.codigog_id == Codigosg.id)
            .filter(
                Horas.tecnico_id == tecnico_id,
                Horas.data >= inicio_mes,
                Codigosg.codigog.like('E.G7%')
            )
            .scalar()
        )

        limite_percentagem = float(conf.horasgerais or 0)  # Ex: 10 significa 10%
        tolerancia = 0.5
        limite_com_tolerancia = limite_percentagem + tolerancia
        
        percentagem = (horas_gerais / horas_totais) * 100
        
        excedeu = percentagem > limite_com_tolerancia

        return jsonify({
            "excedeu": excedeu,
            "percentagem_real": round(percentagem, 2),
            "limite": limite_percentagem,
            "tolerancia": tolerancia,
            "limite_com_tolerancia": round(limite_com_tolerancia, 2)
        })

    
    # Endpoint para listar relatórios pendentes
    @app.route('/home/relatorios_pendentes')
    def home_relatorios_pendentes():
        user = User.query.get(session['user_id'])
        funcao_id = user.funcao_id
        laboratorio_id = request.args.get('laboratorio_id', type=int)
    
        # Testes do tipo "Report" com data de início e sem data de fim
        query = Testes.query.join(Ensaio).filter(
            Testes.qtd != None,
            or_(
                Testes.datafim == None,
                Testes.datafim == '0000-00-00 00:00:00'
            ),
            Testes.teste.has(teste='Report'),
            Ensaio.anulado == False,
            # Verifica se existe pelo menos um teste com datainicio no mesmo ensaio
            Ensaio.testes.any(Testes.datainicio != None)
        )
        if funcao_id == 1:
            query = query.filter(Testes.user_id == user.id)
        elif laboratorio_id:
            if laboratorio_id != 4:
                query = query.filter(Ensaio.laboratorio_id == laboratorio_id)
    
        testes = query.all()
        result = []
        for t in testes:
            ensaio = t.ensaio
            projeto = ensaio.projeto
            solicitante = ensaio.solicitante
            tecnico = t.user
            report = t.report[0] if hasattr(t, 'report') and t.report else None
            if report and report.concluido and str(report.concluido) != '0000-00-00 00:00:00':
                concluido = report.concluido.strftime('%Y-%m-%d')
            else:
                concluido = ''
           
            result.append({
                'ensaio': ensaio.ensaio,
                'link': f"/ensaios?ensaio={ensaio.ensaio}",
                'codigo_projeto': projeto.codigo if projeto else '',
                'denominacao': projeto.descricao if projeto else '',
                'solicitante': solicitante.nome if solicitante else '',
                'tecnico': tecnico.full_name if tecnico else '',
                'datainicio': t.datainicio.strftime('%Y-%m-%d') if t.datainicio else '',
                'concluido': concluido,
                'report_id': t.id
            })
        return jsonify(result)
    
    @app.route('/reports/<int:teste_id>/concluido', methods=['POST'])
    def update_report_concluido(teste_id):
        data = request.get_json()
        checked = bool(data.get('concluido', False))
        report = Report.query.filter_by(teste_id=teste_id).first()
        if checked:
            valor = datetime.now()
        else:
            valor = None  # ou '0000-00-00 00:00:00' se quiser string
        
        if report:
            report.concluido = valor
        else:
            report = Report(teste_id=teste_id, concluido=valor)
            db.session.add(report)
        db.session.commit()
        return jsonify({'success': True, 'concluido': report.concluido, 'report_id': report.id})

    
    @app.route('/home/resumo_horas')
    def home_resumo_horas():
        user = User.query.get(session['user_id'])
        funcao_id = user.funcao_id
    
        laboratorio_id = request.args.get('laboratorio_id', type=int)
        ano = request.args.get('ano', type=int)
        mes = request.args.get('mes', type=int)
        if ano is None or mes is None or laboratorio_id == '':
            return jsonify([])
    
        # Técnicos (funcao_id=1) veem SÓ os seus dados
        # Coordenadores/Sistema (funcao_id 2,3) veem todos os users do lab
        if funcao_id == 1:
            tecnicos = [user]  # Apenas o próprio
        elif funcao_id in (2, 3):
            if laboratorio_id == 0:
                tecnicos = User.query.all()
            else:
                tecnicos = User.query.filter_by(laboratorio_id=laboratorio_id).all()
        else:
            return jsonify([])  # Outras funções não veem

        hoje = date.today()
        ultimo_dia = monthrange(ano, mes)[1]
        dia_fim = hoje.day if (ano == hoje.year and mes == hoje.month) else ultimo_dia
    
        dias_uteis = sum(1 for dia in range(1, dia_fim + 1) if date(ano, mes, dia).weekday() < 5)
        data_ini = date(ano, mes, 1)
        data_fim = date(ano, mes, dia_fim)
    
        result = []
        for tecnico in tecnicos:
            conf = ConfHorasAuto.query.filter_by(tecnico_id=tecnico.id).first()
            horasdia = conf.horasdia if conf and conf.horasdia else 0
            horas_previstas = horasdia * dias_uteis
    
            horas_lancadas = db.session.query(db.func.coalesce(db.func.sum(Horas.horas), 0)).filter(
                Horas.tecnico_id == tecnico.id,
                Horas.data >= data_ini,
                Horas.data <= data_fim
            ).scalar() or 0
    
            horas_gerais = (
                db.session.query(db.func.coalesce(db.func.sum(Horas.horas), 0))
                .join(Codigosg, Horas.codigog_id == Codigosg.id)
                .filter(
                    Horas.tecnico_id == tecnico.id,
                    Horas.data >= data_ini,
                    Horas.data <= data_fim,
                    Codigosg.codigog.like('E.G7%')
                )
                .scalar()
                or 0
            )
    
            pct_gerais = (horas_gerais / horas_lancadas * 100) if horas_lancadas else 0
    
            ultima_exportacao = (
                db.session.query(db.func.max(Horas.exportado))
                .filter(Horas.tecnico_id == tecnico.id)
                .scalar()
            )
            
            # alerta se vazio ou mais de 7 dias
            exportacao_alerta = (
                ultima_exportacao is None or
                (hoje - ultima_exportacao).days > 7
            )

            result.append({
                'tecnico': tecnico.full_name,
                'horas_previstas': round(horas_previstas, 2),
                'horas_lancadas': round(horas_lancadas, 2),
                'percentagem_gerais': round(pct_gerais, 1),
                'limite_gerais': conf.horasgerais if conf and conf.horasgerais is not None else 0,
                'ultima_exportacao': ultima_exportacao.strftime('%Y-%m-%d') if ultima_exportacao else '', 
                'exportacao_alerta': exportacao_alerta
            })
        return jsonify(result)
    
    #############################################################

    @app.route('/api/normas_by_laboratorio')
    def normas_by_laboratorio():
        laboratorio_id = request.args.get('laboratorio_id', type=int)
        normas = Normas.query.filter_by(laboratorio_id=laboratorio_id).all()
        return jsonify(normas=[{'id': n.id, 'norma': n.norma} for n in normas])

    
    #conf emails automáticos
    @app.route('/laboratorios/ativos', methods=['GET'])
    @login_required
    def laboratorios_ativos():
        """Retorna lista de laboratórios ativos para dropdown"""
        labs = Laboratorio.query.filter_by(obsoleto=False).order_by(Laboratorio.laboratorio).all()
        return jsonify([{'id': l.id, 'laboratorio': l.laboratorio} for l in labs])
    
    
    @app.route('/api/confemailauto', methods=['GET'])
    @login_required
    def get_confemailauto():
        """Lista todas as configurações de email automático"""
        cfgs = ConfEmailAuto.query.order_by(ConfEmailAuto.id).all()
        result = []
        for cfg in cfgs:
            # Buscar nomes dos laboratórios associados
            lab_ids = [rel.laboratorio_id for rel in cfg.laboratorios]
            lab_names = []
            if lab_ids:
                labs = Laboratorio.query.filter(Laboratorio.id.in_(lab_ids)).all()
                lab_names = [l.laboratorio for l in labs]
            
            result.append({
                'id': cfg.id,
                'nome': cfg.nome,
                'evento': cfg.evento,
                'assunto': cfg.assunto,
                'texto': cfg.texto,
                'to_email': cfg.to_email,
                'cc_email': cfg.cc_email or '',
                'obsoleto': cfg.obsoleto,
                'laboratorios': lab_ids,
                'laboratorios_nomes': lab_names
            })
        return jsonify(result)
    
    
    @app.route('/api/confemailauto', methods=['POST'])
    @login_required
    def save_confemailauto():
        """Cria ou atualiza configuração de email automático"""
        try:
            data = request.get_json()
            cfg_id = data.get('id')
            
            if cfg_id:
                # Atualizar existente
                cfg = ConfEmailAuto.query.get(cfg_id)
                if not cfg:
                    return jsonify({'error': 'Configuração não encontrada'}), 404
            else:
                # Criar novo
                cfg = ConfEmailAuto()
                db.session.add(cfg)
            
            # Atualizar campos
            cfg.nome = data.get('nome', '').strip()
            cfg.evento = data.get('evento', '').strip()
            cfg.assunto = data.get('assunto', '').strip()
            cfg.texto = data.get('texto', '').strip()
            cfg.to_email = data.get('to_email', '').strip()
            cfg.cc_email = data.get('cc_email', '').strip()
            cfg.obsoleto = data.get('obsoleto', False)
            cfg.laboratorio_id = 0  # legado/compatibilidade
            
            # Commit para obter o ID se for novo
            db.session.commit()
            
            # Atualizar laboratórios (N:N)
            lab_ids = data.get('laboratorios', [])
            
            # Remover relações antigas
            ConfEmailAutoLab.query.filter_by(confemailauto_id=cfg.id).delete()
            
            # Criar novas relações
            for lab_id in lab_ids:
                rel = ConfEmailAutoLab(
                    confemailauto_id=cfg.id,
                    laboratorio_id=lab_id
                )
                db.session.add(rel)
            
            db.session.commit()
            
            return jsonify({'success': True, 'id': cfg.id})
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @app.route('/api/email-variables', methods=['GET'])
    @login_required
    def email_variables():
        evento = (request.args.get('evento') or '').strip()
    
       
        catalogo = {
                'ensaio_concluido': [
                    {'key': 'ensaio', 'label': 'Numero do ensaio', 'example': '8400159562'},
                    {'key': 'link_pasta', 'label': 'Link da pasta', 'example': r'L:\AIRBAG\TESTS\...'},
                    {'key': 'solicitante_email', 'label': 'Email do solicitante', 'example': 'nome@zf-lifetec.com'},
                    {'key': 'destinatario', 'label': 'Destinatario final', 'example': 'nome@zf-lifetec..com'},
                    {'key': 'n_pecas', 'label': 'Numero de pecas', 'example': '12'},
                    {'key': 'tipo_peca', 'label': 'Tipo de peca', 'example': 'DAB'},
                    {'key': 'cod_projeto', 'label': 'Codigo do projeto', 'example': 'E.16000402'},
                    {'key': 'denominacao_projeto', 'label': 'Denominacao do projeto', 'example': 'BMW G5x'},
                    {'key': 'email_laboratorio', 'label': 'Email do Laboratório', 'example': 'nome@zf-lifetec..com'}
                ],
                'envio_externo_concluido': [
                    {'key': 'email_localizacao_origem', 'label': 'Email da localização de origem', 'example': 'armazem_origem@empresa.com'},
                    {'key': 'email_localizacao_destino', 'label': 'Email da localização de destino', 'example': 'armazem@empresa.com'},
                    {'key': 'email_responsavel', 'label': 'Email do(s) responsável(eis) da(s) referência(s)', 'example': 'resp1@empresa.com; resp2@empresa.com'},
                    {'key': 'data', 'label': 'Data planeada', 'example': '2026-03-25'},
                    {'key': 'hora', 'label': 'Hora planeada', 'example': '14:30'},
                    {'key': 'dia_semana', 'label': 'Dia da semana', 'example': 'Quarta-feira'},
                    {'key': 'destino', 'label': 'Localização de destino', 'example': 'Armazém Airbag'},
                    {'key': 'referencia', 'label': 'Referência(s)', 'example': 'REF001, REF002'},
                    {'key': 'tipo_volume', 'label': 'Tipo(s) de volume', 'example': 'Caixa, Palete'},
                    {'key': 'dimensoes', 'label': 'Dimensões', 'example': 'REF001: 10x20x30; REF002: 15x25x35'},
                    {'key': 'peso', 'label': 'Peso(s)', 'example': 'REF001: 2.50; REF002: 4.10'},
                    {'key': 'tabela_referencias', 'label': 'Tabela de referências formatada', 'example': 'Tipo Embalagem | Referência | Dimensões | Peso\nCaixa | REF001 | 10x5x20 | 10.00'}
                ],
                'recolha_interna_concluida': [
                    {'key': 'email_localizacao_origem', 'label': 'Email da localização de origem', 'example': 'armazem_origem@empresa.com'},
                    {'key': 'email_localizacao_destino', 'label': 'Email da localização de destino', 'example': 'armazem@empresa.com'},
                    {'key': 'email_responsavel', 'label': 'Email do(s) responsável(eis) da(s) referência(s)', 'example': 'resp1@empresa.com; resp2@empresa.com'},
                    {'key': 'data', 'label': 'Data planeada', 'example': '2026-03-25'},
                    {'key': 'hora', 'label': 'Hora planeada', 'example': '14:30'},
                    {'key': 'dia_semana', 'label': 'Dia da semana', 'example': 'Quarta-feira'},
                    {'key': 'destino', 'label': 'Localização de destino', 'example': 'Armazém Airbag'},
                    {'key': 'referencia', 'label': 'Referência(s)', 'example': 'REF001, REF002'},
                    {'key': 'tipo_volume', 'label': 'Tipo(s) de volume', 'example': 'Caixa, Palete'},
                    {'key': 'dimensoes', 'label': 'Dimensões', 'example': 'REF001: 10x20x30; REF002: 15x25x35'},
                    {'key': 'peso', 'label': 'Peso(s)', 'example': 'REF001: 2.50; REF002: 4.10'},
                    {'key': 'tabela_referencias', 'label': 'Tabela de referências formatada', 'example': 'Tipo Embalagem | Referência | Dimensões | Peso\nCaixa | REF001 | 10x5x20 | 10.00'}
                ]
            }
        
    
        return jsonify({
            'evento': evento,
            'variables': catalogo.get(evento, [])
        })

    @app.route('/api/confemailauto/<int:cfg_id>', methods=['DELETE'])
    def delete_confemailauto(cfg_id):
        cfg = ConfEmailAuto.query.get_or_404(cfg_id)
    
        try:
            ConfEmailAutoLab.query.filter_by(confemailauto_id=cfg.id).delete()
            db.session.delete(cfg)
            db.session.commit()
            return jsonify({'success': True})
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'error': str(e)}), 500
 
    @app.route('/api/render-email-conclusao', methods=['POST'])
    @login_required
    def render_email_conclusao():
        """
        Busca configurações ativas de email para ensaio_concluido no laboratório do ensaio,
        renderiza o template com as variáveis do ensaio e retorna o email pronto.
        """
        try:
            data = request.get_json()
            ensaio_id = data.get('ensaio_id')
            
            if not ensaio_id:
                return jsonify({'error': 'ID do ensaio não fornecido'}), 400
            
            # Buscar o ensaio
            ensaio = Ensaio.query.get(ensaio_id)
            if not ensaio:
                return jsonify({'error': 'Ensaio não encontrado'}), 404
            
            laboratorio_id = ensaio.laboratorio_id
            
            # Buscar configurações ativas para ensaio_concluido neste laboratório
            configs = (
                ConfEmailAuto.query
                .join(ConfEmailAutoLab, ConfEmailAuto.id == ConfEmailAutoLab.confemailauto_id)
                .filter(
                    ConfEmailAuto.evento == 'ensaio_concluido',
                    ConfEmailAuto.obsoleto == False,
                    ConfEmailAutoLab.laboratorio_id == laboratorio_id
                )
                .all()
            )
            
            if not configs:
                return jsonify({'error': 'Nenhuma configuração de email ativa encontrada para este laboratório'}), 404
            
            # Usar a primeira configuração encontrada (pode haver várias)
            cfg = configs[0]
            
            # Construir contexto com as variáveis disponíveis
            contexto = {}
            
            # ensaio
            contexto['ensaio'] = ensaio.ensaio or ''
            
            # link_pasta - construir caminho completo
            if ensaio.laboratorio and ensaio.laboratorio.pastatestes:
                ano = ensaio.datapedido.year if ensaio.datapedido else ''
                cliente = ensaio.cliente.cliente.upper() if ensaio.cliente else ''
                tipo_fase = (ensaio.corecustomer or 'Customer').strip().upper()
                cod_projeto = ensaio.projeto.codigo.upper() if ensaio.projeto and ensaio.projeto.codigo else ''
                denominacao = ensaio.projeto.descricao.upper() if ensaio.projeto and ensaio.projeto.descricao else ''
                tipopeca = ensaio.tipopeca.tipopeca.upper() if ensaio.tipopeca else ''
                projeto_folder = f"{cod_projeto}_{denominacao}_{tipopeca}" if cod_projeto and denominacao and tipopeca else ''
                
                link_pasta = f"{ensaio.laboratorio.pastatestes}\\{ensaio.laboratorio.laboratorio.upper()}\\{ano}\\{tipo_fase}\\{cliente}\\{projeto_folder}\\{ensaio.ensaio}"
                contexto['link_pasta'] = link_pasta
            else:
                contexto['link_pasta'] = ''
            
            # solicitante_email
            contexto['solicitante_email'] = ensaio.solicitante.email if ensaio.solicitante and ensaio.solicitante.email else ''
            
            # destinatario (vem do campo destinodevol)
            contexto['destinatario'] = ensaio.destinodevol or ''
            
            # n_pecas
            contexto['n_pecas'] = str(ensaio.npecasrecebidas) if ensaio.npecasrecebidas else ''
            
            # tipo_peca
            contexto['tipo_peca'] = ensaio.tipopeca.tipopeca if ensaio.tipopeca else ''
            
            # cod_projeto
            contexto['cod_projeto'] = ensaio.projeto.codigo if ensaio.projeto else ''
            
            # denominacao_projeto
            contexto['denominacao_projeto'] = ensaio.projeto.descricao if ensaio.projeto else ''
            
            # email_laboratorio
            contexto['email_laboratorio'] = ensaio.laboratorio.email if ensaio.laboratorio and ensaio.laboratorio.email else ''
            
            # Renderizar templates
            emails = []
            for cfg in configs:
                try:
                    assunto_renderizado = render_template_string(cfg.assunto or '', **contexto)
                    texto_renderizado = render_template_string(cfg.texto or '', **contexto)
                    to_email_renderizado = render_template_string(cfg.to_email or '', **contexto)
                    cc_email_renderizado = render_template_string(cfg.cc_email or '', **contexto)
                except Exception as e:
                    return jsonify({'error': f'Erro ao renderizar template ({cfg.nome}): {str(e)}'}), 500

                emails.append({
                    'config_id': cfg.id,
                    'config_nome': cfg.nome,
                    'assunto': assunto_renderizado,
                    'texto': texto_renderizado,
                    'to_email': to_email_renderizado,
                    'cc_email': cc_email_renderizado
                })

            return jsonify({
                'success': True,
                'total': len(emails),
                'emails': emails
            })
            
        except Exception as e:
            current_app.logger.error(f"Erro ao renderizar email de conclusão: {e}")
            return jsonify({'error': str(e)}), 500
        
    
    # ------------------------------------------------------------------ #
    # PEDIR HORAS EXTRA                                                 #
    # ------------------------------------------------------------------ #

    @app.route('/api/testes_por_lab', methods=['GET'])
    @login_required
    def get_testes_por_lab():
        lab_id = request.args.get('lab_id', '')
        so_pendentes = request.args.get('so_pendentes', '1') == '1'
    
        query = (
            db.session.query(Testes, Ensaio)
            .join(Ensaio, Testes.ensaio_id == Ensaio.id)
            .filter(Ensaio.anulado == False)
        )
    
        if lab_id and lab_id != 'todos':
            try:
                query = query.filter(Ensaio.laboratorio_id == int(lab_id))
            except (ValueError, TypeError):
                pass
    
        if so_pendentes:
            query = query.filter(
                or_(Testes.datafim.is_(None), Testes.datafim == '0000-00-00 00:00:00')
            )
    
        def safe_iso(val):
            if not val:
                return ''
            if hasattr(val, 'isoformat'):
                s = val.isoformat()
                return '' if s.startswith('0000') else s
            s = str(val)
            return '' if s.startswith('0000') else s
    
        output = []
        try:
            results = query.order_by(Ensaio.ensaio, Testes.id).all()
            for teste, ensaio in results:
                try:
                    output.append({
                        'id': teste.id,
                        'ensaio': ensaio.ensaio,
                        'teste': teste.teste.teste if teste.teste else '',
                        'datainicio': safe_iso(teste.datainicio),
                        'datafim': safe_iso(teste.datafim),
                    })
                except Exception:
                    continue  # ignora linhas com datas inválidas
        except Exception as e:
            current_app.logger.error(f"Erro em testes_por_lab: {e}")
            return jsonify({'error': str(e)}), 500
    
        return jsonify(output)


    @app.route('/api/pedido_horas_extra', methods=['POST'])
    @login_required
    def save_pedido_horas_extra():
        try:
            data = request.get_json()
            tecnico_id = session.get('user_id')
            pedido = PedidoHorasExtra(
                tecnico_id=tecnico_id,
                teste_id=data.get('teste_id') or None,
                data=datetime.strptime(data['data'], '%Y-%m-%d').date(),
                horas=float(data['horas']),
                justificacao=(data.get('justificacao') or '').strip(),
            )
            db.session.add(pedido)
            db.session.commit()
            return jsonify({'success': True, 'id': pedido.id})
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Erro ao guardar pedido de horas extra: {e}")
            return jsonify({'error': str(e)}), 500

    @app.route('/api/pedidos_horas_extra', methods=['GET'])
    @login_required
    def listar_pedidos_horas_extra():
        user = User.query.get(session.get('user_id'))
        if not user:
            return jsonify([])
    
        lab_id = request.args.get('laboratorio_id', type=int)
    
        q = (
            db.session.query(
                PedidoHorasExtra,
                User.full_name.label('tecnico_nome'),
                Ensaio.ensaio.label('ensaio_nome'),
                Tipotestes.teste.label('teste_nome'),
                Ensaio.laboratorio_id.label('ensaio_lab_id')
            )
            .join(User, PedidoHorasExtra.tecnico_id == User.id)
            .join(Testes, PedidoHorasExtra.teste_id == Testes.id)
            .join(Ensaio, Testes.ensaio_id == Ensaio.id)
            .join(Tipotestes, Testes.teste_id == Tipotestes.id)
        )
    
        # Função 1: só os próprios pedidos (Pendente/Recusado)
        if user.funcao_id == 1:
            q = q.filter(
                PedidoHorasExtra.tecnico_id == user.id,
                PedidoHorasExtra.estado.in_(['Pendente', 'Recusado'])
            )
        # Função 2 e 3: pedidos pendentes do laboratório selecionado
        elif user.funcao_id in (2, 3):
            q = q.filter(PedidoHorasExtra.estado == 'Pendente')
        
            # lab_id > 0 => filtra por laboratório
            # lab_id == 0 ou None => "Todos"
            if lab_id and lab_id > 0:
                q = q.filter(Ensaio.laboratorio_id == lab_id)
        else:
            return jsonify([])
    
        rows = q.order_by(PedidoHorasExtra.data_pedido.desc()).all()
    
        out = []
        for pedido, tecnico_nome, ensaio_nome, teste_nome, ensaio_lab_id in rows:
            out.append({
                'id': pedido.id,
                'tecnico_id': pedido.tecnico_id,
                'tecnico_nome': tecnico_nome,
                'teste_id': pedido.teste_id,
                'teste': f"{ensaio_nome} - {teste_nome}",
                'ensaio_id': Testes.query.get(pedido.teste_id).ensaio_id if pedido.teste_id else None,
                'data': pedido.data.isoformat() if pedido.data else '',
                'horas': float(pedido.horas or 0),
                'justificacao': pedido.justificacao or '',
                'estado': pedido.estado or '',
                'laboratorio_id': ensaio_lab_id
            })
    
        return jsonify(out)
    
    
    @app.route('/api/pedido_horas_extra/<int:pedido_id>/estado', methods=['PUT'])
    @login_required
    def atualizar_estado_pedido_horas_extra(pedido_id):
        user = User.query.get(session.get('user_id'))
        if not user:
            return jsonify({'error': 'Utilizador não autenticado'}), 401
    
        pedido = PedidoHorasExtra.query.get_or_404(pedido_id)
        novo_estado = (request.json or {}).get('estado', '').strip()
    
        # Regra função 1: apenas eliminar os próprios pedidos
        if user.funcao_id == 1:
            if pedido.tecnico_id != user.id:
                return jsonify({'error': 'Sem permissão'}), 403
            if novo_estado != 'Eliminado':
                return jsonify({'error': 'Apenas pode eliminar pedidos'}), 400
    
        # Regra função 2/3: apenas recusar pendentes
        elif user.funcao_id in (2, 3):
            if novo_estado != 'Recusado':
                return jsonify({'error': 'Estado inválido'}), 400
        else:
            return jsonify({'error': 'Sem permissão'}), 403
    
        pedido.estado = novo_estado
        db.session.commit()
        return jsonify({'success': True})
    
    
    @app.route('/api/pedido_horas_extra/<int:pedido_id>/tratar', methods=['POST'])
    @login_required
    def tratar_pedido_horas_extra(pedido_id):
        user = User.query.get(session.get('user_id'))
        if not user or user.funcao_id not in (2, 3):
            return jsonify({'error': 'Sem permissão'}), 403
    
        pedido = PedidoHorasExtra.query.get_or_404(pedido_id)
        if pedido.estado != 'Pendente':
            return jsonify({'error': 'Pedido já tratado'}), 400
    
        payload = request.get_json(silent=True) or {}
        data_str = payload.get('data')
        horas_val = payload.get('horas')
        obs = (payload.get('obs') or '').strip()
    
        if not data_str:
            return jsonify({'error': 'Data obrigatória'}), 400
    
        try:
            dia = date.fromisoformat(data_str)
            horas_num = float(
                Decimal(str(horas_val)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            )
        except Exception:
            return jsonify({'error': 'Data/horas inválidas'}), 400
    
        teste = Testes.query.get(pedido.teste_id)
        if not teste:
            return jsonify({'error': 'Teste não encontrado'}), 404
    
        nova_hora = Horas(
            tecnico_id=pedido.tecnico_id,
            data=dia,
            horas=horas_num,
            ensaio_id=teste.ensaio_id,
            teste_id=pedido.teste_id,
            obs=obs or f"Pedido horas extra #{pedido.id}: {pedido.justificacao or ''}",
            extra=True
        )
        db.session.add(nova_hora)
    
        pedido.estado = 'Tratado'
        db.session.commit()
    
        return jsonify({'success': True, 'hora_id': nova_hora.id})


    #REGRAS VALIDACAO
    @app.route('/api/confvalidacaomanual', methods=['GET'])
    @login_required
    def api_confvalidacaomanual_list():
        regras = (
            ConfValidacaoManual.query
            .order_by(
                ConfValidacaoManual.obsoleto.asc(),
                ConfValidacaoManual.nome.asc(),
                ConfValidacaoManual.id.asc()
            )
            .all()
        )

        return jsonify([
            {
                'id': r.id,
                'nome': r.nome,
                'regex': r.regex,
                'chave_i18n': r.chave_i18n,
                'obsoleto': int(r.obsoleto or 0),
            }
            for r in regras
        ])


    @app.route('/api/confvalidacaomanual/aplicaveis/manual', methods=['GET'])
    @login_required
    def api_confvalidacaomanual_aplicaveis_manual():
        regras = _get_regras_manuais_aplicaveis()
        return jsonify([
            {
                'id': r.id,
                'nome': r.nome,
                'regex': r.regex,
                'chave_i18n': r.chave_i18n,
                'obsoleto': int(r.obsoleto or 0),
            }
            for r in regras
        ])


    @app.route('/api/confvalidacaomanual/validar/manual', methods=['POST'])
    @login_required
    def api_confvalidacaomanual_validar_manual():
        data = request.get_json(silent=True) or {}
        valor = data.get('manual')
        ok, detalhe = _validar_manual_por_regras(valor)

        if ok:
            return jsonify({'success': True, 'valid': True, 'code': detalhe})

        return jsonify({
            'success': True,
            'valid': False,
            'code': detalhe
        }), 400


    @app.route('/api/confvalidacaomanual/<int:regra_id>', methods=['GET'])
    @login_required
    def api_confvalidacaomanual_get(regra_id):
        r = ConfValidacaoManual.query.get(regra_id)
        if not r:
            return jsonify({'success': False, 'error': 'Regra nao encontrada.'}), 404

        return jsonify({
            'id': r.id,
            'nome': r.nome,
            'regex': r.regex,
            'chave_i18n': r.chave_i18n,
            'obsoleto': int(r.obsoleto or 0),
        })


    @app.route('/api/confvalidacaomanual', methods=['POST'])
    @login_required
    def api_confvalidacaomanual_save():
        data = request.get_json(silent=True) or {}

        regra_id = data.get('id')
        nome = (data.get('nome') or '').strip()
        regex_val = (data.get('regex') or '').strip()
        chave_i18n = (data.get('chave_i18n') or '').strip() or None
        obsoleto_raw = data.get('obsoleto', 0)

        if not nome:
            return jsonify({'success': False, 'error': 'O campo nome e obrigatorio.'}), 400
        if not regex_val:
            return jsonify({'success': False, 'error': 'O campo regex e obrigatorio.'}), 400

        try:
            re.compile(regex_val)
        except re.error as ex:
            return jsonify({'success': False, 'error': f'Regex invalida: {ex}'}), 400

        obsoleto = 1 if str(obsoleto_raw).lower() in ('1', 'true', 't', 'yes') else 0

        try:
            if regra_id:
                regra = ConfValidacaoManual.query.get(regra_id)
                if not regra:
                    return jsonify({'success': False, 'error': 'Regra nao encontrada.'}), 404
            else:
                regra = ConfValidacaoManual()
                db.session.add(regra)

            regra.nome = nome
            regra.regex = regex_val
            regra.chave_i18n = chave_i18n
            regra.obsoleto = obsoleto

            db.session.commit()
            return jsonify({'success': True, 'id': regra.id})

        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'error': str(e)}), 500


    @app.route('/api/confvalidacaomanual/<int:regra_id>', methods=['DELETE'])
    @login_required
    def api_confvalidacaomanual_delete(regra_id):
        regra = ConfValidacaoManual.query.get(regra_id)
        if not regra:
            return jsonify({'success': False, 'error': 'Regra nao encontrada.'}), 404

        try:
            db.session.delete(regra)
            db.session.commit()
            return jsonify({'success': True})
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'error': str(e)}), 500

    ###################################################################
    #alterar tempos em todos os testes
    @app.route('/api/tipos_teste', methods=['GET'])
    @login_required
    def api_tipos_teste():
        tipos = Tipotestes.query.order_by(Tipotestes.teste.asc()).all()
        return jsonify([{'id': t.id, 'nome': t.teste} for t in tipos])
    
    @app.route('/api/normas_por_teste', methods=['GET'])
    @login_required
    def api_normas_por_teste():
        teste_id = request.args.get('teste_id', type=int)
        campo = request.args.get('campo', type=str)

        if not teste_id or campo not in {'duracao', 'duracaomontagem', 'tempopp', 'tempomp'}:
            return jsonify([])

        normas = (
            db.session.query(
                Normas.id.label('norma_id'),
                Normas.norma.label('nome'),
                getattr(Templatenormas, campo).label('valor')
            )
            .join(Templatenormas, Templatenormas.norma_id == Normas.id)
            .filter(
                Templatenormas.teste_id == teste_id,
                Templatenormas.obsoleto == False
            )
            .order_by(Normas.norma.asc())
            .all()
        )

        return jsonify([
            {
                'id': n.norma_id,
                'nome': n.nome,
                'valor': n.valor   
            }
            for n in normas
        ])
      
    
    @app.route('/api/alterar_valor_normas', methods=['POST'])
    @login_required
    def api_alterar_valor_normas():
        data = request.get_json()
        tipo_teste = data.get('tipoTeste')
        campo = data.get('campo')
        valor = data.get('valor')
        normas = data.get('normas', [])
    
        if not tipo_teste or not campo or valor is None or not normas:
            return jsonify({'success': False, 'error': 'Dados em falta.'}), 400
    
        # Campos válidos para alteração
        campos_validos = {
            'duracao': 'duracao',
            'duracaomontagem': 'duracaomontagem',
            'tempopp': 'tempopp',
            'tempomp': 'tempomp'
        }
        campo_db = campos_validos.get(campo)
        if not campo_db:
            return jsonify({'success': False, 'error': 'Campo inválido.'}), 400
    
        # Atualizar todos os Templatenormas com o teste e normas selecionadas
        templates = (
            Templatenormas.query
            .filter(Templatenormas.teste_id == int(tipo_teste))
            .filter(Templatenormas.norma_id.in_([int(n) for n in normas]))
            .all()
        )
        for tpl in templates:
            setattr(tpl, campo_db, valor)
        db.session.commit()
    
        return jsonify({'success': True, 'alterados': len(templates)})

    #######################################################
    #ARMAZEM EXTERNO
    @app.route('/api/referencias/proximo_numero')
    @login_required
    def api_referencias_proximo_numero():
        prefixo = request.args.get('prefixo', '').strip()
        if not prefixo:
            return jsonify({'error': 'Parâmetro prefixo obrigatório'}), 400

        # Buscar todas as referências que começam pelo prefixo
        refs = ReferenciaAE.query.filter(
            ReferenciaAE.referencia.ilike(prefixo + "%")
        ).all()

        numeros = []
        regex_num = re.compile(r'^' + re.escape(prefixo) + r'(\d{3})$', re.IGNORECASE)

        for ref in refs:
            m = regex_num.match(ref.referencia)
            if m:
                numeros.append(int(m.group(1)))

        proximo = (max(numeros) + 1) if numeros else 1

        # Mantém o mesmo número de dígitos 
        num_digitos = 3

        return jsonify({'proximo': f'{proximo:0{num_digitos}d}'})

    @app.route('/referenciasae', methods=['POST'])
    @login_required
    def add_referenciaae():
        try:
            data = request.json if request.is_json else request.form
    
            referencia = (data.get('referencia') or '').strip()
            if not referencia:
                return jsonify({'error': 'Referência é obrigatória'}), 400
    
            if ReferenciaAE.query.filter_by(referencia=referencia).first():
                return jsonify({'error': 'Já existe uma referência com esse nome'}), 409
    
            nova = ReferenciaAE(
                referencia=referencia,
                tipo=(data.get('tipo') or 'projeto'),
                laboratorio_id=data.get('laboratorio_id') or None,
                projeto_id=data.get('projeto_id') or None,
                codificacaoae_id=data.get('codificacaoae_id') or None,
                tipopeca_id=data.get('tipopeca_id') or None,
                componente_id=data.get('componente_id') or None,
                estado_codigo=(data.get('estado_codigo') or data.get('estado_id') or '00'),
                localizacao_atual_id=data.get('localizacao_atual_id') or data.get('localizacao_id') or None,
                solicitante_id=data.get('solicitante_id') or None,
                tipovolumeae_id=data.get('tipovolume_id') or None,
                peso=data.get('peso') or None,
                dimensoes=(data.get('dimensoes') or '').strip() or None,
                data_limite_armazenamento=data.get('data_limite_armazenamento') or None,
                observacoes=(data.get('observacoes') or '').strip() or None,
                obsoleto=bool(int(data.get('obsoleto'))) if data.get('obsoleto') is not None else False
            )
            db.session.add(nova)
            db.session.commit()
    
            return jsonify({'success': True, 'message': 'Referência criada com sucesso', 'id': nova.id})
        except Exception as e:
            db.session.rollback()
            current_app.logger.error('Erro ao criar referência: %s', e)
            return jsonify({'error': str(e)}), 500
    
    
    @app.route('/referenciasae/update/<int:id>', methods=['POST'])
    @login_required
    def update_referenciaae(id):
        ref = ReferenciaAE.query.get_or_404(id)
        data = request.json if request.is_json else request.form
    
        novo_nome = (data.get('referencia') or '').strip()
        if novo_nome and novo_nome != ref.referencia:
            if ReferenciaAE.query.filter(ReferenciaAE.referencia == novo_nome, ReferenciaAE.id != id).first():
                return jsonify({'error': 'Já existe outra referência com esse nome'}), 409
            ref.referencia = novo_nome
    
        ref.tipo = data.get('tipo', ref.tipo)
        ref.laboratorio_id = data.get('laboratorio_id') or ref.laboratorio_id
        ref.solicitante_id = data.get('solicitante_id') or None
        ref.tipovolumeae_id = data.get('tipovolume_id') or None
        ref.peso = data.get('peso') or None
        ref.dimensoes = (data.get('dimensoes') or '').strip() or None
        ref.data_limite_armazenamento = data.get('data_limite_armazenamento') or None
        ref.observacoes = (data.get('observacoes') or '').strip() or None
        if data.get('obsoleto') is not None:
            ref.obsoleto = bool(int(data.get('obsoleto')))
    
        try:
            db.session.commit()
            return jsonify({'success': True, 'message': 'Referência atualizada com sucesso'})
        except Exception as e:
            db.session.rollback()
            current_app.logger.error('Erro ao atualizar referência: %s', e)
            return jsonify({'error': str(e)}), 500
    
    
    @app.route('/api/referenciasae')
    @login_required
    def api_referenciasae():
        refs = ReferenciaAE.query.order_by(ReferenciaAE.id.desc()).all()
        out = []
        for r in refs:
            out.append({
                'id': r.id,
                'referencia': r.referencia,
                'tipo': r.tipo,
                'laboratorio_nome': r.laboratorio.laboratorio if r.laboratorio else '',
                'projeto_descricao': r.projeto.descricao if r.projeto else '',
                'codificacao_nome': r.codificacaoae.nome if r.codificacaoae else '',
                'componente_nome': r.componenteae.nome if r.componenteae else '',
                'estado_nome': (
                    'NA' if (r.estado_codigo or '') == '00' or (r.estado_codigo or '')== '0'
                    else 'Usado' if (r.estado_codigo or '') == '01'or (r.estado_codigo or '')== '1'
                    else 'Novo' if (r.estado_codigo or '') == '02'or (r.estado_codigo or '')== '2'
                    else (r.estado_codigo or '')
                ),
                'localizacao_nome': r.localizacao_atual.nome if r.localizacao_atual else '',
                'localizacao_atual_id': r.localizacao_atual_id,
                'tipovolume_nome': r.tipovolumeae.nome if r.tipovolumeae else '',
                'observacoes': r.observacoes if r.observacoes else '',
                'obsoleto': bool(r.obsoleto)
            })
        return jsonify(out)
    
    
    @app.route('/api/referenciaae_by_nome')
    @login_required
    def api_referenciaae_by_nome():
        nome = (request.args.get('referencia') or '').strip()
        if not nome:
            return jsonify({'error': 'Parâmetro referencia obrigatório'}), 400
    
        r = ReferenciaAE.query.filter_by(referencia=nome).first()
        if not r:
            return jsonify({'error': 'Referência não encontrada'}), 404
    
        return jsonify({
            'id': r.id,
            'referencia': r.referencia,
            'tipo': r.tipo,
            'laboratorio_id': r.laboratorio_id,
            'projeto_id': r.projeto_id,
            'codificacaoae_id': r.codificacaoae_id,
            'tipopeca_id': r.tipopeca_id,
            'componente_id': r.componente_id,
            'estado_codigo': r.estado_codigo,
            'localizacao_atual_id': r.localizacao_atual_id,
            'solicitante_id': r.solicitante_id,
            'tipovolumeae_id': r.tipovolumeae_id,
            'peso': float(r.peso) if r.peso is not None else None,
            'dimensoes': r.dimensoes,
            'data_limite_armazenamento': r.data_limite_armazenamento.isoformat() if r.data_limite_armazenamento else None,
            'observacoes': r.observacoes,
            'obsoleto': bool(r.obsoleto)
        })

    @app.route('/api/referenciaae_by_id')
    @login_required
    def api_referenciaae_by_id():
        rid = request.args.get('id', type=int)
        if not rid:
            return jsonify({'error': 'Parâmetro id obrigatório'}), 400
    
        r = ReferenciaAE.query.get(rid)
        if not r:
            return jsonify({'error': 'Referência não encontrada'}), 404
    
        return jsonify({
            'id': r.id,
            'referencia': r.referencia,
            'tipo': r.tipo,
            'laboratorio_id': r.laboratorio_id,
            'projeto_id': r.projeto_id,
            'codificacaoae_id': r.codificacaoae_id,
            'tipopeca_id': r.tipopeca_id,
            'componente_id': r.componente_id,
            'estado_codigo': r.estado_codigo,
            'localizacao_atual_id': r.localizacao_atual_id,
            'solicitante_id': r.solicitante_id,
            'tipovolumeae_id': r.tipovolumeae_id,
            'peso': float(r.peso) if r.peso is not None else None,
            'dimensoes': r.dimensoes,
            'data_limite_armazenamento': r.data_limite_armazenamento.isoformat() if r.data_limite_armazenamento else None,
            'observacoes': r.observacoes,
            'obsoleto': bool(r.obsoleto)
        })
    
    @app.route('/api/movimentosae', methods=['POST'])
    @login_required
    def add_movimentoae():
        referenciaae_id = request.form.get('referenciaae_id')
        localizacao_origem_id = request.form.get('localizacao_origem_id')
        user_id = session.get('user_id')
    
        if not referenciaae_id or not localizacao_origem_id:
            return jsonify({'success': False, 'error': 'Referência e localização de origem são obrigatórios.'}), 400
    
        # Evitar duplicados pendentes
        existente = MovimentoAE.query.filter_by(
            referenciaae_id=referenciaae_id,
            estado='planeado'
        ).first()
        if existente:
            return jsonify({'success': False, 'error': 'Esta referência já tem um envio planeado pendente.'}), 409
    
        m = MovimentoAE(
            referenciaae_id=referenciaae_id,
            localizacao_origem_id=localizacao_origem_id,
            estado='planeado',
            criado_por=user_id
        )
        db.session.add(m)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Referência adicionada aos pendentes de envio.'})
    

    @app.route('/envios')
    @login_required
    def envios():
        user = User.query.get(session['user_id'])
        localizacoes_rows = (
            Localizacao_ae.query
            .filter(Localizacao_ae.obsoleto == False)
            .order_by(Localizacao_ae.nome.asc())
            .all()
        )
    
        localizacoes = [
            {'id': l.id, 'nome': l.nome}
            for l in localizacoes_rows
        ]
    
        return render_template('ae_envios.html', user=user, localizacoes=localizacoes)
    
    @app.route('/api/movimentosae/pendentes', methods=['GET'])
    @login_required
    def api_movimentosae_pendentes():
        rows = (
            db.session.query(
                MovimentoAE.id,
                MovimentoAE.referenciaae_id,
                ReferenciaAE.referencia,
                MovimentoAE.localizacao_origem_id,
                Localizacao_ae.nome.label('origem_nome'),
                MovimentoAE.observacoes,
                MovimentoAE.pep,
                Componentesae.nome.label('componente_nome'),
                Solicitante.nome.label('responsavel_nome'),
                Tipovolumeae.nome.label('tipovolume_nome'),
                case(
                    (ReferenciaAE.estado_codigo == '00', 'NA'),
                    (ReferenciaAE.estado_codigo == '01', 'Usado'),
                    (ReferenciaAE.estado_codigo == '02', 'Novo'),
                    else_=ReferenciaAE.estado_codigo
                ).label('estado_nome')
            )
            .join(ReferenciaAE, ReferenciaAE.id == MovimentoAE.referenciaae_id)
            .join(Localizacao_ae, Localizacao_ae.id == MovimentoAE.localizacao_origem_id)
            .outerjoin(Componentesae, Componentesae.id == ReferenciaAE.componente_id)
            .outerjoin(Solicitante, Solicitante.id == ReferenciaAE.solicitante_id)
            .outerjoin(Tipovolumeae, Tipovolumeae.id == ReferenciaAE.tipovolumeae_id)
            .filter(
                MovimentoAE.estado == 'planeado',
                db.or_(
                    MovimentoAE.localizacao_destino_id.is_(None),
                    MovimentoAE.data_planeada.is_(None)
                )
            )
            .order_by(MovimentoAE.criado_em.asc())
            .all()
        )
    
        return jsonify([{
            'id': r.id,
            'referenciaae_id': r.referenciaae_id,
            'referencia': r.referencia,
            'localizacao_origem_id': r.localizacao_origem_id,
            'origem_nome': r.origem_nome,
            'observacoes': r.observacoes or '',
            'pep':r.pep or '',
            'componente_nome': r.componente_nome or '',
            'estado_nome': r.estado_nome or '',
            'responsavel_nome': r.responsavel_nome or '',
            'tipovolume_nome': r.tipovolume_nome or ''
        } for r in rows])
    
    @app.route('/api/movimentosae/<int:id>', methods=['POST'])
    @login_required
    def api_movimentosae_update(id):

        movimento = MovimentoAE.query.get_or_404(id)

        data = request.json

        movimento.localizacao_destino_id = (
            int(data['localizacao_destino_id'])
            if data.get('localizacao_destino_id')
            else None
        )

        movimento.pep = data.get('pep')
        movimento.observacoes = data.get('observacoes')

        db.session.commit()

        return jsonify(success=True)
    
    @app.route('/api/movimentosae/<int:mov_id>/planear', methods=['POST'])
    @login_required
    def api_movimentosae_planear(mov_id):
        mov = MovimentoAE.query.get_or_404(mov_id)
    
        if mov.estado != 'planeado':
            return jsonify({'success': False, 'error': 'Só é possível planear envios em estado planeado.'}), 400
    
        destino_id = request.form.get('localizacao_destino_id', type=int)
        datahora_str = (request.form.get('data_planeada') or '').strip()
        observacoes = request.form.get('observacoes')
    
        if not destino_id:
            return jsonify({'success': False, 'error': 'Destino é obrigatório.'}), 400
        if not datahora_str:
            return jsonify({'success': False, 'error': 'Data e hora são obrigatórias.'}), 400
    
        try:
            # formato esperado do input datetime-local: YYYY-MM-DDTHH:MM
            datahora = datetime.strptime(datahora_str, '%Y-%m-%dT%H:%M')
        except ValueError:
            return jsonify({'success': False, 'error': 'Formato de data/hora inválido.'}), 400
    
        mov.localizacao_destino_id = destino_id
        mov.data_planeada = datahora
        mov.observacoes = observacoes
        db.session.commit()
    
        return jsonify({'success': True, 'message': 'Envio planeado com sucesso.'})
    
    
    @app.route('/api/movimentosae/lotes_planeados', methods=['GET'])
    @login_required
    def api_movimentosae_lotes_planeados():
        loc_origem = aliased(Localizacao_ae)
        loc_destino = aliased(Localizacao_ae)
    
        lotes = (
            db.session.query(
                cast(MovimentoAE.data_planeada, Date).label('dia'),
                MovimentoAE.localizacao_origem_id,
                loc_origem.nome.label('origem_nome'),
                MovimentoAE.localizacao_destino_id,
                loc_destino.nome.label('destino_nome'),
                func.count(MovimentoAE.id).label('qtd')
            )
            .join(loc_origem, loc_origem.id == MovimentoAE.localizacao_origem_id)
            .join(loc_destino, loc_destino.id == MovimentoAE.localizacao_destino_id)
            .filter(
                MovimentoAE.estado == 'planeado',
                MovimentoAE.localizacao_destino_id.isnot(None),
                MovimentoAE.data_planeada.isnot(None)
            )
            .group_by(
                cast(MovimentoAE.data_planeada, Date),
                MovimentoAE.localizacao_origem_id,
                MovimentoAE.localizacao_destino_id,
                loc_origem.nome,
                loc_destino.nome
            )
            .order_by(cast(MovimentoAE.data_planeada, Date).asc())
            .all()
        )
    
        data = []
        for l in lotes:
            data.append({
                'dia': l.dia.isoformat() if l.dia else None,
                'localizacao_origem_id': l.localizacao_origem_id,
                'origem_nome': l.origem_nome,
                'localizacao_destino_id': l.localizacao_destino_id,
                'destino_nome': l.destino_nome,
                'qtd': int(l.qtd)
            })
        return jsonify(data)
    
    
    @app.route('/api/movimentosae/lotes/confirmar', methods=['POST'])
    @login_required
    def api_movimentosae_confirmar_lote():
        datahora = (request.form.get('datahora') or '').strip()
        origem_id = request.form.get('localizacao_origem_id', type=int)
        destino_id = request.form.get('localizacao_destino_id', type=int)
        
        if not datahora or not destino_id:
            return jsonify({'success': False, 'error': 'Parâmetros do envio incompletos.'}), 400
        
        try:
            dt = datetime.strptime(datahora, '%Y-%m-%dT%H:%M')
        except ValueError:
            return jsonify({'success': False, 'error': 'Data/hora inválida.'}), 400
        
        dt_end = dt + timedelta(minutes=1)
        
        query = MovimentoAE.query.filter(
            MovimentoAE.estado == 'planeado',
            MovimentoAE.localizacao_destino_id == destino_id,
            MovimentoAE.data_planeada >= dt,
            MovimentoAE.data_planeada < dt_end
        )
    
        if origem_id:
            query = query.filter(MovimentoAE.localizacao_origem_id == origem_id)
    
        movimentos = query.all()
    
        if not movimentos:
            return jsonify({'success': False, 'error': 'Lote não encontrado.'}), 404
    
        now = datetime.now()
        user_id = session.get('user_id')
    
        for m in movimentos:
            m.estado = 'confirmado'
            m.data_confirmacao = now
            m.confirmado_por = user_id
    
            ref = ReferenciaAE.query.get(m.referenciaae_id)
            if ref:
                ref.localizacao_atual_id = m.localizacao_destino_id
    
        db.session.commit()
        return jsonify({'success': True, 'message': f'Envio confirmado ({len(movimentos)} envios).'})
    
    @app.route('/api/movimentosae/<int:mov_id>/cancelar', methods=['POST'])
    @login_required
    def api_movimentosae_cancelar(mov_id):
        mov = MovimentoAE.query.get_or_404(mov_id)
        
        if mov.estado == 'planeado':
            db.session.delete(mov)
            db.session.commit()
            return jsonify({'success': True, 'message': 'Linha eliminada.'})
        
        
        return jsonify({'success': False, 'error': 'Não é possível cancelar este movimento.'}), 400
    
    @app.route('/api/movimentosae/lotes/cancelar', methods=['POST'])
    @login_required
    def api_movimentosae_cancelar_lote():
        datahora = (request.form.get('datahora') or '').strip()
        origem_id = request.form.get('localizacao_origem_id', type=int)
        destino_id = request.form.get('localizacao_destino_id', type=int)
    
        if not datahora or not destino_id:
            return jsonify({'success': False, 'error': 'Parâmetros do lote incompletos.'}), 400
    
        try:
            dt = datetime.strptime(datahora, '%Y-%m-%dT%H:%M')
        except ValueError:
            return jsonify({'success': False, 'error': 'Data/hora inválida.'}), 400
    
        dt_end = dt + timedelta(minutes=1)
    
        query = MovimentoAE.query.filter(
            MovimentoAE.estado == 'planeado',
            MovimentoAE.localizacao_destino_id == destino_id,
            MovimentoAE.data_planeada >= dt,
            MovimentoAE.data_planeada < dt_end
        )
    
        if origem_id:
            query = query.filter(MovimentoAE.localizacao_origem_id == origem_id)
    
        movimentos = query.all()
        if not movimentos:
            return jsonify({'success': False, 'error': 'Lote não encontrado.'}), 404
    
        for m in movimentos:
            m.estado = 'cancelado'
    
        db.session.commit()
        return jsonify({'success': True, 'message': f'Lote cancelado ({len(movimentos)} envios).'})
   
    @app.route('/api/movimentosae/datas_planeadas', methods=['GET'])
    @login_required
    def api_movimentosae_datas_planeadas():
        rows = (
            db.session.query(MovimentoAE.data_planeada)
            .filter(
                MovimentoAE.estado == 'planeado',
                MovimentoAE.localizacao_destino_id.isnot(None),
                MovimentoAE.data_planeada.isnot(None)
            )
            .distinct()
            .order_by(MovimentoAE.data_planeada.asc())
            .all()
        )
    
        return jsonify([
            {
                'datahora': r.data_planeada.strftime('%Y-%m-%dT%H:%M')
            }
            for r in rows if r.data_planeada
        ])
    
    
    @app.route('/api/movimentosae/destinos_por_datahora', methods=['GET'])
    @login_required
    def api_movimentosae_destinos_por_datahora():
        datahora_str = (request.args.get('datahora') or '').strip()
        if not datahora_str:
            return jsonify([])
    
        try:
            dt = datetime.strptime(datahora_str, '%Y-%m-%dT%H:%M')
        except ValueError:
            return jsonify({'error': 'Data/hora inválida'}), 400
    
        dt_end = dt + timedelta(minutes=1)
        loc_destino = aliased(Localizacao_ae)
    
        rows = (
            db.session.query(
                MovimentoAE.localizacao_destino_id,
                loc_destino.nome.label('destino_nome')
            )
            .join(loc_destino, loc_destino.id == MovimentoAE.localizacao_destino_id)
            .filter(
                MovimentoAE.estado == 'planeado',
                MovimentoAE.localizacao_destino_id.isnot(None),
                MovimentoAE.data_planeada >= dt,
                MovimentoAE.data_planeada < dt_end
            )
            .group_by(MovimentoAE.localizacao_destino_id, loc_destino.nome)
            .order_by(loc_destino.nome.asc())
            .all()
        )
    
        return jsonify([{'id': r.localizacao_destino_id, 'nome': r.destino_nome} for r in rows])
    
    @app.route('/api/movimentosae/referencias_lote', methods=['GET'])
    @login_required
    def api_movimentosae_referencias_lote():
        datahora_str = (request.args.get('datahora') or '').strip()
        destino_id = request.args.get('destino_id', type=int)
        if not datahora_str or not destino_id:
            return jsonify([])
    
        try:
            dt = datetime.strptime(datahora_str, '%Y-%m-%dT%H:%M')
        except ValueError:
            return jsonify({'error': 'Data/hora inválida'}), 400
    
        dt_end = dt + timedelta(minutes=1)
    
        movs = (
            MovimentoAE.query
            .options(
                joinedload(MovimentoAE.referenciaae).joinedload(ReferenciaAE.tipovolumeae),
                joinedload(MovimentoAE.referenciaae).joinedload(ReferenciaAE.componenteae),
                joinedload(MovimentoAE.referenciaae).joinedload(ReferenciaAE.solicitante)
            )
            .filter(
                MovimentoAE.estado == 'planeado',
                MovimentoAE.localizacao_destino_id == destino_id,
                MovimentoAE.data_planeada >= dt,
                MovimentoAE.data_planeada < dt_end
            )
            .order_by(MovimentoAE.id.asc())
            .all()
        )
    
        result = []
        for m in movs:
            ref = m.referenciaae
            result.append({
                'mov_id': m.id,
                'referenciaae_id': m.referenciaae_id,
                'referencia': ref.referencia if ref else '',
                'tipovolumeae': ref.tipovolumeae.nome if ref and ref.tipovolumeae else '',
                'peso': str(ref.peso) if ref and ref.peso is not None else '',
                'dimensoes': ref.dimensoes if ref and ref.dimensoes else '',
                'observacoes': m.observacoes or '',
                'email_enviado': bool(m.emailenviado),
                'emailenviado_em': m.emailenviado.strftime('%Y-%m-%d %H:%M:%S') if m.emailenviado else '',
                'componente_nome': ref.componenteae.nome if ref and ref.componenteae else '',
                'estado_nome': (
                    'NA' if ref and (ref.estado_codigo or '') == '00'
                    else 'Usado' if ref and (ref.estado_codigo or '') == '01'
                    else 'Novo' if ref and (ref.estado_codigo or '') == '02'
                    else (ref.estado_codigo or '') if ref else ''
                ),
                'responsavel_nome': ref.solicitante.nome if ref and ref.solicitante else '',
                'tipovolume_nome': ref.tipovolumeae.nome if ref and ref.tipovolumeae else ''
            })
    
        return jsonify(result)
    
    
    @app.route('/api/movimentosae/<int:mov_id>/desprogramar', methods=['POST'])
    @login_required
    def api_movimentosae_desprogramar(mov_id):
        """Volta o movimento para pendente (remove destino e data_planeada)"""
        mov = MovimentoAE.query.get_or_404(mov_id)
        if mov.estado != 'planeado':
            return jsonify({'success': False, 'error': 'Só é possível desprogramar envios em estado planeado.'}), 400
        mov.localizacao_destino_id = None
        mov.data_planeada = None
        db.session.commit()
        return jsonify({'success': True, 'message': 'Envio devolvido aos pendentes.'})
    
    @app.route('/api/movimentosae/marcar-email-enviado', methods=['POST'])
    @login_required
    def marcar_email_enviado():
        data = request.get_json()
        datahora = data.get('datahora')
        destino_id = data.get('destino_id')

        if not datahora or not destino_id:
            return jsonify(success=False, error="Dados incompletos."), 400

        try:
            movimentos = MovimentoAE.query.filter(
                MovimentoAE.data_planeada == datahora,
                MovimentoAE.localizacao_destino_id == destino_id,
                MovimentoAE.estado == 'planeado'
            ).all()

            agora = datetime.now()

            for mov in movimentos:
                mov.emailenviado = agora

            db.session.commit()

            return jsonify(success=True, updated=len(movimentos))
        except Exception as e:
            db.session.rollback()
            return jsonify(success=False, error=str(e)), 500


    @app.route('/api/movimentosae/render-email-envio', methods=['POST'])
    @login_required
    def api_movimentosae_render_email_envio():
        """Renderiza templates de email para envio externo ou recolha interna."""
        try:
    
            payload = request.get_json(silent=True) or {}
            datahora_str = (payload.get('datahora') or '').strip()
            destino_id = payload.get('destino_id')
    
            if not datahora_str or not destino_id:
                return jsonify({'error': 'datahora e destino_id são obrigatórios.'}), 400
    
            try:
                dt = datetime.strptime(datahora_str, '%Y-%m-%dT%H:%M')
            except ValueError:
                return jsonify({'error': 'Data/hora inválida.'}), 400
    
            dt_end = dt + timedelta(minutes=1)
    
            destino = Localizacao_ae.query.get(destino_id)
            if not destino:
                return jsonify({'error': 'Destino não encontrado.'}), 404
    
            evento = 'recolha_interna_concluida' if bool(destino.interno) else 'envio_externo_concluido'
    
            movs = (
                MovimentoAE.query
                .options(
                    joinedload(MovimentoAE.referenciaae).joinedload(ReferenciaAE.solicitante),
                    joinedload(MovimentoAE.referenciaae).joinedload(ReferenciaAE.tipovolumeae),
                    joinedload(MovimentoAE.localizacao_destino),
                    joinedload(MovimentoAE.localizacao_origem)
                )
                .filter(
                    MovimentoAE.localizacao_destino_id == destino_id,
                    MovimentoAE.data_planeada >= dt,
                    MovimentoAE.data_planeada < dt_end,
                    MovimentoAE.estado == 'planeado'
                )
                .order_by(MovimentoAE.id.asc())
                .all()
            )
    
            if not movs:
                return jsonify({
                    'emails': [],
                    'aviso': 'Não foram encontrados movimentos confirmados para esse lote.'
                }), 200
    
            dias_semana_pt = {
                0: 'Segunda-feira',
                1: 'Terça-feira',
                2: 'Quarta-feira',
                3: 'Quinta-feira',
                4: 'Sexta-feira',
                5: 'Sábado',
                6: 'Domingo',
            }
    
            referencias = []
            tipos_volume = []
            emails_responsavel = []
            peso_total = 0.0
            itens = []
    
            origens_nomes = []
            origens_emails = []
    
            for mov in movs:
                ref = mov.referenciaae
                origem = mov.localizacao_origem
    
                if origem:
                    if origem.nome:
                        origens_nomes.append(origem.nome)
                    if origem.contactoemail:
                        origens_emails.append(origem.contactoemail.strip())
    
                if not ref:
                    continue
    
                tipo_volume = ref.tipovolumeae.nome if ref.tipovolumeae else ''
                peso_str = ''
    
                if ref.referencia:
                    referencias.append(ref.referencia)
    
                if tipo_volume:
                    tipos_volume.append(tipo_volume)
    
                if ref.peso is not None:
                    peso_float = float(ref.peso)
                    peso_total += peso_float
                    peso_str = f'{peso_float:.2f}'
    
                email_resp = (ref.solicitante.email or '').strip() if ref.solicitante and ref.solicitante.email else ''
                if email_resp:
                    emails_responsavel.append(email_resp)
    
                itens.append({
                    'tipo_volume': tipo_volume,
                    'referencia': ref.referencia or '',
                    'dimensoes': ref.dimensoes or '',
                    'peso': peso_str,
                })
    
            referencias = sorted(set(referencias))
            tipos_volume = sorted(set(tipos_volume))
            emails_responsavel = sorted(set(emails_responsavel))
            itens = sorted(itens, key=lambda x: x.get('referencia') or '')
    
            origens_nomes = sorted(set([x for x in origens_nomes if x]))
            origens_emails = sorted(set([x for x in origens_emails if x]))
    
            blocos = []
            for i in itens:
                ref = (i.get('referencia') or '-').strip()
                tipo = (i.get('tipo_volume') or '-').strip()
                dims = (i.get('dimensoes') or '-').strip()
                peso_raw = (i.get('peso') or '').strip()
                peso = f"{peso_raw} kg" if peso_raw else '-'
    
                bloco = (
                    f"{ref}\n"
                    f"  Tipo: {tipo}\n"
                    f"  Dim : {dims}\n"
                    f"  Peso: {peso}"
                )
                blocos.append(bloco)
    
            tabela_referencias = "\n" + ("\n\n".join(blocos) if blocos else '')
    
            contexto = {
                'email_localizacao_origem': '; '.join(origens_emails),
                'email_localizacao_destino': (destino.contactoemail or '').strip(),
                'email_responsavel': '; '.join(emails_responsavel),
                'data': dt.strftime('%Y-%m-%d'),
                'hora': dt.strftime('%H:%M'),
                'dia_semana': dias_semana_pt.get(dt.weekday(), ''),
                'origem': ', '.join(origens_nomes),
                'destino': destino.nome or '',
                'referencia': ', '.join(referencias),
                'tipo_volume': ', '.join(tipos_volume),
                'peso_total': f'{peso_total:.2f}',
                'n_referencias': str(len(referencias)),
                'tabela_referencias': tabela_referencias,
            }
    
            configs = (
                ConfEmailAuto.query
                .filter(
                    ConfEmailAuto.evento == evento,
                    ConfEmailAuto.obsoleto == False
                )
                .all()
            )
    
            if not configs:
                return jsonify({'emails': [], 'aviso': f'Nenhuma configuração de email para {evento}.'}), 200
    
            emails = []
            for cfg in configs:
                emails.append({
                    'config_id': cfg.id,
                    'config_nome': cfg.nome,
                    'evento': evento,
                    'assunto': render_template_string(cfg.assunto or '', **contexto),
                    'texto': render_template_string(cfg.texto or '', **contexto),
                    'to_email': render_template_string(cfg.to_email or '', **contexto),
                    'cc_email': render_template_string(cfg.cc_email or '', **contexto),
                })
    
            return jsonify({
                'success': True,
                'evento': evento,
                'contexto': contexto,
                'emails': emails
            })
    
        except Exception as e:
            current_app.logger.error(f'Erro ao renderizar email de envio/recolha: {e}')
            return jsonify({'error': str(e)}), 500


    @app.route('/api/movimentosae/<int:mov_id>/observacoes', methods=['POST'])
    @login_required
    def api_movimentosae_observacoes(mov_id):
        mov = MovimentoAE.query.get_or_404(mov_id)
    
        if mov.estado != 'planeado':
            return jsonify({'success': False, 'error': 'Só é possível editar observações em envios planeados.'}), 400
    
        mov.observacoes = (request.form.get('observacoes') or '').strip() or None
        db.session.commit()
        return jsonify({'success': True})
    
    #############################################################
    ## consultas ae
    @app.route('/api/movimentosae/historico_resumo', methods=['GET'])
    @login_required
    def api_movimentosae_historico_resumo():
        localizacao_id = request.args.get('localizacao_id', type=int)
        mes = request.args.get('mes', type=int)
        ano = request.args.get('ano', type=int)
    
        if not localizacao_id or not mes or not ano:
            return jsonify({'success': False, 'error': 'Parâmetros em falta.'}), 400
    
        loc = Localizacao_ae.query.get(localizacao_id)
        if not loc:
            return jsonify({'success': False, 'error': 'Localização não encontrada.'}), 404
    
        movs = (
            MovimentoAE.query
            .options(
                joinedload(MovimentoAE.referenciaae).joinedload(ReferenciaAE.componenteae),
                joinedload(MovimentoAE.referenciaae).joinedload(ReferenciaAE.solicitante),
                joinedload(MovimentoAE.referenciaae).joinedload(ReferenciaAE.tipovolumeae),
                joinedload(MovimentoAE.localizacao_origem),
                joinedload(MovimentoAE.localizacao_destino)
            )
            .filter(
                MovimentoAE.estado == 'confirmado',
                MovimentoAE.data_planeada.isnot(None),
                extract('year', MovimentoAE.data_planeada) == ano,
                extract('month', MovimentoAE.data_planeada) == mes,
                or_(
                    MovimentoAE.localizacao_origem_id == localizacao_id,
                    MovimentoAE.localizacao_destino_id == localizacao_id
                )
            )
            .order_by(MovimentoAE.data_planeada.asc(), MovimentoAE.id.asc())
            .all()
        )
    
        rows_by_slot = {}
        total_enviadas = 0
        total_recebidas = 0
    
        for mov in movs:
            slot = mov.data_planeada.replace(second=0, microsecond=0)
            slot_datahora = slot.strftime('%Y-%m-%dT%H:%M')
            destino_id = mov.localizacao_destino_id or 0
            slot_key = f'{slot_datahora}|{destino_id}'
    
            if slot_key not in rows_by_slot:
                rows_by_slot[slot_key] = {
                    'datahora': slot_datahora,
                    'data': slot.strftime('%Y-%m-%d'),
                    'hora': slot.strftime('%H:%M'),
                    'destino_id': destino_id,
                    'enviadas': 0,
                    'recebidas': 0,
                    'total': 0,
                    'movimentos': []
                }
    
            is_enviada = (mov.localizacao_destino_id == localizacao_id)
            is_recebida = (mov.localizacao_origem_id == localizacao_id)
    
            if is_enviada:
                rows_by_slot[slot_key]['enviadas'] += 1
                total_enviadas += 1
    
            if is_recebida:
                rows_by_slot[slot_key]['recebidas'] += 1
                total_recebidas += 1
    
            ref = mov.referenciaae
            rows_by_slot[slot_key]['movimentos'].append({
                'mov_id': mov.id,
                'referenciaae_id': ref.id if ref else None,
                'referencia': ref.referencia if ref else '',
                'componente_nome': ref.componenteae.nome if ref and ref.componenteae else '',
                'estado_nome': (
                    'NA' if ref and (ref.estado_codigo or '') == '00'
                    else 'Usado' if ref and (ref.estado_codigo or '') == '01'
                    else 'Novo' if ref and (ref.estado_codigo or '') == '02'
                    else (ref.estado_codigo or '') if ref else ''
                ),
                'responsavel_nome': ref.solicitante.nome if ref and ref.solicitante else '',
                'tipovolume_nome': ref.tipovolumeae.nome if ref and ref.tipovolumeae else '',
                'peso': f'{float(ref.peso):.2f}' if ref and ref.peso is not None else '',
                'dimensoes': ref.dimensoes if ref and ref.dimensoes else '',
                'observacoes': mov.observacoes or '',
                'pep': mov.pep or ''
            })
    
        rows = sorted(rows_by_slot.values(), key=lambda x: x['datahora'])
        for row in rows:
            row['total'] = row['enviadas'] + row['recebidas']
    
        return jsonify({
            'success': True,
            'resumo': {
                'enviadas': total_enviadas,
                'recebidas': total_recebidas,
                'total': total_enviadas + total_recebidas
            },
            'rows': rows
        })
    
    @app.route('/api/movimentosae/historico_reabrir_dia', methods=['POST'])
    @login_required
    def api_movimentosae_historico_reabrir_dia():
        data = request.get_json(silent=True) or {}
    
        localizacao_id = data.get('localizacao_id')
        datahora_str = (data.get('datahora') or '').strip()
        destino_id = data.get('destino_id')

        if not localizacao_id or not datahora_str or not destino_id:
            return jsonify({'success': False, 'error': 'Parâmetros em falta.'}), 400

    
        try:
            dt = datetime.strptime(datahora_str, '%Y-%m-%dT%H:%M')
        except ValueError:
            return jsonify({'success': False, 'error': 'Data/hora inválida.'}), 400
    
        dt_end = dt + timedelta(minutes=1)
    
        movs = (
            MovimentoAE.query
            .options(joinedload(MovimentoAE.referenciaae))
            .filter(
                MovimentoAE.estado == 'confirmado',
                MovimentoAE.data_planeada >= dt,
                MovimentoAE.data_planeada < dt_end,
                MovimentoAE.localizacao_destino_id == int(destino_id),
                or_(
                    MovimentoAE.localizacao_origem_id == int(localizacao_id),
                    MovimentoAE.localizacao_destino_id == int(localizacao_id)
                )
            )
            .all()
        )
    
        if not movs:
            return jsonify({'success': False, 'error': 'Nenhum movimento encontrado.'}), 404
    
        for mov in movs:
            mov.estado = 'planeado'
            mov.data_confirmacao = None
            mov.confirmado_por = None
    
            ref = mov.referenciaae
            if ref:
                ref.localizacao_atual_id = mov.localizacao_origem_id
    
        db.session.commit()
    
        return jsonify({
            'success': True,
            'message': f'{len(movs)} movimentos repostos para planeado.'
        })

    @app.route('/api/referenciasae/stocks_resumo', methods=['GET'])
    @login_required
    def api_referenciasae_stocks_resumo():
        refs = (
            ReferenciaAE.query
            .options(
                joinedload(ReferenciaAE.componenteae),
                joinedload(ReferenciaAE.solicitante),
                joinedload(ReferenciaAE.tipovolumeae),
                joinedload(ReferenciaAE.localizacao_atual),
                joinedload(ReferenciaAE.projeto),
                joinedload(ReferenciaAE.codificacaoae)
            )
            .filter(ReferenciaAE.obsoleto == False)
            .order_by(ReferenciaAE.referencia.asc())
            .all()
        )

        rows = []
        resumo_map = {}

        for r in refs:
            estado_nome = (
                'NA' if (r.estado_codigo or '') == '00'
                else 'Usado' if (r.estado_codigo or '') == '01'
                else 'Novo' if (r.estado_codigo or '') == '02'
                else (r.estado_codigo or '')
            )

            localizacao_nome = r.localizacao_atual.nome if r.localizacao_atual else 'Sem localização'
            projeto_ou_codificacao = (
                r.projeto.descricao if (r.tipo == 'projeto' and r.projeto)
                else (r.codificacaoae.nome if r.codificacaoae else '')
            )

            rows.append({
                'id': r.id,
                'referencia': r.referencia or '',
                'tipo': r.tipo or '',
                'projeto_ou_codificacao': projeto_ou_codificacao,
                'componente_nome': r.componenteae.nome if r.componenteae else '',
                'estado_nome': estado_nome,
                'responsavel_nome': r.solicitante.nome if r.solicitante else '',
                'tipovolume_nome': r.tipovolumeae.nome if r.tipovolumeae else '',
                'peso': f'{float(r.peso):.2f}' if r.peso is not None else '',
                'dimensoes': r.dimensoes or '',
                'localizacao_nome': localizacao_nome,
                'data_limite_armazenamento': r.data_limite_armazenamento.isoformat() if r.data_limite_armazenamento else '',
                'observacoes': r.observacoes or ''
            })

            resumo_map[localizacao_nome] = resumo_map.get(localizacao_nome, 0) + 1

        resumo_localizacoes = [
            {'localizacao': k, 'total': v}
            for k, v in sorted(resumo_map.items(), key=lambda x: (-x[1], x[0].lower()))
        ]

        return jsonify({
            'success': True,
            'total_referencias': len(rows),
            'resumo_localizacoes': resumo_localizacoes,
            'rows': rows
        })
   
    
    @app.route('/api/ensaios/<string:ensaio_numero>/exportar_orcamento', methods=['GET'])
    @app.route('/api/ensaios/<string:ensaio_numero>/exportar_custo_pessoa', methods=['GET'])  # compatibilidade
    @login_required
    def exportar_orcamento(ensaio_numero):
        
    
        ensaio = Ensaio.query.filter_by(ensaio=ensaio_numero).first()
        if not ensaio:
            return jsonify({'error': f'Ensaio {ensaio_numero} não encontrado.'}), 404
    
        if not ensaio.norma_id:
            return jsonify({'error': 'O ensaio selecionado não tem norma associada.'}), 400
    
        cfg = DadosGerais.query.order_by(DadosGerais.id.asc()).first()
        custo_hora_pessoa = float(cfg.custohorapessoa) if cfg and cfg.custohorapessoa is not None else None
        if custo_hora_pessoa is None:
            return jsonify({'error': 'Não existe valor de custo hora pessoa em dadosgerais.'}), 400
    
        testes = (
            Testes.query
            .filter_by(ensaio_id=ensaio.id)
            .order_by(Testes.ordem.asc(), Testes.id.asc())
            .all()
        )
    
        wb = Workbook()
        ws = wb.active
        ws.title = "Orcamento"
    
        linhas = []
        total_custo_pessoa = 0.0
        total_custo_maquina = 0.0
    
        for t in testes:
            template = (
                Templatenormas.query
                .filter_by(norma_id=ensaio.norma_id, teste_id=t.teste_id, obsoleto=False)
                .order_by(Templatenormas.ordem.asc(), Templatenormas.id.asc())
                .first()
            )
    
            qtd = float(t.qtd or 0)
    
            tempo_montagem = float(template.duracaomontagem or 0) if template else 0.0
            tempo_pessoa_peca = float(template.tempopp or 0) if template else 0.0
            custo_pessoa = (tempo_montagem + (tempo_pessoa_peca * qtd)) * custo_hora_pessoa
    
            duracao_maquina = float(t.duracao or 0)
            tempo_maquina_peca = float(template.tempomp or 0) if template else 0.0
            custo_hora_maquina = float(t.maquina.custo) if t.maquina and t.maquina.custo is not None else 0.0
            custo_maquina = (duracao_maquina + (tempo_maquina_peca * qtd)) * custo_hora_maquina
    
            total_custo_pessoa += custo_pessoa
            total_custo_maquina += custo_maquina
    
            linhas.append([
                ensaio.ensaio,
                t.ordem,
                t.teste.teste if t.teste else "",
                t.qtd,
                round(tempo_montagem, 4),
                round(tempo_pessoa_peca, 4),
                round(custo_hora_pessoa, 4),
                round(custo_pessoa, 2),
                round(duracao_maquina, 4),
                round(tempo_maquina_peca, 4),
                round(custo_hora_maquina, 4),
                round(custo_maquina, 2)
            ])
    
        total_geral = total_custo_pessoa + total_custo_maquina
    
        ws.append(["RESUMO ORCAMENTO"])
        ws.append(["Total Custo Pessoa", round(total_custo_pessoa, 2)])
        ws.append(["Total Custo Maquina", round(total_custo_maquina, 2)])
        ws.append(["Total Geral", round(total_geral, 2)])
        ws.append([])
    
        ws.append([
            "Ensaio", "Ordem", "Teste", "Qtd",
            "Tempo Montagem", "Tempo Pessoa/Peça", "Custo Hora Pessoa", "Custo Pessoa",
            "Duracao Maquina", "Tempo Maquina/Peça", "Custo Hora Maquina", "Custo Maquina"
        ])
    
        for linha in linhas:
            ws.append(linha)
    
        out = BytesIO()
        wb.save(out)
        out.seek(0)
    
        return send_file(
            out,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=f'{ensaio.ensaio}_Orcamento.xlsx'
        )

    


    
    


    