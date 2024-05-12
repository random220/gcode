Sure, let's break down the requirements and outline the steps to create the app:

1. **Set up Android Studio**: Ensure you have Android Studio installed and set up on your development machine.

2. **Create a New Android Project**: Open Android Studio and create a new project with an empty activity.

3. **Design the UI Layout**: Design the UI layout using XML in the layout file. You'll need:
   - Text input field for searching drugs.
   - Display area to show matching drugs and their availability.
   - Buttons for submitting usage, viewing transactions, and editing transactions.

4. **Implement Search Functionality**:
   - Parse the sample data and store it in a data structure (e.g., a list of drug objects).
   - Implement a search function that filters drugs based on user input in real-time and displays matching drugs and their availability.

5. **Handle Drug Selection**:
   - Implement logic to handle drug selection when the user taps on a drug name.
   - Update the text input field to allow the user to input usage (e.g., 0.5).
   - Provide options for selecting units (ml or vial) and a submit button.

6. **Record Transactions**:
   - Implement functionality to record transactions when the user submits usage.
   - Store transaction information (drug, quantity, unit, timestamp) in a data structure or database.

7. **View Transactions**:
   - Implement a button to view transactions.
   - Create a new activity or dialog to display transaction history.
   - Provide functionality to edit transactions.

8. **Testing**:
   - Test the app thoroughly to ensure all features work as expected.
   - Check for any bugs or edge cases.

Here's a simplified example of how you could start implementing some of the functionality:

```java
public class MainActivity extends AppCompatActivity {
    private EditText searchEditText;
    private TextView displayTextView;
    private Button submitButton;
    private List<Drug> drugs; // List to store drug objects

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // Initialize UI components
        searchEditText = findViewById(R.id.search_edit_text);
        displayTextView = findViewById(R.id.display_text_view);
        submitButton = findViewById(R.id.submit_button);

        // Parse and store sample data
        drugs = parseSampleData();

        // Search functionality
        searchEditText.addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence s, int start, int count, int after) {}

            @Override
            public void onTextChanged(CharSequence s, int start, int before, int count) {
                String query = s.toString().toLowerCase();
                List<Drug> matchingDrugs = searchDrugs(query);
                // Display matching drugs in display area
                displayMatchingDrugs(matchingDrugs);
            }

            @Override
            public void afterTextChanged(Editable s) {}
        });

        // Submit button functionality
        submitButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                // Handle submission of usage
                // You can implement this based on user input and selection
            }
        });
    }

    private List<Drug> parseSampleData() {
        // Parse the sample data and create Drug objects
        // Return list of drugs
    }

    private List<Drug> searchDrugs(String query) {
        // Filter drugs based on user input query
        // Return list of matching drugs
    }

    private void displayMatchingDrugs(List<Drug> matchingDrugs) {
        // Display matching drugs and their availability in the display area
    }
}
```

This is a basic outline to get started. You'll need to implement each step in detail and handle various edge cases and error conditions. Additionally, you'll need to design the UI layout according to your requirements and implement the transaction viewing and editing functionality. Let me know if you need further assistance with any specific part of the implementation!