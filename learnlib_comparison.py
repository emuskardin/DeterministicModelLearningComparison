import os
from statistics import mean

from aalpy import load_automaton_from_file, RandomWordEqOracle, AutomatonSUL, run_Lstar, run_KV, RandomWMethodEqOracle


def automata_increase(learning_alg):
    files = os.listdir('models/stateIncrease')
    files.sort(key=len)
    states_files = [files[i:i + 10] for i in range(0, len(files), 10)]

    all_times = []
    all_queries = []
    all_steps = []

    for num_states in states_files:
        print('Experiments for', num_states[0])
        times, queries, steps = [], [], []

        for file in num_states:
            model = load_automaton_from_file(f'models/stateIncrease/{file}', automaton_type='mealy')
            input_al = model.get_input_alphabet()
            sul = AutomatonSUL(model)

            eq_oracle = RandomWordEqOracle(input_al, sul, min_walk_len=10, max_walk_len=40, num_walks=3500)

            learned_model, data = learning_alg(input_al, sul, eq_oracle, 'mealy', print_level=0, return_data=True)

            times.append(data['learning_time'])
            queries.append(data['queries_learning'])
            steps.append(data['steps_learning'])

        all_times.append(mean(times))
        all_queries.append(mean(queries))
        all_steps.append(mean(steps))

    print('Times')
    print(all_times)
    print('Queries')
    print(all_queries)
    print('Steps')
    print(all_steps)


def alphabet_increase(learning_alg):
    files = os.listdir('models/alphIncrease')
    files.sort(key=len)
    states_files = [files[i:i + 10] for i in range(0, len(files), 10)]

    all_times = []
    all_queries = []
    all_steps = []

    for num_states in states_files:
        print('Experiments for', num_states[0])
        times, queries, steps = [], [], []

        for file in num_states:
            model = load_automaton_from_file(f'models/alphIncrease/{file}', automaton_type='mealy')
            input_al = model.get_input_alphabet()
            sul = AutomatonSUL(model)

            eq_oracle = RandomWordEqOracle(input_al, sul, min_walk_len=10, max_walk_len=40, num_walks=3500)

            learned_model, data = learning_alg(input_al, sul, eq_oracle, 'mealy', print_level=0, return_data=True)

            times.append(data['learning_time'])
            queries.append(data['queries_learning'])
            steps.append(data['steps_learning'])

        all_times.append(mean(times))
        all_queries.append(mean(queries))
        all_steps.append(mean(steps))

    print('Times')
    print(all_times)
    print('Queries')
    print(all_queries)
    print('Steps')
    print(all_steps)


def compareReal():
    files = os.listdir('models/realWorldExamples')

    for file in files:
        print(file)
        model = load_automaton_from_file(f'models/realWorldExamples/{file}', 'mealy')
        input_al = model.get_input_alphabet()
        for learning_alg, alg_name in [(run_Lstar, 'L*'),(run_KV, 'KV')]:
            times, steps = [], []
            for _ in range(10):
                sul = AutomatonSUL(model)

                eq_oracle = RandomWordEqOracle(input_al, sul, num_walks=20000, min_walk_len=10, max_walk_len=50)

                learned_model, data = learning_alg(input_al, sul, eq_oracle, 'mealy', print_level=3, return_data=True)

                if learned_model.size != model.size:
                    print('Learning Failed')

                times.append(data['learning_time'])
                steps.append(data['steps_learning'])

            print(alg_name, ' time/steps')
            print(mean(times))
            print(mean(steps))


print('L*')
print('alphabet increase')
alphabet_increase(run_Lstar)
print('automata increase')
automata_increase(run_Lstar)

print('-----------------')

print('KV')
print('alphabet increase')
alphabet_increase(run_KV)
print('automata increase')
automata_increase(run_KV)

print('Benchmark models of real world systems')
compareReal()