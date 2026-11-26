import logging
import os
from typing import Any, Dict, List, Optional

from supabase import Client, create_client

logger = logging.getLogger(__name__)

_supabase_client: Optional[Client] = None


def get_supabase_client() -> Optional[Client]:
    """Return a cached Supabase client if SUPABASE_URL and key are configured."""
    global _supabase_client
    if _supabase_client is not None:
        return _supabase_client

    url = os.getenv("SUPABASE_URL", "").strip()
    key = (
        os.getenv("SUPABASE_SERVICE_ROLE_KEY", "").strip()
        or os.getenv("SUPABASE_KEY", "").strip()
    )

    if not url or not key:
        return None

    _supabase_client = create_client(url, key)
    return _supabase_client


def save_report(
    user_id: str,
    filename: str,
    report_type: str,
    language: str,
    ocr_source: str,
    analysis: Dict[str, Any],
) -> Optional[Dict[str, Any]]:
    """Persist a processed medical report to Supabase. Returns the inserted row or None."""
    client = get_supabase_client()
    if client is None or not user_id:
        return None

    payload = {
        "user_id": user_id,
        "filename": filename,
        "report_type": report_type,
        "language": language,
        "ocr_source": ocr_source,
        "analysis": analysis,
    }
    response = client.table("reports").insert(payload).execute()
    if response.data:
        return response.data[0]
    return None


def get_user_reports(user_id: str, limit: int = 20) -> List[Dict[str, Any]]:
    """Fetch recent reports for a Clerk user, ordered newest first."""
    client = get_supabase_client()
    if client is None or not user_id:
        return []

    response = (
        client.table("reports")
        .select("id, filename, report_type, language, ocr_source, analysis, created_at")
        .eq("user_id", user_id)
        .order("created_at", desc=True)
        .limit(limit)
        .execute()
    )
    return response.data or []


def get_report_by_id(user_id: str, report_id: str) -> Optional[Dict[str, Any]]:
    """Fetch a single report owned by user_id."""
    client = get_supabase_client()
    if client is None or not user_id:
        return None

    response = (
        client.table("reports")
        .select("id, filename, report_type, language, ocr_source, analysis, created_at")
        .eq("id", report_id)
        .eq("user_id", user_id)
        .limit(1)
        .execute()
    )
    if response.data:
        return response.data[0]
    return None


def delete_report(user_id: str, report_id: str) -> bool:
    """Delete a report owned by user_id. Returns True if a row was deleted."""
    client = get_supabase_client()
    if client is None or not user_id:
        return False

    response = (
        client.table("reports")
        .delete()
        .eq("id", report_id)
        .eq("user_id", user_id)
        .execute()
    )
    return bool(response.data)
