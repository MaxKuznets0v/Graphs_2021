import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("results_table.csv")
sigma = data['Сигма'].values
lambda_ = data['Лямбда'].values

accuracy = data['Метрика 1'].values
jaccard = data['Мера Жаккара'].values
acc = []
jacc = []
for i in range(len(accuracy)):
    acc.append(float(accuracy[i].replace(',', '.')))
    jacc.append(float(jaccard[i].replace(',', '.')))

def plot1():
    plt.scatter(sigma, acc)
    plt.xlabel('sigma')
    plt.ylabel('accuracy')
    plt.savefig('graphics/sigma_acc')

def plot2():
    plt.scatter(sigma, jacc)
    plt.xlabel('sigma')
    plt.ylabel('jaccard')
    plt.savefig('graphics/sigma_jacc')

def plot3():
    plt.scatter(lambda_, acc)
    plt.xlabel('lambda')
    plt.ylabel('accuracy')
    plt.savefig('graphics/lambda_acc')

def plot4():
    plt.scatter(lambda_, jacc)
    plt.xlabel('lambda')
    plt.ylabel('jaccard')
    plt.savefig('graphics/lambda_jacc')

plot1()
# plot2()
# plot3()
# plot4()
