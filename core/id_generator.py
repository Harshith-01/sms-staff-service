from sqlalchemy import text


def _next_prefixed_id(db, table: str, prefix: str, lock_key: str) -> str:
    db.execute(text("SELECT pg_advisory_xact_lock(hashtext(:lock_key))"), {"lock_key": lock_key})
    value = db.execute(
        text(
            f"""
            SELECT COALESCE(MAX(CAST(SUBSTRING(id FROM :pattern) AS BIGINT)), 0)
            FROM {table}
            WHERE id ~ :regex
            """
        ),
        {
            "pattern": f"^{prefix}([0-9]+)$",
            "regex": f"^{prefix}[0-9]+$",
        },
    ).scalar_one()
    return f"{prefix}{int(value) + 1}"


def generate_user_id(db) -> str:
    return _next_prefixed_id(db, table="users", prefix="U", lock_key="idgen:users:U")


def generate_staff_id(db) -> str:
    return _next_prefixed_id(db, table="non_teaching_staff", prefix="NTS", lock_key="idgen:non_teaching_staff:NTS")
