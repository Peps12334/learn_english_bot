from sqlalchemy import BigInteger, String, Boolean, ForeignKey, DateTime, func, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import datetime
from words_list import word_list
class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key= True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
    use: Mapped[str] = mapped_column(String(100), nullable=True)

engine = create_engine('sqlite:///mydatabase.db', echo=False)

Base.metadata.create_all(engine)