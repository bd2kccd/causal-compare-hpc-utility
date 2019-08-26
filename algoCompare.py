import xml.etree.ElementTree as ET
from itertools import product
from xml.dom import minidom
import copy
from uuid import uuid4

from pprint import pprint



tree = ET.parse('comparison.xml')
root = tree.getroot()

pprint(root)
pprint(root.tag)


def copy_comparison():
    for comparison in root.iter('comparison'):
        return copy.deepcopy(comparison)

def copy_statistics():
    for statistics in root.iter('statistics'):
        return copy.deepcopy(statistics)


# Create a list of param lists
params_list = list()
for parameter in root.iter('parameter'):
    print(parameter.tag, parameter.attrib)
    values =  parameter.get('value')
    values_list = values.split(',')
    params_list.append(values_list)

# All combinations of a list of lists
params_combinations = list(product(*params_list))


def create_sims(simulation):
    new_sims = ET.Element('simulations')
    new_sims.append(simulation)
    return new_sims

def create_algos(algorithm):
    new_algos = ET.Element('algorithms')
    new_algos.append(algorithm)
    return new_algos

# Create a parameters element for each parameters combination
def create_params(combination):
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
def prettify(elem):
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    # Use 4 spaces
    return reparsed.toprettyxml()

# Create single configuration xml file
def create_single_config_file(simulations, algorithms, parameters):
    root = ET.Element('comparisontool')
    
    # Append new elements
    root.append(simulations)
    root.append(algorithms)
    root.append(parameters)

    # Just copy over the old comparison and statistics
    root.append(copy_comparison())
    root.append(copy_statistics())

    # Pretty print the xml string 
    formatted_str = prettify(root)

    # Create the tree with the formatted string
    tree = ET.ElementTree(ET.fromstring(formatted_str))
    
    # Write to output file
    # Use a random UUID to name the file
    tree.write(str(uuid4()) + "_config.xml", encoding='utf-8', xml_declaration=True, method="xml")



# Final output
# Calculate the number of single config cases
for simulation in root.iter('simulation'):
    for algorithm in root.iter('algorithm'):
        for params_combination in params_combinations:
            new_simulations = create_sims(simulation)
            new_algorithms = create_algos(algorithm)
            new_parameters = create_params(params_combination)

            # Generating config file
            create_single_config_file(new_simulations, new_algorithms, new_parameters)

