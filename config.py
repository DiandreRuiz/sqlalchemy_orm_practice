class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:hetaT-601@localhost:3306/library'
    DEBUG = True
    
class TestingConfig:
    pass
    
class ProductionConfig:
    pass