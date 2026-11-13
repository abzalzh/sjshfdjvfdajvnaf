from fastapi import APIRouter
from sqlalchemy import text

from app.deps import SessionDep
from app.routers.messages import get_room_or_404
from app.schemas import SearchHit

router = APIRouter(prefix="/rooms/{room_id}/search", tags=["search"])


@router.get("", response_model=list[SearchHit])
def search(room_id: int, q: str, session: SessionDep):
    # A teammate wrote this "fast search" in raw SQL. It works for normal words. Try it with  ' OR 1=1 --
    # TODO M1 (deck slides 5 to 9): no f-string in the SQL. Put :room_id and :pattern in the text,
    # and pass the values as a dict: session.execute(sql, {...})
    get_room_or_404(session, room_id)
    sql = text(
        "SELECT id, text FROM messages "
        f"WHERE room_id = {room_id} AND text LIKE '%{q}%' "
        "ORDER BY id"
    )
    rows = session.execute(sql)
    return [{"id": row.id, "text": row.text} for row in rows]
