
let checkbox = document.querySelectorAll(".accept-answer");
checkbox.forEach(item => {
    item.addEventListener('click', event => {
        let currentLocation = location.href;
        let questionId = currentLocation.split("/");
        let answerId = item.value;
        if (item.checked === true) {
            location.href = `/accept-answer/${questionId[questionId.length - 1]}/${answerId}`
        } else {
            location.href = `/decline-answer/${questionId[questionId.length - 1]}/${answerId}`
        }
    })
});