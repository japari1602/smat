from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import models, schemas, crud
from database import engine, get_db

# Crear tablas
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SMAT - Sistema de Monitoreo de Alerta Temprana",
    version="1.0.0",
    description="API para gestión de desastres naturales y telemetría."
)
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/estaciones/", status_code=201, tags=["Gestión de Infraestructura"])
def crear_estacion(estacion: schemas.EstacionCreate, db: Session = Depends(get_db)):
    return {"msj": "Estación guardada en DB", "data": crud.crear_estacion(db, estacion)}

@app.post("/lecturas/", status_code=201, tags=["Telemetría de Sensores"])
def registrar_lectura(lectura: schemas.LecturaCreate, db: Session = Depends(get_db)):
    # Validar si la estación existe
    estacion = crud.get_estacion(db, lectura.estacion_id)
    if not estacion:
        raise HTTPException(status_code=404, detail="Estación no existe")
    
    crud.registrar_lectura(db, lectura)
    return {"status": "Lectura guardada en DB"}

@app.get("/estaciones/{id}/riesgo", tags=["Análisis de Riesgo"])
def obtener_riesgo(id: int, db: Session = Depends(get_db)):
    # 1. Validar existencia de la estación
    estacion = crud.get_estacion(db, id)
    if not estacion:
        raise HTTPException(status_code=404, detail="Estación no encontrada")
    
    # 2. Obtener lecturas
    lecturas = crud.get_lecturas_by_estacion(db, id)
    if not lecturas:
        return {"id": id, "nivel": "SIN DATOS", "valor": 0}
    
    # 3. Evaluar última lectura
    ultima_lectura = lecturas[-1].valor
    if ultima_lectura > 20.0:
        nivel = "PELIGRO"
    elif ultima_lectura > 10.0:
        nivel = "ALERTA"
    else:
        nivel = "NORMAL"

    return {"id": id, "valor": ultima_lectura, "nivel": nivel}

@app.get("/estaciones/stats", tags=["Resumen Ejecutivo"])
def obtener_stats(db: Session = Depends(get_db)):
    estaciones = crud.get_all_estaciones(db)
    lecturas = crud.get_all_lecturas(db)

    if not estaciones or not lecturas:
        raise HTTPException(status_code=404, detail="No hay datos suficientes")

    valores = [l.valor for l in lecturas]
    promedio_global = sum(valores) / len(valores)

    return {
        "total_estaciones": len(estaciones),
        "total_lecturas": len(lecturas),
        "promedio_global": promedio_global
    }