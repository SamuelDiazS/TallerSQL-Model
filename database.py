import os

from sqlmodel import Field, Session, SQLModel, create_engine


class CancionBase(SQLModel):
    titulo: str = Field(index=True)
    artista: str 
    genero: str | None = Field(default=None, index=True)
    duracion_segundos: int = Field(gt=0) 
    favorita: bool = Field(default=False)


class Cancion(CancionBase, table=True):
    __tablename__: str = "canciones" 
    id: int | None = Field(default=None, primary_key=True)

EN_VERCEL = bool(os.environ.get("VERCEL"))

if EN_VERCEL:
    DATA_BASE_URL = "sqlite:////tmp/database.db"
else:
    DATA_BASE_URL = "sqlite:///database.db"
connects_args = {"check_same_thread": False}

engine = create_engine(DATA_BASE_URL, connect_args=connects_args, echo=not EN_VERCEL)


def crear_db_y_tablas():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session



if EN_VERCEL:
    crear_db_y_tablas()
