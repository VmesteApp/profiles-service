from typing import List, Optional

from fastapi import APIRouter, Depends, Request, Query
from app.db.session import get_db
from sqlalchemy import select, not_
from sqlalchemy.orm import Session

from app.models.models import pulse, images, pulse_tags, pulse_members
from app.models.models import tag as tag_table


router = APIRouter()


@router.get("/feed")
def get_feed(request: Request, skip: Optional[int] = 0, limit: Optional[int] = 100,
             tag: Optional[List[int]] = Query(None), name: Optional[str] = None,
             session: Session = Depends(get_db)):

    pulse_members_subquery = (select(pulse_members.c.pulse_id)
                                .where(pulse_members.c.user_id == request.state.uid))

    query = (select(pulse).where(not_(pulse.c.founder_id == request.state.uid),
                                 not_(pulse.c.id.in_(pulse_members_subquery)),
                                 pulse.c.blocked.isnot(True)).offset(skip).limit(limit))

    result = session.execute(query).all()

    tags = session.query(pulse_tags.c.pulse_id, tag_table.c.name, tag_table.c.id).join(tag_table, tag_table.c.id == pulse_tags.c.tag_id).all()

    return [{"id": res.id,
            "category": res.category,
            "name": res.name,
            "founder_id": res.founder_id,
            "description": res.description,
            "short_description": res.short_description,
            "images": [j[3] for j in session.query(images).where(images.c.pulse_id == res.id).all()],
            "tags": [{"id": j[2], "name": j[1]} for j in tags if j.pulse_id == res.id]
            } for res in result]
