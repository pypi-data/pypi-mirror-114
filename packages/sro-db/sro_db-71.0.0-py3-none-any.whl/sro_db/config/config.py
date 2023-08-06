from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

import os
from pprint import pprint


try:

    SQLALCHEMY_DATABASE_URI = f"postgresql://{os.environ['USERDB']}:{os.environ['PASSWORDDB']}@{os.environ['HOST']}/{os.environ['DBNAME']}"

except Exception as e:
    print(e)
    print("Favor configurar as variáveis de ambiente: [USERDB, PASSWORDDB, HOST, DBNAME]")
    exit(1)

engine = create_engine(SQLALCHEMY_DATABASE_URI,pool_size=20, max_overflow=0)

Base = declarative_base()

class Config():

    def create_database(self):
        try:
            Session = scoped_session(sessionmaker(bind=engine,autocommit=True))
            session = Session()
            session.begin(subtransactions=True)
            Base.metadata.create_all(engine)
        except Exception as e:
            print (e)
    
   
    def drop_database(self):
        try:
            metadata = MetaData()
            metadata.reflect(bind=engine)
            for table in metadata.tables.keys():
                with engine.connect() as con:
                    print ('DROP TABLE '+table)
                    con.execute('DROP TABLE '+table+' CASCADE')                
        
        except Exception as e:
            print (e)
