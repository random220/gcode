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
    const usageInput = document.getElementById('usageInput').value.trim();
    if (!usageInput) {
        alert('Please enter the quantity used.');
        return;
    }

    const quantity = parseFloat(usageInput);
    if (isNaN(quantity) || quantity <= 0) {
        alert('Please enter a valid positive number for the quantity.');
        return;
    }

    if (!selectedItem) {
        alert('Please select an item first.');
        return;
    }

    const logEntry = {
        id: selectedItem.id,
        item: selectedItem.item,
        quantity: quantity,
        timestamp: new Date().toLocaleString()
    };

    saveUsageLog(logEntry);
    displayUsageLog();
    resetForm();
}

function saveUsageLog(logEntry) {
    let usageLog = JSON.parse(localStorage.getItem('usageLog')) || [];
    usageLog.push(logEntry);
    localStorage.setItem('usageLog', JSON.stringify(usageLog));
}

function displayUsageLog() {
    const usageLog = JSON.parse(localStorage.getItem('usageLog')) || [];
    const usageLogTableBody = document.getElementById('usageLog').querySelector('tbody');
    usageLogTableBody.innerHTML = '';

    // Sort log entries in reverse chronological order
    usageLog.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));

    usageLog.forEach((entry) => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${entry.item}</td>
            <td>${entry.quantity}</td>
            <td>${entry.timestamp}</td>
            <td>
                <button onclick="editUsage('${entry.timestamp}')">Edit</button>
                <button onclick="deleteUsage('${entry.timestamp}')">Delete</button>
            </td>
        `;
        usageLogTableBody.appendChild(row);
    });
}

function resetForm() {
    document.getElementById('selectedItem').classList.add('hidden');
    document.getElementById('usageInput').value = '';
    selectedItem = null;
}

// Update the editUsage function
function editUsage(timestamp) {
    const usageLog = JSON.parse(localStorage.getItem('usageLog')) || [];
    const entryIndex = usageLog.findIndex(entry => entry.timestamp === timestamp);
    if (entryIndex !== -1) {
        const entry = usageLog[entryIndex];
        const newQuantity = prompt(`Edit quantity for ${entry.item}:`, entry.quantity);
        if (newQuantity !== null) {
            entry.quantity = newQuantity;
            localStorage.setItem('usageLog', JSON.stringify(usageLog));
            displayUsageLog();
        }
    } else {
        alert('Entry not found.');
    }
}

// Update the deleteUsage function
function deleteUsage(timestamp) {
    const confirmDelete = confirm('Are you sure you want to delete this entry?');
    if (confirmDelete) {
        const usageLog = JSON.parse(localStorage.getItem('usageLog')) || [];
        const updatedLog = usageLog.filter(entry => entry.timestamp !== timestamp);
        localStorage.setItem('usageLog', JSON.stringify(updatedLog));
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


function exportUsageToCSV() {
    const usageLog = JSON.parse(localStorage.getItem('usageLog')) || [];
    if (usageLog.length === 0) {
        alert('Usage log is empty.');
        return;
    }

    // Construct CSV content
    const csvContent = "timestamp,drugid,drugname,quantity\n" +
        usageLog.map(entry => {
            const drugName = entry.item ? `"${entry.item.replace(/"/g, '""')}"` : ''; // Handling undefined item
            const timestamp = `"${entry.timestamp.replace(/"/g, '""')}"`; // Handling commas in timestamp
            return `${timestamp},${entry.id},${drugName},${entry.quantity}`;
        }).join("\n");

    // Create and download CSV file
    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.setAttribute('href', url);
    a.setAttribute('download', 'usage_log.csv');
    a.click();
    window.URL.revokeObjectURL(url);
}

function downloadReconciledCSV() {
    const usageLog = JSON.parse(localStorage.getItem('usageLog')) || [];
    const reconciledData = data.map(item => {
        const usedQuantity = usageLog.filter(entry => entry.drugid === item.id)
            .reduce((total, entry) => total + entry.quantity, 0);
        const remainingQuantity = item.qty - usedQuantity;
        return { ...item, qty: remainingQuantity < 0 ? 0 : remainingQuantity };
    });

    const csvContent = "id,number,category,item,qty,unit,mfgDate,expDate\n" +
        reconciledData.map(item => {
            return `${item.id},${item.number},${item.category},"${item.item}",${item.qty},"${item.unit}","${item.mfgDate}","${item.expDate}"`;
        }).join("\n");

    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.setAttribute('href', url);
    a.setAttribute('download', 'reconciled_drug_data.csv');
    a.click();
    window.URL.revokeObjectURL(url);
}

function clearUsageData() {
    const confirmation = prompt("Are you sure you want to clear the usage data? Type 'YES' in capital letters to confirm.");
    if (confirmation === "YES") {
        localStorage.removeItem('usageLog');
        displayUsageLog();
        alert('Usage data cleared successfully.');
    } else {
        alert('Clear operation canceled.');
    }
}

// Initialize the usage log display
document.addEventListener('DOMContentLoaded', displayUsageLog);
