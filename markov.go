package main

import (
	"bufio"
	"flag"
	"fmt"
	"io"
	"log"
	"math/rand"
	"os"
	"strings"
	"time"
)

// Prefix is a chain of one or more words.
type Prefix []string

// String returns the Prefix as a string.
func (p Prefix) String() string {
	return strings.Join(p, " ")
}

// Shift removes the first word from the Prefix and appends the given word.
func (p Prefix) Shift(word string) {
	copy(p, p[1:])
	p[len(p)-1] = word
}

// Chain contains a map of Prefixes to a list of suffixes.
// A prefix is a string of prefixLen words joined with spaces.
// A suffix is a single word. A prefix can have multiple suffixes.
type Chain struct {
	chain     map[string][]string
	prefixLen int
}

// NewChain returns a new Chain built from the provided Reader.
// Prefixes and their suffixes within a single document (line
// of Reader input) are parsed and stored in the Chain.
func NewChain(br *bufio.Reader, prefixLen int) *Chain {
	c := &Chain{make(map[string][]string), prefixLen}
	for {
		p := make(Prefix, c.prefixLen)
		line, err := br.ReadString('\n')
		for _, w := range strings.Split(line, " ") {
			key := p.String()
			c.chain[key] = append(c.chain[key], w)
			p.Shift(w)
		}
		if err == io.EOF {
			break
		}
	}
	return c
}

// Generate returns a string of at most n words generated from Chain.
func (c *Chain) Generate(n int) string {
	p := make(Prefix, c.prefixLen)
	var words []string
	for i := 0; i < n; i++ {
		choices := c.chain[p.String()]
		if len(choices) == 0 {
			break
		}
		next := choices[rand.Intn(len(choices))]
		words = append(words, next)
		p.Shift(next)
	}
	return strings.Join(words, " ")
}

func main() {
	corpFile := flag.String("corpus", "", "path to corpus file")
	numWords := flag.Int("words", 100, "maximum number of words to print")
	prefixLen := flag.Int("prefix", 2, "prefix length in words")

	flag.Parse()
	rand.Seed(time.Now().UnixNano())

	f, err := os.Open(*corpFile)
	defer f.Close()
	if err != nil {
		log.Fatalf("Failed to open corpFile: %v", err)
	}

	c := NewChain(bufio.NewReader(f), *prefixLen)
	for {
		fmt.Println(c.Generate(*numWords))
		fmt.Println("Press any key to continue ...")
		fmt.Scanln()
	}
}
