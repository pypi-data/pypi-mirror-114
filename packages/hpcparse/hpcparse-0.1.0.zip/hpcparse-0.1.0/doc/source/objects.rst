AccountingParser objects
========================


.. class:: hpcsap.AccountingParser()

    Create a new :mod:`AccountingParser` object. we provided a short list here
    as quick list reference:

    * filepath_ - string representation of the filepath.

    * num_lines_ - number of lines to read from the file. (default: ``None``)

    * start_ - line in file to start reading from. (default: ``0``)

The next few section describe in detail what each of the object parameters do and what they are used for.

filepath
^^^^^^^^^^^

All calls to the :class:`AccountingParser` constructor, will require the filepath argument
to be passed. This argument give the file name or absolute path to the file that is to be
parsed. Currently it takes a csv file from either Sun Grid Engine (SGE) or SLURM. 
standard argument::

    >>> parser = AccountingParser(filepath)
    >>> joblist = parser.slurm_Parser()
    usage: print(repr(joblist))

    {'account': 'beodefault', 'admin_comment': '', 'alloc_cpus': '8', 'alloc_gres': '', 'alloc_nodes': '1', 'alloc_tres': 'billing=8,cpu=8,mem=40G,node=1',
    'assoc_id': '435', 'ave_cpu': '', 'ave_cpu_freq': '', 'ave_disk_read': '', 'ave_disk_write': '', 'ave_pages': '', 'ave_rss': '', 'ave_vm_size': '',
    'block_id': None, 'cluster': 'beocat', 'comment': '', 'consumed_energy': '', 'consumed_energy_raw': '', 'cpu_time': '00:24:00', 'cpu_time_raw': None,
    'derived_exit_code': '0:0', 'elapsed': '00:03:00', 'elapsed_raw': '180', 'eligible': '2019-09-12T17:22:47', 'end': '2019-09-12T23:57:07', 'exit_code': '0:0',
    'gid': '2023', 'group': 'liu3zhen_users', 'job_id': '7427537_11', 'job_id_raw': '7435129', 'job_name': 'A188v021cg272', 'layout': '', 'max_disk_read': '',
    'max_disk_read_node': '', 'max_disk_read_task': '', 'max_disk_write': '', 'max_disk_write_node': '', 'max_disk_write_task': '', 'max_pages': '', 'max_pages_node': '',
    'max_pages_task': '', 'memory': '', 'memory_node': '', 'memory_task': '', 'max_vm_size': '', 'max_vm_size_node': '', 'max_vm_size_task': '', 'mcs_label': '',
    'min_cpu': '', 'min_cpu_node': '', 'min_cpu_task': '', 'num_cpus': '8', 'num_nodes': '1', 'node_list': 'hero12', 'num_tasks': '', 'priority': '1087',
    'partition': 'killable.q', 'qos': 'normal', 'qos_raw': '1', 'req_cpu_freq': 'Unknown', 'req_cpu_freq_min': 'Unknown', 'req_cpu_freq_max': 'Unknown',
    'req_cpu_freq_gov': 'Unknown', 'req_cpuS': '8', 'req_gres': '', 'req_mem': '5Gc', 'req_nodes': '1', 'req_tres': 'billing=8,cpu=8,mem=40G,node=1',
    'reservation': '', 'reservation_Id': '', 'reserved': '06:31:20', 'resv_cpu': '2-04:10:40', 'resv_cpu_raw': '187840', 'start': '2019-09-12T23:54:07',
    'state': 'PREEMPTED', 'submit': '2019-09-12 17:22:46', 'suspended': '00:00:00', 'system_cpu': '00:07.062', 'system_comment': '', 'time_limit': '23:00:00',
    'time_limit_raw': '1380', 'total_cpu': '04:03.303', 'tres_usage_in_ave': '', 'tres_usage_in_max': '', 'tres_usage_in_max_node': '', 'tres_usage_in_max_task': '',
    'tres_usage_in_min': '', 'tres_usage_in_min_node': '', 'tres_usage_in_min_task': '', 'tres_usage_in_tot': '', 'tres_usage_out_ave': '', 'tres_usage_out_max': '',
    'tres_usage_out_max_node': '', 'tres_usage_out_max_task': '', 'tres_usage_out_min': '', 'tres_usage_out_min_node': '', 'tres_usage_out_min_task': '',
    'tres_usage_out_tot': '', 'uid': '2022', 'user': 'liu3zhen', 'user_cpu': '03:56.241', 'wc_key': '', 'wc_key_id': '0',
    'working_dir': '/bulk/liu3zhen/research/A188asm/07-nanopolish2/3-np/3-np1/A188v021cg272', 'granted_pe': None, 'catagotries': None, 'block_ID': ''}

    usage print('the number of job is ' + str(len(joblist)))

    the number of job is 1





There is also a formatted str representation that can be sused to print individual jobs if needed.

num_lines
^^^^^^^^^

Some use cases may call for more control over the number of lines that are read in. In this case you can set the optional num_lines
parameter when calling the :class:`AccountingParser` constructor. The default for this values is zero, which tells the parser to read
all lines. If you pass a value greater than zero then the parser will read that number of lines and generate a joblist with the same
amount. This can be done using two arguments::

    >>> num = 2
    >>> parser = AccountingParser(filepath, num_lines=num)
    >>> joblist = parser.slurm_Parser()
    usage print(repr(joblist))

    [{'account': 'beodefault', 'admin_comment': '', 'alloc_cpus': '8', 'alloc_gres': '', 'alloc_nodes': '1', 'alloc_tres': 'billing=8,cpu=8,mem=40G,node=1',
    'assoc_id': '435', 'ave_cpu': '', 'ave_cpu_freq': '', 'ave_disk_read': '', 'ave_disk_write': '', 'ave_pages': '', 'ave_rss': '', 'ave_vm_size': '',
    'block_id': None, 'cluster': 'beocat', 'comment': '', 'consumed_energy': '', 'consumed_energy_raw': '', 'cpu_time': '00:24:00', 'cpu_time_raw': None,
    'derived_exit_code': '0:0', 'elapsed': '00:03:00', 'elapsed_raw': '180', 'eligible': '2019-09-12T17:22:47', 'end': '2019-09-12T23:57:07', 'exit_code': '0:0',
    'gid': '2023', 'group': 'liu3zhen_users', 'job_id': '7427537_11', 'job_id_raw': '7435129', 'job_name': 'A188v021cg272', 'layout': '', 'max_disk_read': '',
    'max_disk_read_node': '', 'max_disk_read_task': '', 'max_disk_write': '', 'max_disk_write_node': '', 'max_disk_write_task': '', 'max_pages': '', 'max_pages_node': '',
    'max_pages_task': '', 'memory': '', 'memory_node': '', 'memory_task': '', 'max_vm_size': '', 'max_vm_size_node': '', 'max_vm_size_task': '', 'mcs_label': '',
    'min_cpu': '', 'min_cpu_node': '', 'min_cpu_task': '', 'num_cpus': '8', 'num_nodes': '1', 'node_list': 'hero12', 'num_tasks': '', 'priority': '1087',
    'partition': 'killable.q', 'qos': 'normal', 'qos_raw': '1', 'req_cpu_freq': 'Unknown', 'req_cpu_freq_min': 'Unknown', 'req_cpu_freq_max': 'Unknown',
    'req_cpu_freq_gov': 'Unknown', 'req_cpuS': '8', 'req_gres': '', 'req_mem': '5Gc', 'req_nodes': '1', 'req_tres': 'billing=8,cpu=8,mem=40G,node=1', 'reservation': '',
    'reservation_Id': '', 'reserved': '06:31:20', 'resv_cpu': '2-04:10:40', 'resv_cpu_raw': '187840', 'start': '2019-09-12T23:54:07', 'state': 'PREEMPTED',
    'submit': '2019-09-12 17:22:46', 'suspended': '00:00:00', 'system_cpu': '00:07.062', 'system_comment': '', 'time_limit': '23:00:00', 'time_limit_raw': '1380',
    'total_cpu': '04:03.303', 'tres_usage_in_ave': '', 'tres_usage_in_max': '', 'tres_usage_in_max_node': '', 'tres_usage_in_max_task': '', 'tres_usage_in_min': '',
    'tres_usage_in_min_node': '', 'tres_usage_in_min_task': '', 'tres_usage_in_tot': '', 'tres_usage_out_ave': '', 'tres_usage_out_max': '', 'tres_usage_out_max_node': '',
    'tres_usage_out_max_task': '', 'tres_usage_out_min': '', 'tres_usage_out_min_node': '', 'tres_usage_out_min_task': '', 'tres_usage_out_tot': '',
    'uid': '2022', 'user': 'liu3zhen', 'user_cpu': '03:56.241', 'wc_key': '', 'wc_key_id': '0',
    'working_dir': '/bulk/liu3zhen/research/A188asm/07-nanopolish2/3-np/3-np1/A188v021cg272', 'granted_pe': None, 'catagotries': None, 'block_ID': ''},
    
    {'account': 'beodefault', 'admin_comment': '', 'alloc_cpus': '8', 'alloc_gres': '', 'alloc_nodes': '1', 'alloc_tres': 'cpu=8,mem=40G,node=1', 
    'assoc_id': '435', 'ave_cpu': '00:04:03', 'ave_cpu_freq': '12.44M', 'ave_disk_read': '4.13M', 'ave_disk_write': '0.00M', 'ave_pages': '0',
    'ave_rss': '6823336K', 'ave_vm_size': '173072K', 'block_id': None, 'cluster': 'beocat', 'comment': '', 'consumed_energy': '0', 'consumed_energy_raw': '0',
    'cpu_time': '00:24:16', 'cpu_time_raw': None, 'derived_exit_code': '', 'elapsed': '00:03:02', 'elapsed_raw': '182', 'eligible': '2019-09-12T23:54:07',
    'end': '2019-09-12T23:57:09', 'exit_code': '0:15', 'gid': '', 'group': '', 'job_id': '7427537_11.batch', 'job_id_raw': '7435129.batch', 'job_name': 'batch',
    'layout': 'Unknown', 'max_disk_read': '4.13M', 'max_disk_read_node': 'hero12', 'max_disk_read_task': '0', 'max_disk_write': '0.00M',
    'max_disk_write_node': 'hero12', 'max_disk_write_task': '0', 'max_pages': '0', 'max_pages_node': 'hero12', 'max_pages_task': '0', 'memory': '6823336K',
    'memory_node': 'hero12', 'memory_task': '0', 'max_vm_size': '173072K', 'max_vm_size_node': 'hero12', 'max_vm_size_task': '0', 'mcs_label': '',
    'min_cpu': '00:04:03', 'min_cpu_node': 'hero12', 'min_cpu_task': '0', 'num_cpus': '8', 'num_nodes': '1', 'node_list': 'hero12', 'num_tasks': '1',
    'priority': '', 'partition': '', 'qos': '', 'qos_raw': '', 'req_cpu_freq': '0', 'req_cpu_freq_min': '0', 'req_cpu_freq_max': '0', 'req_cpu_freq_gov': '0',
    'req_cpuS': '8', 'req_gres': '', 'req_mem': '5Gc', 'req_nodes': '1', 'req_tres': '', 'reservation': '', 'reservation_Id': '', 'reserved': '', 'resv_cpu': '',
    'resv_cpu_raw': '', 'start': '2019-09-12T23:54:07', 'state': 'CANCELLED', 'submit': '2019-09-12 23:54:07', 'suspended': '00:00:00', 'system_cpu': '00:07.062',
    'system_comment': '', 'time_limit': '', 'time_limit_raw': '', 'total_cpu': '04:03.302',
    'tres_usage_in_ave': 'cpu=00:04:03,energy=0,fs/disk=4329968,mem=6823336K,pages=0,vmem=173072K',
    'tres_usage_in_max': 'cpu=00:04:03,energy=0,fs/disk=4329968,mem=6823336K,pages=0,vmem=173072K',
    'tres_usage_in_max_node': 'cpu=hero12,energy=hero12,fs/disk=hero12,mem=hero12,pages=hero12,vmem=hero12',
    'tres_usage_in_max_task': 'cpu=0,fs/disk=0,mem=0,pages=0,vmem=0',
    'tres_usage_in_min': 'cpu=00:04:03,energy=0,fs/disk=4329968,mem=6823336K,pages=0,vmem=173072K',
    'tres_usage_in_min_node': 'cpu=hero12,energy=hero12,fs/disk=hero12,mem=hero12,pages=hero12,vmem=hero12',
    'tres_usage_in_min_task': 'cpu=0,fs/disk=0,mem=0,pages=0,vmem=0', 'tres_usage_in_tot': 'cpu=00:04:03,energy=0,fs/disk=4329968,mem=6823336K,pages=0,vmem=173072K',
    'tres_usage_out_ave': 'energy=0,fs/disk=4990', 'tres_usage_out_max': 'energy=0,fs/disk=4990', 'tres_usage_out_max_node': 'energy=hero12,fs/disk=hero12',
    'tres_usage_out_max_task': 'fs/disk=0', 'tres_usage_out_min': 'energy=0,fs/disk=4990', 'tres_usage_out_min_node': 'energy=hero12,fs/disk=hero12',
    'tres_usage_out_min_task': 'fs/disk=0', 'tres_usage_out_tot': 'energy=0,fs/disk=4990', 'uid': '', 'user': '', 'user_cpu': '03:56.240', 'wc_key': '',
    'wc_key_id': '', 'working_dir': '', 'granted_pe': None, 'catagotries': None, 'block_ID': ''}]

    usage print('the number of job is ' + str(len(joblist)))

    the number of job is 2

If the number of lines to read is greater than the the number of lines in the file the this will terminate when it reaches the end of the file
and return a joblist that is the size equal to the lines in the file.

start
^^^^^

Some cases you may need to start reading lines that are further into the file. In this case you can set the optional start
parameter when calling the :class:`AccountingParser` constructor. The default for this values is zero, which tells the parser to start
reading from the begining of the file. If you pass a value greater than zero then the parser will skip over that number of lines and 
generate a joblist for each job on the remaining lines of the file. 
This can be done using two arguments::

    >>> num = 114082
    >>> parser = AccountingParser(filepath, start=num)
    >>> joblist = parser.slurm_Parser()
    usage print(repr(joblist))

    [{'account': 'beodefault', 'admin_comment': '', 'alloc_cpus': '8', 'alloc_gres': '', 'alloc_nodes': '1',
    'alloc_tres': 'billing=8,cpu=8,mem=40G,node=1', 'assoc_id': '435', 'ave_cpu': '00:00:00', 'ave_cpu_freq': '2.60G',
    'ave_disk_read': '0.00M', 'ave_disk_write': '0', 'ave_pages': '0', 'ave_rss': '0', 'ave_vm_size': '107952K',
    'block_id': None, 'cluster': 'beocat', 'comment': '', 'consumed_energy': '0', 'consumed_energy_raw': '0', 'cpu_time': '02:31:04',
    'cpu_time_raw': None, 'derived_exit_code': '', 'elapsed': '00:18:53', 'elapsed_raw': '1133', 'eligible': '2019-09-13T07:11:12',
    'end': '2019-09-13T07:30:05', 'exit_code': '0:0', 'gid': '', 'group': '', 'job_id': '7432242_1.extern', 'job_id_raw': '7437837.extern',
    'job_name': 'extern', 'layout': 'Unknown', 'max_disk_read': '0.00M', 'max_disk_read_node': 'dwarf60', 'max_disk_read_task': '0',
    'max_disk_write': '0', 'max_disk_write_node': 'dwarf60', 'max_disk_write_task': '0', 'max_pages': '0',
    'max_pages_node': 'dwarf60', 'max_pages_task': '0', 'memory': '0', 'memory_node': 'dwarf60', 'memory_task': '0',
    'max_vm_size': '107952K', 'max_vm_size_node': 'dwarf60', 'max_vm_size_task': '0', 'mcs_label': '',
    'min_cpu': '00:00:00', 'min_cpu_node': 'dwarf60', 'min_cpu_task': '0', 'num_cpus': '8', 'num_nodes': '1',
    'node_list': 'dwarf60', 'num_tasks': '1', 'priority': '', 'partition': '', 'qos': '', 'qos_raw': '',
    'req_cpu_freq': '0', 'req_cpu_freq_min': '0', 'req_cpu_freq_max': '0', 'req_cpu_freq_gov': '0',
    'req_cpuS': '8', 'req_gres': '', 'req_mem': '5Gc', 'req_nodes': '1', 'req_tres': '', 'reservation': '', 
    'reservation_Id': '', 'reserved': '', 'resv_cpu': '', 'resv_cpu_raw': '', 'start': '2019-09-13T07:11:12',
    'state': 'COMPLETED', 'submit': '2019-09-13 07:11:12', 'suspended': '00:00:00', 
    'system_cpu': '00:00:00', 'system_comment': '', 'time_limit': '', 'time_limit_raw': '',
    'total_cpu': '00:00:00', 'tres_usage_in_ave': 'cpu=00:00:00,energy=0,fs/disk=2012,mem=0,pages=0,vmem=107952K',
    'tres_usage_in_max': 'cpu=00:00:00,energy=0,fs/disk=2012,mem=0,pages=0,vmem=107952K',
    'tres_usage_in_max_node': 'cpu=dwarf60,energy=dwarf60,fs/disk=dwarf60,mem=dwarf60,pages=dwarf60,vmem=dwarf60',
    'tres_usage_in_max_task': 'cpu=0,fs/disk=0,mem=0,pages=0,vmem=0',
    'tres_usage_in_min': 'cpu=00:00:00,energy=0,fs/disk=2012,mem=0,pages=0,vmem=107952K',
    'tres_usage_in_min_node': 'cpu=dwarf60,energy=dwarf60,fs/disk=dwarf60,mem=dwarf60,pages=dwarf60,vmem=dwarf60',
    'tres_usage_in_min_task': 'cpu=0,fs/disk=0,mem=0,pages=0,vmem=0',
    'tres_usage_in_tot': 'cpu=00:00:00,energy=0,fs/disk=2012,mem=0,pages=0,vmem=107952K',
    'tres_usage_out_ave': 'energy=0,fs/disk=0', 'tres_usage_out_max': 'energy=0,fs/disk=0',
    'tres_usage_out_max_node': 'energy=dwarf60,fs/disk=dwarf60', 'tres_usage_out_max_task': 'fs/disk=0',
    'tres_usage_out_min': 'energy=0,fs/disk=0', 'tres_usage_out_min_node': 'energy=dwarf60,fs/disk=dwarf60',
    'tres_usage_out_min_task': 'fs/disk=0', 'tres_usage_out_tot': 'energy=0,fs/disk=0', 'uid': '', 'user': '',
    'user_cpu': '00:00:00', 'wc_key': '', 'wc_key_id': '', 'working_dir': '', 'granted_pe': None,
    'catagotries': None, 'block_ID': ''}]

    usage print('the number of job is ' + str(len(joblist)))

    the number of job is 1

This can also be combined with num_lines to start at a location with in the file and read x number of lines.


Job objects
===========


.. class:: hpcsap.Job()

The :class:`Job` is a helper class for use by the parser and should not be called directly, so we will not go into detail here.
