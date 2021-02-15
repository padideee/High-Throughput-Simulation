# High-Throughput-Simulation
HTD is a wrapper for High Throughput Docking on Beluga

Installation:
- Create a python3 virtual environment, provide the path in `job.sh` as indicated
- Install the necessary libraries, including: Pandas, Numpy
- Install FlexAID, change the path in `utility.pl`
- Install Process_Ligand, change the path in `smile_gen.pl`


Run:
- An example available in `cmd.sh`
- Adjust the parameters in `job.sh`

```bash
$ sbatch job.sh
```

This will create the top_CF_#.txt, epoche_log_#.csv and only keeps the final top pdb files.

-- Author: Padideh Nouri
