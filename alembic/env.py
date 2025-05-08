import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from alembic import context
from sqlalchemy import engine_from_config, pool
from logging.config import fileConfig

# Import Base and models
from app.database import Base
from app.models import user, document 



# Alembic Config
config = context.config
fileConfig(config.config_file_name)

target_metadata = Base.metadata
