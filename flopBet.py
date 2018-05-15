from final import *
import io

# Create training set
J = dataset[0:17000,7:25]
K = dataset[0:17000,73:79]

# Create test set
jtest = dataset[17000:34000,7:25]
ktest = dataset[17000:34000,73:79]



# create model
model3 = Sequential()
#model2.add(Dense(16,input_dim=12, activation='relu'))
#model3.add(Dense(16,input_dim=24, activation='relu'))
model3.add(Dense(24,input_dim =18, activation='relu'))
model3.add(Dense(14, activation='relu'))
model3.add(Dense(6, activation='softmax'))
model3.compile(loss='categorical_crossentropy', optimizer= 'AdaGrad', metrics=['accuracy'])
model3.fit(J, K, epochs= 200, batch_size=32)

scores = model3.evaluate(jtest, ktest)
print("\n%s: %.2f%%" % (model3.metrics_names[1], scores[1]*100))

# with open('report.txt','r') as fh: data = fh.read()
# with open('report.txt','w') as fh: 
#   model3.summary(print_fn=lambda x: fh.write(data + '\n' + x + '\n'  ))