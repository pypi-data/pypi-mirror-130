import numpy as np
import pandas as pd
from sklearn import preprocessing
import plotly.express as px


class Neuron:
    """A single neuron with an activation function.
       Attributes:
          inputs: The number of inputs in the perceptron, not counting the bias.
          bias:   The bias term. By defaul it's 1.0.
          activ:  The activation function: linear (default), relu, sigmoid."""

    def __init__(self, inputs, bias = 1.0, activ = 'linear'):
        """Return a new Perceptron object with the specified number of inputs (+1 for the bias) and random initial weights.""" 
        self.weights = (np.random.rand(inputs+1) * 2) - 1 
        self.bias = bias
        self.activ = activ

    def run(self, x):
        """Run the perceptron. x is a python list with the input values."""
        sum = np.dot(np.append(x,self.bias),self.weights)
        if self.activ == 'linear':
          return sum
        if self.activ == 'sigmoid':
          return self.sigmoid(sum)
        if self.activ == 'relu':
          return self.relu(sum)
        if self.activ == 'mrelu':
          return self.mrelu(sum)

    def set_weights(self, w_init):
        """Overrides the np.random.rand() weights and the bias weight."""
        # w_init is a list of floats. Organize it as you'd like.
        self.weights=np.array(w_init, dtype='double')

    def set_activ(self, activ, param=0):
        """Overrides the 'linear' activation function."""
        self.activ = activ
        self.param = param

    def sigmoid(self, x):
        # return the output of the sigmoid function applied to x
        return 1/(1+np.exp(-x))
    
    def relu(self, x):
        # return the output of the relu function applied to x
        if x >= 0:
          return x
        return 0

    def mrelu(self, x):
        # return the output of the modified relu function applied to x
        if x >= 0:
          return x
        return self.param*x
    
class MultiLayerNeuron:     
    """A multilayer neuron class that uses the Neuron class above.
       Builds a list of neurons with the specific activation function.
       The activation function may be modified later using the set_activ method.
       For example: mln.network[layer][neuron].set_activ('linear').
       Attributes:
          layers:  A list with the number of neurons per layer. Including the input (first) and the output (last) layers.
          bias:    The bias term. The same bias is used for all neurons.
          activ:   The activation function: linear (default), relu, sigmoid."""

    def __init__(self, layers, bias = 1.0, activ='linear'):
        """Return a new MLP object with the specified parameters.""" 
        self.layers = np.array(layers,dtype=object)
        self.bias = bias
        self.network = [] # The list of lists of neurons (perceptrons).
        self.values = []  # The list of lists of neurons' (perceptrons') output values.
        self.d = []       # The list of lists of error terms (lowercase deltas)
        self.activ = activ

        # 2 nested loops to create neurons layer by layer
        for i in range(len(self.layers)): # outer loop iterates on each layer
            self.values.append([]) #The new list of values will be filled with zeros, for every neuron in the layer. 
            self.values[i] = [0.0 for j in range(self.layers[i])]
            self.d.append([])
            self.d[i] = [0.0 for j in range(self.layers[i])]                        
            self.network.append([])
            if i > 0:      #network[0] is the input layer, so it has no neurons
                for j in range(self.layers[i]): # inner loop iterates on each neuron in a layer
                    neur=Neuron(inputs = self.layers[i-1], bias = self.bias, activ = self.activ) # 
                    self.network[i].append(neur) # adding j perceptrons
        self.network = np.array([np.array(x) for x in self.network],dtype=object) #transforms list of lists to numpy array
        self.values = np.array([np.array(x) for x in self.values],dtype=object)
        self.d = np.array([np.array(x) for x in self.d],dtype=object)

    def set_weights(self, w_init): # set_weights of the MultiLayer class
        """Set the weights. 
           w_init is a list of lists with the weights for all but the input layer."""
        for i in range(len(w_init)):
            for j in range(len(w_init[i])):
                self.network[i+1][j].set_weights(w_init[i][j]) # set_weights for each perceptron i

    def set_activ(self, activ, param=0):
        """Set the activation function to every neurons."""
        for i in range(1,len(self.network)):
            for j in range(self.layers[i]):
                self.network[i][j].set_activ(activ, param) # set_activ for each neuron
        self.param=param
    
    def set_output_activ(self, activ, param=0):
        """Set the activation function to the last (output) neurons."""
        i = len(self.network)-1
        for j in range(self.layers[i]):
            self.network[i][j].set_activ(activ, param) 

    def printWeights(self):
        """Displays a summary of weights and activation functions per layer and neuron."""
        print()
        print('Layer 0 is the Input Layer')
        for i in range(1,len(self.network)):
            for j in range(self.layers[i]):
                print("Layer",i,"Neuron",j,":",self.network[i][j].weights,self.network[i][j].activ)
        print()

    def run(self, x):
        """Feed a sample x into the MultiLayer Neuron."""
        x = np.array(x,dtype=object)
        self.values[0] = x
        for i in range(1,len(self.network)):
            for j in range(self.layers[i]):  
                self.values[i][j] = self.network[i][j].run(self.values[i-1]) #runs preceptrons with the previous outputs
        return self.values[-1]

    def bp_classif(self, x, y, eta=0.2):
        """Run a single (x,y) pair with the backpropagation algorithm - Gradient Descent.
        Uses the derivative of the sigmoid function."""
        x = np.array(x,dtype=object)
        y = np.array(y,dtype=object)
        self.eta=eta
        # STEP 1: Feed a sample to the network 
        outputs = self.run(x)
        # STEP 2: Calculate the MSE
        error = 2*(y - outputs) # A list of outputs
        MSE = sum( error ** 2) / self.layers[-1] 
        # ∂MSE/∂weight=∂MSE/∂output*∂output/∂weight
        # STEP 3: Calculate the OUTPUT error terms
        # ∂MSE/∂output -- depends on neuron's activation function
        self.d[-1] = outputs * (1 - outputs) * (error) # derivative of the SIGMOID function 
        # STEP 4: Calculate the error term of EACH UNIT on each layer
        for i in reversed(range(1,len(self.network)-1)):
            for h in range(len(self.network[i])):
                fwd_error = 0.0
                for k in range(self.layers[i+1]): 
                    fwd_error += self.network[i+1][k].weights[h] * self.d[i+1][k]               
                self.d[i][h] = self.values[i][h] * (1-self.values[i][h]) * fwd_error # derivative of the SIGMOID function
        # STEPS 5 & 6: Calculate the deltas and update the weights
        for i in range(1,len(self.network)): # runs on layers
            for j in range(self.layers[i]): # runs on neurons
                for k in range(self.layers[i-1]+1): # runs on inputs. +1 for bias
                    if k==self.layers[i-1]:
                        delta = self.eta * self.d[i][j] * self.bias
                    else:
                        delta = self.eta * self.d[i][j] * self.values[i-1][k] # applying the delta rule
                    self.network[i][j].weights[k] += delta
        return MSE

    def sigmoid(self, x):
        # return the output of the sigmoid function applied to x
        return 1/(1+np.exp(-x))

    def deriv(self, value, i, j=0):
        if self.network[i][j].activ == 'linear':
          # print ('lin')
          return 1
        if self.network[i][j].activ == 'sigmoid':
          # print ('sig')
          return self.sigmoid(value)*(1-self.sigmoid(value))
        if self.network[i][j].activ == 'relu':
          if value > 0:
            # print ('re>')
            return 1
          else:
            # print ('re<')
            return 0
        if self.network[i][j].activ == 'mrelu':
          if value > 0:
            return 1
          else:
            return self.param

    def bp_regres(self, x, y, eta=0.2):
        """Run a single (x,y) pair with the backpropagation algorithm - Gradient Descent.
        Uses the derivative according each neuron's activation function."""
        x = np.array(x,dtype=object)
        y = np.array(y,dtype=object)
        self.eta=eta
        # STEP 1: Feed a sample to the network 
        outputs = self.run(x)
        # STEP 2: Calculate the MSE
        error = 2*(y - outputs) # A list of outputs
        MSE = sum( error ** 2) / self.layers[-1] 
        # ∂MSE/∂weight=∂MSE/∂output*∂output/∂weight
        # STEP 3: Calculate the OUTPUT error terms
        # ∂MSE/∂output -- depends on neuron's activation function
        for j in range (len(outputs)):
            self.d[-1][j] = self.deriv(outputs[j], len(self.network)-1) * error
        # STEP 4: Calculate the error term of EACH UNIT on each layer
        for i in reversed(range(1,len(self.network)-1)):
            for h in range(len(self.network[i])):
                fwd_error = 0.0
                for k in range(self.layers[i+1]): 
                    fwd_error += self.network[i+1][k].weights[h] * self.d[i+1][k] 
                self.d[i][h] = self.deriv(self.values[i][h], i, h) * fwd_error
        # STEPS 5 & 6: Calculate the deltas and update the weights
        for i in range(1,len(self.network)): # runs on layers
            for j in range(self.layers[i]): # runs on neurons
                for k in range(self.layers[i-1]+1): # runs on inputs. +1 for bias
                    # output=sum(weight*value)+bias*bias_weight
                    if k==self.layers[i-1]:
                        # ∂output/∂bias_weight=bias
                        delta = self.eta * self.d[i][j] * self.bias
                    else:
                        # ∂output/∂weight=value
                        delta = self.eta * self.d[i][j] * self.values[i-1][k] 
                    self.network[i][j].weights[k] += delta # applying the delta rule
        return MSE

class Regres:
    def __init__(self, layers, bias=1.0):
        self.layers = layers
        self.bias = bias
        self.regres_network = MultiLayerNeuron(layers=layers, bias=bias)

    def set_weights(self, w_init):
        self.regres_network.set_weights(w_init)

    def set_hidden_activ(self, activ, param=0):
        self.regres_network.set_activ(activ, param=0)
        self.regres_network.set_output_activ('linear')

    def fit(self, X, y, epochs, eta=0.2):
        self.epochs=epochs
        self.eta=eta
        self.weight_history=[]
        self.weight_history_table=[]
        self.MSE_history=[]
        for i in range(self.epochs):
            weight_epoch=[]
            weight_epoch_table=[]
            MSE = 0.0
            for j in range (len(X)):
                MSE +=  self.regres_network.bp_regres(X[j],[y[j]], self.eta)
            MSE = MSE / len(X)
            self.MSE_history.append(MSE)
            for m in range(1,len(self.layers)):
                weight_layer=[]
                for n in range(self.layers[m]):
                    neuron_w=self.regres_network.network[m][n].weights
                    neuron_w_list=[x for x in neuron_w]
                    weight_layer.append(neuron_w_list)
                    weight_epoch_table+=neuron_w_list
                weight_epoch.append(weight_layer)
            self.weight_history.append(weight_epoch)
            self.weight_history_table.append(weight_epoch_table)
        self.weight_history_table=pd.DataFrame(data=self.weight_history_table, columns=self.get_cols())
        print ("""Model fitted.
self.weight_history - list of lists of weights propagation
self.weight_history_table - pandas table of weights propagation
self.MSE_history - list of MSEs propagation""")

    def get_cols(self): 
        cols=[]
        for i in range(1,len(self.layers)):
            for h in range(self.layers[i]):
                for k in range(self.layers[i-1]+1): 
                    col="{}_{}_{}".format(i,h,k) 
                    cols.append(col)
        return cols 
    
    def printWeights(self):
        self.regres_network.printWeights()

    def run(self, x):
        return self.regres_network.run(x)

    def predict(self, x):
        y=[]
        for i in range(len(x)):
            y.append(self.run(x[i])[0])
        return y

# nuzhno podumat' kak vesa obratno perevesti. mozhet inverse_transform
class Regres_scale:
    def __init__(self, layers, bias=1.0):
        self.layers = layers
        self.bias = bias
        self.regres_network = MultiLayerNeuron(layers=layers, bias=bias)

    def set_weights(self, w_init):
        self.regres_network.set_weights(w_init)

    def set_hidden_activ(self, activ):
        self.regres_network.set_activ(activ)
        self.regres_network.set_output_activ('linear')

    def fit(self, x, y, epochs, eta=0.2):
        self.scaler = preprocessing.StandardScaler().fit(x)
        x_scaled=self.scaler.transform(x)
        self.epochs=epochs
        self.eta=eta
        for i in range(epochs):
            MSE = 0.0
            for j in range (len(x)):
                MSE +=  self.regres_network.bp_regres(x_scaled[j],[y[j]])
            MSE = MSE / len(x)
            # dobavit' istoriyu kak v Regres

    def printWeights(self):
        self.regres_network.printWeights()

    def run(self, x):
        return self.regres_network.run(x)

    def predict(self, x):
        y=[]
        for i in range(len(x)):
            y.append(self.run(x[i])[0])
        return y

    def get_standard_params(self, x):
        x2=np.array(x)
        mean=x2.mean(axis=0)
        stdev=x2.std(axis=0)
        return mean, stdev