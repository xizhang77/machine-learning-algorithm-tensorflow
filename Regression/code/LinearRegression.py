# -*- coding: utf-8 -*-

import tensorflow as tf
import numpy as np

import matplotlib.pyplot as plt 


def inputs():
	'''
	Define the placeholder for X and Y
	:return type X: tensor
	:return type Y: tensor
	'''
	X = tf.compat.v1.placeholder(tf.float32, shape=[None])
	Y = tf.compat.v1.placeholder(tf.float32, shape=[None])

	return X, Y

def hypothesis( X, W, b ):
	'''
	Define the hypothesis
	:input X: The input tensor (data).
	:input W: The weight variable.
	:input b: The bias variable.
	:return: X*W + b.
	'''
	return X * W + b

def loss( X, Y, W, b ):
	'''
	Create the loss/cost function
	:input X: The data tensor.
	:input Y: The label tensor.
	:input W: The weight variable (tensor).
	:input b: The bias variable (tensor).
	:return: the loss.
	'''
	y_hat = hypothesis(X, W, b) # also known as predicted Y

	# Calculating the cost using: sum(y_hat - y)^2/n
	return tf.reduce_mean( tf.square(y_hat - Y) )


def ridgeLoss( X, Y, W, b, beta ):
	'''
	Create the loss/cost function with L2 Regularization (Ridge)
	'''
	y_hat = hypothesis(X, W, b)

	regularizer = tf.reduce_mean( tf.square(W) )
	# regularizer = tf.nn.l2_loss( W )

	loss = tf.reduce_mean( tf.square(y_hat - Y) )

	return loss + beta*regularizer

def lassoLoss( X, Y, W, b, beta ):
	'''
	Create the loss/cost function with L1 Regularization (LASSO)
	'''
	y_hat = hypothesis(X, W, b)

	regularizer = tf.reduce_sum( tf.abs(W) )
	loss = tf.reduce_mean( tf.square(y_hat - Y) )

	return loss + beta*regularizer

def train( rate, loss ):
	'''
	Optimize the loss function using gradient descent.
	:input rate: The learning_rate (tensor)
	:input loss: The loss/cost (tensor)
	:return: optimizing result
	'''

	opt = tf.compat.v1.train.GradientDescentOptimizer( learning_rate= rate )
	return opt.minimize( loss )


if __name__ == '__main__':

	## Generate artificial data
	# There will be 50 data points ranging from 0 to 50 
	x = np.linspace(0, 50, 50) 
	y = np.linspace(0, 50, 50) 
	# Adding noise to the random linear data 
	x += np.random.uniform(-4, 4, 50) 
	y += np.random.uniform(-4, 4, 50) 
	

	## Initialize the training variables
	# Two different ways to initialize: random or 0
	W = tf.Variable(tf.random_normal([1]), name='weight')
	b = tf.Variable(tf.random_normal([1]), name='bias')

	# W = tf.Variable(0.0, name='weight')
	# b = tf.Variable(0.0, name='bias')

	# Launch the graph in a session.
	with tf.compat.v1.Session() as sess:
		# Initialize the variables W and b.
		sess.run( tf.global_variables_initializer() )
		alpha, epochs = 0.0001, 500

		# Get the input tensors
		X, Y = inputs()

		# cost = loss( X, Y, W, b )
		cost = ridgeLoss( X, Y, W, b, 1.0 )
		optimizer = train( alpha, cost )

		for epoch in range( epochs ):
			sess.run( optimizer, feed_dict = {X : x, Y : y} )
			if epoch % 20 == 0:
				c = sess.run( cost, feed_dict = {X : x, Y : y} ) 
				print "Epoch : ", epoch, ", cost =", c, "W =", sess.run(W), "b =", sess.run(b)

		# Get the optimized result
		training_cost = sess.run( cost, feed_dict ={X: x, Y: y} ) 
		weight = sess.run(W) 
		bias = sess.run(b) 
		print "Training cost =", training_cost, "Weight =", weight, "bias =", bias, '\n'

		# Calculating the predictions 
		predictions = weight * x + bias 

		# Plotting the Results 
		plt.plot(x, y, 'ro', label ='Original data') 
		plt.plot(x, predictions, label ='Fitted line') 
		plt.title('Linear Regression Result') 
		plt.legend() 
		plt.show() 
