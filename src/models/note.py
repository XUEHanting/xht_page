"""Helpers for normalizing note records returned by Supabase."""


def normalize_note(row: dict) -> dict:
    """Normalize a Supabase note row into the API response shape."""
    if not row:
        return {}

    return {
        'id': row.get('id'),
        'title': row.get('title') or '',
        'content': row.get('content') or '',
        'created_at': row.get('created_at'),
        'updated_at': row.get('updated_at'),
    }
