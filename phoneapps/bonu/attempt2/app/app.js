const supplyTable = [
    {
        id: 13945,
        no: 1,
        Category: 'Drug',
        Item: 'Injection Enrofloxacin 100 mg. /ml. I.P.',
        Qty0: 40, // base unit quantity
        Qty1: '', // additional unit quantity (if any)
        Unit: '50 ml.Vial', // base unit
        Mfg_Date: '01/04/2023',
        Exp_Date: '31/03/2025'
    },
    {
        id: 13948,
        no: 2,
        Category: 'Drug',
        Item: 'Tablet Enrofloxacin. 50 mg.',
        Qty0: 200, // base unit quantity
        Qty1: '', // additional unit quantity (if any)
        Unit: '10 tablets Strip', // base unit
        Mfg_Date: '01/07/2023',
        Exp_Date: '30/06/2025'
    },
    {
        id: 13951,
        no: 3,
        Category: 'Drug',
        Item: 'Enrofloxacin Oral 50 mg per ml',
        Qty0: 50, // base unit quantity
        Qty1: '', // additional unit quantity (if any)
        Unit: '100 ml. Bottle', // base unit
        Mfg_Date: '01/08/2023',
        Exp_Date: '01/07/2025'
    },
    // ...
];

let currentTable = [...supplyTable]; // Make a copy of the supply table

document.getElementById('search-bar').addEventListener('input', function(e) {
    const searchTerm = e.target.value.toLowerCase();
    const results = document.getElementById('search-results');
    results.innerHTML = '';

    if (searchTerm === '') {
        document.getElementById('usage-form').style.display = 'none';
        return;
    }

    // Use supplyTable to filter the search results
    const matches = supplyTable.filter(function(drug) {
        return drug.Item.toLowerCase().includes(searchTerm);
    });

    if (matches.length === 0) {
        document.getElementById('usage-form').style.display = 'none';
        return;
    }

    matches.forEach(function(drug) {
        const li = document.createElement('li');
        li.textContent = drug.Item;
        li.addEventListener('click', function() {
            document.getElementById('drug-name').value = drug.Item;
            document.getElementById('quantity').value = '';
            document.getElementById('unit').innerHTML = '';
            // Use currentTable to populate the unit options
            currentTable.find(function(drug) {
                return drug.Item === drugName;
            }).Unit.split(',').forEach(function(unit) {
                const option = document.createElement('option');
                option.value = unit;
                option.textContent = unit;
                document.getElementById('unit').appendChild(option);
            });
            document.getElementById('usage-form').style.display = 'block';
        });
        results.appendChild(li);
    });
});

document.getElementById('usage-form').addEventListener('submit', function(e) {
    e.preventDefault();

    const drugName = document.getElementById('drug-name').value;
    const quantity = parseFloat(document.getElementById('quantity').value);
    const unit = document.getElementById('unit').value;

    const drug = currentTable.find(function(drug) {
        return drug.Item === drugName;
    });

    if (drug.Unit.includes(',')) {
        // Drug has multiple units, so we need to convert the used quantity to the base unit
        const unitIndex = drug.Unit.split(',').indexOf(unit);
        const conversionFactor = parseFloat(drug[`Qty${unitIndex !== 0 ? unitIndex : ''}`]`);
        const baseQuantity = quantity / conversionFactor;
        drug.Qty0 -= baseQuantity;
    } else {
        // Drug has a single unit, so we can just subtract the used quantity
        drug.Qty0 -= quantity;
    }

    // Update the currentTable with the new quantity
    currentTable = currentTable.map(function(drug) {
        if (drug.Item === drugName) {
            return {
                ...drug,
                Qty0: drug.Qty0
            };
        } else {
            return drug;
        }
    });

    document.getElementById('search-bar').value = '';
    document.getElementById('usage-form').style.display = 'none';
});
