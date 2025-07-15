# scripts/migrations/env.py

"""
Alembic migration environment setup (async-compatible).

Purpose:
- Dynamically load DB URL from .env (.ini fallback)
- Enable both offline (SQL script) and online (live DB) migrations
- Handle SQLAlchemy async engines (aiosqlite, aiomysql)
- Register metadata for autogenerate support
"""

import asyncio
from logging.config import fileConfig
from typing import Optional

from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context

# 🧠 SQLAlchemy base metadata (includes all defined models)
from app.database.base import Base

# 🔧 Load DB connection string from .env (via Pydantic Settings)
from app.api.config.settings import settings

# 📁 Alembic configuration object (from alembic.ini)
config = context.config

# 📝 Load logging configuration from alembic.ini, if present
if config.config_file_name:
    fileConfig(config.config_file_name)

# 🧪 Inject the runtime DB URL from settings (replaces alembic.ini hardcoded value)
config.set_main_option("sqlalchemy.url", settings.database_url)

# 🎯 Metadata for models (used in autogenerate diffs)
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """
    Run Alembic migrations in offline mode.

    Use Case:
    - CI/CD pipelines where DB access is restricted
    - Generate SQL script instead of applying directly

    This uses `literal_binds` to embed values directly into SQL.
    """
    context.configure(
        url=settings.database_url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """
    Run Alembic migrations in online mode (live DB connection).

    Use Case:
    - Directly apply schema changes to dev/staging/prod DB
    - Works with async drivers like `aiosqlite` and `aiomysql`
    """
    config_section: Optional[dict] = config.get_section(config.config_ini_section)
    engine = async_engine_from_config(
        config_section or {},  # Fallback to empty dict if section is missing
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with engine.connect() as connection:
        # 🧠 Migration context setup is done using a sync wrapper inside async
        await connection.run_sync(
            lambda sync_conn: context.configure(
                connection=sync_conn,
                target_metadata=target_metadata,
                compare_type=True,
            )
        )
        # 🚀 Apply the migrations
        await connection.run_sync(lambda _: context.run_migrations())

    await engine.dispose()


def run() -> None:
    """
    Entrypoint for Alembic.

    Automatically routes to offline or online mode based on command.
    """
    if context.is_offline_mode():
        run_migrations_offline()
    else:
        asyncio.run(run_migrations_online())


# 🔁 Execute based on CLI context
run()
