from sqlalchemy import engine_from_config, pool
import sys
import os
from alembic import context

# Añade la raíz del proyecto al PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/..')
from modelosBiblioteca import Base