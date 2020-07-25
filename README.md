## 2Mile markov

Markov chain generated Channel and Patch reports.

```shell
# Build a Markov chain and save it to a file for re-use.
$ go build ./cmd/make_chain
$ ./make_chain -corpFile all_reports.txt -chainFile 2MM.chain -prefixLen 2
$ du -h 2MM.chain
3.3M    2MM.chain

# Use a serialized Markov chain to generate surf reports.
$ go build ./cmd/sample_chain
$ ./sample_chain -chainFile 2MM.chain
CHANNEL: Right side of cranberry compote. Savory goodness indeed.

Press ENTER to generate a new report...

CHANNEL: Marginal movements in the water this morning as this. Come join us in wait. Peek high not until the evening. 

Press ENTER to generate a new report...

PATCH: Neither fit for fish - yes. Not now. Maybe later.

Press ENTER to generate a new report...
^C
```

Needed now [more than ever](https://www.2milesurf.com/surfreport/2-ctddf-x3n8n-56y6c-n2y8b-tmlaf-mpsjm-h53h3-hate4-hx796-4lgp8-b8e7e-t2ks2-b5226-znkzd-e2223-jt8fk-54w8j-4wzah-ftn93-b6a9t-2j38f-2623l-f94zt-635hy-ahd5t-8bg84-3df7b-mmat6-pdkgl).
