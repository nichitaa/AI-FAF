from production import IF, THEN, AND, OR, match, populate


def get_and_or_rule(statements, rule): return AND(statements) if isinstance(rule, AND) else OR(statements)


def backchain_to_goal_tree(rules, desired_goal):
    results = [desired_goal]

    for rule in rules:
        # assuming that a consequent can have a single outcome (for this fw chaining implementation)
        consequent_template = rule.consequent()[0]  # THEN('(?x) has xy') -> '(?x) has xy'
        bindings = match(consequent_template, desired_goal)

        if bindings is not None:
            # found a match
            antecedent = rule.antecedent()  # IF(AND(rule), THEN(outcome)) -> AND(rule)
            if isinstance(antecedent, str):
                # traverse for the next desired goal
                next_desired_goal = populate(antecedent, bindings)
                results.append(backchain_to_goal_tree(rules, next_desired_goal))
                results.append(next_desired_goal)
            else:
                # is AND/OR
                next_desired_goal_list = [populate(template, bindings) for template in antecedent]
                next_rules = [backchain_to_goal_tree(rules, goal) for goal in next_desired_goal_list]
                results.append(get_and_or_rule(next_rules, antecedent))

    return OR(results)


r = (
    IF(OR('(?x) has x', '(?x) has y'),
       THEN('(?x) has x or y')),

    IF(AND('(?x) has x or y',
           '(?x) has z'),
       THEN('(?x) has x or y and z'))
)
res = backchain_to_goal_tree(r, 'bob has x or y and z')
print('result: ', res)
