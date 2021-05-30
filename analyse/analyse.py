import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv(r"person1.csv")
p_sigma = data['Сигма'].values
p_lambda_ = data['Лямбда'].values
p_acc = data['Метрика 1'].values
p_jacc = data['Мера Жаккара'].values

data = pd.read_csv(r"elefant.csv")
e_sigma = data['Сигма'].values
e_lambda_ = data['Лямбда'].values
e_acc = data['Метрика 1'].values
e_jacc = data['Мера Жаккара'].values


def plot1():
    plt.scatter(p_sigma, p_acc, color='orange')
    plt.scatter(e_sigma, e_acc, color='blue')
    plt.xlabel('sigma')
    plt.ylabel('accuracy')
    plt.savefig('graphics/sigma_acc')

def plot2():
    plt.scatter(p_sigma, p_jacc, color='orange')
    plt.scatter(e_sigma, e_jacc, color='blue')
    plt.xlabel('sigma')
    plt.ylabel('jaccard')
    plt.savefig('graphics/sigma_jacc')

def plot3():
    plt.scatter(p_lambda_, p_acc, color='orange')
    plt.scatter(e_lambda_, e_acc, color='blue')
    plt.xlabel('lambda')
    plt.ylabel('accuracy')
    plt.savefig('graphics/lambda_acc')

def plot4():
    plt.scatter(p_lambda_, p_jacc, color='orange')
    plt.scatter(e_lambda_, e_jacc, color='blue')
    plt.xlabel('lambda')
    plt.ylabel('jaccard')
    plt.savefig('graphics/lambda_jacc')


plot1()
plot2()
plot3()
plot4()
