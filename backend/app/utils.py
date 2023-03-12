from sqlalchemy.ext.asyncio import AsyncSession


async def check_db(db: AsyncSession) -> bool:
    try:
        await db.execute("SELECT version_num FROM alembic_version")
    except Exception:
        return False
    return True
