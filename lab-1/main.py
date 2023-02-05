# Pasecinic Nichita FAF 192

import random

from expert_system import get_statements, generate_questions
from production import forward_chain
from tourist_rules import TOURIST_RULES

if __name__ == '__main__':
    verbose = True
    data_set = ()
    found = False
    name = input('Enter person name that system will inspect: ')
    questions = generate_questions(name, TOURIST_RULES)

    while not found:
        if len(questions) <= 0:
            print('No more questions, extend the rules that defines a tourist type')
            found = True
        else:
            question = random.choice(questions)
            questions.remove(question)
            statements = get_statements(question)
            if statements is not None:
                data_set += statements
            forward_chain_result = forward_chain(TOURIST_RULES, data_set)

            if verbose:
                print('statements to append: ', statements)
                print('new data set: ', data_set)
            for statement in forward_chain_result:
                if '[answer]' in statement:
                    print(statement.replace('[answer]', ''))
                    found = True
