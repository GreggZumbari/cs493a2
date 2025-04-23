'use strict';

window.addEventListener('load', function () {

    console.log("Hello World!");

});

function createBusiness() {
    const owner_id = document.getElementById("owner_id").value;
    const name = document.getElementById("name").value;
    const street_address = document.getElementById("street_address").value;
    const city = document.getElementById("city").value;
    const state = document.getElementById("state").value;
    const zip_code = document.getElementById("zip_code").value;

    fetch("/businesses", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(
            {
                "owner_id": owner_id,
                "name": name,
                "street_address": street_address,
                "city": city,
                "state": state,
                "zip_code": zip_code
            }
        ),
    })
        .then((response) => {
            console.log(response);
        })
        .catch((error) => {
            console.error("Error creating business. Code:", error);
        });
}

function fetchBusinessById(business_id) {
    fetch(`/businesses/${business_id}`, {
        method: "GET",
        headers: {
            "Content-Type": "application/json"
        }
    })
        .then((response) => {
            if (!response.ok) {
                console.error("Business not found or server error. Code:", error);
            }
            return response.json();
        })
        .then((data) => {
            console.log("Business data:", data);
        })
        .catch((error) => {
            console.error("Error fetching business. Code:", error);
        });
}

function fetchAllBusinesses() {
    fetch(`/businesses`, {
        method: "GET",
        headers: {
            "Content-Type": "application/json"
        }
    })
        .then((response) => {
            if (!response.ok) {
                console.error("Server error. Code:", error);
            }
            return response.json();
        })
        .then((data) => {
            console.log("Business data:", data);
        })
        .catch((error) => {
            console.error("Error fetching businesses. Code:", error);
        });
}

function editBusinessById() {
    const owner_id = document.getElementById("owner_id").value;
    const name = document.getElementById("name").value;
    const street_address = document.getElementById("street_address").value;
    const city = document.getElementById("city").value;
    const state = document.getElementById("state").value;
    const zip_code = document.getElementById("zip_code").value;
    
    fetch(`/businesses/${business_id}`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(
            {
                "id": business_id,
                "owner_id": owner_id,
                "name": name,
                "street_address": street_address,
                "city": city,
                "state": state,
                "zip_code": zip_code
            }
        ),
    })
        .then((response) => {
            if (!response.ok) {
                console.error("Business not found or server error. Code:", error);
            }
            return response.json();
        })
        .catch((error) => {
            console.error("Error fetching or editing business. Code:", error);
        });
}

function deleteBusinessById() {
    fetch(`/businesses/${business_id}`, {
        method: "DELETE",
        headers: {
            "Content-Type": "application/json"
        }
    })
        .then((response) => {
            if (!response.ok) {
                console.error("Business not found or server error. Code:", error);
            }
            return response.json();
        })
        .catch((error) => {
            console.error("Error fetching or deleting business. Code:", error);
        });
}

function fetchBusinessByOwner() {
    fetch(`/owners/${owner_id}/businesses`, {
        method: "GET",
        headers: {
            "Content-Type": "application/json"
        }
    })
        .then((response) => {
            if (!response.ok) {
                console.error("Owner not found or server error. Code:", error);
            }
            return response.json();
        })
        .then((data) => {
            console.log("Owner's business data:", data);
        })
        .catch((error) => {
            console.error("Error fetching owner's businesses. Code:", error);
        });
}

function createReview() {
    const user_id = document.getElementById("user_id").value;
    const business_id = document.getElementById("business_id").value;
    const stars = document.getElementById("stars").value;
    const review_text = document.getElementById("review_text").value;

    fetch("/reviews", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(
            {
                "user_id": user_id,
                "business_id": business_id,
                "stars": stars,
                "review_text": review_text
            }
        ),
    })
        .then((response) => {
            console.log(response);
        })
        .catch((error) => {
            console.error("Error creating review. Code:", error);
        });
}

function fetchReviewById(review_id) {
    fetch(`/businesses/${review_id}`, {
        method: "GET",
        headers: {
            "Content-Type": "application/json"
        }
    })
        .then((response) => {
            if (!response.ok) {
                console.error("Review not found or server error. Code:", error);
            }
            return response.json();
        })
        .then((data) => {
            console.log("Review data:", data);
        })
        .catch((error) => {
            console.error("Error fetching review. Code:", error);
        });
}

function editReviewById() {
    const user_id = document.getElementById("user_id").value;
    const business_id = document.getElementById("business_id").value;
    const stars = document.getElementById("stars").value;
    const review_text = document.getElementById("review_text").value;

    fetch(`/reviews/${reviews_id}`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(
            {
                "user_id": user_id,
                "business_id": business_id,
                "stars": stars,
                "review_text": review_text
            }
        ),
    })
        .then((response) => {
            if (!response.ok) {
                console.error("Review not found or server error. Code:", error);
            }
            return response.json();
        })
        .catch((error) => {
            console.error("Error fetching or editing review. Code:", error);
        });
}

function deleteReviewById() {
    fetch(`/reviews/${reviews_id}`, {
        method: "DELETE",
        headers: {
            "Content-Type": "application/json"
        }
    })
        .then((response) => {
            if (!response.ok) {
                console.error("Review not found or server error. Code:", error);
            }
            return response.json();
        })
        .catch((error) => {
            console.error("Error fetching or deleting review. Code:", error);
        });
}

function fetchReviewsByUser() {
    fetch(`/users/${user_id}/reviews`, {
        method: "GET",
        headers: {
            "Content-Type": "application/json"
        }
    })
        .then((response) => {
            if (!response.ok) {
                console.error("User not found or server error. Code:", error);
            }
            return response.json();
        })
        .then((data) => {
            console.log("User's review data:", data);
        })
        .catch((error) => {
            console.error("Error fetching user's reviews. Code:", error);
        });
}