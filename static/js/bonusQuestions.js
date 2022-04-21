// you receive an array of objects which you must sort in the by the key "sortField" in the "sortDirection"
function getSortedItems(items, sortField, sortDirection) {
    console.log(items)
    console.log(sortField)
    console.log(sortDirection)

    if (sortField === 'VoteCount' || sortField === 'ViewNumber'){
        if (sortDirection === "asc") {
        items.sort((a, b) => {
            let fa = a[sortField],
                fb = b[sortField];
            if (Number(fa) < Number(fb)) {
                return -1;
            }
            if (Number(fa) > Number(fb)) {
                return 1;
            }
            return 0;
        })
    } else {
        items.sort((a, b) => {
            let fa = a[sortField],
                fb = b[sortField];
            if (Number(fa) < Number(fb)) {
                return 1;
            }
            if (Number(fa) > Number(fb)) {
                return -1;
            }
            return 0;
    })}
    } else {
        if (sortDirection === "asc") {
            items.sort((a, b) => {
                let fa = a[sortField].toLowerCase(),
                    fb = b[sortField].toLowerCase();
                if (fa < fb) {
                    return -1;
                }
                if (fa > fb) {
                    return 1;
                }
                return 0;
            })
        } else {
            items.sort((a, b) => {
                let fa = a[sortField].toLowerCase(),
                    fb = b[sortField].toLowerCase();
                if (fa < fb) {
                    return 1;
                }
                if (fa > fb) {
                    return -1;
                }
                return 0;
        })}}

    // === SAMPLE CODE ===
    // if you have not changed the original html uncomment the code below to have an idea of the
    // effect this function has on the table
    //

    // if (sortDirection === "asc") {
    //     const firstItem = items.shift()
    //     if (firstItem) {
    //         items.push(firstItem)
    //     }
    // } else {
    //     const lastItem = items.pop()
    //     if (lastItem) {
    //         items.push(lastItem)
    //     }
    // }

    return items

}

// you receive an array of objects which you must filter by all it's keys to have a value matching "filterValue"
function getFilteredItems(items, filterValue) {
    console.log(items);
    console.log(filterValue);
    let newItem = [];
    if (filterValue.startsWith("Description") || filterValue.startsWith("!Description")) {
        let filterValueParts = filterValue.split(":");
        if (filterValueParts[0].startsWith("!")) {
            let filterValueString = filterValueParts[1];
        for (let i=0; i<items.length; i++) {
        if (items[i]['Description'].indexOf(filterValueString) === -1) {
            newItem.push(items[i]);
        }}
        } else {
            let filterValueString = filterValueParts[1];
            for (let i=0; i<items.length; i++) {
            if (items[i]['Description'].indexOf(filterValueString) !== -1) {
                newItem.push(items[i]);
            }}
        }
    } else {
        if (filterValue[0] === "!") {
            let filterValueString = filterValue.slice(1,);
            for (let i = 0; i < items.length; i++) {
                if (items[i]['Title'].indexOf(filterValueString) === -1) {
                    newItem.push(items[i]);
                }}
        } else {
            for (let i = 0; i < items.length; i++) {
                if (items[i]['Title'].indexOf(filterValue) !== -1) {
                    newItem.push(items[i]);
                }}
        }
    }
    return newItem

    // === SAMPLE CODE ===
    // if you have not changed the original html uncomment the code below to have an idea of the
    // effect this function has on the table
    //
    // for (let i=0; i<filterValue.length; i++) {
    //     items.pop()
    // }
    //
    // return items
}

function toggleTheme() {
    console.log("toggle theme")
    let bgColor = document.querySelector('body');
    if (bgColor.style.backgroundColor) {
        console.log(bgColor.style.backgroundColor);
    }
}

function increaseFont() {
    console.log("increaseFont");
    let textSize = window.getComputedStyle(document.querySelector('td')).fontSize;
    let elem = window.document.querySelectorAll('td');
    let fontNumber = textSize.slice(0, 2);
    console.log(textSize);
    console.log(elem);
    if (+fontNumber <= 30) {
        for (let text of elem) {
            text.style.fontSize = +fontNumber + 1 + 'px';
        }}
}

function decreaseFont() {
    console.log("decreaseFont")
    let textSize = window.getComputedStyle(document.querySelector('td')).fontSize;
    let elem = window.document.querySelectorAll('td');
    let fontNumber = textSize.slice(0, 2);
    if (+fontNumber >= 11) {
        for (let text of elem) {
            text.style.fontSize = +fontNumber - 1 + 'px';
        }}
}