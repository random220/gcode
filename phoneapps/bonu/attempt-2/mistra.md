Sure, I can provide a basic structure for your app using JavaScript, HTML, and CSS. This won't be a complete solution, but it should give you a good starting point.

First, let's create the HTML structure for the app. We'll need a search bar, a list to display the search results, and a form to enter the usage details.

```html
<!DOCTYPE html>
<html>
<head>
    <title>Drug Tracker</title>
    <link rel="stylesheet" type="text/css" href="styles.css">
</head>
<body>
    <h1>Drug Tracker</h1>
    <input type="text" id="search-bar" placeholder="Search for a drug...">
    <ul id="search-results"></ul>
    <form id="usage-form">
        <label for="drug-name">Drug Name:</label>
        <input type="text" id="drug-name" readonly>
        <br>
        <label for="quantity">Quantity:</label>
        <input type="number" id="quantity">
        <br>
        <label for="unit">Unit:</label>
        <select id="unit">
            <!-- Units will be populated dynamically -->
        </select>
        <br>
        <button type="submit">Record Usage</button>
    </form>
    <script src="app.js"></script>
</body>
</html>
```

Next, let's add some basic CSS to make the app look a bit nicer.

```css
body {
    font-family: Arial, sans-serif;
    max-width: 600px;
    margin: 0 auto;
}

h1 {
    text-align: center;
}

#search-bar {
    width: 100%;
    padding: 10px;
    margin-bottom: 20px;
}

#search-results {
    list-style-type: none;
    padding: 0;
}

#search-results li {
    padding: 10px;
    border-bottom: 1px solid #ccc;
}

#search-results li:hover {
    background-color: #f5f5f5;
    cursor: pointer;
}

#usage-form {
    display: none;
}

#usage-form label,
#usage-form input,
#usage-form select,
#usage-form button {
    width: 100%;
    padding: 10px;
    margin-bottom: 10px;
}
```

Finally, let's add the JavaScript to handle the search and form submission. For now, we'll use a hard-coded array to represent the SUPPLY table. In a real app, you'd want to replace this with data loaded from Google Drive.

```javascript
const supplyTable = [
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
            drug.Unit.split(',').forEach(function(unit) {
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

    document.getElementById('search-bar').value = '';
    document.getElementById('usage-form').style.display = 'none';
});
```