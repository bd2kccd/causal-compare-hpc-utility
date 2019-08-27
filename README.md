# causal-compare-hpc-utility

This is a utility tool written in Python to faciliate with running the [causal-compare](https://github.com/bd2kccd/causal-compare) CLI tool on HPC cluster. It generates individual configuration XML file based on the `causal-compare` configuration (multiple simulations and multiple algorithms with multiple combinations of parameters) so you can run the CLI tool for each single case and distribute the workload to the cluster nodes.

````
cd causal-compare-hpc-utility
python algoCompare.py
````

The above run will generate a directory named as the original configuration file name and create individual XML configuration files in that directory. Then you can run the individual comparison with the CLI tool.
