from datetime import datetime

from sqlalchemy.engine.create import create_engine
from sqlalchemy.orm.session import sessionmaker


class PostgreSQLHandler:

    def __init__(self, db_table, container, db_info):
        self.db_table = db_table
        self.container = container
        # DB 연결
        db_link = f'postgresql://{db_info["user"]}:{db_info["password"]}' \
                  f'@{db_info["host"]}:{db_info["port"]}/{db_info["database"]}'

        # engine 생성
        self.engine = create_engine(db_link)
        # DB 연결 create
        self.session_maker = sessionmaker(bind=self.engine)

        # 테이블 생성
        self.create_table()

    def create_table(self):
        create_table_sql = f"CREATE TABLE IF NOT EXISTS {self.db_table}(" \
                           "id           serial  primary key      not null," \
                           "container    varchar(50)              not null," \
                           "process      integer                  not null," \
                           "process_name varchar(50)              not null," \
                           "thread_name  varchar(50)              not null," \
                           "name         varchar(50)              not null," \
                           "thread       bigint                   not null," \
                           "pathname     varchar(200)             not null," \
                           "func_name    varchar(50)              not null," \
                           "lineno       integer                  not null," \
                           "levelname    varchar(50)              not null," \
                           "time         timestamp with time zone not null," \
                           "message      text                     not null," \
                           "exc_info     text                     not null," \
                           "exc_text     text                     not null," \
                           "stack_info   text                     not null," \
                           "levelno      integer                  not null" \
                           ");"
        self.execute_sql(sql=create_table_sql)


    def insert_data(self, record):
        insert_sql = f"INSERT INTO {self.db_table} (" \
                     f"container, process, process_name, " \
                     f"thread, thread_name, " \
                     f"name, pathname, func_name, lineno, " \
                     f"levelno, levelname, time, " \
                     f"message, exc_info, exc_text, stack_info" \
                     f") VALUES (" \
                     f"'{self.container}', '{record.process}', '{record.process}', " \
                     f"'{record.thread}', '{record.threadName}', " \
                     f"'{record.name}', '{record.pathname}', '{record.funcName}', '{record.lineno}', " \
                     f"'{record.levelno}', '{record.levelname}', '{datetime.now()}', " \
                     f"'{record.message}', '{record.exc_info}', '{record.exc_text}', '{record.stack_info}'" \
                     f");"
        self.execute_sql(sql=insert_sql)

    def execute_sql(self, sql: str):
        """
        sql문 단순 실행
        :param sql:
        :return:
        """
        session = self.session_maker()
        try:
            session.execute(sql)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
