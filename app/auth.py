from ldap3 import Server, Connection, NTLM, AUTO_BIND_NO_TLS
from flask import session
from app.models import User  # supondo que tenha um modelo User

LDAP_SERVER = '10.20.138.18'
LDAP_DOMAIN = 'PSS'
LDAP_SEARCH_BASE = 'DC=PSS,DC=local'  # ajuste conforme o seu domínio

def ldap_authenticate(username, password):
    user_dn = f'{LDAP_DOMAIN}\\{username}'
    server = Server(LDAP_SERVER)
    try:
        conn = Connection(server, user=user_dn, password=password, authentication=NTLM, auto_bind=AUTO_BIND_NO_TLS)
        if conn.bind():
            # Verifica se o usuário está na base de dados
            user = User.query.filter_by(username=username).first()
            if user:
                session['user_id'] = user.id
                session['group_id'] = user.group_id
                return True
        return False
    except Exception as e:
        print(f'LDAP error: {e}')
        return False