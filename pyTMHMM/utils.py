from collections import namedtuple


FastaEntry = namedtuple('FastaEntry', 'id, description, sequence')


def load_posterior_file(fileobj):
    # skip header
    fileobj.readline()
    res = []
    for line in fileobj:
        res.append(map(float, line.split()))
    return zip(*res)


def dump_posterior_file(fileobj, posterior):
    print('inside', 'membrane', 'outside', file=fileobj)
    for i in range(posterior.shape[0]):
        line = '{} {} {}'.format(
            posterior[i, 0], posterior[i, 1], posterior[i, 2])
        print(line, file=fileobj)


def load_fasta_file(fileobj):
    """load_fasta_file

    Returns a list of `(id, description, sequence)` tuples. The `id` and
    `description` is extracted from the header line. The `id` is the part of
    the header line before the first whitespace character. The `description` 
    is everything coming after the first whitespace character and not all 
    FASTA headers have descriptions.
    """
    entries = []
    header = ''
    sequence = ''

    def append_entry(header, sequence):
        arr = header.split(None, 1)
        if len(arr) == 1:
            arr.append("")
        entries.append(FastaEntry(arr[0], arr[1], sequence))

    for line in fileobj:
        if line.startswith(">"):
            # Beginning of file
            if header == '':
                header = line[1:].strip()
            # Middle of file
            else:
                append_entry(header, sequence)
                sequence = ''
                header = line[1:].strip()
        else:
            sequence += line.strip()
    # End of file
    if header != '' and sequence != '':
        append_entry(header, sequence)
    return entries

