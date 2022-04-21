let checkbox = document.querySelectorAll(".accept-answer");
let questionUserId = document.querySelector(".info").id;
let userId = document.querySelector(".userId").id;
checkbox.forEach(item => {
    item.addEventListener('click', event => {
        let currentLocation = location.href;
        let questionId = currentLocation.split("/");
        let answerId = item.value;
        if (userId === questionUserId) {
            if (item.checked === true) {
            location.href = `/accept-answer/${questionId[questionId.length - 1]}/${answerId}`
        } else {
            location.href = `/decline-answer/${questionId[questionId.length - 1]}/${answerId}`
        }} else {
            alert("Can't touch this!");
            location.href = currentLocation;
        }
    })
});