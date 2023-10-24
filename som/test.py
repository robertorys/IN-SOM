from som import somObject

N = 100

som = somObject(N, 1000,'data/sensorimotor.csv')

som.init_weights()

som.graph()

som.init_training()

som.save('som_test_1', 'som_test_1_100x100.json')

som.graph()
