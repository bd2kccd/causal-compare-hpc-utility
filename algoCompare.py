import xml.etree.ElementTree as ET
from itertools import product
from xml.dom import minidom
import copy
import sys
import os

# Read in xml
file = 'comparison.xml'
filename = os.path.splitext(file)[0]
tree = ET.parse(file)
root = tree.getroot()

def validate():
    for parameter in root.iter('parameter'):
        if (parameter.get('name') == 'numRuns') and (len(parameter.get('value').split(',')) > 1):
            sys.exit('Error: parameter named "numRuns" can not take multiple values.')

# Reuse the current comparison and statistics elements
def copy_comparison():
    for comparison in root.iter('comparison'):
        return copy.deepcopy(comparison)

def copy_statistics():
    for statistics in root.iter('statistics'):
        return copy.deepcopy(statistics)

# Get all unique combinations of parameters
def get_parameters_combinations():
    # Create a list of params lists
    params_list = list()
    for parameter in root.iter('parameter'):
        values =  parameter.get('value')
        # Split the comma-separated values into a list
        values_list = values.split(',')

        # Add the list to the params lists for calculating combinations
        params_list.append(values_list)

    # All combinations of a list of lists
    params_combinations = list(product(*params_list))
    return params_combinations

# Create new simulations element for single config file
def create_new_simulations(simulation):
    new_sims = ET.Element('simulations')
    new_sims.append(simulation)
    return new_sims

# Create new algorithms element for single config file
def create_new_algorithms(algorithm):
    new_algos = ET.Element('algorithms')
    new_algos.append(algorithm)
    return new_algos

# Create a parameters element for each individual parameters combination
def create_new_parameters(combination):
    parameters_element = root.find('parameters')
    parameters_list = parameters_element.findall('parameter')
    count = len(parameters_list)

    new_parameters = ET.Element('parameters')
    for i in range(count):
        param = ET.Element('parameter')
        param.set('name', parameters_list[i].get('name'))
        param.set('value', combination[i])

        new_parameters.append(param)

    return new_parameters

# Return a pretty-printed XML string for the Element
def prettify(element):
    raw_string = ET.tostring(element, 'utf-8')
    reparsed = minidom.parseString(raw_string)
    # minidom's toprettyxml() produces rather unpretty XML with default values and adds un-necessary newlines
    formatted_string = reparsed.toprettyxml()
    # We'll do extra work to remove the junk new-lines
    return '\n'.join([line for line in formatted_string.split('\n') if line.strip()])

# Create single configuration xml file
def create_single_config_file(simulations, algorithms, parameters, index):
    new_root = ET.Element('comparisontool')
    
    # Append new elements
    new_root.append(simulations)
    new_root.append(algorithms)
    new_root.append(parameters)

    # Just copy over the old comparison and statistics
    new_root.append(copy_comparison())
    new_root.append(copy_statistics())

    # Pretty print the xml string 
    formatted_str = prettify(new_root)
    # Create the tree with the formatted string
    new_tree = ET.ElementTree(ET.fromstring(formatted_str))
    
    # Write to output file
    # Sufix a number to the filename
    new_tree.write(filename + "_" + str(index) + ".xml", encoding='utf-8', xml_declaration=True, method="xml")

# Validate parameter and generate individual config files
def create_config_files():
    # First validate 'numRuns' parameter value
    validate()

    # Create a single config case each individual simulation, algorithm, and parameters combination
    index = 1
    for simulation in root.iter('simulation'):
        for algorithm in root.iter('algorithm'):
            for params_combination in get_parameters_combinations():
                new_simulations = create_new_simulations(simulation)
                new_algorithms = create_new_algorithms(algorithm)
                new_parameters = create_new_parameters(params_combination)
                
                # Generating config file
                create_single_config_file(new_simulations, new_algorithms, new_parameters, index)
                index = index + 1

# Generate the sbatch.sh
def create_slurm_sbatch():
    # read in sbatch template
    sbatch = ''
    # By this step, we've changed the working directory
    with open('../sbatch.template', 'r') as file:
        template = file.read()
        sbatch = template.format(filename=filename)

    with open("sbatch.sh", "w") as script:
        script.write(sbatch)

# The general workflow here
def run():
    # Put all individual config files as well as the sbatch script 
    # into a folder named with the orginal file name
    os.mkdir(filename)
    os.chdir(filename)

    create_config_files()
    create_slurm_sbatch()

# Entry point
run()