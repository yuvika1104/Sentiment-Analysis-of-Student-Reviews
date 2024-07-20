#importing libraries
from joblib import dump
import pandas as pd
import numpy as np
#reading the dataset
dataset = pd.read_csv('new_coursera_reviews.csv')
dataset= dataset.drop_duplicates(subset='Review')

#assigning labels
dataset["labels"]= dataset["Rating"].map({ 1: "Negative", 2:"Negative",3:"Neutral", 4: "Positive",5: "Positive"})

#reducing the dataset to tweets and labels
dataset=dataset[["Review","labels"]]
print(dataset.head())

#libraries  for NLP
import re
import nltk
import string
# importing stopwords
nltk.download('stopwords')
from nltk.corpus import stopwords
stopword=set(stopwords.words('english'))

#Stemmer
stemmer=nltk.SnowballStemmer('english',ignore_stopwords=True)

#function to clean the text
def clean(rev):
  rev= rev.lower()
  rev= re .sub('[.?]','', rev)
  rev= re.sub('<.?>+', '', rev)
  rev= re.sub('[%s]' % re.escape(string.punctuation), '', rev)
  rev= re.sub('\n', '', rev)
  rev= [word for word in rev.split(' ')if word not in stopword]
  rev= " ".join(rev)
  rev= [stemmer.stem(word) for word in rev.split(' ')]
  rev= " ".join(rev)
  return rev
#cleaning the dataset
dataset["Review"] = dataset["Review"].apply(clean)

# #seperating the dataset
x= np.array(dataset["Review"])
y= np.array(dataset["labels"])
from sklearn.feature_extraction.text import TfidfVectorizer

# Forming the TF-IDF model
v = TfidfVectorizer()
v.fit(x)

def vectorize(train_data):
    X = v.transform(train_data)
    return X
if __name__ == "__main__":
  X = vectorize(x)

  from sklearn. model_selection import train_test_split
  X_train,X_test,y_train,y_test= train_test_split(X ,y, test_size=0.33, random_state= 42)

  # from sklearn. tree import DecisionTreeClassifier
  # model= DecisionTreeClassifier(random_state=100)
# # Training the model
  # model.fit(X_train, y_train)
#0.8737027923397882
  from sklearn.naive_bayes import ComplementNB

# # Create and train a Complement Naive Bayes model
  # model = ComplementNB(alpha = 2.3)
  # model.fit(X_train, y_train)
# 0.6  0.8754145715202739
# 0.7 0.8806034021611212
# 0.5 0.8681127634535145
# 0.4 0.8578420883706002
# 0.8 0.8840002139723976
# 0.9 0.8858457259013587
# 1.0 0.8871830533861131
# 1.1 0.8884668877714775
# 1.2 0.8888145929175136
# 1.3 0.8895634963089761
# 1.4 0.8902321600513534
# 1.5 0.8909008237937306
# 2.3 0.8919974323312293
# 4.8 0.8929335615705574
# 14.1 0.8938161977104954

  from sklearn.svm import SVC

  # model = SVC(kernel='linear')  # Use linear kernel for simplicity
#   # model.fit(X_train, y_train)
# #0.9149994650690061
# #0.914063335829678

  from sklearn.ensemble import RandomForestClassifier,VotingClassifier
#   # model = RandomForestClassifier(n_estimators=100, random_state=42)  # Use 100 trees for example
#   # model.fit(X_train, y_train)
# # 0.9002888627367069
  print("Model building")

  cnb= ComplementNB(alpha=2.3)

  svm = SVC(kernel='rbf', probability=True,class_weight='balanced')

  rf = RandomForestClassifier(n_estimators=100, random_state=42,class_weight='balanced')

# Creating an ensemble of models using VotingClassifier
  model = VotingClassifier(estimators=[('svm', svm), ('rf', rf),('cnb',cnb)], voting='soft')
  model.fit(X_train, y_train)
  
  
#0.9062265967690168

#0.9055569826183748

#0.9024459856722893

# Save model
  dump(model, 'saved_model.joblib')
  
#testing the model
  y_pred= model.predict (X_test)

#accuracy of model
  from sklearn.metrics import accuracy_score
  print(accuracy_score(y_test,y_pred))
