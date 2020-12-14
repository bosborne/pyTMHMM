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
    """Load a FASTA-formatted file.

    Returns a list of `(id, description, sequence)` tuples. The `id` and
    `description` is extracted from the header line. The `id` is the part of
    the header line before the first whitespace character and must be unique.
    The `description` is everything coming after the first whitespace character
    and does not need to be unique, and not all FASTA headers have descriptions.
    """
    entries = []
    header = None
    sequence_parts = []

    def append_entry(header, sequence_parts, entries):
        arr = header.split(None, 1)
        if len(arr) == 1:
            arr.append('')
        sequence = ''.join(sequence_parts)
        entries.append(FastaEntry(arr[0], arr[1], sequence))

        header = None
        sequence_parts = []

    for line in fileobj:
        if line.startswith('#'):
            continue
        if line.startswith('>'):
            if header is None:
                header = line[1:].strip()
            else:
                append_entry(header, sequence_parts, entries)
                header = line[1:].strip()
        else:
            sequence_parts.append(line.strip())
    if header is not None:
        append_entry(header, sequence_parts, entries)
    return entries
