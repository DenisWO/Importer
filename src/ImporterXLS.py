import xlrd

#script para salvar os dados dentro do arquivo SQL
def saveScript(sql):
    arq = open('../files/destino/ImportacaoXLS.sql', 'a')
    arq.write(sql + '\n\n')
    arq.close()

#Função para retirar da entrada dados desnecessários do tipo Cell
def tratamentoEntrada(texto):
    if('text:' in texto):
        return texto.replace('text:', '')
    elif('number:' in texto):
        return  texto.replace('number:', '')
    elif('empty:' in texto):
        return  texto.replace('empty:', '')
    else:
         return texto

#Função para tratar os CPFs de entrada e deixar num formato único
def tratamentoCPF(texto):
    texto = texto.replace('.0', '')
    texto = texto.replace('.', '')
    texto = texto.replace('-', '')
    if(not texto.startswith("'") and not texto.endswith("'")):
        texto = "'" + texto + "'"
    return texto

#Função para tratar os CNPJs de entrada e deixar num formato único
def tratamentoCNPJ(texto):
    texto = texto.replace('.', '')
    texto = texto.replace('-', '')
    texto = texto.replace('/', '')
    if(not texto.startswith("'") and not texto.endswith("'")):
        texto = "'" + texto + "'"
    return texto

#Script para montagem da query que será salva no arquivo SQL
def insertProdutos(cabecalho, dados):
    #Tratando dados do cabecalho
    campos = ''
    for i in cabecalho:
        if(i == cabecalho[-1]):
            i = tratamentoEntrada(str(i))
            i = i.replace("'", '')
            campos = campos + i
        else:
            i = tratamentoEntrada(str(i))
            i = i.replace("'", '')
            campos = campos + i + ", "

    entrada = ''
    for i in dados:
        if(i == dados[-1]):
            i = tratamentoEntrada(str(i))
            entrada = entrada + i
        elif(i == dados[0]):
            i = tratamentoEntrada(str(i))
            i = i.replace('.0', '')
            entrada = entrada + i + ", "
        else:
            i = tratamentoEntrada(str(i))
            if('F' in i):
                i = "'False'"
            elif('T' in i):
                i = "'True'"
            entrada = entrada + i + ", "
    sql = "INSERT INTO (" + campos + ") VALUES (" + entrada + ")"
    saveScript(sql)

#Script para montagem da query que será salva no arquivo SQL
def insertPessoas(cabecalho, dados):
    campos = ''
    for i in cabecalho:
        if(i == cabecalho[-1]):
            i = tratamentoEntrada(str(i))
            i = i.replace("'", '')
            campos = campos + i
        else:
            i = tratamentoEntrada(str(i))
            i = i.replace("'", '')
            campos = campos + i + ", "

    entrada = ''
    for i in dados:
        if(i == dados[-1]):
            i = tratamentoEntrada(str(i))
            if('SIM' in i):
                i = "'True'"
            else:
                i = "'False'"
            entrada = entrada + i
        elif(i == dados[1]):
            i = tratamentoEntrada(str(i))
            i = tratamentoCPF(str(i))
            entrada = entrada + str(i) + ", "
        elif(i == dados[2]):
            i = tratamentoEntrada(str(i))
            i = tratamentoCNPJ(i)
            entrada = entrada + str(i) + ", "
        else:
            i = tratamentoEntrada(str(i))
            entrada = entrada + i + ", "

    sql = "INSERT INTO (" + campos + ") VALUES (" + entrada + ")"
    saveScript(sql)


#Lendo dados da planilha de dados e salvando no script SQL
planilha = xlrd.open_workbook('../files/source_2/produtos_pessoas.xls')
sheet = planilha.sheet_by_index(0)

for i in range(sheet.nrows):
    if(i != 0):
       insertProdutos(sheet.row(0), sheet.row(i))

sheet = planilha.sheet_by_index(1)

for i in range(sheet.nrows):
    if(i!=0):
        insertPessoas(sheet.row(0), sheet.row(i))
