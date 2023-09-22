function logout() {
    document.cookie = "user=;expires=Thu, 01 Jan 1970 00:00:01 GMT"
    document.location = "/signin"
}

function addToTable() {
    const tableBody = document.querySelector("#tb tbody");
    const newRow = document.createElement("tr");
    const exerciseCell = document.createElement("td");
    const repstimeCell = document.createElement("td");
    const setsCell = document.createElement("td");
    const restCell = document.createElement("td");

    const exerciseInput = document.createElement("input");
    const repstimeInput = document.createElement("input");
    const setsInput = document.createElement("input");
    const restInput = document.createElement("input");
    
    // make names not the same between rows
    // so that they don't overwrite each other
    exerciseInput.type = "text"
    exerciseInput.name = "exercise_input"

    repstimeInput.type = "number"
    repstimeInput.min = "0"
    repstimeInput.name = "repstime_input"

    setsInput.type = "number"
    setsInput.name = "sets_input"
    setsInput.min = "0"

    restInput.type = "number"
    restInput.name = "rest_input"
    restInput.min = "0"

    const deleteRow = document.createElement("button")
    deleteRow.textContent = "Delete"
    deleteRow.addEventListener("click", function(){
        tableBody.removeChild(newRow);
    });

    exerciseCell.appendChild(exerciseInput)
    repstimeCell.appendChild(repstimeInput)
    setsCell.appendChild(setsInput)
    restCell.appendChild(restInput)
    exerciseCell.appendChild(deleteRow)

    
    newRow.appendChild(exerciseCell)
    newRow.appendChild(repstimeCell)
    newRow.appendChild(setsCell)
    newRow.appendChild(restCell)

    tableBody.appendChild(newRow);
};