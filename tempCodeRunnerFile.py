from app import create_app
from datetime import datetime

app = create_app()
app.jinja_env.globals['now'] = datetime.now  # <-- Adiciona esta linha

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)