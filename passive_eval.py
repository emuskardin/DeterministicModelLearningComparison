import random

from aalpy import generate_random_mdp, run_Alergia, AutomatonSUL
from aalpy.learning_algs import run_RPNI
from aalpy.utils import generate_random_deterministic_automata
from aalpy.utils.HelperFunctions import all_prefixes, convert_i_o_traces_for_RPNI


model_type = 'mealy'
assert model_type in {'mealy', 'mdp'}

if model_type == 'det':
    model = generate_random_deterministic_automata(automaton_type='mealy', num_states=50,
                                               input_alphabet_size=5, output_alphabet_size=5)
else:
    model = generate_random_mdp(num_states=50, input_size=5, output_size=5)

dataset_sizes = list(range(5000, 100001, 5000))
dataset_sizes.insert(0, 1000)
min_seq_len = 5
max_seq_len = 30

input_al = model.get_input_alphabet()
sul = AutomatonSUL(model)
for num_seq in dataset_sizes:
    data = []
    print(num_seq)
    for _ in range(num_seq):
        seq_len = random.randint(min_seq_len, max_seq_len)
        random_seq = tuple(random.choices(input_al, k=seq_len))
        sul.pre()
        outputs = sul.query(random_seq)
        sul.post()

        if model_type == 'mealy':
            # ensure all prefixes are there
            prefix_closed = convert_i_o_traces_for_RPNI(list(zip(random_seq, outputs)))
            data.extend(prefix_closed)
        else:
            io_seq = list(zip(random_seq, outputs))
            io_seq.insert(0, model.initial_state.output)
            data.append(io_seq)

    if model_type == 'mealy':
        rpni_model = run_RPNI(data, automaton_type='mealy', print_info=True)
    else:
        alergia_model = run_Alergia(data, automaton_type=model_type, print_info=True)
