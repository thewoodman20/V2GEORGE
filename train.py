import json
from main import tokenize, stem, bag_of_words
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from model import NeuralNet

with open('intents.json', 'r') as f:  #r opens the file in read mode
    intents = json.load(f)

all_words = [] #creates an empty array/list
tags = [] #collects all different patterns and know which different tags they have
xy = [] #holds both patterns and tags later on
for intent in intents['intents']:   #intents key, iterates for each tag and holds tag, pattern and response
    tag = intent['tag']
    tags.append(tag)
    for pattern in intent['patterns']: #want to apply tokenization
        w = tokenize(pattern)
        all_words.extend(w) #use extend because this is an array, we dont want to append because we dont want an array of arrays
        xy.append((w, tag))  #pattern and corresponding tag ex. [(['Hi'], 'greeting'), (['Hey'], 'greeting'), ...]

#we want to lower and stem the words, exclude punctuation characters
ignore_words = ['?','!',',','.']
all_words = [stem(w) for w in all_words if  w not in ignore_words]
all_words = sorted(set(all_words))  #removes duplicate elements so left with only unique words
tags = sorted(set(tags))


#now we want to create training data, create the bag of words

x_train = []
y_train = []
for (pattern_sentence, tag) in xy:
    bag = bag_of_words(pattern_sentence, all_words)
    x_train.append(bag)

    label = tags.index(tag)
    y_train.append(label) #CrossEntropyLoss

#now we are converting this into a numpy array
x_train = np.array(x_train)
y_train = np.array(y_train)
#still need to implement bag of words function
class ChatDataset(Dataset):
    def __init__(self):
        self.n_samples = len(x_train) # the number of samples is the number of words in the intents after it has converted to bag of words
        self.x_data = x_train
        self.y_data = y_train
    def __getitem__(self, index): #we can later access datasets with the index
        return self.x_data[index], self.y_data[index]

    def __len__(self):
        return self.n_samples

#hyperparameters
batch_size = 1
hidden_size = 8
output_size = len(tags)#num of different classes or tags
input_size =  len(x_train[0])#length of each bag of words created, has same length as all words array can use either
learning_rate = 0.001
num_epochs = 1000

dataset = ChatDataset()
train_loader = DataLoader(dataset=dataset, batch_size=batch_size, shuffle=True, num_workers=0)
#we can automatically iterate over this and get batch training

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = NeuralNet(input_size, hidden_size, output_size).to(device)

#loss and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

for epoch in range(num_epochs):
    for (words, labels) in train_loader:
        words = words.to(device, dtype=torch.float)
        labels = labels.to(device, dtype=torch.long)

        #forward pass
        outputs = model(words)
        loss = criterion(outputs, labels)

        #backwards and optimizer step
        optimizer.zero_grad()
        loss.backward() #calculates backpropagation
        optimizer.step()

    if (epoch+1) % 100 ==0:
        print(f'epoch {epoch+1}/{num_epochs}, loss={loss.item():.4f}')

print(f'final loss, loss={loss.item():.4f}')

data = {
    "model_state": model.state_dict(),
    "input_size": input_size,
    "output_size": output_size,
    "hidden_size": hidden_size,
    "all_words": all_words,
    "tags": tags
}
FILE = "data.pth"
torch.save(data, FILE)
print(f'training complete! File saved to {FILE}')