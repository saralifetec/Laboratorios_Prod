from datetime import date


def parse_horas(value):

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

            return h + (m / 60)

        except Exception:

            raise ValueError(
                "Formato de horas inválido. Use HH:MM."
            )

    s = s.replace(",", ".")

    try:
        return float(s)

    except Exception:

        raise ValueError(
            "Formato de horas inválido."
        )


def parse_horas_iso(value):
    """
    Aceita:
        2.5
        "2.5"
        "2,5"
        "02:30"

    Devolve:
        2.5

    Lança ValueError se inválido.
    """

    if value is None:
        raise ValueError("Valor de horas vazio.")

    if isinstance(value, (int, float)):
        return float(value)

    s = str(value).strip()

    if not s:
        raise ValueError("Valor de horas vazio.")

    # formato HH:MM
    if ":" in s:

        try:
            h_str, m_str = s.split(":")

            h = int(h_str)
            m = int(m_str)

            if h < 0 or m < 0 or m >= 60:
                raise ValueError

            return h + (m / 60.0)

        except Exception:

            raise ValueError(
                "Formato de horas inválido. Use HH:MM (ex.: 02:30)."
            )

    # formato decimal
    s = s.replace(",", ".")

    try:
        return float(s)

    except Exception:

        raise ValueError(
            "Formato de horas inválido. Use 2.5 ou 02:30."
        )
