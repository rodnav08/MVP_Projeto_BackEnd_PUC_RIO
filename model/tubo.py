from sqlalchemy import Column, String, Integer, Float


from  model import Base

# classe que define o que esperar de um tubo/duto
class Tubo(Base):
    __tablename__ = 'tubo'

    id = Column("pk_tubo", Integer, primary_key=True)
    nome = Column(String(200))
    diametro = Column(Float)
    espessura = Column(Float)
    material = Column(String(140))
    produto = Column(String(140))
    arranjo = Column(String(140))
    origem = Column(String(140))
    destino = Column(String(140))
    



    def __init__(self, nome:str, diametro:float, espessura:float, material:str,produto:str,arranjo:str,origem:str,destino:str):
        
        self.nome = nome
        self.diametro = diametro
        self.espessura = espessura
        self.material = material
        self.produto = produto
        self.arranjo = arranjo
        self.origem = origem
        self.destino = destino
        
        


        