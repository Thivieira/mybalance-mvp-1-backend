from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect, url_for, jsonify
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from models import Session, Transaction, Category
from schemas import *
from flask_cors import CORS

from controllers.category import category_routes
from controllers.transaction import transaction_routes
from controllers.balance_history import balance_routes
from services.balance import calculate_balance

# Define tags first
home_tag = Tag(name="Documentação", description="Documentação da API MyBalance")
site_map_tag = Tag(name="Mapa do site", description="Mapa do site da API")

info = Info(title="MyBalance API", version="1.0.0")
app = OpenAPI(__name__, info=info)
app.url_map.strict_slashes = False

# Atualiza a configuração CORS com opções adicionais
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

app.config['OPENAPI_URL_PREFIX'] = ''
app.config['OPENAPI_VERSION'] = '3.0.3'
app.config['OPENAPI_JSON_PATH'] = 'openapi.json'
app.config['OPENAPI_SWAGGER_UI_PATH'] = '/docs'
app.config['OPENAPI_SWAGGER_UI_URL'] = 'https://cdn.jsdelivr.net/npm/swagger-ui-dist/'
app.config['OPENAPI_SWAGGER_UI_CONFIG'] = {
    'deepLinking': True,
    'layout': "BaseLayout",
    'defaultModelsExpandDepth': -1,
    'docExpansion': 'list',
    'defaultModelExpandDepth': 2,
    'displayRequestDuration': True,
    'language': 'pt-BR'
}

# Register the blueprints
app.register_api(transaction_routes)
app.register_api(category_routes)
app.register_api(balance_routes)

# Add this function instead
@app.before_first_request
def init_app():
    """Initialize application state before first request"""
    session = Session()
    try:
        calculate_balance(session)
    finally:
        session.close()

@app.get('/', tags=[home_tag])
def home():
    """Redireciona para documentação em português.
    """
    return redirect('/openapi')

def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)

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
