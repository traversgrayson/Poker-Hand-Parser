from main import *
import io


# Create training test
G = dataset[0:17000,7:13]
H = dataset[0:17000,73:79]

# Create Test set
gtest = dataset[17000:34000,7:13]
htest = dataset[17000:34000,73:79]



# create model
model2 = Sequential()
#model2.add(Dense(16,input_dim=12, activation='relu'))
model2.add(Dense(12,input_dim=6, activation='relu'))
model2.add(Dense(6, activation='softmax'))
model2.compile(loss='categorical_crossentropy', optimizer= 'AdaGrad', metrics=['accuracy'])
model2.fit(G, H, epochs= 200, batch_size=32)

scores = model2.evaluate(gtest, htest)
print("\n%s: %.2f%%" % (model2.metrics_names[1], scores[1]*100))
# c = model2.predict_classes(x= G, batch_size= 32)
#with open('report.txt','r') as fh: data = fh.read()
#with open('report.txt','w') as fh:
 #   # Pass the file handle in as a lambda function to make it callable
  #  model2.summary(print_fn=lambda x: fh.write(data + '\n' + x + '\n'))

plot_model(model2, to_file='model2.png')
