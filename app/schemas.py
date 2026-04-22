from pydantic import BaseModel
from typing import List, Optional

# Esquemas para Estaciones
class EstacionBase(BaseModel):
    id: int
    nombre: str
    ubicacion: str

class EstacionCreate(EstacionBase):
    pass

class Estacion(EstacionBase):
    class Config:
        from_attributes = True

# Esquemas para Lecturas
class LecturaBase(BaseModel):
    valor: float
    estacion_id: int

class LecturaCreate(LecturaBase):
    pass

class Lectura(LecturaBase):
    id: int
    
    class Config:
        from_attributes = True