package markov

import (
	"bufio"
	"io"
	"math/rand"
	"strings"
)

// Prefix is a sequence of one or more words.
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
	Chain     map[string][]string
	PrefixLen int
}

// NewChain returns a new Chain built from the provided Reader.
// Prefixes and their suffixes within a single document (line
// of Reader input) are parsed and stored in the Chain.
func NewChain(br *bufio.Reader, prefixLen int) *Chain {
	c := &Chain{make(map[string][]string), prefixLen}
	for {
		p := make(Prefix, c.PrefixLen)
		line, err := br.ReadString('\n')
		for _, w := range strings.Split(line, " ") {
			key := p.String()
			c.Chain[key] = append(c.Chain[key], w)
			p.Shift(w)
		}
		if err == io.EOF {
			break
		}
	}
	return c
}

// Generate returns a new document generated from Chain.
func (c *Chain) Generate() string {
	p := make(Prefix, c.PrefixLen)
	words := []string{}
	for {
		choices := c.Chain[p.String()]
		if len(choices) == 0 {
			break
		}
		next := choices[rand.Intn(len(choices))]
		words = append(words, next)
		p.Shift(next)
	}
	return strings.Join(words, " ")
}
