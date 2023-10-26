function logout() {
    fetch("/logout")
    setTimeout(() => {
        document.cookie = "user=;expires=Thu, 01 Jan 1970 00:00:01 GMT"
        document.location = "/signin"
    }, 100)
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
    

    exerciseInput.type = "text"
    exerciseInput.name = "exercise_input" + numberOfRows

    repstimeInput.type = "number"
    repstimeInput.min = "0"
    repstimeInput.name = "repstime_input" + numberOfRows

    setsInput.type = "number"
    setsInput.name = "sets_input" + numberOfRows
    setsInput.min = "0"

    restInput.type = "number"
    restInput.name = "rest_input" + numberOfRows
    restInput.min = "0"
    numberOfRows++

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
numberOfRows = 0



function addRow() {
    const tableBody = document.querySelector("#tb tbody");
    const newRow = document.createElement("tr");
    const cell1 = document.createElement("td");
    const cell2 = document.createElement("td");
    const cell3 = document.createElement("td");
    const cell4 = document.createElement("td");
    const cell5 = document.createElement("td");
    const cell6 = document.createElement("td");

    newRow.appendChild(cell1)
    newRow.appendChild(cell2)
    newRow.appendChild(cell3)
    newRow.appendChild(cell4)
    newRow.appendChild(cell5)
    newRow.appendChild(cell6)
    tableBody.appendChild(newRow);
}
