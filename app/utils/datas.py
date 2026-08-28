from datetime import datetime, date

def parse_data(valor):

    if not valor:
        return None

    if isinstance(valor, str):

        if valor.startswith('0000-00-00'):
            return None

        try:
            return datetime.fromisoformat(valor).date()
        except ValueError:
            return None

    if isinstance(valor, datetime):
        return valor.date()

    if isinstance(valor, date):
        return valor

    return None


def parse_data_iso(dstr):

    if not dstr:
        raise ValueError("Data é obrigatória.")

    try:
        return date.fromisoformat(dstr)

    except Exception:
        raise ValueError(
            "Formato de data inválido. Use YYYY-MM-DD."
        )

def formatar_data(valor):
    if not valor:
        return ""

    if isinstance(valor, str):
        return valor

    try:
        return valor.strftime("%d-%m-%Y %H:%M")
    except Exception:
        return str(valor)