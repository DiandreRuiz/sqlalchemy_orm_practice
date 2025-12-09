from .schemas import member_schema, members_schema
from . import members_bp
from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from app.models import Member, db
from typing import Dict

# Get all Members
@members_bp.route("/", methods=['GET'])
def get_members():
    query = select(Member)
    # Returns a tuple, where:
    # - 1st item is a Member object based on Member's class definition
    # - All other items represent the values of respective columns for that row
    # Scalars() returns the first item in the tuple which would be the Member object
    members = db.session.execute(query).scalars().all()
    
    return members_schema.jsonify(members)

# Get a specific member based on his / her member_id
@members_bp.route("/<int:member_id>", methods=['GET'])
def get_member(member_id):
    member = db.session.get(Member, member_id)
    if not member:
        return jsonify({"error": f"Member w/ id: {member_id} not found"}), 404
    else:
        return member_schema.jsonify(member), 200
    
@members_bp.route("/", methods=['POST'])
def create_member():
    
    # We explicityly check if the json body is present since Flask's
    # stubs type request.json as Any | None which is incompatible 
    # with member_schema.load(). We will follow this design pattern for
    # all routes.
    
    # Validation
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Invalid or missing JSON body"}), 400
    
    try:
        member_data = member_schema.load(data)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    query = select(Member).where(Member.email == member_data['email']) # Checking our db for a member with this email
    existing_member = db.session.execute(query).scalars().all()
    if existing_member:
        return jsonify({"error": "Email already associated with an account"}), 400
    
    # Creation of Member row
    new_member = Member(**member_data)
    db.session.add(new_member)
    db.session.commit()
    return member_schema.jsonify(new_member), 201

# Update a specific member based on his / her member_id
@members_bp.route("/<int:member_id>", methods=["PUT"])
def update_member(member_id):
    # Validation
    member = db.session.get(Member, member_id)
    if not member:
        return jsonify({"error": f"No member found with id: {member_id}"}), 404
    
    data = request.get_json()
    if data is None: 
        return jsonify({"error": "Invalid or missing JSON body"}), 400
    
    # Attempt de-serialization w/ Marshmallow
    try:
        member_data: Dict = member_schema.load(data)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    # Update member object to have all supplied attributes from request body
    for k,v in member_data.items():
        setattr(member, k, v)
        
    db.session.commit() # commit member object based on it's new state
    
    return member_schema.jsonify(member), 200

@members_bp.route("/most-active", methods=["GET"])
def get_most_active():
    query = select(Member)
    members = db.session.execute(query).scalars().all()
    
    for member in members:
        print(member.email, len(member.loans))
    


# Delete a member based his / her id
@members_bp.route("/<int:member_id>", methods=['DELETE'])
def delete_member(member_id):
    member = db.session.get(Member, member_id)
    if not member:
        return jsonify({"error": f"No member with id: {member_id} found"}), 404
    else:
        db.session.delete(member)
        db.session.commit()
    return jsonify({"message": f"Member with id: {member_id} succesfully deleted!"}), 200
    