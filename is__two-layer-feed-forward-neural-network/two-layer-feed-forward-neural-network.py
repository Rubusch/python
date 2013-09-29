(60+5 points total) Write code to train the two-layer feed-forward neural network
with the architecture depicted in ﬁg. 2.
The training set consists of the following data points:
• Class 1 (t = 1): (4,2), (4,4), (5,3), (5,1), (7,2)
• Class 2 (t = −1): (1,2), (2,1), (3,1), (6,5), (3,6), (6,7), (4,6), (7,6)
The accompanying test set is:
• Class 1 (t = 1): (4,1), (5,2), (3,4), (5,4), (6,1), (7,1)
• Class 2 (t = −1): (3,2), (8,7), (4,7), (7,5), (2,3), (2,5)
This network uses sigmoidal activation function (i.e. the logistic function) for the
hidden layer and linear activation for the output layer. Also, don’t forget the biases
(even though they are not shown in the image). The weights (and biases) should
be randomly initialized from a uniform distribution in the range [−0.1, 0.1].

(5 points) Plot the data. Would the network be able to solve this task if it
had linear neurons only? Explain why.
(b) (30 points) Implement and apply backpropagation (with η = 1/30) until all
examples are correctly classiﬁed. (This might take a few thousand epochs)
(c) (10 points) Perform 10 runs with diﬀerent random initializations of the weights,
and plot the training and test error for each epoch averaged across the 10
runs. How many epochs does it take, on average, to correctly classify all
points. What do you notice?
(d) (15 points) Try diﬀerent learning rates η = [1, 1/3, 1/10, 1/30, 1/100, 1/300, 1/1000]
and plot the training error over 1000 epochs. What is the eﬀect of varying
the learning rate?
(e) (Bonus: 5 points) Vary the number of hidden units (from 1 to 10) and run
each network with 10 diﬀerent random initializations. Plot the average train
and test errors. Explain the eﬀect of varying the number of hidden units.

