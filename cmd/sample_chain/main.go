package main

import (
	"encoding/gob"
	"flag"
	"fmt"
	"log"
	"math/rand"
	"os"
	"time"

	markov "github.com/abtrout/2Mile-markov"
)

func main() {
	chainFile := flag.String("chainFile", "", "Path to serialized Markov chain to sample")
	numWords := flag.Int("words", 100, "Maximum number of words to generate per report")
	randSeed := flag.Int64("randSeed", time.Now().UnixNano(), "Seed for random number generator")
	flag.Parse()

	f, err := os.Open(*chainFile)
	defer f.Close()
	if err != nil {
		log.Fatalf("Failed to open corpFile: %v", err)
	}

	var chain markov.Chain
	dec := gob.NewDecoder(f)
	if err := dec.Decode(&chain); err != nil {
		log.Fatalf("Failed to Decode chain from chainFile: %v", err)
	}

	rand.Seed(*randSeed)
	for {
		fmt.Println(chain.Generate(*numWords))
		fmt.Println("Press ENTER to generate a new report...")
		fmt.Scanln()
	}
}
