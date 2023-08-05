High Performance Computing Accounting parser
============================================

hpcparse (HPC Scheduler/resource manager general purpose parser) is a Python library that adds functionality to parse HPC scheduler/Resource manager
infromation like Accounting, users, qos, ..etc. This librarary Fully supports SLURM, partial SGE and more to be added later
Parsers available currently are:

* AccountingParser "*"
    - Parser that gets a list of jobs based on accounting information "-"
    - Returns a list of job objects "-"

* AccountsParser "*"
    - Parser that get a list of accounts "-"
    - Returns list of account objects "-"

* ClusterParser "*"
    - Parser that get a list of clusters and associated information "-"
    - Returns a list of cluster object "-"

* ConfigParser "*"
    - Parser that reads in the scheduler's configuration imformation "-"
    - Returns  a configuration options object
    - Returns a list of node objects "-"
    - Returns a list of partition objects "-"
    - ordering a out put is configuration options, nodes, partitions

* QOSParser "*" 
    - Parser that gets a list of QOS's for the cluster "-"
    - Returns a list of qos objects "-" 

* UserParser "*"
    - Parser that gets a list of Users for the HPC "-"
    - Returns a list of user objects "-"
       
Prerequisites
^^^^^^^^^^^^^