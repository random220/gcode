Running a Kotlin program on a Linux machine involves installing the Kotlin compiler and then compiling and executing the Kotlin code. Here are the steps to run the example Kotlin program provided:

### 1. Install Kotlin
First, you need to install Kotlin on your Linux machine. You can do this using the package manager or by downloading the compiler directly.

#### Using SDKMAN (recommended)
SDKMAN! is a tool for managing parallel versions of multiple Software Development Kits on most Unix-based systems.

1. **Install SDKMAN**:

   ```sh
   curl -s "https://get.sdkman.io" | bash
   source "$HOME/.sdkman/bin/sdkman-init.sh"
   ```

2. **Install Kotlin using SDKMAN**:

   ```sh
   sdk install kotlin
   ```

#### Using Snap
Alternatively, you can use Snap to install Kotlin.

1. **Install Snap** (if it's not already installed):

   ```sh
   sudo apt update
   sudo apt install snapd
   ```

2. **Install Kotlin using Snap**:

   ```sh
   sudo snap install --classic kotlin
   ```

### 2. Write the Kotlin Code
Create a new file with the `.kt` extension for your Kotlin code. For example, you can create a file named `HelloWorld.kt`.

1. **Create and edit the file**:

   ```sh
   nano HelloWorld.kt
   ```

2. **Paste the Kotlin code**:

   ```kotlin
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
   ```

3. **Save and exit**: Press `Ctrl+X`, then `Y`, and then `Enter` to save and exit.

### 3. Compile the Kotlin Code
Use the Kotlin compiler to compile your `HelloWorld.kt` file.

1. **Compile the code**:

   ```sh
   kotlinc HelloWorld.kt -include-runtime -d HelloWorld.jar
   ```

   This command compiles the Kotlin file and includes the Kotlin runtime in the resulting JAR file named `HelloWorld.jar`.

### 4. Run the Kotlin Program
Run the compiled Kotlin program using the `java` command.

1. **Run the program**:

   ```sh
   java -jar HelloWorld.jar
   ```

2. You should see the following output:
	
	```
	Hello, World!
	6
	Hello, World!
	Hello, Kotlin!
	```

### Summary
To run a Kotlin program on a Linux machine, you need to install the Kotlin compiler, write your Kotlin code in a file, compile the code using the Kotlin compiler, and then run the compiled JAR file using the `java` command. These steps should help you get started with running Kotlin programs on your Linux machine.