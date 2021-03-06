gridOptions=-q big.q

genomeSize=4.8m
stopOnReadQuality=false

#
#  --   Found 14418 reads.
#  --   Found 139118335 bases (28.98 times coverage).
#  --
#  --   Read length histogram (one '*' equals 24.24 reads):
#  --        0    999      0 
#  --     1000   1999    227 *********
#  --     2000   2999    472 *******************
#  --     3000   3999    510 *********************
#  --     4000   4999    534 **********************
#  --     5000   5999    737 ******************************
#  --     6000   6999   1183 ************************************************
#  --     7000   7999   1490 *************************************************************
#  --     8000   8999   1697 **********************************************************************
#  --     9000   9999   1568 ****************************************************************
#  --    10000  10999   1344 *******************************************************
#  --    11000  11999   1114 *********************************************
#  --    12000  12999    891 ************************************
#  --    13000  13999    659 ***************************
#  --    14000  14999    534 **********************
#  --    15000  15999    374 ***************
#  --    16000  16999    309 ************
#  --    17000  17999    197 ********
#  --    18000  18999    165 ******
#  --    19000  19999    123 *****
#  --    20000  20999     76 ***
#  --    21000  21999     52 **
#  --    22000  22999     46 *
#  --    23000  23999     29 *
#  --    24000  24999     31 *
#  --    25000  25999     21 
#  --    26000  26999     15 
#  --    27000  27999      6 
#  --    28000  28999      3 
#  --    29000  29999      1 
#  --    30000  30999      2 
#  --    31000  31999      2 
#  --    32000  32999      2 
#  --    33000  33999      2 
#  --    34000  34999      0 
#  --    35000  35999      0 
#  --    36000  36999      0 
#  --    37000  37999      1 
#  --    38000  38999      1 
#

-nanopore-raw /data/regression/reads/escherichia_coli_k12.nanopore.map006-2.2d.fasta.xz

onSuccess=/work/canu/src/pipelines/sanity/success.escherichia_coli_k12.sh
