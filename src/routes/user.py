from flask import Blueprint, jsonify

user_bp = Blueprint('user', __name__)


@user_bp.route('/users', methods=['GET'])
def get_users():
    return jsonify({'error': 'User API is not implemented. Notes use Supabase directly.'}), 501


@user_bp.route('/users', methods=['POST'])
def create_user():
    return jsonify({'error': 'User API is not implemented.'}), 501


@user_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    return jsonify({'error': 'User API is not implemented.'}), 501


@user_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    return jsonify({'error': 'User API is not implemented.'}), 501


@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    return jsonify({'error': 'User API is not implemented.'}), 501
