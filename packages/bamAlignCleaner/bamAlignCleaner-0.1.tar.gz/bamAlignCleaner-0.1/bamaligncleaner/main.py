import pysam


def filter_bam(bam, output):
    """Filter bam file to remove unaligned references

    Args:
        bam (str): Path to alignement file
        output (str): Path to output alignment file
    """

    mode = {"sam": "r", "bam": "rb", "cram": "rc"}
    filetype = bam.split(".")[-1]    
    alignment = pysam.AlignmentFile(bam, mode[filetype])
    total_refs = alignment.nreferences
    present_refs = set()

    for ref_stat in alignment.get_index_statistics():
        refname = ref_stat[0]
        nb_mapped_reads = ref_stat[1]
        if nb_mapped_reads > 0:
            present_refs.add(refname)
    refs = tuple(present_refs)
    reflens = list()
    for ref in refs:
        reflens.append(alignment.get_reference_length(ref))

    outbam = pysam.AlignmentFile(output, "wb", reference_names=refs, reference_lengths=reflens)
    for ref in refs:
        for read in alignment.fetch(ref):
            outbam.write(read)

    print(f"{total_refs - len(present_refs)} references with unaligned reads were removed from index")
    print(f"Output bam file written to: {output}")

