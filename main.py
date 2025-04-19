import datetime

from flask import Flask, render_template, request, jsonify
from google.cloud import datastore

app = Flask(__name__)
datastore_client = datastore.Client()

@app.route("/submit_name", methods=["POST"])
def submit_name():
    data = request.get_json()
    name = data.get("name")
    if name:
        store_name(name, datetime.datetime.now(tz=datetime.timezone.utc))
        return jsonify({"status": "success"}), 200
    return jsonify({"status": "error", "message": "No name provided"}), 400

def store_time(dt):
    entity = datastore.Entity(key=datastore_client.key("visit"))
    entity.update({"timestamp": dt})

    datastore_client.put(entity)


def fetch_times(limit):
    query = datastore_client.query(kind="visit")
    query.order = ["-timestamp"]

    times = query.fetch(limit=limit)

    return times

def store_name(name, dt):
    entity = datastore.Entity(key=datastore_client.key("name"))
    entity.update({
        "name": name,
        "timestamp": dt
    })

    datastore_client.put(entity)


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