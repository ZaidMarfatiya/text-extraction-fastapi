from alembic import context
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from backend.app.db.base import Base

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = Base.metadata


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    configuration = config.get_section(config.config_ini_section)
    # try to get tag is needed for tests
    uri_from_tag = context.get_tag_argument()
    uri = uri_from_tag if uri_from_tag else 'postgresql://postgres:root@text-extraction-db-1/text-extraction'
    configuration['sqlalchemy.url'] = uri
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

run_migrations_online()