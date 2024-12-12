from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect, url_for
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from models import Session, Transaction, Category
from schemas import *
from flask_cors import CORS

from controllers.category import category_routes
from controllers.transaction import transaction_routes
from controllers.balance_history import balance_routes
from balance import calculate_balance
info = Info(title="MyBalance API", version="1.0.0")
app = OpenAPI(__name__, info=info)
app.url_map.strict_slashes = False

# Atualiza a configuração CORS com opções adicionais
CORS(app, resources={
    r"/*": {
        "origins": "http://localhost:5500",
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

app.config['OPENAPI_URL_PREFIX'] = '/'
app.config['OPENAPI_SWAGGER_UI_PATH'] = '/openapi'
app.config['OPENAPI_SWAGGER_UI_URL'] = 'https://cdn.jsdelivr.net/npm/swagger-ui-dist/'
app.config['OPENAPI_REDOC_PATH'] = '/redoc'
app.config['OPENAPI_REDOC_URL'] = 'https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js'

# Register the blueprints
app.register_api(transaction_routes)
app.register_api(category_routes)
app.register_api(balance_routes)

# Add this function instead
@app.before_first_request
def init_app():
    """Inicializa o estado da aplicação antes da primeira requisição"""
    session = Session()
    try:
        calculate_balance(session)
    finally:
        session.close()

# Definindo tags
home_tag = Tag(name="Documentation", description="Seleção de documentação: Swagger, Redoc ou Rapidoc")

@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite escolher o estilo de documentação.
    """
    return redirect('/openapi')

def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)

site_map_tag = Tag(name="Site Map", description="Mapa do site da API")
@app.get("/site-map", tags=[site_map_tag])
def site_map():
    links = []
    for rule in app.url_map.iter_rules():
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            links.append((url, rule.endpoint))
    
    return {"routes": [{"url": url, "endpoint": endpoint} for url, endpoint in links]}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6700, debug=True)
