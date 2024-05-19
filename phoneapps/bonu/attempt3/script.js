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
                <p><strong>Item:</strong> ${result.item}</p>
                <p><strong>Category:</strong> ${result.category}</p>
                <p><strong>Qty:</strong> ${result.qty} ${result.unit}</p>
                <p><strong>Mfg Date:</strong> ${result.mfgDate}</p>
                <p><strong>Exp Date:</strong> ${result.expDate}</p>
            `;
            resultsContainer.appendChild(resultItem);
        });
    }
}
