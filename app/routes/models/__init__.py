'''Index for models routes'''
from app.routes.models.crud_blueprint import create_crud_blueprint
from app.routes.models.money_bp import money_bp


__all__ = ['create_crud_blueprint', 'money_bp']
