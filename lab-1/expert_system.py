import random

from production import AND, populate
from production import forward_chain, backward_chain
from tourist_rules import TOURIST_RULES


def dataset_from_user_answer(q):
    print()
    if q['type'] == 'yes/no':
        ans = input(q['text']).lower().strip()
        if ans == 'yes' or ans == 'y':
            return (q['statement'],)
        elif ans == 'no' or ans == 'n':
            return None
        else:
            print('invalid answer (valid answers are yes or no)')
            return dataset_from_user_answer(q)

    elif q['type'] == 'multy-choice':
        print(q['text'])
        options = q['options']
        for option in options:
            print(str(option['value']) + ' - ' + option['text'])
        ans = input('answer: ').split()
        statements = []
        for value in ans:
            for option in options:
                if option['value'] == int(value):
                    statements.append(option['text'])
        return tuple(statements)


def generate_questions_for_fw(binding, rules):
    question_types = ['multy-choice', 'yes/no']
    questions = []
    for rule in rules:
        antecedent = rule.antecedent()

        question_type = random.choice(question_types)

        if isinstance(antecedent, AND) and len(antecedent) > 1 and question_type == 'multy-choice':
            options = [{
                'value': index,
                'text': populate(template, binding)
            } for index, template in enumerate(antecedent)]

            questions.append({
                'type': 'multy-choice',
                'text': 'Select one or more options (e.g.: 1 6 2 or type Enter to skip): ',
                'options': options
            })

        else:
            statements = [populate(template, binding) for template in antecedent]
            for statement in statements:
                questions.append({
                    'type': 'yes/no',
                    'text': f'Statement: {statement}. (answers: y/n): ',
                    'statement': statement
                })

    return questions


def node_to_flat_list(condition):
    flat = []
    for statement in condition:
        if isinstance(statement, str):
            flat.append(statement)
        else:
            flat += node_to_flat_list(statement)
    return flat


def generate_questions_for_bkw(condition):
    questions = []
    statements = node_to_flat_list(condition)
    for statement in statements:
        questions.append({
            'type': 'yes/no',
            'text': f'Statement: {statement}. (answers: y/n): ',
            'statement': statement
        })
    return questions


def generate_answers_for_bkw(binding, rules):
    answers = []
    for index, rule in enumerate(rules):
        consequent = populate(rule.consequent()[0], binding)
        if ':answer:' in consequent:
            answers.append({
                'value': index,
                'statement': consequent
            })
    return answers


def get_desired_goal_for_bkw(answers):
    print('\nPlease select a statement to check against: ')
    for ans in answers:
        formatted = ans['statement'].replace(':answer:', '')
        print(str(ans['value']) + ' - ' + formatted)
    guess = int(input('answer: ').strip())

    for ans in answers:
        if guess == ans['value']:
            return ans['statement']

    print('invalid input, try again')
    return get_desired_goal_for_bkw(answers)


def expert_system():
    name = input('Enter person name that system will inspect: ')
    bindings = {'x': name}
    chaining_type = input('Select chaining type (b - backward, Enter - forward): ')
    is_backward = chaining_type.lower() == 'b'

    if is_backward:
        answers = generate_answers_for_bkw(bindings, TOURIST_RULES)
        desired = get_desired_goal_for_bkw(answers)
        tree = backward_chain(TOURIST_RULES, desired)
        condition = tree[1]
        print('Condition tree for selected statement: ', condition)
        questions = generate_questions_for_bkw(condition)
    else:
        questions = generate_questions_for_fw(bindings, TOURIST_RULES)

    found = False
    verbose = True
    dataset = ()
    while not found:
        if len(questions) <= 0:
            if is_backward:
                print('[RESULT] Selected statement is not confirmed!')
            else:
                print('[RESULT] No more questions, extend the rules that defines a tourist type')
            found = True
        else:
            question = random.choice(questions)
            questions.remove(question)
            statements = dataset_from_user_answer(question)
            if statements is not None:
                dataset += statements

            if verbose:
                print('update dataset: ', dataset)
            forward_chain_result = forward_chain(TOURIST_RULES, dataset)

            for statement in forward_chain_result:
                if ':answer:' in statement:
                    if is_backward:
                        print('[RESULT] Selected statement was confirmed')
                    else:
                        print('[RESULT] ' + statement.replace(':answer:', ''))
                    found = True
