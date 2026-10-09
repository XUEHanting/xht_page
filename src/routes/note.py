from flask import Blueprint, jsonify, request

from src.models.note import normalize_note
from src.services.supabase_client import get_supabase
from src.services.translator import TranslationError, translate_note

try:
    from postgrest import APIError
except ImportError:  # pragma: no cover
    APIError = Exception  # type: ignore[misc, assignment]

note_bp = Blueprint('note', __name__)
NOTES_TABLE = 'notes'


def _db_error_response(exc: Exception, status: int = 500):
    return jsonify({'error': str(exc)}), status


@note_bp.route('/notes', methods=['GET'])
def get_notes():
    """Get all notes, ordered by most recently updated"""
    try:
        response = (
            get_supabase()
            .table(NOTES_TABLE)
            .select('*')
            .order('updated_at', desc=True)
            .execute()
        )
        return jsonify([normalize_note(row) for row in (response.data or [])])
    except RuntimeError as exc:
        return _db_error_response(exc, 500)
    except APIError as exc:
        return _db_error_response(exc, 502)
    except Exception as exc:
        return _db_error_response(exc, 500)


@note_bp.route('/notes', methods=['POST'])
def create_note():
    """Create a new note"""
    try:
        data = request.json
        if not data or 'title' not in data or 'content' not in data:
            return jsonify({'error': 'Title and content are required'}), 400

        response = (
            get_supabase()
            .table(NOTES_TABLE)
            .insert({
                'title': data['title'],
                'content': data['content'],
            })
            .execute()
        )
        if not response.data:
            return jsonify({'error': 'Failed to create note'}), 500
        return jsonify(normalize_note(response.data[0])), 201
    except RuntimeError as exc:
        return _db_error_response(exc, 500)
    except APIError as exc:
        return _db_error_response(exc, 502)
    except Exception as exc:
        return _db_error_response(exc, 500)


@note_bp.route('/notes/<int:note_id>', methods=['GET'])
def get_note(note_id):
    """Get a specific note by ID"""
    try:
        response = (
            get_supabase()
            .table(NOTES_TABLE)
            .select('*')
            .eq('id', note_id)
            .limit(1)
            .execute()
        )
        if not response.data:
            return jsonify({'error': 'Note not found'}), 404
        return jsonify(normalize_note(response.data[0]))
    except RuntimeError as exc:
        return _db_error_response(exc, 500)
    except APIError as exc:
        return _db_error_response(exc, 502)
    except Exception as exc:
        return _db_error_response(exc, 500)


@note_bp.route('/notes/<int:note_id>', methods=['PUT'])
def update_note(note_id):
    """Update a specific note"""
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        payload = {}
        if 'title' in data:
            payload['title'] = data['title']
        if 'content' in data:
            payload['content'] = data['content']

        if not payload:
            return jsonify({'error': 'No updatable fields provided'}), 400

        response = (
            get_supabase()
            .table(NOTES_TABLE)
            .update(payload)
            .eq('id', note_id)
            .execute()
        )
        if not response.data:
            return jsonify({'error': 'Note not found'}), 404
        return jsonify(normalize_note(response.data[0]))
    except RuntimeError as exc:
        return _db_error_response(exc, 500)
    except APIError as exc:
        return _db_error_response(exc, 502)
    except Exception as exc:
        return _db_error_response(exc, 500)


@note_bp.route('/notes/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    """Delete a specific note"""
    try:
        response = (
            get_supabase()
            .table(NOTES_TABLE)
            .delete()
            .eq('id', note_id)
            .execute()
        )
        if not response.data:
            return jsonify({'error': 'Note not found'}), 404
        return '', 204
    except RuntimeError as exc:
        return _db_error_response(exc, 500)
    except APIError as exc:
        return _db_error_response(exc, 502)
    except Exception as exc:
        return _db_error_response(exc, 500)


@note_bp.route('/notes/search', methods=['GET'])
def search_notes():
    """Search notes by title or content"""
    query = (request.args.get('q') or '').strip()
    if not query:
        return jsonify([])

    # PostgREST filter special chars
    safe_query = (
        query.replace(',', ' ')
        .replace('%', '')
        .replace('*', '')
        .replace('(', ' ')
        .replace(')', ' ')
        .strip()
    )
    if not safe_query:
        return jsonify([])

    pattern = f'*{safe_query}*'
    try:
        response = (
            get_supabase()
            .table(NOTES_TABLE)
            .select('*')
            .or_(f'title.ilike.{pattern},content.ilike.{pattern}')
            .order('updated_at', desc=True)
            .execute()
        )
        return jsonify([normalize_note(row) for row in (response.data or [])])
    except RuntimeError as exc:
        return _db_error_response(exc, 500)
    except APIError as exc:
        return _db_error_response(exc, 502)
    except Exception as exc:
        return _db_error_response(exc, 500)


@note_bp.route('/notes/translate', methods=['POST'])
def translate_note_content():
    """Translate note title and content to Chinese or English via OpenRouter"""
    data = request.json or {}
    title = data.get('title', '')
    content = data.get('content', '')
    target_lang = data.get('target_lang', '')

    if not isinstance(title, str):
        title = '' if title is None else str(title)
    if not isinstance(content, str):
        content = '' if content is None else str(content)

    if not title.strip() and not content.strip():
        return jsonify({'error': 'Title or content is required'}), 400

    if not target_lang:
        return jsonify({'error': 'target_lang is required (zh or en)'}), 400

    try:
        translated = translate_note(title, content, target_lang)
        return jsonify({
            'translated_title': translated['title'],
            'translated_content': translated['content'],
            'target_lang': target_lang,
        })
    except TranslationError as exc:
        message = str(exc)
        status = 400 if (
            'OPENROUTER_API_KEY' in message
            or 'Unsupported language' in message
            or 'required' in message.lower()
            or 'empty' in message.lower()
        ) else 502
        return jsonify({'error': message}), status
    except Exception as exc:
        return jsonify({'error': str(exc)}), 500
