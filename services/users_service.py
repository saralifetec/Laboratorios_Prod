from app.models import User
from flask import session


def get_current_user():
    """
    Devolve o utilizador autenticado.
    """

    user_id = session.get('user_id')

    if not user_id:
        return None

    return User.query.get(user_id)

def get_current_user_lab_id():

    user = get_current_user()

    return user.laboratorio_id if user else None

def get_current_user_funcao_id():

    user = get_current_user()

    return user.funcao_id if user else None

def get_users_by_lab(laboratorio_id, incluir_obsoletos=False):
    """
    Devolve todos os utilizadores de um laboratório.
    """

    query = User.query.filter(
        User.laboratorio_id == laboratorio_id
    )

    if not incluir_obsoletos:
        query = query.filter(
            User.obsoleto == False
        )

    return query.order_by(
        User.full_name
    ).all()

def get_all_users(incluir_obsoletos=False):

    query = User.query

    if not incluir_obsoletos:
        query = query.filter(
            User.obsoleto == False
        )

    return query.order_by(
        User.full_name
    ).all()


def get_scope_users(laboratorio_id, apenas_eu=False):
    """
    Devolve a lista de utilizadores que devem ser
    considerados numa consulta.
    """

    if apenas_eu:

        user = get_current_user()

        return [user] if user else []

    # Todos os laboratórios
    if not laboratorio_id:
        return get_all_users()

    # Laboratório específico
    return get_users_by_lab(laboratorio_id)