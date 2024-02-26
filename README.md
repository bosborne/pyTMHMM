# Introduction

pyTMHMM is a Python 3.5+ implementation of the transmembrane helix predictor using a
hidden Markov model ([TMHMM](http://www.cbs.dtu.dk/services/TMHMM/)) originally
described in:

E.L. Sonnhammer, G. von Heijne, and A. Krogh. **A hidden Markov model for
predicting transmembrane helices in protein sequences**. In J. Glasgow,
T. Littlejohn, F. Major, R. Lathrop, D. Sankoff, and C. Sensen, editors,
Proceedings of the Sixth International Conference on Intelligent Systems for
Molecular Biology, pages 175-182, Menlo Park, CA, 1998. AAAI Press. PMID [9783223](https://pubmed.ncbi.nlm.nih.gov/9783223/)

# History

[Dan Søndergaard](https://github.com/dansondergaard) is the original author of this 
package and his repository is now [archived](https://github.com/dansondergaard/tmhmm.py). Dan wrote this code for a few reasons:

- the source code is not available as part of the publication
- the downloadable binaries are Linux-only
- the downloadable binaries may not be redistributed, so it's not possible to
  put them in a Docker image or a VM for other people to use
- the need to predict transmembrane helices in a scripted, automated way

This Python implementation includes a parser for the undocumented file format
used to describe the model and a fast Cython implementation of the
Viterbi algorithm used to perform the annotation. The tool will output files
similar to the files produced by the original TMHMM implementation.

# Incompatibilities

* The original TMHMM implementation handles ambigious characters and gaps in an
  undocumented way. However, `pyTMHMM` does not attempt to handle such
  characters at all and will fail. A possible fix is to replace those
  characters with something also based on expert/domain knowledge.

# Installation

This package supports Python 3.5 or greater. Install with:

    $ pip install pyTMHMM

# Usage

    $ pyTMHMM -h
      usage: pyTMHMM [-h] -f SEQUENCE_FILE [-m MODEL_FILE] [-p]

      optional arguments:
        -h, --help            show this help message and exit
        -f SEQUENCE_FILE, --file SEQUENCE_FILE
                              path to file in fasta format with sequences
        -m MODEL_FILE, --model MODEL_FILE
                              path to the model to use
        -p, --plot            plot posterior probabilies

The `-p`/`--plot` option requires `matplotlib`.

The input sequence file should be in FASTA format, for example:

    >B9DFX7|1B|HMA8_ARATH Copper-transporting ATPase PAA2, chloroplastic  [Arabidopsis thaliana ]
    MASNLLRFPLPPPSSLHIRPSKFLVNRCFPRLRRSRIRRHCSRPFFLVSNSVEISTQSFESTESSIESVKSITSDTPIL
    LDVSGMMCGGCVARVKSVLMSDDRVASAVVNMLTETAAVKFKPEVEVTADTAESLAKRLTESGFEAKRRVSGMGVAENV
    KKWKEMVSKKEDLLVKSRNRVAFAWTLVALCCGSHTSHILHSLGIHIAHGGIWDLLHNSYVKGGLAVGALLGPGRELLF
    DGIKAFGKRSPNMNSLVGLGSMAAFSISLISLVNPELEWDASFFDEPVMLLGFVLLGRSLEERAKLQASTDMNELLSLI
    STQSRLVITSSDNNTPVDSVLSSDSICINVSVDDIRVGDSLLVLPGETFPVDGSVLAGRSVVDESMLTGESLPVFKEEG
    CSVSAGTINWDGPLRIKASSTGSNSTISKIVRMVEDAQGNAAPVQRLADAIAGPFVYTIMSLSAMTFAFWYYVGSHIFP
    DVLLNDIAGPDGDALALSLKLAVDVLVVSCPCALGLATPTAILIGTSLGAKRGYLIRGGDVLERLASIDCVALDKTGTL
    TEGRPVVSGVASLGYEEQEVLKMAAAVEKTATHPIAKAIVNEAESLNLKTPETRGQLTEPGFGTLAEIDGRFVAVGSLE
    WVSDRFLKKNDSSDMVKLESLLDHKLSNTSSTSRYSKTVVYVGREGEGIIGAIAISDCLRQDAEFTVARLQEKGIKTVL
    LSGDREGAVATVAKNVGIKSESTNYSLSPEKKFEFISNLQSSGHRVAMVGDGINDAPSLAQADVGIALKIEAQENAASN
    AASVILVRNKLSHVVDALSLAQATMSKVYQNLAWAIAYNVISIPIAAGVLLPQYDFAMTPSLSGGLMALSSIFVVSNSL
    LLQLHKSETSKNSL

Example command:

    $ pyTMHMM -f test.fa

This produces three files.

## Summary file

The coordinates of the predicted domains:

    $ cat B9DFX7|1B|HMA8_ARATH.summary
    0-444: outside
    445-467: transmembrane helix
    468-820: inside
    821-843: transmembrane helix
    844-852: outside
    853-870: transmembrane helix
    871-882: inside

## Annotation file

An annotated sequence in FASTA-like format:

    $ cat B9DFX7|1B|HMA8_ARATH.annotation
    >B9DFX7|1B|HMA8_ARATH Copper-transporting ATPase PAA2, chloroplastic  [Arabidopsis thaliana ]
    OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
    OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
    OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
    OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
    OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
    OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOMMMMMMMMMMMMMMMMMMMMMMMiiiiii
    iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii
    iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii
    iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii
    iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii
    iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiMMMMMMMMMMMMMMMMMMMMMMMoooooooooMMMMMMMMMMMMMMMM
    MMiiiiiiiiiiii

## Posterior probabilies file

A file containing the posterior probabilities for each label for plotting.

    $ cat B9DFX7|1B|HMA8_ARATH.plot
    inside membrane outside
    0.20341044516 0.0 0.79658955484
    0.210104176071 2.77194446172e-08 0.78989579621
    0.189291062167 3.11365191554e-08 0.810708906697
    0.253334801857 7.17866017044e-07 0.746664480277
    0.126185012808 1.34197873962e-05 0.873801567405
    ...

If the `-p` flag is set a plot in PDF format will also be produced, following
the same naming scheme as the other output files.

# API

You can also use `pyTMHMM` as a library:

    import pyTMHMM
    annotation, posterior = pyTMHMM.predict(sequence_string)

This returns the annotation as a string and the posterior probabilities for
each label as a numpy array with shape `(len(sequence), 3)` where column 0, 1
and 2 corresponds to being inside, transmembrane and outside, respectively.

If you don't need the posterior probabilities set `compute_posterior=False`,
this will save computation:

    annotation = pyTMHMM.predict(
        sequence_string, compute_posterior=False
    )
