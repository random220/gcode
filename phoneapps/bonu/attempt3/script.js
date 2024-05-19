const data = [
    {
        id: 13945,
        number: 1,
        category: 'Drug',
        item: 'Injection Enrofloxacin 100 mg. /ml. I.P.',
        qty: 40,
        unit: '50 ml.Vial',
        mfgDate: '01/04/2023',
        expDate: '31/03/2025'
    },
    {
        id: 13948,
        number: 2,
        category: 'Drug',
        item: 'Tablet Enrofloxacin. 50 mg.',
        qty: 200,
        unit: '10 tablets Strip',
        mfgDate: '01/07/2023',
        expDate: '30/06/2025'
    }
];

let selectedItem = null;

function searchItems() {
    const query = document.getElementById('searchBar').value.toLowerCase().trim();
    const queryTerms = query.split(' ').filter(term => term.length > 0);

    const results = data.filter(entry => {
        return queryTerms.every(term =>
            entry.item.toLowerCase().includes(term)
        );
    });

    displayResults(results);
}

function displayResults(results) {
    const resultsContainer = document.getElementById('results');
    resultsContainer.innerHTML = '';
    if (results.length === 0) {
        resultsContainer.innerHTML = '<p>No matches found</p>';
    } else {
        results.forEach(result => {
            const resultItem = document.createElement('div');
            resultItem.classList.add('result-item');
            resultItem.innerHTML = `
                <p class="highlight">${result.item}</p>
                <p><strong>Quantity:</strong> ${result.qty}</p>
                <p><strong>Unit:</strong> ${result.unit}</p>
            `;
            resultItem.onclick = () => selectItem(result);
            resultsContainer.appendChild(resultItem);
        });
    }
}

function selectItem(item) {
    selectedItem = item;
    document.getElementById('selectedItemName').textContent = item.item;
    document.getElementById('selectedItem').classList.remove('hidden');
}

function submitUsage() {
    const usageInput = document.getElementById('usageInput').value;
    const unitSelect = document.getElementById('unitSelect').value;
    if (selectedItem && usageInput && unitSelect) {
        const logEntry = {
            item: selectedItem.item,
            quantity: usageInput,
            unit: unitSelect,
            timestamp: new Date().toLocaleString()
        };

        saveUsageLog(logEntry);
        displayUsageLog();
        resetForm();
    } else {
        alert('Please enter the amount used and select a unit.');
    }
}

function saveUsageLog(logEntry) {
    let usageLog = JSON.parse(localStorage.getItem('usageLog')) || [];
    usageLog.push(logEntry);
    localStorage.setItem('usageLog', JSON.stringify(usageLog));
}

// Update the displayUsageLog function
function displayUsageLog() {
    const usageLog = JSON.parse(localStorage.getItem('usageLog')) || [];
    const usageLogTableBody = document.getElementById('usageLog').querySelector('tbody');
    usageLogTableBody.innerHTML = '';

    // Sort log entries in reverse chronological order
    usageLog.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));

    usageLog.forEach((entry, index) => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${entry.item}</td>
            <td>${entry.quantity}</td>
            <td>${entry.unit}</td>
            <td>${entry.timestamp}</td>
            <td>
                <button onclick="editUsage(${index})">Edit</button>
                <button onclick="deleteUsage(${index})">Delete</button>
            </td>
        `;
        usageLogTableBody.appendChild(row);
    });
}

function resetForm() {
    document.getElementById('selectedItem').classList.add('hidden');
    document.getElementById('usageInput').value = '';
    document.getElementById('unitSelect').value = '';
    selectedItem = null;
}

// Update the editUsage function
function editUsage(index) {
    console.log('Editing entry at index:', index);
    const usageLog = JSON.parse(localStorage.getItem('usageLog')) || [];
    const entry = usageLog[index];
    const newQuantity = prompt(`Edit quantity for ${entry.item}:`, entry.quantity);
    if (newQuantity !== null) {
        entry.quantity = newQuantity;
        usageLog[index] = entry; // Update the entry in the array
        localStorage.setItem('usageLog', JSON.stringify(usageLog));
        displayUsageLog();
    }
}

// Add this function to handle deleting a log entry
function deleteUsage(index) {
    const confirmDelete = confirm('Are you sure you want to delete this entry?');
    if (confirmDelete) {
        const usageLog = JSON.parse(localStorage.getItem('usageLog')) || [];
        usageLog.splice(index, 1);
        localStorage.setItem('usageLog', JSON.stringify(usageLog));
        displayUsageLog();
    }
}

// Initialize the usage log display
document.addEventListener('DOMContentLoaded', displayUsageLog);
