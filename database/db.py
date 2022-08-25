from sqlmodel import create_engine, SQLModel, Session


_file_name = f"test.db"
_db_url = f"sqlite:///{_file_name}?check_same_thread=False"

engine = create_engine(_db_url, echo=True)


def create_table():
    """创建数据表"""
    SQLModel.metadata.create_all(engine)


def get_session():
    """获取 Session"""
    with Session(engine) as session:
        yield session


if __name__ == '__main__':
    create_table()
