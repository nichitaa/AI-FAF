import random

from production import AND, populate


def get_statements(q):
    print()
    if q['type'] == 'yes/no':
        ans = input(q['text']).lower().strip()
        if ans == 'yes' or ans == 'y':
            return (q['statement'],)
        elif ans == 'no' or ans == 'n':
            return None
        else:
            print('invalid answer (valid answers are yes or no)')
            return get_statements(q)

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


def generate_questions(name, rules):
    binding = {'x': name}
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
