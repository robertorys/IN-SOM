from som import somObject

a = [2.214,0,0.429,0,0,2.429,0,0.357,1.071,0.357,0]
v = [1.375,0.25,1.562,0.562,2.375,1.938,0.529,1.471,2.118,2.529,1.706]
ab = [1.294,0.059,0.294,1.353,0,2.824,0,0,3.273,0.364,0.182]
print(len(a))

som = somObject(100, 1000, 'data/sensorimotor.csv', 'som_test_1_100x100.json')

som.graphDif(a, ab)

som.save('som_test_1', 'som_test_1_100x100.json')