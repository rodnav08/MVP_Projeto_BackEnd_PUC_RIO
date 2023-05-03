from pydantic import BaseModel
from typing import  List
from model.tubo import Tubo


class TuboSchema(BaseModel):
    """Define como um novo tubo inserido deve ser representado"""
    nome: str = "Oleoduto A"
    diametro: float = 12.0
    espessura: float = 0.50
    material: str = "API 5L Gr. B"
    produto: str = "Gasolina"
    arranjo: str = "2A+2P"
    origem: str = "Rio de Janeiro"
    destino: str = "Duque de Caxias"
    


class TuboBuscaSchema(BaseModel):
    """Define a busca apenas com base no nome do tubo."""
    nome: str = "Oleoduto B"


class TuboBuscaIdSchema(BaseModel):
    """Define a busca apenas com base no id do tubo."""
    id: int = 1


class ListagemTubosSchema(BaseModel):
    """Define como uma listagem de tubos será representada."""
    tubos: List[TuboSchema]


def apresenta_tubos(tubos: List[Tubo]):
    """Retorna uma representação do tubo seguindo o schema definido em
    TuboViewSchema."""
    result = []
    for tubo in tubos:
        result.append({
            "nome": tubo.nome,
            "diametro": tubo.diametro,
            "espessura": tubo.espessura,
            "material": tubo.material,
            "produto": tubo.produto,
            "arranjo": tubo.arranjo,
            "origem": tubo.origem,
            "destino": tubo.destino,
            
        })

    return {"tubos": result}


class TuboViewSchema(BaseModel):
    """Define como um tubo será retornado."""
    id: int = 1
    nome: str = "Oleoduto C"
    diametro: float = 40.0
    espessura: float = 0.312
    material: str = "API 5L X46"
    produto: str = "Nafta"
    arranjo: str = "1A+1P"
    origem: str = "Volta Redonda"
    destino: str = "Lorena"
    


class TuboDelSchema(BaseModel):
    """Define como deve ser a estrutura do dado retornado após uma requisição
    de remoção."""
    mesage: str
    nome: str


def apresenta_tubo(tubo: Tubo):
    """Retorna uma representação do tubo seguindo o schema definido em
    TuboViewSchema."""
    return {
        "id": tubo.id,
        "nome": tubo.nome,
        "diametro": tubo.diametro,
        "espessura": tubo.espessura,
        "material": tubo.material,
        "produto": tubo.produto,
        "arranjo": tubo.arranjo,
        "origem": tubo.origem,
        "destino": tubo.destino,
        
    }
