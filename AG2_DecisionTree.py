#Alunos: João Victor Oliveira -  e Júlia da Silva Villela - 1799 GEC
#from pandas.core import frame
#Importação das bibliotecas
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import cohen_kappa_score
from sklearn.metrics import hamming_loss
import pandas as pd
import mysql.connector

#Conexão com o Banco de Dados
conector = mysql.connector.connect(host='localhost', database='statlog',
                                    user='root',
                                    password='R!bero123')

if conector.is_connected():
    db_info = conector.get_server_info()
    print("Conectado ao servidor do MySQL na versão: ", db_info)

    try:
        cursor = conector.cursor()
        cursor.execute("""select database();""")
        linha = cursor.fetchone()
        print("Conectado ao banco de dados", linha[0])
    finally:       
        #Leitura dos dados do banco
        dtFrame = pd.read_sql("SELECT * FROM germancredit", conector)
        pd.set_option('display.expand_frame_repr', False)
        print(dtFrame.head())
        cursor.close()
        conector.close()


#Tratamento dos dados vindos do banco
cols = ['laufkont','laufzeit','moral','verw','hoehe','sparkont','beszeit','rate','famges','buerge',
        'wohnzeit','verm','alter','weitkred','wohn','bishkred','beruf','pers', 'telef','gastarb', 'kredit']
X = dtFrame.iloc[:,[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21]].values
y = dtFrame.iloc[:, [21]].values

#Separação da porcentagem de dados para teste e treinamento da rede
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=0)

#Classificação através da Árvore de Decisão
classifier = DecisionTreeClassifier()
classifier.fit(X_train, y_train)

#Medindo a acurácia do modelo com base nas métricas de avaliação
y_predict = classifier.predict(X_test)

print('Acuracy:', metrics.accuracy_score(y_test, y_predict))
print(classification_report(y_test, y_predict))
print(cohen_kappa_score(y_test, y_predict))
print(hamming_loss(y_test, y_predict))
print(metrics.fbeta_score(y_test, y_predict, beta=0.5))

#Entrada de dados do usuário para avaliação de crédito
print('Entre com os dados solicitados abaixo: ')

while True:
    moral = int(input('Historico moral de credito: '))
    if (moral >= 1 and moral <= 4):
        break

#usar moral - histórico de cumprimento de contratos de crédito anteriores ou concorrentes
#usar verw - motivo do crédito
''' 
 0 : others             
 1 : car (new)          
 2 : car (used)         
 3 : furniture/equipment
 4 : radio/television   
 5 : domestic appliances
 6 : repairs            
 7 : education          
 8 : vacation           
 9 : retraining         
 10 : business
'''
#usar alter - idade do solicitante do crédito
#idade, entre 25 e 60 anos
#usar kredit - contrato de crédito foi cumprido?
'''
0 : bad 
1 : good
'''

X_input = [[4, 20, moral, 1, 100000, 5, 5, 3, 2, 1, 3, 3, 40, 1, 3, 2, 4, 1, 2, 2, 1]]

if classifier.predict(X_input) == 1:
    print('Risco de credito ruim')
if classifier.predict(X_input) == 0:
    print('Risco de credito bom')