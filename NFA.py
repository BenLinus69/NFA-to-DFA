from .DFA import DFA
import itertools
from dataclasses import dataclass
from collections.abc import Callable
from typing import Set, Dict, Tuple
from collections import deque

EPSILON = ''  


@dataclass
class NFA[STATE]:
    S: set[str]
    K: set[STATE]
    q0: STATE
    d: dict[tuple[STATE, str], set[STATE]]
    F: set[STATE]

    def epsilon_closure(self, state: STATE) -> set[STATE]:
        epsilon_states: Set[STATE] = set()

        def recursive_closure(current_state: STATE):
            epsilon_states.add(current_state)

            epsilon_transitions = self.d.get((current_state, EPSILON), set())

            for next_state in epsilon_transitions:
                if next_state not in epsilon_states:
                    recursive_closure(next_state)

        recursive_closure(state)

        return epsilon_states

    def subset_construction(self) -> DFA[frozenset[STATE]]:
        dfa_states = set()
        dfa_alphabet = self.S
        dfa_transitions = {}
        dfa_initial_state = frozenset(self.epsilon_closure(self.q0))
        dfa_final_states = set()

        stack = [dfa_initial_state]

        while stack:
            current_states = stack.pop()
            dfa_states.add(current_states)

            for state in current_states:
                if state in self.F:
                    dfa_final_states.add(current_states)
                    break

            for symbol in dfa_alphabet:
                next_states = set()
                for state in current_states:
                    transitions = self.d.get((state, symbol), set())
                    for next_state in transitions:
                        next_states |= self.epsilon_closure(next_state)

                if next_states:
                    next_states = frozenset(next_states)
                    dfa_transitions[(current_states, symbol)] = next_states
                    if next_states not in dfa_states:
                        stack.append(next_states)
        
        dfa_states.add(frozenset({}))
        for state, symbol in itertools.product(dfa_states, dfa_alphabet):
            if (state, symbol) not in dfa_transitions:
                dfa_transitions[(state, symbol)] = frozenset() 
       
        


        return DFA(
            S=dfa_alphabet,
            K=dfa_states,
            q0=dfa_initial_state,
            d=dfa_transitions,
            F=dfa_final_states
        )
        
    def remap_states[OTHER_STATE](self, f: 'Callable[[STATE], OTHER_STATE]') -> 'NFA[OTHER_STATE]':
        pass
