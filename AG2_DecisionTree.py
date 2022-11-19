'''
Alunos: João Victor Oliveira - 106 GES
        Júlia da Silva Villela - 1799 GEC
'''

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
X = dtFrame.iloc[:,[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]].values
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
print('\nEntre com os dados solicitados abaixo: ')

while True: #laufkont = status
    status = int(input('Status: '))
    if (status >= 1 and status <= 4):
        break

while True: #laufzeit = duration
    duration = int(input('Duração: '))
    if (duration > 0):
        break

while True: #moral = credit_history
    moral = int(input('Historico moral de credito: '))
    if (moral >= 0 and moral <= 4):
        break

while True: #verw = purpose
    purpose = int(input('Propósito: '))
    if (purpose >= 0 and purpose <= 10):
        break

while True: #hoehe = amount
    amount = int(input('Montante (valor do credito): '))
    if (amount > 0):
        break

while True: #sparkont = savings
    savings = int(input('Reserva/Poupanca: '))
    if (savings >= 1 and savings <= 5):
        break

while True: #beszeit = employment_duration
    employment_duration = int(input('Tempo no emprego: '))
    if (employment_duration >= 1 and employment_duration <= 5):
        break

while True: #rate = installment_rate
    installment_rate = int(input('Parcelamento: '))
    if (installment_rate >= 1 and installment_rate <= 4):
        break

while True: #famges = personal_status_sex
    personal_status_sex = int(input('Genero e Status civil: '))
    if (personal_status_sex >= 1 and personal_status_sex <= 4):
        break

while True: #buerge = other_debtors
    other_debtors = int(input('Outros devedores: '))
    if (other_debtors >= 1 and other_debtors <= 3):
        break

while True: #wohnzeit = present_residence
    present_residence = int(input('Tempo de moradia na residencia atual: '))
    if (present_residence >= 1 and present_residence <= 4):
        break
    
while True: #verm = property
    verm = int(input('Propriedade: '))
    if (verm >= 1 and verm <= 4):
        break

while True: #alter = age
    age = int(input('Idade: '))
    if (age >= 18): #no banco 19-75
        break

while True: #weitkred = other_installment_plans
    other_installment_plans = int(input('Outros planos de parcelamento: '))
    if (other_installment_plans >= 1 and other_installment_plans <= 3):
        break

while True: #wohn = housing
    housing = int(input('Moradia (1-Gratis, 2-Aluguel ou 3-Propria): '))
    if (housing >= 1 and housing <= 3):
        break

while True: #bishkred = number_credits
    number_credits = int(input('Creditos numericos: '))
    if (number_credits >= 1 and number_credits <= 4):
        break

while True: #beruf = job
    job = int(input('Tipo de emprego: '))
    if (job >= 1 and job <= 4):
        break

while True: #pers = people_liable
    people_liable = int(input('Dependentes: '))
    if (people_liable == 1 or people_liable == 2):
        break

while True: #telef = telephone gastarb = foreign_worker
    telephone = int(input('Telefone: '))
    if (telephone == 1 or telephone == 2):
        break

while True: #gastarb = foreign_worker
    foreign_worker = int(input('Trabalhador estrangeiro (S/N): '))
    if (foreign_worker == 1 or foreign_worker == 2):
        break


#Inserindo os valores passados pelo usuario para realizar a predicao
X_input = [[status, duration, moral, purpose, amount, savings, employment_duration, 
            installment_rate, personal_status_sex, other_debtors, present_residence,
            verm, age, other_installment_plans, housing, number_credits, job,
            people_liable, telephone, foreign_worker]]


#  BOM: 4, 5, 4,  6,     1000, 5, 5, 2, 3, 1, 4, 4, 30, 1, 3, 2, 3, 2, 2, 2
# RUIM: 2, 2, 1, 10, 10000000, 1, 1, 2, 3, 1, 4, 1, 20, 1, 1, 1, 1, 2, 1, 2

if classifier.predict(X_input) == 1:
    print('\nRisco de credito ruim')
if classifier.predict(X_input) == 0:
    print('\nRisco de credito bom')