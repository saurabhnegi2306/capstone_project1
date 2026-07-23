async function loadCustomers() {

    const response = await fetch("/api/customers");
    const data = await response.json();

    let html = "";

    data.forEach(c => {

        html += `
        <tr>
            <td>${c.id}</td>
            <td>${c.name}</td>
            <td>${c.email}</td>
            <td>$${parseFloat(c.balance).toFixed(2)}</td>
            <td>
                <button onclick="deleteCustomer(${c.id})">
                    Delete
                </button>
            </td>
        </tr>
        `;

    });

    document.getElementById("customers").innerHTML = html;
}


async function addCustomer() {

    await fetch("/api/customers", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({

            name: document.getElementById("name").value,

            email: document.getElementById("email").value,

            balance: document.getElementById("balance").value

        })

    });

    document.getElementById("name").value = "";
    document.getElementById("email").value = "";
    document.getElementById("balance").value = "";

    loadCustomers();

}


async function deleteCustomer(id) {

    await fetch("/api/customers/" + id, {

        method: "DELETE"

    });

    loadCustomers();

}


loadCustomers();