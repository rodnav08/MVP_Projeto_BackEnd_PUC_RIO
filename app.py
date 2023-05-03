from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Tubo
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação",
               description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
tubo_tag = Tag(
    name="Tubo", description="Adição, visualização e remoção de tubos à base")



@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/tubo', tags=[tubo_tag],
          responses={"200": TuboViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_tubo(form: TuboSchema):
    """Adiciona um novo Tubo à base de dados

    Retorna uma representação dos tubos.
    """
    tubo = Tubo(
        nome = form.nome,
        diametro = form.diametro,
        espessura = form.espessura,
        material = form.material,
        produto = form.produto,
        arranjo = form.arranjo,
        origem = form.origem,
        destino = form.destino
    )
    logger.debug(f"Adicionando: '{tubo.nome}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando tubo
        session.add(tubo)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"'{tubo.nome}' adicionado")
        return apresenta_tubo(tubo), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Tubo ja existente na base"
        logger.warning(f"Erro ao adicionar '{tubo.nome}', {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo tubo"
        logger.warning(f"Erro ao adicionar '{tubo.nome}', {error_msg}")
        return {"mesage": error_msg}, 400


@app.get('/tubos', tags=[tubo_tag],
         responses={"200": ListagemTubosSchema, "404": ErrorSchema})
def get_tubos():
    """Faz a busca por todos os Tubos cadastrados

    Retorna uma representação da listagem de tubos.
    """
    logger.debug(f"Coletando tubos na base ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    tubos = session.query(Tubo).all()

    if not tubos:
        # se não há tubos cadastrados
        return {"tubos": []}, 200
    else:
        logger.debug(f"%d Tubos econtrados" % len(tubos))
        # retorna a representação de tubo
        print(tubos)
        return apresenta_tubos(tubos), 200


@app.get('/tubo', tags=[tubo_tag],
         responses={"200": TuboViewSchema, "404": ErrorSchema})
def get_tubo(query: TuboBuscaIdSchema):

    """Faz a busca por um Tubo a partir do id do tubo

    Retorna uma representação dos tubos e comentários associados.
    """
    
    tubo_id = query.id
    logger.debug(f"Coletando dados sobre o tubo #{tubo_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    tubo = session.query(Tubo).filter(Tubo.id == tubo_id).first()

    if not tubo:
        # se o tubo não foi encontrado
        error_msg = "Tubo não encontrado na base"
        logger.warning(f"Erro ao buscar tubo '{tubo.nome}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"Tubo econtrado: '{tubo_id}'")
        # retorna a representação do tubo
        return apresenta_tubo(tubo), 200


@app.delete('/tubo', tags=[tubo_tag],
            responses={"200": TuboDelSchema, "404": ErrorSchema})
def del_tubo(query: TuboBuscaSchema):
    """Deleta um Tubo a partir do nome informado

    Retorna uma mensagem de confirmação da remoção.
    """
    tubo_nome = unquote(unquote(query.nome))
    logger.debug(f"Deletando dados sobre tubo #{tubo_nome}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    tubo = session.query(Tubo).filter(Tubo.nome== tubo_nome).delete()
    session.commit()

    if tubo:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletando tubo #{tubo_nome}")
        return {"mesage": "Tubo removido", "nome": tubo_nome}
    else:
        # se o tubo não foi encontrado
        error_msg = "Tubo não encontrado na base"
        logger.warning(f"Erro ao deletar tubo #'{tubo_nome}', {error_msg}")
        return {"mesage": error_msg}, 404

