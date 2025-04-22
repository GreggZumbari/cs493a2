import datetime

from flask import Flask, render_template, request, jsonify
from google.cloud import datastore

app = Flask(__name__)
datastore_client = datastore.Client()

@app.route("/businesses", methods=["POST"])
def create_business():
    # Get data
    data = request.get_json()
    owner_id = data.get("owner_id")
    name = data.get("name")
    street_address = data.get("street_address")
    city = data.get("city")
    state = data.get("state")
    zip_code = data.get("zip_code")

    # If all fields are there, return 201 Created, otherwise 400 Bad Request
    if data and owner_id and name and street_address and city and state and zip_code:
        store_business(owner_id, name, street_address, city, state, zip_code)
        return jsonify({"status": "success"}), 201
    return (
        jsonify({
            "Error": "The request body is missing at least one of the required attributes"
        }),
        400,
        {"Content-Type": "application/json"}
    )

def store_business(owner_id, name, street_address, city, state, zip_code):
    entity = datastore.Entity(key=datastore_client.key("owner_id"))
    entity.update({
        "owner_id": owner_id,
        "name": name,
        "street_address": street_address,
        "city": city,
        "state": state,
        "zip_code": zip_code
    })

    datastore_client.put(entity)

def store_time(dt):
    entity = datastore.Entity(key=datastore_client.key("visit"))
    entity.update({"timestamp": dt})

    datastore_client.put(entity)


def fetch_times(limit):
    query = datastore_client.query(kind="visit")
    query.order = ["-timestamp"]

    times = query.fetch(limit=limit)

    return times


def fetch_names(limit):
    query = datastore_client.query(kind="name")
    query.order = ["-timestamp"]

    names = query.fetch(limit=limit)

    return names


@app.route("/")
def root():
    # Store the current access time in Datastore.
    store_time(datetime.datetime.now(tz=datetime.timezone.utc))

    # Fetch the most recent 10 access times and names from Datastore.
    times = fetch_times(10)
    names = fetch_names(10)

    return render_template("index.html", times=times, names=names)

if __name__ == "__main__":
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host="127.0.0.1", port=8080, debug=True)