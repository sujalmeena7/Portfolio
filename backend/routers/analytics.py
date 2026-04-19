from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Request, Depends
from typing import Dict, List

from core.database import db
from core.security import require_admin
from models.schemas import (
    AnalyticsEvent, AnalyticsEventInput, AnalyticsSummary,
)

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.post("/event", response_model=AnalyticsEvent, status_code=201)
async def track_event(body: AnalyticsEventInput, request: Request):
    ua = request.headers.get("user-agent")
    doc = AnalyticsEvent(**body.model_dump(), ua=ua).model_dump()
    await db.analytics_events.insert_one(doc)
    doc.pop("_id", None)
    return doc


@router.get("", response_model=AnalyticsSummary)
async def summary(_: dict = Depends(require_admin)):
    total = await db.analytics_events.count_documents({})

    by_type: Dict[str, int] = {}
    pipeline = [{"$group": {"_id": "$type", "n": {"$sum": 1}}}]
    async for row in db.analytics_events.aggregate(pipeline):
        by_type[row["_id"] or "unknown"] = row["n"]

    # Last 7 days bucketed by YYYY-MM-DD
    start = datetime.now(timezone.utc) - timedelta(days=7)
    last_7: Dict[str, int] = {}
    cursor = db.analytics_events.find(
        {"created_at": {"$gte": start}}, {"created_at": 1, "_id": 0}
    )
    async for row in cursor:
        d = row["created_at"].strftime("%Y-%m-%d")
        last_7[d] = last_7.get(d, 0) + 1

    recent: List[dict] = await (
        db.analytics_events.find({}, {"_id": 0})
        .sort("created_at", -1)
        .limit(25)
        .to_list(25)
    )

    return AnalyticsSummary(
        total_events=total,
        by_type=by_type,
        last_7_days=last_7,
        recent=[AnalyticsEvent(**r) for r in recent],
    )
