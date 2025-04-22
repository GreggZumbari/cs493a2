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
            console.error("Error submitting name. Code: ", error);
        });
}