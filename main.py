from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from sqlmodel import Session, select

from database import Cancion, CancionBase, crear_db_y_tablas, get_session


@asynccontextmanager
async def lifespan(app: FastAPI):
    crear_db_y_tablas()
    yield
    


app = FastAPI(title="Mi Playlist", lifespan=lifespan)

session_dependency = Annotated[Session, Depends(get_session)]


def buscar_cancion(cancion_id: int, session: Session) -> Cancion:
    """Busca una canción por id; si no existe, responde 404."""
    cancion = session.get(Cancion, cancion_id)
    if cancion is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Canción {cancion_id} no encontrada",
        )
    return cancion

@app.post("/canciones/", response_model=Cancion, status_code=status.HTTP_201_CREATED)
def crear_cancion(cancion: CancionBase, session: session_dependency):
    nueva_cancion = Cancion.model_validate(cancion)
    session.add(nueva_cancion)
    session.commit()
    session.refresh(nueva_cancion)
    return nueva_cancion

@app.get("/canciones/", response_model=list[Cancion])
def ver_canciones(session: session_dependency):
    consulta = select(Cancion)
    return session.exec(consulta).all()

@app.get("/canciones/{cancion_id}", response_model=Cancion)
def ver_cancion(cancion_id: int, session: session_dependency):
    return buscar_cancion(cancion_id, session)

@app.put("/canciones/{cancion_id}", response_model=Cancion)
def actualizar_cancion(
    cancion_id: int, cancion_nueva: CancionBase, session: session_dependency
):
    cancion = buscar_cancion(cancion_id, session)

    cancion.titulo = cancion_nueva.titulo
    cancion.artista = cancion_nueva.artista
    cancion.genero = cancion_nueva.genero
    cancion.duracion_segundos = cancion_nueva.duracion_segundos
    cancion.favorita = cancion_nueva.favorita

    session.add(cancion)
    session.commit()
    session.refresh(cancion)
    return cancion

@app.delete("/canciones/{cancion_id}", response_model=Cancion)
def borrar_cancion(cancion_id: int, session: session_dependency):
    cancion = buscar_cancion(cancion_id, session)
    data = cancion.model_dump()
    session.delete(cancion)
    session.commit()
    return data
