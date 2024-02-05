package markov

import (
	"bufio"
	"io"
	"sort"
	"strings"
)

// All fields are exported for gob encoding.
type Chain struct {
	PrefixLen int
	Probs     map[int]map[float64]int

	//PrefixToIndex, SuffixToIndex map[string]int
	IndexToPrefix, IndexToSuffix map[int]string
}

// NewChain constructs a new Markov Chain from the given input.
func NewChain(input *bufio.Reader, prefixLen int) *Chain {
	// Read input and construct mapping between prefixes and suffixes.
	nextMap := map[string]map[string]int{} // prefix -> frequency of suffix
	for {
		line, err := input.ReadString('\n')
		p := make(Prefix, prefixLen)
		// TODO: Add start/end token.
		for _, w := range strings.Split(line, " ") {
			key := p.String()
			if _, ok := nextMap[key]; !ok {
				nextMap[key] = map[string]int{}
			}
			nextMap[key][w]++
			p.Shift(w)
		}
		if err == io.EOF {
			break
		}
	}

	// Collect unique prefixes and suffixes
	pSet, sSet := map[string]bool{}, map[string]bool{}
	for p, ss := range nextMap {
		pSet[p] = true
		for s := range ss {
			sSet[s] = true
		}
	}
	pToI, iToP := encodeAlphas(pSet)
	sToI, iToS := encodeAlphas(sSet)

	// Compute cumulative probabilities.
	probs := map[int]map[float64]int{}
	for p, ss := range nextMap {
		i := pToI[p]
		if _, ok := probs[i]; !ok {
			probs[i] = map[float64]int{}
		}
		total := 0
		for _, count := range ss {
			total += count
		}
		for s, count := range ss {
			probs[i][float64(count/total)] = sToI[s]
		}
	}

	return &Chain{prefixLen, probs, iToP, iToS}

}

func encodeAlphas(input map[string]bool) (map[string]int, map[int]string) {
	var xs []string
	for x := range input {
		xs = append(xs, x)
	}
	sort.Slice(xs, func(i int, j int) bool { return xs[i] < xs[j] })
	toIndex, fromIndex := map[string]int{}, map[int]string{}
	for i, p := range xs {
		toIndex[p] = i
		fromIndex[i] = p
	}
	return toIndex, fromIndex
}

/*
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
*/

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
