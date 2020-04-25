package main

import (
	"bufio"
	"strings"
	"testing"

	"github.com/google/go-cmp/cmp"
)

func TestNewChain(t *testing.T) {
	tests := []struct {
		corpus    string
		prefixLen int
		chain     map[string][]string
	}{
		{
			"1 2\n1 2 2 1\n1 2 1 2 2 2",
			1,
			map[string][]string{
				"":  {"1", "1", "1"},
				"1": {"2\n", "2", "2", "2"},
				"2": {"2", "1\n", "1", "2", "2"},
			},
		},
	}
	for _, test := range tests {
		br := bufio.NewReader(strings.NewReader(test.corpus))
		c := NewChain(br, test.prefixLen)
		if diff := cmp.Diff(test.chain, c.chain); diff != "" {
			t.Errorf("Chains do not match: diff=%s", diff)
		}
	}
}
