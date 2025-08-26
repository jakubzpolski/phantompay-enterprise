from fastapi import APIRouter
from app.db.session import engine

router = APIRouter(prefix="/api", tags=["health"])

@router.get("/health")
def health():
    # simple DB check: try get a connection
    try:
        with engine.connect() as conn:
            conn.exec_driver_sql("SELECT 1")
        db = "ok"
    except Exception as e:
        db = f"error: {e}"
    return {"status": "ok", "db": db}
