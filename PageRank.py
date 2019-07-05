import numpy as np

ones = np.identity(3)
prob = np.array([[0.1, 0.6, 0.3],
				 [0.1, 0.25, 0.65],
				 [0.3, 0.5, 0.2]])

test = 0.15 * np.ones([3, 3]) / 3 + 0.85 * np.transpose(prob)
test = np.sum(test, axis = 0)
print test

subt = ones - np.transpose(prob)
subt = np.concatenate((subt, np.ones([1, 3])), axis = 0)

print subt

zero = np.zeros([3, 1])
zero = np.concatenate((zero, np.ones([1, 1])), axis = 0)
print zero

aswr = np.linalg.solve(subt[1:], zero[1:])
print aswr
