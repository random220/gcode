fun main() {
    val greeting: String = "Hello, World!"
    println(greeting)

    // Using a nullable variable
    var nullableString: String? = null
    nullableString = "Kotlin"
    println(nullableString?.length)

    // Defining a function with default parameters
    fun greet(name: String = "World") {
        println("Hello, $name!")
    }

    greet()
    greet("Kotlin")
}
