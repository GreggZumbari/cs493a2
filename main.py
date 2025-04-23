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
        id = store_business(owner_id, name, street_address, city, state, zip_code)
        # 201 Created
        return (
            jsonify({
                "id": id,
                "owner_id": owner_id,
                "name": name,
                "street_address": street_address,
                "city": city,
                "state": state,
                "zip_code": zip_code
            }),
            201,
            {"Content-Type": "application/json"}
        )
    # 400 Bad Request
    return (
        jsonify({
            "Error": "The request body is missing at least one of the required attributes"
        }),
        400,
        {"Content-Type": "application/json"}
    )

def store_business(owner_id, name, street_address, city, state, zip_code):
    entity = datastore.Entity(key=datastore_client.key("Businesses"))
    entity.update({
        "owner_id": owner_id,
        "name": name,
        "street_address": street_address,
        "city": city,
        "state": state,
        "zip_code": zip_code
    })
    datastore_client.put(entity)

    return entity.key.id

@app.route("/businesses/<int:business_id>", methods=["GET"])
def fetch_business_by_id(business_id):
    # Fetch business
    key = datastore_client.key("Businesses", business_id)
    business = datastore_client.get(key)

    if business is not None:
        # Add the id because it doesn't come with it by default
        business_with_id = dict(business)
        business_with_id["id"] = business_id

        # 200 OK
        return (
            jsonify(business_with_id),
            200,
            {"Content-Type": "application/json"}
        )
    # 404 Not Found
    return (
        jsonify({
            "Error": "No business with this business_id exists"
        }),
        404,
        {"Content-Type": "application/json"}
    )

@app.route("/businesses", methods=["GET"])
def fetch_all_businesses():
    # Fetch the businesses as an iterator
    query = datastore_client.query(kind="Businesses")
    data = query.fetch()

    # Add id to each one
    businesses = []
    for business in data:
        business_with_id = dict(business)
        business_with_id["id"] = business.key.id
        businesses.append(business_with_id)
    
    # 200 OK
    return (
        jsonify(businesses),
        200,
        {"Content-Type": "application/json"}
    )

@app.route("/businesses/<int:business_id>", methods=["PUT"])
def edit_business_by_id(business_id):
    # Fetch the already existing business
    key = datastore_client.key("Businesses", business_id)
    business = datastore_client.get(key)

    if business is None:
        # 404 Not Found
        return jsonify({"Error": "No business with this business_id exists"}), 404
    
    # Get data from request to update the business with
    data = request.get_json()
    owner_id = data.get("owner_id")
    name = data.get("name")
    street_address = data.get("street_address")
    city = data.get("city")
    state = data.get("state")
    zip_code = data.get("zip_code")

    # If all fields are there edit the business & return 200 OK, otherwise 400 Bad Request
    if data and owner_id and name and street_address and city and state and zip_code:
        # Update business in-place
        business["owner_id"] = owner_id
        business["name"] = name
        business["street_address"] = street_address
        business["city"] = city
        business["state"] = state
        business["zip_code"] = zip_code

        # Save the updated business to datastore
        datastore_client.put(business)
        
        # 200 OK
        return (
            jsonify({
                "id": business_id,
                "owner_id": owner_id,
                "name": name,
                "street_address": street_address,
                "city": city,
                "state": state,
                "zip_code": zip_code
            }),
            200,
            {"Content-Type": "application/json"}
        )
    # 400 Bad Request
    return (
        jsonify({
            "Error": "The request body is missing at least one of the required attributes"
        }),
        400,
        {"Content-Type": "application/json"}
    )

@app.route("/businesses/<int:business_id>", methods=["DELETE"])
def delete_business_by_id(business_id):
    # Fetch the already existing business
    key = datastore_client.key("Businesses", business_id)
    business = datastore_client.get(key)

    if business is None:
        # 404 Not Found
        return jsonify({"Error": "No business with this business_id exists"}), 404
    
    # Delete the business by its key
    datastore_client.delete(key)

    # 204 No Content
    return "", 204

@app.route("/owners/<int:owner_id>/businesses", methods=["GET"])
def fetch_business_by_owner(owner_id):
    # Fetch businesses owned by the owner with owner_id
    # SQL Equivalent: SELECT * FROM Businesses WHERE owner_id=owner_id
    query = datastore_client.query(kind="Businesses")
    query.add_filter("owner_id", "=", owner_id)
    data = query.fetch()

    # Add id to each one
    businesses = []
    for business in data:
        business_with_id = dict(business)
        business_with_id["id"] = business.key.id
        businesses.append(business_with_id)

    # 200 OK
    return (
        jsonify(businesses),
        200,
        {"Content-Type": "application/json"}
    )

@app.route("/reviews", methods=["POST"])
def create_review():
    # Get data
    data = request.get_json()
    user_id = data.get("user_id")
    business_id = data.get("business_id")
    stars = data.get("stars")

    if data and user_id and business_id and stars:
        # Make sure the business being reviewed exists
        # SQL Equivalent: SELECT * FROM Businesses WHERE id=business_id
        business_key = datastore_client.key("Businesses", int(business_id))
        business = datastore_client.get(business_key)

        if business is None:
            # 404 Not Found
            return (
                jsonify({
                    "Error": "No business with this business_id exists"
                }),
                404,
                {"Content-Type": "application/json"}
            )
        
        # Make sure there aren't already any reviews with same user_id & business_id
        # SQL Equivalent: SELECT * FROM Reviews WHERE user_id=user_id AND business_id=business_id
        conflict_query = datastore_client.query(kind="Reviews")
        conflict_query.add_filter("business_id", "=", business_id)
        conflict_query.add_filter("user_id", "=", user_id)
        conflict_data = conflict_query.fetch()

        if list(conflict_data):
            # 409 Conflict
            return (
                jsonify({
                    "Error": "You have already submitted a review for this business. You can update your previous review, or delete it and submit a new review"
                }),
                409,
                {"Content-Type": "application/json"}
            )
        
        # Create the review in datastore
        id = store_review(data)

        # Add the id because it doesn't come with it by default
        review_with_id = dict(data)
        review_with_id["id"] = id

        # 201 Created
        return (
            jsonify(review_with_id),
            201,
            {"Content-Type": "application/json"}
        )
    # 400 Bad Request
    return (
        jsonify({
            "Error": "The request body is missing at least one of the required attributes"
        }),
        400,
        {"Content-Type": "application/json"}
    )

def store_review(data):
    entity = datastore.Entity(key=datastore_client.key("Reviews"))
    entity.update(data)
    datastore_client.put(entity)

    return entity.key.id

@app.route("/reviews/<int:review_id>", methods=["GET"])
def fetch_review_by_id(review_id):
    # Fetch review
    key = datastore_client.key("Reviews", review_id)
    review = datastore_client.get(key)

    if review is not None:
        # Add the id because it doesn't come with it by default
        review_with_id = dict(review)
        review_with_id["id"] = review_id

        # 200 OK
        return (
            jsonify(review_with_id),
            200,
            {"Content-Type": "application/json"}
        )
    # 404 Not Found
    return (
        jsonify({
            "Error": "No review with this review_id exists"
        }),
        404,
        {"Content-Type": "application/json"}
    )

@app.route("/reviews/<int:review_id>", methods=["PUT"])
def edit_review_by_id(review_id):
    # Fetch the already existing review
    key = datastore_client.key("Reviews", review_id)
    review = datastore_client.get(key)

    if review is None:
        # 404 Not Found
        return jsonify({"Error": "No review with this review_id exists"}), 404
    
    # Get data from request to update the review with
    data = request.get_json()
    user_id = data.get("user_id")
    business_id = data.get("business_id")
    stars = data.get("stars")
    review_text = data.get("review_text")

    # If all required fields are there...
    if data and stars:
        # Update review in-place
        review["stars"] = stars
        if user_id:
            review["user_id"] = user_id
        if business_id:
            review["business_id"] = business_id
        if review_text:
            review["review_text"] = review_text

        # Save the updated review to datastore
        datastore_client.put(review)
        
        # 200 OK
        return (
            review,
            200,
            {"Content-Type": "application/json"}
        )
    # 400 Bad Request
    return (
        jsonify({
            "Error": "The request body is missing at least one of the required attributes"
        }),
        400,
        {"Content-Type": "application/json"}
    )

@app.route("/reviews/<int:review_id>", methods=["DELETE"])
def delete_review_by_id(review_id):
    # Fetch the already existing review
    key = datastore_client.key("Reviews", review_id)
    review = datastore_client.get(key)

    if review is None:
        # 404 Not Found
        return jsonify({"Error": "No review with this review_id exists"}), 404
    
    # Delete the review by its key
    datastore_client.delete(key)

    # 204 No Content
    return "", 204

@app.route("/users/<int:user_id>/reviews", methods=["GET"])
def fetch_reviews_by_user(user_id):
    # Fetch reviews owned by the user with user_id
    # SQL Equivalent: SELECT * FROM Reviews WHERE user_id=user_id
    query = datastore_client.query(kind="Reviews")
    query.add_filter("user_id", "=", user_id)
    data = query.fetch()

    # Add id to each one
    reviews = []
    for review in data:
        review_with_id = dict(review)
        review_with_id["id"] = review.key.id
        reviews.append(review_with_id)

    # 200 OK
    return (
        jsonify(reviews),
        200,
        {"Content-Type": "application/json"}
    )

@app.route("/")
def root():
    return render_template("index.html", time=datetime.datetime.now(tz=datetime.timezone.utc))

if __name__ == "__main__":
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host="127.0.0.1", port=8080, debug=True)