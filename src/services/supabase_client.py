import os

from supabase import Client, create_client

_client: Client | None = None


def get_supabase() -> Client:
    """Return a shared Supabase client configured from environment variables."""
    global _client
    if _client is not None:
        return _client

    url = (os.getenv('SUPABASE_URL') or '').strip()
    key = (
        (os.getenv('SUPABASE_SERVICE_ROLE_KEY') or '').strip()
        or (os.getenv('SUPABASE_KEY') or '').strip()
    )

    if not url or not key:
        raise RuntimeError(
            'Supabase is not configured. Set SUPABASE_URL and '
            'SUPABASE_SERVICE_ROLE_KEY (or SUPABASE_KEY) in your .env file.'
        )

    if 'your-project' in url or key.startswith('your_'):
        raise RuntimeError(
            'Replace the placeholder Supabase credentials in your .env file.'
        )

    _client = create_client(url, key)
    return _client
