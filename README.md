## 2Mile markov

Markov chain generated Channel and Patch reports. For example:

> CHANNEL: A solitary tactician makes his way through slow ripples to an AMWAY sales person. Four longboarders are out there now and will connect inside at Mali-Bo working on paddle arm strength as footprint trails around the seadrift side. One (1) desperado out there right now but tide switch may shut it down as wide rollers release their pent up frustrations on the surface, the ocean that is consistenly breaking waist high. Shallow inside due to small sample size. Space is the only things in motion. Egg and log rides that run up to a respectable level and should be a quartet has laid his paint on thick and gray, moving at a stand still as waves are progressing this morning. 
>
> PATCH: Smooth like butter. Slather it on. Mouse treats for all sliding levels from thigh to almost waist high +. Tide peaks in 2 hours and changes may yet be rides but it is the only one (1) managed to catch up on world politics, BART strike debates and discuss steroid use in Major League baseball. Ten (10) out there now on logs and the energy and tele-presence. For now, practice patience and time scores. Inside right is throwing down waist (+/-) section-y wedges that are waist high. Breaking in the knee high range. Maybe with the high tide with inside rights can be forecast if you drove all this way...

Needed now [more than ever](https://www.2milesurf.com/surfreport/2-ctddf-x3n8n-56y6c-n2y8b-tmlaf-mpsjm-h53h3-hate4-hx796-4lgp8-b8e7e-t2ks2-b5226-znkzd-e2223-jt8fk-54w8j-4wzah-ftn93-b6a9t-2j38f-2623l-f94zt-635hy-ahd5t-8bg84-3df7b-mmat6-pdkgl).

## Usage

Use `make_chain` to fit a Markov chain on a given corpus file.

```shell
$ go build ./cmd/make_chain
$ ./make_chain -help
Usage of ./make_chain:
  -chainFile string
        Path to file chain will be serialized to
  -corpFile string
        Path to input corpus file
  -prefixLen int
        Number of words per Prefix (default 2)
```

Use `sample_chain` to generate new documents from a previously made chain.

```shell
$ go build ./cmd/sample_chain
$ ./sample_chain -help
Usage of ./sample_chain:
  -chainFile string
        Path to serialized Markov chain to sample
  -randSeed int
        Seed for random number generator (default 1595824635666537000)
```