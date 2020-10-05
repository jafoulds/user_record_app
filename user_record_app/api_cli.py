import click
import requests

BASE_URL = "http://127.0.0.1:5000"

@click.group()
def main():
    pass

@main.command()
@click.option(
    "-o",
    "--output_format",
    help="Name of the output you want to serialize the data in (ex. json)"
)
def serialize(output_format : str):
    """
    Outputs all users currently in the database to a specified output format.
    """
    response = requests.get(
        url="{}/api/v1/users/serialize/{}".format(
            BASE_URL,
            output_format
        )
    )
    print_server_response(response)

@main.command()
@click.option(
    "-d",
    "--display_format",
    help="Name of the format you want to display the data in. Currently supports html or text"
)
def display_all(display_format : str):
    """
    Displays all users currently in a desired display format.
    """
    response = requests.get(
        url="{}/api/v1/users/all/{}".format(
            BASE_URL,
            display_format
        )
    )
    print_server_response(response)

@main.command()
@click.option("-c", "--city", help="City of user you want to add (ex. Bowser) ")
@click.option("-f", "--first_name", help="First name of user you want to add (ex. Jack)")
@click.option("-l", "--last_name", help="Last name of user you want to add (Ex. Johnson)")
@click.option("-p", "--phone_number", help="Phone number of user you want to add (ex. 6046049999)")
@click.option("-r", "--province", help="Province of user you want to add (ex. BC)")
@click.option("-s", "--street", help="Street of user you want to add (ex. 123 Fake St.)")
def create_user(city : str, first_name : str, last_name : str, province : str, street : str , phone_number : str):
    """
    Creates a user record that contains the specified fields.
    """
    user_dict = {
        "city": city,
        "first_name": first_name,
        "last_name": last_name,
        "phone_number": phone_number,
        "province": province,
        "street": street
    }
    response = requests.post("{}/api/v1/users/create_user".format(BASE_URL), json=user_dict)
    print_server_response(response)

@main.command()
@click.option("-d", "--display_format", help="Name of the format you want to display the data in. Currently supports html or text")
@click.option("-f", "--filters", nargs=2, multiple=True, type=click.Tuple([str, str]))
def filter_user(display_format, filters):
    """
    Filters out user records by providing a tuple of arguments in the
    (field, filter) format. This will filter out user records that contain
    fields that match on the filter. Wildcards can be added to the filter and
    are represented by the following character: %

    ex.
    python apis_cli.py filter-user -d html --filters first_name Ja% --filters province BC
    """
    query_string = create_query_string(filters)
    url = "{}/api/v1/users/filter/{}{}".format(
        BASE_URL,
        display_format,
        query_string
    )
    response = requests.get(url=url)
    print_server_response(response)

def print_server_response(response):

    print("Response from server:\n", response.text)

def create_query_string(tuple_tuple):
    """
    Helper function to convert the (field, filter) tuple to a string that is
    used in the URL.
    """
    query_string = ""
    for tuple in tuple_tuple:
        query_string += "?{}&".format("=".join(tuple))

    # remove trailing & from string
    return query_string[:-1]


if __name__ == "__main__":
    main()

# Example command:
# python api_cli.py create-user --city TestCity --first_name FName --last_name LName --phone_number 6046049999 --province BC --street "123 Fake St"
