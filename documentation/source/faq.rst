
.. _faq:

Canu FAQ
========


.. contents::
  :local:


What resources does Canu require for a bacterial genome assembly? A mammalian assembly?
-------------------------------------
    Canu will detect available resources and configure itself to run efficiently using those
    resources.  It will request resources, for example, the number of compute threads to use, Based
    on the ``genomeSize`` being assembled. It will fail to even start if it feels there are
    insufficient resources available.
    
    A typical bacterial genome can be assembled with 8GB memory in a few CPU hours - around an hour
    on 8 cores.  It is possible, but not allowed by default, to run with only 4GB memory.

    A well-behaved large genome, such as human or other mammals, can be assembled in 10,000 to
    25,000 CPU hours, depending on coverage.  A grid environment is strongly recommended, with at
    least 16GB available on each compute node, and one node with at least 64GB memory.  You should
    plan on having 3TB free disk space, much more for highly repetitive genomes.

    Our compute nodes have 48 compute threads and 128GB memory, with a few larger nodes with up to
    1TB memory.  We develop and test (mostly bacteria, yeast and drosophila) on laptops and desktops
    with 4 to 12 compute threads and 16GB to 64GB memory.

    
How do I run Canu on my SLURM / SGE / PBS / LSF / Torque system?
-------------------------------------
    Canu will detect and configure itself to use on most grids. You can supply your own grid
    options, such as a partition on SLURM or an account code on SGE, with ``gridOptions="<your
    options list>"`` which will passed to every job submitted by Canu.  Similar options exist for
    every stage of Canu, which could be used to, for example, restrict overlapping to a specific
    partition or queue.

    To disable grid support and run only on the local machine, specify ``useGrid=false``


What parameters should I use for my genome? Sequencing type?
-------------------------------------
    Canu is designed to be universal on a large range of PacBio (C2-P6-C4) and Oxford Nanopore
    (R6-R9) data. You can adjust parameters to increase efficiency for your datatype:
    
    **Nanopore R7 1D** and **Low Identity Reads**
       With R7 1D sequencing data, and generally for any reads lower than 80% identity, five to ten
       rounds of error correction are helpful. To run just the correction phase, use options
       ``-correct corOutCoverage=500 corMinCoverage=0 corMhapSensitivity=high``.  Use the output of
       the previous run (in ``asm.correctedReads.fasta.gz``) as input to the next round.

       Once corrected, assemble with ``-nanopore-corrected <your data> errorRate=0.1 utgGraphDeviation=50``

    **Nanopore R7 2D** and **Nanopore R9 1D**
       ``errorRate=0.025``

    **Nanopore R9 2D** and **PacBio P6**
       ``errorRate=0.013``

    **PacBio Sequel**
       Based on exactly one publically released `*A. thaliana* dataset <http://www.pacb.com/blog/sequel-system-data-release-arabidopsis-dataset-genome-assembly/>`_),
       ``errorRate=0.013 corMhapSensitivity=normal``


My assembly continuity is not good, how can I improve it?
-------------------------------------
    The most important determinant for assembly quality is sequence length, followed by the repeat
    complexity/heterozygosity of your sample.  The first thing to check is the amount of corrected
    bases output by the correction step.  This is logged in the stdout of Canu or in
    canu-scripts/canu.*.out if you are running in a grid environment. For example on `a
    haploid H. sapiens <https://www.ncbi.nlm.nih.gov/Traces/study/?acc=SAMN02744161>`_ sample:
    
    ::
    
       -- BEGIN TRIMMING
       --
       ...
       -- In gatekeeper store 'chm1/trimming/asm.gkpStore':
       --   Found 5459105 reads.
       --   Found 91697412754 bases (29.57 times coverage).
       ...

   Canu tries to correct the longest 40X of data. Some loss is normal but having output coverage
   below 20-25X is a sign that correction did not work well (assuming you have more input coverage
   than that). If that is the case, re-running with ``corMhapSensitivity=normal`` if you have >50X
   or ``corMhapSensitivity=high corMinCoverage=0`` otherwise can help. You can also increase the
   target coverage to correct ``corOutCoverage=100`` to get more correct sequences for assembly. If
   there are sufficient corrected reads, the poor assembly is likely due to either repeats in the
   genome being greater than read lengths or a high heterozygosity in the sample. Stay tuned for mor
   information on tuning unitigging in those instances.


What parameters can I tweak?
-------------------------------------
    For all stages:

    - ``errorRate`` is the expected error rate in _corrected_ reads.  It is a meta-parameter that
      sets other parameters.  It has been obsolesced and will eventually be removed.

    - ``minReadLength`` and ``minOverlapLength``.  The defaults are to discard reads shorter than
      1000bp and to not look for overlaps shorter than 500bp.  Increasing ``minReadLength`` can
      improve run time, and increasing ``minOverlapLength`` can improve assembly quality by removing
      false overlaps.  However, increasing either too much will quickly degrade assemblies by either
      omitting valuable reads or missing true overlaps.

    For correction:

    - ``corOutCoverage`` controls how much coverage in corrected reads is generated.  The default is
      to target 40X, but, for various reasons, this results in 30X to 35X of reads being generated.
    - ``corMinCoverage``, loosely, controls the quality of the corrected reads.  It is the coverage
      in evidence reads that is needed before a (portion of a) corrected read is reported.
      Corrected reads are generated as a consensus of other reads; this is just the minimum ocverage
      needed for the consensus sequence to be reported.  The default is based on input read
      coverage: 0x coverage for less than 30X input coverage, and 4x coverage for more than that.

    For assembly:

    - ``utgOvlErrorRate`` is essientially a speed optimization.  Overlaps above this error rate are
      not computed.  Setting it too high generally just wastes compute time, while setting it too
      low will degrade assemblies by missing true overlaps between lower quality reads.

    - ``utgGraphDeviation`` and ``utgRepeatDeviation`` what quality of overlaps are used in contig
      construction or in breaking contigs at false repeat joins, respectively.  Both are in terms of
      a deviation from the mean error rate in the longest overlaps.

    - ``utgRepeatConfusedBP`` controls how similar a true overlap (between two reads in the same
      contig) and a false overlap (between two reads in different contigs) need to be before the
      contig is split.  When this occurs, it isn't clear which overlap is 'true' - the longer one or
      the slightly shorter one - and the contig is split to avoid misassemblies.

    
My asm.contigs.fasta is empty, why?
-------------------------------------
    Canu will split the final output into three files:

    <prefix>.contigs.fasta
      Everything which could be assembled and is part of the primary assembly, including both unique
      and repetitive elements.  Each contig has several flags included on the fasta def line.

      **This file currently includes alternate paths.**

    <prefix>.bubbles.fasta
       Alternate paths in the graph which could not be merged into the primary assembly.

       **This file is currently ALWAYS empty.**

    <prefix>.unassembled.fasta
       Reads and small contigs that appear to be falsely assembled.  These are generally low quality
       reads or assemblies of a few low quality reads.

       **Small plasmids (unfortunately) tend to end up here.**

    The ``contigFilter=<minReads minLength singleReadSpan lowCovFraction lowCovDepth>`` parameter
    sets parameters for several filters that decide which contigs are 'unassembled'.  A contig is
    'unassembled' if it:
      - has fewer than minReads (2) reads, or
      - is shorter than minLength (1000), or
      - has a single read spanning singleReadSpan percent (75%) of the contig, or
      - has less than lowCovDepth (2) coverage over at least lowCovSpan fraction (0.75) of the contig
    The default filtering is ``contigFilter="2 1000 0.75 0.75 2"``.

    If you are assembling amplified or viral data, it is possible your assembly will be flagged as
    unassembled. Turn off filtering with the parameters ``contigFilter="2 1000 1.0 1.0 2"``.


Why is my assembly is missing my favorite short plasmid?
-------------------------------------
    Only the longest 40X of data (based on the specified genome size) is used for
    correction. Datasets with uneven coverage or small plasmids can fail to generate enough
    corrected reads to give enough coverage for assembly, resulting in gaps in the genome or zero
    reads for small plasmids.  Set ``corOutCoverage=1000`` (any value greater than your total input
    coverage) to correct all input data.

    This option is also recommended for metagenomic datasets where all data is useful for assembly.


Why do I get less corrected read data than I asked for?
-------------------------------------
    Some reads are trimmed during correction due to being chimeric or because there wasn't enough
    evidence to generate a quality corrected sequence.  Typically, this results in a 25% loss.
    Setting ``corMinCoverage=0`` will report all bases, even low those of low quality.  Canu will
    trim these in its 'trimming' phase before assembly.


What is the minimum coverage required to run Canu?
-------------------------------------
    For eukaryotic genomes, coverage more than 20X is enough to outperform current hybrid methods:
     - For less than 30X coverage, we recommend using ``corMinCoverage=0 errorRate=0.035`` to correct
       as many reads as possible.
     - For more than 60X coverage, we recommend using ``errorRate=0.013`` to slightly decrease the
       error rate to use only the better reads.  This is primarily an optimization for speed and
       generally does not improve (or degrade) assembly continuity.


My genome is AT (or GC) rich, do I need to adjust parameters?  What about highly repetitive genomes?
-------------------------------------
   On bacterial genomes, no adjustment of parameters is (usually) needed.  See the next question.

   On repetitive genomes with with a significantly skewed AT/GC ratio, the Jaccard estimate used by
   MHAP is biased.  Setting ``corMaxEvidenceErate=0.15`` is sufficient to correct for the bias in
   our testing.

   In general, with high coverage repetitive genomes (such as plants) it can be beneficial to set
   the above parameter anyway, as it will eliminate repetitive matches, speed up the assembly, and
   sometime improve unitigs.
