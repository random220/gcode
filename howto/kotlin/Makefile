all: HelloWorld.jar

clean:
	rm -f HelloWorld.jar

HelloWorld.jar: HelloWorld.kt
	kotlinc HelloWorld.kt -include-runtime -d HelloWorld.jar
	java -jar HelloWorld.jar
