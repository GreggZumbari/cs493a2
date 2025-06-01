# **REST API Implementation with GAE and Cloud Datastore**

This website is a REST API that uses Google Cloud and a Firestore Database with Datastore compatibility.

Here is a list of every type of request you can send, and where you can send them.
For more specific information about the functionality, see `docs/assignment2-api-doc.pdf`.

> POST /businesses
> 
> Request Body Example:
> {
>  "owner_id": 123,
>  "name": "Mandola's",
>  "street_address": "4900 N Lamar Blvd",
>  "city": "Austin",
>  "state": "TX",
>  "zip_code": 78751
> }

> POST /reviews
> 
> Request Body Example:
> {
>  "user_id": 12134,
>  "business_id": 156789,
>  "stars": 4,
>  "review_text": "Mandola’s has great pasta"
> }

> GET /businesses/:business_id
> 
> Request Body Example:
> none

> GET /businesses
> 
> Request Body Example:
> none

> GET /owners/:owner_id/businesses
> 
> Request Body Example:
> none

> GET /reviews/:review_id
> 
> Request Body Example:
> none

> GET /users/:user_id/reviews
> 
> Request Body Example:
> none

> PUT /businesses/:business_id
> 
> Request Body Example:
> {
>  "owner_id": 123,
>  "name": "Mandola's",
>  "street_address": "4900 N Lamar Blvd",
>  "city": "Austin",
>  "state": "TX",
>  "zip_code": 78751
> }

> PUT /reviews/:review_id
> 
> Request Body Example:
> {
>  "stars": 4,
>  "review_text": "Mandola’s has great pasta. Mista salad is great too!"
> }

> DELETE /businesses/:business_id
> 
> Request Body Example:
> none

> DELETE /reviews/:review_id
> 
> Request Body Example:
> none