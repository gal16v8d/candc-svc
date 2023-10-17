'''Index for models routes'''
from app.routes.models.crud_blueprint import create_crud_blueprint
from app.routes.models.money import create_money_bp

__all__ = ['create_crud_blueprint', 'create_money_bp']
