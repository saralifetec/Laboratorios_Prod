import json

def get_dashboard_config(user):

    if (
        not user.dashboard_perfil
        or not user.dashboard_perfil.configuracao
    ):
        return get_default_dashboard_config()

    try:

        return json.loads(
            user.dashboard_perfil.configuracao
        )

    except Exception:

        return get_default_dashboard_config()

def widget_ativo( dashboard_config, widget_id ):
    return (
        dashboard_config
        .get('widgets', {})
        .get(widget_id, {})
        .get('ativo', True)
    )

def widget_config( dashboard_config, widget_id ):
    return (
        dashboard_config
        .get('widgets', {})
        .get(widget_id, {})
    )

def get_default_dashboard_config():

    return {
        "widgets": {

            "ensaios_pendentes": {
                "ativo": True,
                "coluna": "left",
                "ordem": 1,
                "registos": 5
            },

            "relatorios_pendentes": {
                "ativo": True,
                "coluna": "left",
                "ordem": 2,
                "registos": 5
            },

            "pedidos_horas_extra": {
                "ativo": True,
                "coluna": "right",
                "ordem": 3,
                "registos": 5
            },

            "avisos_horas": {
                "ativo": True,
                "coluna": "right",
                "ordem": 1
            },

            "avisos_ensaios": {
                "ativo": True,
                "coluna": "right",
                "ordem": 2
            },

            "avisos_armazem": {
                "ativo": True,
                "coluna": "left",
                "ordem": 3,
                "registos": 10
            },

            "resumo_horas": {
                "ativo": True,
                "coluna": "right",
                "ordem": 5,
                "registos": 10
            },

            "horas_bloqueadas": {
                "ativo": True,
                "coluna": "right",
                "ordem": 4,
                "registos": 5
            }

        }
    }

WIDGETS_DASHBOARD = [
    {
        "id": "ensaios_pendentes",
        "i18n": "index.pending_tests",
        "tipo": "tabela"
    },
    {
        "id": "relatorios_pendentes",
        "i18n": "index.pending_reports",
        "tipo": "tabela"
    },
    {
        "id": "pedidos_horas_extra",
        "i18n": "index.extra_hours_requests",
        "tipo": "tabela"
    },
    {
        "id": "avisos_horas",
        "i18n": "index.hours_alerts",
        "tipo": "aviso"
    },
    {
        "id": "avisos_ensaios",
        "i18n": "index.test_alerts",
        "tipo": "aviso"
    },
    {
        "id": "avisos_armazem",
        "i18n": "index.warehouse_alerts",
        "tipo": "aviso"
    },
    {
        "id": "resumo_horas",
        "i18n": "index.hours_summary",
        "tipo": "tabela"
    },
    {
        "id": "horas_bloqueadas",
        "i18n": "index.missing_information",
        "tipo": "tabela"
    }
]