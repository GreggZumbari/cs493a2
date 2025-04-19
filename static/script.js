'use strict';

window.addEventListener('load', function () {

    console.log("Hello World!");

});

function submitName() {
    const name = document.getElementById("name").value;

    fetch("/submit_name", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ name: name }),
    })
        .then((response) => {
            if (response.ok) {
                location.reload();
            }
        })
        .catch((error) => {
            console.error("Error submitting name. Code: ", error);
        });
}