from sqlalchemy import text
from database import engine

with engine.begin() as conn:
    try:
        conn.execute(text("ALTER TABLE users ADD COLUMN email VARCHAR;"))
        print("Added email column")
    except Exception as e:
        print(f"email exists or error: {e}")
    try:
        conn.execute(text("ALTER TABLE users ADD COLUMN reset_token VARCHAR;"))
        print("Added reset_token column")
    except Exception as e:
        print(f"reset_token exists or error: {e}")
    try:
        conn.execute(text("ALTER TABLE users ADD COLUMN reset_token_expiry TIMESTAMP;"))
        print("Added reset_token_expiry column")
    except Exception as e:
        print(f"reset_token_expiry exists or error: {e}")
