from sqlalchemy.orm import Session
import models, schemas

# Operaciones para Estaciones
def get_estacion(db: Session, estacion_id: int):
    return db.query(models.EstacionDB).filter(models.EstacionDB.id == estacion_id).first()

def get_all_estaciones(db: Session):
    return db.query(models.EstacionDB).all()

def crear_estacion(db: Session, estacion: schemas.EstacionCreate):
    db_estacion = models.EstacionDB(
        id=estacion.id, 
        nombre=estacion.nombre, 
        ubicacion=estacion.ubicacion
    )
    db.add(db_estacion)
    db.commit()
    db.refresh(db_estacion)
    return db_estacion

# Operaciones para Lecturas
def registrar_lectura(db: Session, lectura: schemas.LecturaCreate):
    db_lectura = models.LecturaDB(
        valor=lectura.valor, 
        estacion_id=lectura.estacion_id
    )
    db.add(db_lectura)
    db.commit()
    db.refresh(db_lectura)
    return db_lectura

def get_lecturas_by_estacion(db: Session, estacion_id: int):
    return db.query(models.LecturaDB).filter(models.LecturaDB.estacion_id == estacion_id).all()

def get_all_lecturas(db: Session):
    return db.query(models.LecturaDB).all()