# routes/contact_routes.py

from flask import Blueprint, request, jsonify
from services import contact_service

contact_routes = Blueprint("contact_routes", __name__)

@contact_routes.route("/uploadfile", methods=["POST"])
def upload_file():
    return contact_service.extract_table(request)

@contact_routes.route("/contact", methods=["GET"])
def get_contacts():
    return contact_service.get_all_contacts()

@contact_routes.route("/contact/<int:id>", methods=["GET"])
def get_contact_by_id(id):
    return contact_service.get_contact_by_id(id)
