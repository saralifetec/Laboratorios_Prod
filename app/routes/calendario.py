from flask import Blueprint, jsonify, render_template, request, session
from app.models import User
from app.routes.geral import login_required
from datetime import datetime
from app.models import db, UserCalendar, Feriado



calendario_bp = Blueprint('calendario', __name__)

@calendario_bp.route('/calendario')
@login_required
def calendario():
    user = User.query.get(session['user_id'])
    tecnicos = User.query.all()
    return render_template('calendario.html', user=user, tecnicos=tecnicos)

@calendario_bp.route('/api/calendar', methods=['GET'])
def api_calendar():
    start = request.args.get('start')
    end = request.args.get('end')
    user_id = request.args.get('user_id')

    start_date = datetime.fromisoformat(start[:10]).date()
    end_date = datetime.fromisoformat(end[:10]).date()

    events = []

    #  mapa por data (chave única)
    events_by_date = {}

    #  1. Feriados (base)
    feriados = Feriado.query.filter(
        Feriado.data.between(start_date, end_date)
    ).all()

    for f in feriados:
        events_by_date[f.data] = {
            "data": f.data.isoformat(),
            "tipo": "feriado"
        }

    #  2. Eventos do utilizador (sobrepõem)
    if user_id != "all":
        user_events = UserCalendar.query.filter(
            UserCalendar.user_id == int(user_id),
            UserCalendar.data.between(start_date, end_date)
        ).all()

        for e in user_events:
            #  substitui o feriado (ou qualquer coisa)
            events_by_date[e.data] = {
                "data": e.data.isoformat(),
                "tipo": e.tipo,
                "horas": e.horas
            }

    #  converter para lista
    events = list(events_by_date.values())

    return jsonify(events)



@calendario_bp.route('/api/get', methods=['GET'])
@login_required
def get_calendario():

    user_id = request.args.get('user_id')
    ano = request.args.get('ano')
    mes = request.args.get('mes')

    if not ano or not mes:
        return jsonify([])

    ano = int(ano)
    mes = int(mes)

    # intervalo do mês
    start_date = datetime(ano, mes, 1)
    if mes == 12:
        end_date = datetime(ano + 1, 1, 1)
    else:
        end_date = datetime(ano, mes + 1, 1)

    eventos = []

    # -------------------------
    # FERIADOS (GLOBAL)
    # -------------------------
    feriados = Feriado.query.filter(
        Feriado.data >= start_date,
        Feriado.data < end_date
    ).all()

    for f in feriados:
        eventos.append({
            "date": f.data.strftime("%Y-%m-%d"),
            "tipo": "feriado"
        })

    # -------------------------
    # UTILIZADOR (EXCEÇÕES)
    # -------------------------
    if user_id and user_id != "all":

        regs = UserCalendar.query.filter(
            UserCalendar.user_id == user_id,
            UserCalendar.data >= start_date,
            UserCalendar.data < end_date
        ).all()

        for r in regs:
            eventos.append({
                "date": r.data.strftime("%Y-%m-%d"),
                "tipo": r.tipo,
                "horas": float(r.horas) if r.horas else None
            })

    return jsonify(eventos)

@calendario_bp.route('/api/save', methods=['POST'])
def save_event():
    data = request.json

    user_id = data.get('user_id')
    tipo = data.get('tipo')
    horas = data.get('horas')
    date = datetime.fromisoformat(data.get('data')).date()

    # "Todos" → guardar como feriado
    if user_id == "all":
        existing = Feriado.query.filter_by(data=date).first()
        if not existing:
            f = Feriado(data=date, descricao="Manual")
            db.session.add(f)
    else:
        user_id = int(user_id)

        existing = UserCalendar.query.filter_by(
            user_id=user_id,
            data=date
        ).first()

        if existing:
            existing.tipo = tipo
            existing.horas = horas if tipo == "parcial" else None
        else:
            new = UserCalendar(
                user_id=user_id,
                data=date,
                tipo=tipo,
                horas=horas if tipo == "parcial" else None
            )
            db.session.add(new)

    db.session.commit()

    return {"status": "ok"}


@calendario_bp.route('/api/delete', methods=['POST'])
def delete_event():
    data = request.json
    user_id = data.get('user_id')
    date = datetime.fromisoformat(data.get('data')).date()

    if user_id == "all":
        Feriado.query.filter_by(data=date).delete()
    else:
        UserCalendar.query.filter_by(
            user_id=int(user_id),
            data=date
        ).delete()

    db.session.commit()
    return {"status": "ok"}