getDate = () => {
    var date = new Date();
    return `${String(date.getMonth()+1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}-${date.getFullYear()}`
}

main = () => {
    document.getElementById("date").innerText = getDate();
}

document.getElementById("add").onsubmit = (e) => {
    e.preventDefault()
    var name = document.getElementById("name").value
    var subject = document.getElementById("subject").value
    var due = document.getElementById("due").value
    console.log(name, subject, due)

    var total = localStorage.getItem("total-count");
    if (total === null) {
        localStorage.setItem("total-count", "1")
    } else {
        localStorage.setItem("total-count", String(Number(total)+1))
    }

    localStorage.setItem(`assignment-${localStorage.getItem("total-count")}`, JSON.stringify({name: name, subject: subject, due: due}));
}

displayAssignment = (id, name, subject, due) => {
    var div = document.createElement("div");
    if (due == getDate()) {
        console.log(due, getDate(), true)
        div.innerHTML = `<div class="card" style="width: 18rem;">
        <div class="card-body">
        <span class="badge bg-danger">Due Today!</span>
          <h5 class="card-title">${subject} | ${name}</h5>
          <h6 class="card-subtitle mb-2 text-muted">Due: ${due}</h6>
          <button type="button" class="btn btn-link" onclick="done(${id+1})">Link</button>
        </div>
      </div>`
    } else {
        console.log(due, getDate(), false)
        div.innerHTML = `<div class="card" style="width: 18rem;">
        <div class="card-body">
          <h5 class="card-title">${subject} | ${name}</h5>
          <h6 class="card-subtitle mb-2 text-muted">Due: ${due}</h6>
          <button type="button" class="btn btn-link" onclick="done(${id+1})">Link</button>
          </div>
      </div>`
    }

  document.getElementById("assignments").appendChild(div);
}


done = id => {
    console.log(id)
    localStorage.removeItem(`assignment-${id}`)
}


assignments = () => {
    var total = localStorage.getItem("total-count");
    for (let i=0; i<Number(total); i++) {
        try {
        displayAssignment(i, JSON.parse(localStorage.getItem(`assignment-${i+1}`))["name"], JSON.parse(localStorage.getItem(`assignment-${i+1}`))["subject"], JSON.parse(localStorage.getItem(`assignment-${i+1}`))["due"])
        } catch (err) {

        }
    }
}

main()
assignments();