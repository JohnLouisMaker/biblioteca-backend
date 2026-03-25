import enum

from sqlalchemy import (
    Boolean,
    Column,
    Date,
    Enum,
    ForeignKey,
    Integer,
    String,
    Table,
    create_engine,
)
from sqlalchemy.orm import declarative_base, relationship

db = create_engine("sqlite:///./app/database/database.db")
Base = declarative_base()

# TABELAS ASSOCIATIVAS ---

livro_categoria = Table(
    "livro_categoria",
    Base.metadata,
    Column("id_livro", Integer, ForeignKey("livro.id"), primary_key=True),
    Column("id_categoria", Integer, ForeignKey("categoria.id"), primary_key=True),
)

# --- TABELAS DE APOIO ---


# AUTOR DO LIVRO
class AutorModel(Base):
    __tablename__ = "autor"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(150), nullable=False)
    livros = relationship("LivroModel", back_populates="autor")


# CATEGORIA DO LIVRO
class CategoriaModel(Base):
    __tablename__ = "categoria"
    id = Column(Integer, primary_key=True, autoincrement=True)
    categoria = Column(String(100), nullable=False, unique=True)
    livros = relationship(
        "LivroModel", secondary=livro_categoria, back_populates="categorias"
    )


# ESTADO DO EXEMPLAR
class EstadoExemplar(enum.Enum):
    DISPONIVEL = "DISPONIVEL"
    EMPRESTADO = "EMPRESTADO"


# STATUS DO EMPRESTIMO
class StatusEmprestimo(enum.Enum):
    ATIVO = "ATIVO"
    DEVOLVIDO = "DEVOLVIDO"
    ATRASADO = "ATRASADO"


# --- TABELAS PRINCIPAIS ---


# OPERADOR DA BIBLIOTECA
class OperadorModel(Base):
    __tablename__ = "operador"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    senha = Column(String(250), nullable=False)
    ativo = Column(Boolean, default=True, nullable=False)
    admin = Column(Boolean, default=False, nullable=False)


# USUARIO DA BIBLIOTECA
class UsuarioModel(Base):
    __tablename__ = "usuario"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    cpf = Column(String(14), unique=True, nullable=False)
    data_nascimento = Column(Date, nullable=True)
    sexo = Column(String(1), nullable=True)
    status = Column(Boolean, default=True, nullable=False)
    contato = Column(String(150), nullable=True)
    emprestimos = relationship("EmprestimoModel", back_populates="usuario")


# LIVRO DA BIBLIOTECA
class LivroModel(Base):
    __tablename__ = "livro"
    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(200), nullable=False)
    ano = Column(Integer, nullable=True)
    issn = Column(String(20), nullable=True)
    quantidade_exemplares = Column(Integer, default=0, nullable=False)
    id_autor = Column(Integer, ForeignKey("autor.id"), nullable=True)
    autor = relationship("AutorModel", back_populates="livros")
    categorias = relationship(
        "CategoriaModel", secondary=livro_categoria, back_populates="livros"
    )
    exemplares = relationship("ExemplarModel", back_populates="livro")


# EXEMPLAR DO LIVRO
class ExemplarModel(Base):
    __tablename__ = "exemplar"
    id = Column(Integer, primary_key=True, autoincrement=True)
    codigo_localizacao = Column(String(50), nullable=True)
    estado = Column(
        Enum(EstadoExemplar), default=EstadoExemplar.DISPONIVEL, nullable=False
    )
    id_livro = Column(Integer, ForeignKey("livro.id"), nullable=False)
    livro = relationship("LivroModel", back_populates="exemplares")
    emprestimos = relationship("EmprestimoModel", back_populates="exemplar")


# EMPRESTIMO DA BIBLIOTECA
class EmprestimoModel(Base):
    __tablename__ = "emprestimo"
    id = Column(Integer, primary_key=True, autoincrement=True)
    data_emprestimo = Column(Date, nullable=False)
    data_prevista = Column(Date, nullable=False)
    data_devolucao = Column(Date, nullable=True)
    status = Column(
        Enum(StatusEmprestimo), default=StatusEmprestimo.ATIVO, nullable=False
    )
    id_usuario = Column(Integer, ForeignKey("usuario.id"), nullable=False)
    id_exemplar = Column(Integer, ForeignKey("exemplar.id"), nullable=False)
    usuario = relationship("UsuarioModel", back_populates="emprestimos")
    exemplar = relationship("ExemplarModel", back_populates="emprestimos")
