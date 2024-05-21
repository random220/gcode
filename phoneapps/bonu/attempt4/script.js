let selectedItem = null;

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

function searchItems() {
    const query = document.getElementById('searchBar').value.toLowerCase().trim();
    const resultsContainer = document.getElementById('results');
    resultsContainer.innerHTML = '';

    if (query) {
        const filteredData = data.filter(item => item.item.toLowerCase().includes(query));
        filteredData.forEach(item => {
            const resultItem = document.createElement('p');
            resultItem.textContent = `${item.item.slice(0, 40)}${item.item.length > 40 ? '...' : ''} - Qty: ${item.qty}`;
            resultItem.onclick = () => selectItem(item);
            resultsContainer.appendChild(resultItem);
        });
    }
}

function selectItem(item) {
    selectedItem = item;
    document.getElementById('searchBar').value = item.item;
    document.getElementById('results').innerHTML = '';
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
        drugid: selectedItem.id, // Ensure drugid is included in the log entry
        item: selectedItem.item,
        quantity: quantity,
        timestamp: new Date().toLocaleString()
    };

    saveUsageLog(logEntry);
    displayUsageLog();
    resetForm();
}

function saveUsageLog(logEntry) {
    const usageLog = JSON.parse(localStorage.getItem('usageLog')) || [];
    usageLog.push(logEntry);
    localStorage.setItem('usageLog', JSON.stringify(usageLog));
}

function displayUsageLog() {
    const usageLog = JSON.parse(localStorage.getItem('usageLog')) || [];
    const usageLogTableBody = document.getElementById('usageLog').querySelector('tbody');
    usageLogTableBody.innerHTML = '';

    usageLog.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));

    usageLog.forEach((entry) => {
        const truncatedItemName = entry.item.length > 40 ? entry.item.slice(0, 40) + '...' : entry.item;

        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${truncatedItemName}</td>
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
    document.getElementById('searchBar').value = '';
    document.getElementById('usageInput').value = '';
    document.getElementById('selectedItemName').textContent = '';
    document.getElementById('selectedItem').classList.add('hidden');
    selectedItem = null;
}

function exportToCSV() {
    const usageLog = JSON.parse(localStorage.getItem('usageLog')) || [];
    let csvContent = "timestamp,drugid,drugname,quantity\n";

    usageLog.forEach((entry) => {
        csvContent += `"${entry.timestamp}",${entry.drugid},"${entry.item}",${entry.quantity}\n`;
    });

    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = 'usage_log.csv';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

function clearUsageLog() {
    const confirmation = prompt("Type YES to confirm clearing the usage log:");
    if (confirmation === "YES") {
        localStorage.removeItem('usageLog');
        displayUsageLog();
    }
}
