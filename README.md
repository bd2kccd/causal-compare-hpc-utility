# causal-compare-hpc-utility

This is a utility tool written in Python to faciliate with running the [causal-compare](https://github.com/bd2kccd/causal-compare) CLI tool on HPC cluster. It generates individual configuration XML file based on the `causal-compare` configuration (multiple simulations and multiple algorithms with multiple combinations of parameters) so you can run the CLI tool for each single case and distribute the workload to the cluster nodes.

````
cd causal-compare-hpc-utility
python algoCompare.py
````

The above run will generate a directory named as the original configuration file name (e.e., `configuration/`) and create individual XML configuration files (`configuration_1.xml`, `configuration_2.xml`...) in that directory. It will also create a slurm batch script called `sbatch.sh`, which can be used as a slurm job array to submit those individual causal compare jobs.

````
cd configuration
sbatch sbatch.sh
````

If you want to get email notifiations of the jobs, you can add the following to the generated `sbatch.sh` script:

````
#SBATCH --mail-user=username@example.com
#SBATCH --mail-type=ALL
````
