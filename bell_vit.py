import math
from collections import deque
import argparse

def bellman_ford(states, l, s, g, debug=False):
    T = len(states)
    k = len(l)
    F = [[0] * T for _ in range(k)]
    trace = [[0] * T for _ in range(k)]

    for i in range(k):
        F[i][0] = 0

    for t in range(1, T):
        for j in range(k):
            max_val = -float('inf')
            max_state = -1
            for i in range(k):
                val = F[i][t-1] + l[i] * (s ** -abs(j-i)) - g * states[t-1]
                if val > max_val:
                    max_val = val
                    max_state = i
            F[j][t] = max_val
            trace[j][t] = max_state
            if debug:
                print(f"t={t}, j={j}, F={F[j][t]}, trace={trace[j][t]}")

    max_states = max(range(k), key=lambda x: F[x][T-1])
    state_sequence = [max_states]
    current_time = sum(states)

    for t in range(T-1, 0, -1):
        prev_state = trace[state_sequence[-1]][t]
        state_sequence.append(prev_state)
        if prev_state != state_sequence[-2]:  
            print(f"{prev_state} [{sum(states[:t])} {current_time})")
            current_time = sum(states[:t])

    state_sequence.reverse()
    return state_sequence


def read_states(file_path):
    with open(file_path, 'r') as file:
        line = file.readline().strip()
        return [float(state) for state in line.split()]

def viterbi(states, s, g, debug=False):
    n = len(states)
    T = sum(states)

    non_zero_states = [i for i in states if i > 0]
    if not non_zero_states:
        raise ValueError("All states are zero, unable to compute.")
    
    min_state = min(non_zero_states)
    if min_state == 0:
        raise ValueError("Encountered zero state, unable to compute.")

    k = int(1 + math.log(T) / math.log(s) + math.log(1 / min_state) / math.log(s))

    l = [1 / s**i for i in range(k)]
    costs = [[float('inf')] * (n + 1) for _ in range(k)]
    costs[0][0] = 0
    path_trace = [[None] * (n + 1) for _ in range(k)]

    def log_f(lmbda, x):
        return -math.log(lmbda) + lmbda * x

    if debug:
        print([0.0] + [float('inf')] * (k - 1))

    for t in range(1, n + 1):
        x_t = states[t - 1]
        for j in range(k):
            min_cost = float('inf')
            min_state = None
            for prev_state in range(k):
                transition_cost = g * abs(j - prev_state) * math.log(n)
                cost = log_f(l[j], x_t) + costs[prev_state][t - 1] + transition_cost
                if cost < min_cost:
                    min_cost = cost
                    min_state = prev_state
            costs[j][t] = min_cost
            path_trace[j][t] = min_state

        if debug:
            print([round(costs[j][t], 2) for j in range(k)])

    state_sequence = [0] * n
    state_sequence[-1] = min(range(k), key=lambda j: costs[j][n])
    for t in range(n-1, 0, -1):
        state_sequence[t-1] = path_trace[state_sequence[t]][t]

    return state_sequence

def display_results(state_sequence, states):
    current_state = state_sequence[0]
    start_time = 0.0
    current_time = 0.0
    for i in range(1, len(state_sequence)):
        current_time += states[i-1]
        if state_sequence[i] != current_state:
            print(f"{current_state} [{start_time:.1f} {current_time:.1f})")
            current_state = state_sequence[i]
            start_time = current_time
    print(f"{current_state} [{start_time:.1f} {current_time + states[-1]:.1f})")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Detect bursts in message traffic using Viterbi or Trellis algorithm.')
    parser.add_argument('algorithm', choices=['viterbi', 'trellis'], help='Algorithm to use.')
    parser.add_argument('offsets_file', help='File containing message offsets.')
    parser.add_argument('-s', type=float, default=2, help='Parameter s of the algorithm (default: 2).')
    parser.add_argument('-g', type=float, default=1, help='Parameter g of the algorithm (default: 1).')
    parser.add_argument('-d', action='store_true', help='Enable debug mode for detailed output.')

    args = parser.parse_args()

    states = read_states(args.offsets_file)
    s = args.s
    g = args.g
    debug = args.d

    if args.algorithm == 'viterbi':
        state_sequence = viterbi(states, s, g, debug)
    elif args.algorithm == 'trellis':
        l = [1 / s**i for i in range(2)] 
        state_sequence = bellman_ford(states, l, s, g, debug)

    print(f"10 {state_sequence}")
    
    display_results(state_sequence, states)