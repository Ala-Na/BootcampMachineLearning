from data_spliter import data_spliter
from ridge import MyRidge
from polynomial_model_extended import add_polynomial_features
import numpy as np
import matplotlib.pyplot as plt
import os
import csv
import pandas as pd

def extract_datas(filename):
    assert os.path.isfile(filename)
    try:
        datas = pd.read_csv(filename)
        x = np.asarray(datas)
        return x[:, 1:x.shape[1] - 1].reshape(-1, 3), x[:, x.shape[1] - 1:].reshape(-1, 1)
    except:
        print('Something went wrong with extract_datas function')
        return None

def create_model_file():
	try:
		if (os.path.isfile('models.csv')):
			os.remove('models.csv')
		header = ['Form', 'Lambda', 'Loss on validation set', 'Thetas after fit', 'Alpha']
		f = open('models.csv', 'w')
		writer = csv.writer(f)
		writer.writerow(header)
		f.close()
	except:
		print('Something went wrong with create_model_file function')

def mean_normalization(x):
	mean = np.mean(x)
	std = np.std(x)
	x = (x - mean) / std
	return x

def add_model_to_file(name, loss, thetas, alpha, lambda_):
	try:
		df = pd.DataFrame({'Form' : name,  'Lambda': lambda_, 'Loss on validation set' : loss, \
			'Thetas after fit' : [thetas[:, 0].tolist()], 'Alpha' : alpha})
		df.to_csv('models.csv', mode='a', header=False, index=False)
	except:
		print('Something went wrong with add_model_to_file function')

def generate_polynomial_forms(max_degree, x, x_valid):
	forms = []
	x_poly = []
	x_val_poly = []
	for i in range(1, max_degree + 1):
		forms.append('x^' + str(i))
		x_poly.append(add_polynomial_features(x, i))
		x_val_poly.append(add_polynomial_features(x_valid, i))
	return forms, x_poly, x_val_poly

def recuperate_thetas(form, lambda_, len_thetas):
	try:
		df = pd.read_csv('models.csv')
		find_form = df.loc[df['Form'] == form]
		if find_form.empty:
			return [1] * len_thetas
		find_lambda = find_form.loc[find_form['Lambda'] == lambda_]
		if find_lambda.empty:
			return [1] * len_thetas
		thetas = (find_lambda['Thetas after fit'].values)[0].strip('[]').replace('\' ', '').split(',')
		thetas = [float(i) for i in thetas]
		if np.isnan(np.sum(thetas)):
			return [1] * len_thetas
		return thetas
	except:
		print('Something went wrong with recuperate_thetas function')
		return None

def train_model(max_iter, form, x, y, x_val, y_val, lambda_):
	print('Training model of polynomial form {} with lambda {}...'.format(form, lambda_))

	# Recuperate thetas from previous training
	thetas = [1] * (x.shape[1] + 1)

	# Create model
	ridge = MyRidge(thetas, alpha=0.007, lambda_=lambda_, max_iter=max_iter)
	ridge.fit_(x, y)

	# Evaluate model on validation set
	loss = ridge.loss_(y_val, ridge.predict_(x_val))
	print('Loss on validation set: {}\n'.format(loss))

	# Save model
	add_model_to_file(form, loss, ridge.theta, ridge.alpha, lambda_)


def find_best_model(filename):
	assert os.path.isfile(filename)
	try:
		df = pd.read_csv(filename)
		min_col = df.min()
		best = df.loc[df['Loss on validation set'] == min_col['Loss on validation set']]
		print('\033[92mBest model:\033[0m Form \033[34m{}\033[0m of loss \033[34m{}\033[0m with lambda \033[34m{}\033[0m'.format(best['Form'].values[0], best['Loss on validation set'].values[0], best['Lambda'].values[0]))
		return best
	except:
		print('Something went wrong with find_best_model function')
		return None

def launch_benchmark(max_iter):
	filename = './space_avocado.csv'

	# Create model file and extract data as array
	create_model_file()
	X, y = extract_datas(filename)

	# Value can be too big and screw up calculations : Let's scale it
	x = mean_normalization(X)

	# Split dataset i nto training/cross-validation and tests sets
	x_train, x_test, y_train, y_test = data_spliter(x, y, 0.6)
	x_valid, x_test, y_valid, y_test = data_spliter(x_test, y_test, 0.5)

	# Generate polynomial forms with maximum degree of 4
	forms, x_poly, x_val_poly = generate_polynomial_forms(4, x_train, x_valid)
	
	# Train differents models with differents lambdas
	lambdas = np.round(np.linspace(0, 1, 6), 2)
	for form in range(len(forms)):
		for lambda_ in lambdas:
			train_model(max_iter, forms[form], x_poly[form], y_train, x_val_poly[form], y_valid, lambda_)
	
	# Display best model found
	best = find_best_model('./models.csv')
	return best, X, y, x_train, y_train, x_valid, y_valid, x_test, y_test

if __name__ == '__main__':
	launch_benchmark(50000)
