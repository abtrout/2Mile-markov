package main

import (
	"bufio"
	"encoding/gob"
	"flag"
	"log"
	"os"

	markov "github.com/abtrout/2Mile-markov"
)

func main() {
	corpFile := flag.String("corpFile", "", "Path to input corpus file")
	chainFile := flag.String("chainFile", "", "Path to file chain will be serialized to")
	prefixLen := flag.Int("prefixLen", 2, "Number of words per Prefix")
	flag.Parse()

	fIn, err := os.Open(*corpFile)
	defer fIn.Close()
	if err != nil {
		log.Fatalf("Failed to open corpFile for reading: %v", err)
	}
	c := markov.NewChain(bufio.NewReader(fIn), *prefixLen)

	fOut, err := os.Create(*chainFile)
	defer fOut.Close()
	if err != nil {
		log.Fatalf("Failed to open chainFile for writing: %v", err)
	}
	enc := gob.NewEncoder(fOut)
	if err := enc.Encode(c); err != nil {
		log.Fatalf("Failed to Encode chain: %v\n", err)
	}
}
