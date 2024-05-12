Need help with writing an app to run on android
The app will run on a smartphone and help a veteranarian keep track of her medicine supplies

This is a part of the sample data


```
id,#,Category,Item,Qty,Unit,Mfg Date,Exp Date
13973,10,Drug,Injection Triamcinolone 6 mg. per ml.,7,5 ml. Vial,01/08/2023,31/07/2025
13974,11,Drug,Injection Prednisolone Acetate 10 mg per ml.,5,10 ml. Vial,01/01/2023,31/12/2024
13975,12,Drug,Injection Pheniramine Maleate 22.75 mg/ml.,30,30 ml.Vial,01/05/2023,30/04/2025
13976,13,Drug,Injection Xylazine Hydrochloride equivalent to Xylazine 20 mg for 2% Solution,5,10 ml. Vial,01/07/2023,30/06/2025
13977,14,Drug,Injection Meloxicam 5 mg /ml. I.P. & Paracetamol IP 150 mg per ml,5,30 ml.Vial,01/12/2022,30/11/2024
13978,15,Drug,Injection Meloxicam 5 mg /ml. I.P.,20,30 ml.Vial,01/08/2023,31/07/2025
13979,16,Drug,Bolus contains: Nimesulide 400 mg & Paracetamol (1500 mg),20,4 bolus Strip,01/01/2023,31/12/2024
13980,17,Drug,"Injection contains: ( Vitamin-A 2,50,000 IU, Vitamin-D3 25,000 IU, Vitamin-E100 IU, Biotin12.5 mcg) / ml",5,10 ml. Vial,01/12/2023,31/05/2025
```

Requirements:

- She would like the data to reside on the phone itself.
- When she opens the app, it should present a text input field and a display area.
- Suppose she is using or wants to use half a vial of Prednisolone Acetate, she would start typing pred ... etc.
- As she types the display area will match the drug and will be tappable. It should also show how much of the drug is available
- If she taps the drug name, her text input field will now be ready to take usage input
- If she types .5, a choice between ml and vial would show for her to click, and also a submit button
- Say she types .5, selects vial and hits submit. The information will be entered into the system and a timestamped transaction would be recorded.
- All transactions should be viewable by hitting the a dedicated Transactions button.
- The transactions window is actually an edit window to let the user make corrections to the historical transaction information.

Please attempt to provide detailed instructions and code

---

To create this app, you'll need to use Android Studio and have a basic understanding of Java or Kotlin, XML, and SQL. Here's a high-level overview of the steps you'd take to create this app, along with some sample code snippets.

- Set up a new project in Android Studio with an Empty Activity template. Choose Java or Kotlin according to your preference.

- Create a database using SQLite to store the medicine data and transactions. Use the Room library for easier database management. Define an entity for the medicine data:

```kotlin
@Entity(tableName = "medicine_table")
data class Medicine(
    @PrimaryKey(autoGenerate = true) val id: Int,
    val category: String,
    val item: String,
    val qty: Int,
    val unit: String,
    val mfgDate: String,
    val expDate: String
)
```

- Create a DAO (Data Access Object) to interact with the database:

```kotlin
@Dao
interface MedicineDao {
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insert(medicine: Medicine)

    @Query("SELECT * FROM medicine_table WHERE item LIKE :searchQuery")
    fun searchMedicine(searchQuery: String): LiveData<List<Medicine>>

    // Add other necessary functions like update, delete, etc.
}
```

- Set up the Room database:

```kotlin
@Database(entities = [Medicine::class], version = 1, exportSchema = false)
abstract class AppDatabase : RoomDatabase() {
    abstract fun medicineDao(): MedicineDao

    companion object {
        @Volatile
        private var INSTANCE: AppDatabase? = null

        fun getDatabase(context: Context): AppDatabase {
            return INSTANCE ?: synchronized(this) {
                val instance = Room.databaseBuilder(
                    context.applicationContext,
                    AppDatabase::class.java,
                    "app_database"
                ).build()
                INSTANCE = instance
                instance
            }
        }
    }
}
```

- Create a ViewModel and Repository to handle the app's logic and data:

```kotlin
class MedicineViewModel(application: Application) : AndroidViewModel(application) {
    private val medicineDao = AppDatabase.getDatabase(application).medicineDao()

    val searchedMedicine: LiveData<List<Medicine>>

    init {
        searchedMedicine = medicineDao.searchMedicine("")
    }

    fun searchMedicine(searchQuery: String) {
        searchedMedicine = medicineDao.searchMedicine("%$searchQuery%")
    }

    // Add other necessary functions like insert, update, etc.
}
```

- Design the app's layout using XML. You'll need an EditText for user input, a RecyclerView for displaying the search results, and a button for transactions.

- Implement the search functionality, displaying the results in the RecyclerView as the user types.

- Add click listeners for the drug items in the RecyclerView and the transaction button, and implement the usage input functionality.

- Create a transactions activity or fragment for viewing and editing historical transactions.

- Test your app on an emulator or physical device, and make any necessary adjustments.

This is a high-level guide to creating the app. You'll need to write more code and handle various edge cases to have a fully functional app. You can find more detailed information and examples in the Android documentation and various online tutorials.