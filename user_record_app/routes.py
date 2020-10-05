"""Application routes."""
import json

from flask import request, Response
from flask import current_app as app

from .models import db, User
from .display_format_factory import DisplayFormatFactory
from .serializer_factory import SerializerFactory

@app.route("/")
def home_page():
    """
    This route is responsible for displaying the home page.
    """
    return "Welcome to the User Record API"

@app.route('/api/v1/users/create_user', methods=['POST'])
def create_user():
    """
    This route is responsible for adding a user record. It can currently only
    take a json containing key, value pairs based on the attributes of the User
    model.
    Ex.
    {
        "city": "city",
        "first_name": "first_name",
        "last_name": "last_name",
        "phone_number": "phone_number",
        "province": "province",
        "street": "street"
    }
    """
    user_record = request.get_json(force=True)

    add_user_to_db(user_record)

    return "Successfully added user.", 200

def add_user_to_db(dict):
    """
    This function is responsible for adding a given dictionary to the database.
    """
    new_user = User(
        city=dict.get("city"),
        first_name=dict.get("first_name"),
        last_name=dict.get("last_name"),
        phone_number=dict.get("phone_number"),
        province=dict.get("province"),
        street=dict.get("street")
    )
    # Add new User record to database and commit changes
    db.session.add(new_user)
    db.session.commit()

@app.route("/api/v1/users/all/<display>")
def display_all(display):
    """
    This route is responsible for displaying all user records in a given display
    format. The current possible display parameter values are "html" and "text".
    """
    user_list = db.session.query(User).all()
    user_dict = convert_result_to_dict(user_list)

    display_factory = DisplayFormatFactory()
    try:
        display_format = display_factory.get_display(display.upper())
    except ValueError:
        return "Invalid display format: {}".format(str(display)), 500

    display_format.dict = user_dict

    return display_format.display()

@app.route("/api/v1/users/filter/<display>", methods=["GET"])
def filter_users(display):
    """
    This route is responsible for filtering out user records given request
    arguments that match the attributes of our User model. The filter value can
    contain a wildcard character, which is the following character: %
    It can also display the results in different display formats. The current
    possible display parameter values are "html" and "text".
    """
    valid_field_list = get_valid_field_list()

    query = db.session.query(User)

    for field in valid_field_list:
        value = request.args.get(field)
        if value is None:
            continue
        attr = getattr(User, field)
        query = query.filter(attr.like(value))

    result_dict = convert_result_to_dict(query.all())

    display_factory = DisplayFormatFactory()
    try:
        display_format = display_factory.get_display(display.upper())
    except ValueError:
        return "Invalid display format: {}".format(str(display)), 500

    display_format.dict = result_dict

    return display_format.display()

def get_valid_field_list():
    """
    Simply returns a list of the valid attributes of our User model.
    """
    valid_field_list = [
        "city",
        "first_name",
        "last_name",
        "phone_number",
        "province",
        "street"
    ]

    return valid_field_list

@app.route("/api/v1/users/all/serialize/<format>")
def serialize_data(format):
    """
    This route is responsible for serializing all the user records data to a
    specified output format. The current formats are json and yaml.
    """
    user_list = db.session.query(User).all()
    user_dict = convert_result_to_dict(user_list)

    try:
        serialized_data = serialize_data(format, user_dict)
    except ValueError:
        return "Invalid output format: {}".format(str(format)), 500

    response = Response(
        serialized_data,
        mimetype="application/json",
        headers={
            "Content-Disposition":"attachment;filename=users.{}".format(format)
        }
    )

    return response

def convert_result_to_dict(user_list):
    """
    Simply converts the database query results into a dictionary.
    """
    user_dict = {}
    for user in user_list:
       user_dict.update(user.as_dict())

    return user_dict

def serialize_data(format, data_dict):
    """
    This function is responsible for serializing data to specified output
    format.
    """
    serializer_factory = SerializerFactory()
    serializer = serializer_factory.get_serializer(format.upper())
    serializer.dict = data_dict
    serialized_data = serializer.serialize()

    return serialized_data
