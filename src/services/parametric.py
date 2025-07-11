from sqlalchemy.orm import Session
from repositories.base import BaseRepository
from utils.exceptions import RecordNotFoundError
from repositories import (
    document_type_repo,
    gender_repo,
    operational_role_repo,
    availability_status_repo
)
from typing import Type
import logging
class ParametricService:
    def __init__(self, repository: BaseRepository):
        """
        Servicio genérico para manejar tablas paramétricas.
        :param repository: Una instancia de un repositorio para una tabla paramétrica.
        """
        self.repository = repository

    def get_all(self, db: Session) -> list:
        """Obtiene todos los registros de una tabla paramétrica."""
        logging.info(f"Getting all {self.repository.model.__tablename__}")
        return self.repository.get_multi(db, limit=200) # Aumentamos el límite para tablas de opciones

    def get_by_id(self, db: Session, id: int):
        """Obtiene un registro por su ID."""
        logging.info(f"Getting {self.repository.model.__tablename__} by id: {id}")
        record = self.repository.get(db, id=id)
        if not record:
            raise RecordNotFoundError(f"Record with id {id} not found in {self.repository.model.__tablename__}.")
        return record

class OperationalRoleService(ParametricService):
    def get_all_with_count(self, db: Session) -> list:
        """Obtiene todos los roles con el conteo de empleados."""
        logging.info(f"Getting all operational roles with employee count")
        return self.repository.get_with_employee_count(db)

# --- Creamos una instancia del servicio para cada tabla paramétrica ---

document_type_service = ParametricService(document_type_repo)
gender_service = ParametricService(gender_repo)
operational_role_service = OperationalRoleService(operational_role_repo)
availability_status_service = ParametricService(availability_status_repo)