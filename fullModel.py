from main import *
import io

# Create training set
# split into input (X) and output (Y) variables
X = dataset[0:17000,7:73]
Y = dataset[0:17000,73:79]

# Create test set
Xtest = dataset[17000:34000,7:73]
Ytest = dataset[17000:34000,73:79]


"""# Section 1: Set up the Model"""

# First create Model for all of our data
model = Sequential()
model.add(Dense(100,input_dim=66, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(40, input_dim=66, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(16,activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(6, activation='softmax'))

# Compile model
model.compile(loss='categorical_crossentropy', optimizer= 'AdaGrad', metrics=['accuracy'])

# Fit the model
model.fit(X, Y, epochs=250, batch_size=32)

b = model.predict_classes(x= X, batch_size= 32)

# evaluate the model
scores = model.evaluate(Xtest, Ytest)
print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))
