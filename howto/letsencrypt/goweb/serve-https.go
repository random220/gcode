package main

import (
	"log"
	"net/http"
)

func main() {
	fs := http.FileServer(http.Dir("."))
	http.Handle("/", fs)

	log.Println("Serving on https://localhost:4343...")
	err := http.ListenAndServeTLS(":4343", "../certs/fullchain.pem", "../certs/privkey.pem", nil)
	if err != nil {
		log.Fatal(err)
	}
}
