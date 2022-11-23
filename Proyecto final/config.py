class BaseConfig:
    #Configuración de la bd
    USER_DB = 'postgres'
    PASS_DB = 'admin'
    URL_DB = 'localhost'
    NAME_DB = 'productosCRUD'
    FULL_URL_DB = f'postgresql://{USER_DB}:{PASS_DB}@{URL_DB}/{NAME_DB}'
    SQLALCHEMY_DATABASE_URI = FULL_URL_DB
    SECRET_KEY = "secretKey1212"
    DEBUG = False
    BCRYPT_LOG_ROUNDS = 13
    SQLALCHEMY_TRACK_MODIFICATIONS = False