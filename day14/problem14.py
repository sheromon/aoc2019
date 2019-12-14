import json
import logging

import numpy as np


logging.basicConfig(level=logging.INFO)

def problem14a():
    file_name = 'problem14.txt'
    with open(file_name) as file_obj:
        reactions = read_reactions(file_obj)
    factory = Factory(reactions)
    num_ore = factory.calc_ore_needed('FUEL', 1)
    for name, val in factory.leftovers.items():
        out_num = reactions[name]['num']
        if val > out_num:
            logging.info('Have %d %s, more than one batch (%d)' %
                         (val, name, out_num))
    with open('leftovers.json', 'w') as file_obj:
        json.dump(factory.leftovers, file_obj, indent=4)
    return num_ore


def read_reactions(reaction_spec):
    reactions = dict()
    for line in reaction_spec:
        inputs, out = line.strip().split('=>')
        out_num, out_name = out.strip().split()
        input_items = inputs.strip().split(',')
        input_dict = dict()
        for inp in input_items:
            in_num, in_name = inp.strip().split()
            input_dict[in_name] = int(in_num)
        reactions[out_name] = {
            'num': int(out_num),
            'inputs': input_dict,
        }
    return reactions


class Factory():

    def __init__(self, reactions):
        self.reactions = reactions
        self.leftovers = {}

    def calc_ore_needed(self, name, num_needed, level=0):
        if name == 'ORE':
            return num_needed
        if num_needed == 0:
            return 0

        spacer = 4 * level * ' '
        current_stock = self.leftovers.get(name, 0)
        num_taken = min(num_needed, current_stock)
        num_needed -= num_taken
        current_stock -= num_taken
        if num_taken:
            logging.debug('%sTaking %d from stock' % (spacer,  num_taken))
            logging.debug('%sNum needed reduced to %d' % (spacer, num_needed))

        batch_size = self.reactions[name]['num']
        batches = int(np.ceil(num_needed / batch_size))

        extra = batches * batch_size - num_needed
        current_stock += extra
        self.leftovers[name] = current_stock

        num_ore = 0
        inputs = self.reactions[name]['inputs']
        for inp_name, inp_num in inputs.items():
            logging.debug('%sNeed %d batches of %d %s to make %d %s' %
                          (spacer, batches, inp_num, inp_name,
                           batches * batch_size, name))
            num_ore += self.calc_ore_needed(inp_name, batches * inp_num, level + 1)
        return num_ore


def test_problem14a():
    test_input = [
        '10 ORE => 10 A',
        '1 ORE => 1 B',
        '7 A, 1 B => 1 C',
        '7 A, 1 C => 1 D',
        '7 A, 1 D => 1 E',
        '7 A, 1 E => 1 FUEL',
    ]
    reactions = read_reactions(test_input)
    factory = Factory(reactions)
    num_ore = factory.calc_ore_needed('FUEL', 1)
    assert num_ore == 31

    test_input = [
        '9 ORE => 2 A',
        '8 ORE => 3 B',
        '7 ORE => 5 C',
        '3 A, 4 B => 1 AB',
        '5 B, 7 C => 1 BC',
        '4 C, 1 A => 1 CA',
        '2 AB, 3 BC, 4 CA => 1 FUEL',
    ]
    reactions = read_reactions(test_input)
    factory = Factory(reactions)
    num_ore = factory.calc_ore_needed('FUEL', 1)
    assert num_ore == 165

    test_input = [
        '157 ORE => 5 NZVS',
        '165 ORE => 6 DCFZ',
        '44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL',
        '12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ',
        '179 ORE => 7 PSHF',
        '177 ORE => 5 HKGWZ',
        '7 DCFZ, 7 PSHF => 2 XJWVT',
        '165 ORE => 2 GPVTF',
        '3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT',
    ]
    reactions = read_reactions(test_input)
    factory = Factory(reactions)
    num_ore = factory.calc_ore_needed('FUEL', 1)
    assert num_ore == 13312

    test_input = [
        '2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG',
        '17 NVRVD, 3 JNWZP => 8 VPVL',
        '53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL',
        '22 VJHF, 37 MNCFX => 5 FWMGM',
        '139 ORE => 4 NVRVD',
        '144 ORE => 7 JNWZP',
        '5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC',
        '5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV',
        '145 ORE => 6 MNCFX',
        '1 NVRVD => 8 CXFTF',
        '1 VJHF, 6 MNCFX => 4 RFSQX',
        '176 ORE => 6 VJHF',
    ]
    reactions = read_reactions(test_input)
    factory = Factory(reactions)
    num_ore = factory.calc_ore_needed('FUEL', 1)
    assert num_ore == 180697


    test_input = [
        '171 ORE => 8 CNZTR',
        '7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL',
        '114 ORE => 4 BHXH',
        '14 VRPVC => 6 BMBT',
        '6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL',
        '6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT',
        '15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW',
        '13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW',
        '5 BMBT => 4 WPTQ',
        '189 ORE => 9 KTJDG',
        '1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP',
        '12 VRPVC, 27 CNZTR => 2 XDBXC',
        '15 KTJDG, 12 BHXH => 5 XCVML',
        '3 BHXH, 2 VRPVC => 7 MZWV',
        '121 ORE => 7 VRPVC',
        '7 XCVML => 6 RJRHP',
        '5 BHXH, 4 VRPVC => 5 LTCX',
    ]
    reactions = read_reactions(test_input)
    factory = Factory(reactions)
    num_ore = factory.calc_ore_needed('FUEL', 1)
    assert num_ore == 2210736


if __name__ == '__main__':
    test_problem14a()
    print(problem14a())
