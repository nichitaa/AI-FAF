from production import IF, AND, THEN, OR, forward_chain

RULES = (
    IF(OR('(?x) prefers expensive restaurants',
          '(?x) rents a car'),
       THEN('(?x) has big budget')),

    IF(OR('(?x) rents cycling equipment',
          '(?x) spends time visiting museums/theatres'),
       THEN('(?x) has moderate budget')),

    IF(AND('(?x) stays at a hostel',
           '(?x) prefers public transport'),
       THEN('(?x) has small budget')),

    IF(AND('(?x) has moderate budget',
           '(?x) has an athletic build',
           '(?x) is interested in extreme sports'),
       THEN('(?x) is an Adventure tourist type')),

    IF(AND('(?x) has moderate budget',
           '(?x) participates in local cultural events',
           '(?x) is interested in local culture and history'),
       THEN('(?x) is an Cultural tourist type')),

    IF(AND('(?x) has big budget',
           '(?x) stays at five-star hotels',
           '(?x) prioritizes high-end and exclusive experiences'),
       THEN('(?x) is an Luxury tourist type')),

    IF(AND('(?x) has big budget',
           '(?x) has a busy schedule',
           '(?x) is mostly attending conferences and meetings'),
       THEN('(?x) is an Business tourist type')),

    IF(AND('(?x) has small budget',
           '(?x) is interested in exploring new destinations',
           '(?x) is carrying belongings in a rucksack'),
       THEN('(?x) is an Backpacker tourist type')),

    IF(AND('(?x) prefers public transport',
           '(?x) loves local cuisine',
           '(?x) knows city\'s history and culture'),
       THEN('(?x) is an Loonie')),
)

DATA = (
    'marta is interested in extreme sports',
    'marta has an athletic build',
    'marta rents cycling equipment',
    'marta loves local cuisine',
    'marta prefers public transport',
    'marta knows city\'s history and culture'
)

print(forward_chain(RULES, DATA, verbose=True))
