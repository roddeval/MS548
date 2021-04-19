# roderick devalcourt
# ms 548
# ms548_roderick_devalcourt_assignment_application_of_ai.py

from random import randint
from sklearn.linear_model import LinearRegression


def calculation(x, y, z):
    return x + (2 * y) + (3 * z)


TRAIN_LIMIT = 10
TRAIN_COUNT = 200

TRAIN_INPUT = list()
TRAIN_OUTPUT = list()

for i in range(TRAIN_COUNT):
    # get a random integer (max is 10)
    a = randint(0, TRAIN_LIMIT)
    b = randint(0, TRAIN_LIMIT)
    c = randint(0, TRAIN_LIMIT)
    # op = (a ^ b) + c
    # op = (a ** b) + c
    op = a + (2 * b) + (3 * c)

    TRAIN_INPUT.append([a, b, c])
    TRAIN_OUTPUT.append(op)

print('train_input')
print(TRAIN_INPUT)

print('train_output')
print(TRAIN_OUTPUT)

predictor = LinearRegression(n_jobs=-1)

predictor.fit(X=TRAIN_INPUT, y=TRAIN_OUTPUT)

a = 2
b = 3
c = 8

testing = [[a, b, c]]

outcome = predictor.predict(X=testing)
coefficients = predictor.coef_

print('testing with: {}\n', testing)
print('Outcome : {}\nCoefficients : {}'.format(outcome, coefficients))

actual = calculation(a, b, c)
print ('calculation : {}\n'.format(actual))

a = 4
b = 5
c = 1024

testing = [[a, b, c]]

outcome = predictor.predict(X=testing)

coefficients = predictor.coef_

print('testing with: {}\n', testing)
print('Outcome : {}\nCoefficients : {}'.format(outcome, coefficients))
actual = calculation(a, b, c)
print ('calculation : {}\n'.format(actual))

a = 13
b = 2
c = 1

testing2 = [[a, b, c]]

outcome = predictor.predict(X=testing2)
coefficients = predictor.coef_

print('testing with: {}\n', testing2)
print('Outcome : {}\nCoefficients : {}'.format(outcome, coefficients))
actual = calculation(a, b, c)
print ('calculation : {}\n'.format(actual))
