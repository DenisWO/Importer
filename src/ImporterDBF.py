from dbfread import DBF

#Script para salvar as querys dentro do arquivo SQL
def saveScript(sql):
    arq = open('../files/destino/ImportacaoDBF.sql', 'a')
    arq.write(sql + '\n\n')
    arq.close()

#Função para montagem da query de insert dos produtos
def insertProduto(args):
    if(args['TRIBUTACAO'] == True):
        args['TRIBUTACAO'] = 'True'
    else:
        args['TRIBUTACAO'] = 'False'
    params = "'" + args['CODBARRAS'] + "', '" + args['NOME'] + "', '" + str(args['TRIBUTACAO']) + "', "+ str(args['VR_COMPRA']) + ", " + str(args['VR_VENDA'])
    sql = "INSERT INTO Produto (CODBARRAS, NOME, TRIBUTACAO, VR_COMPRA, VR_VENDA) VALUES (" + params + ")"
    saveScript(sql)

#Função para montagem da query de insert dos clientes
def insertCliente(args):
    params = "'" + args['CNPJ'] + "', '" + args['CPF'] + "', '" + args['TIPO'] + "', '" + args['BAIRRO'] + "', " + \
    str(args['END_NUM']) + ", '" + args['ENDERECO'] + "', '" + args['RAZAOSOCIA'] + "', " + str(args['CODIGO'])

    sql = "INSERT INTO Cliente (CNPJ, CPF, TIPO, BAIRRO, END_NUM, ENDERECO, RAZAOSOCIAL, CODIGO) VALUES (" + params +")"
    saveScript(sql)

#Função para montagem da query de insert dos fornecedores
def insertFornecedor(args):
    params = str(args['CODIGO']) + ", '" + args['RAZAOSOCIA'] + "', '" + args['ENDERECO'] + "', " \
    + str(args['END_NUM']) + ", '" + args['TIPO'] + "', '" + args['CPF'] + "', '" + args['CNPJ'] + "'"

    sql = "INSERT INTO Fornecedor (CODIGO, RAZAOSOCIAL, ENDERECO, END_NUM, TIPO, CPF, CNPJ) VALUES (" + params + ")"
    saveScript(sql)

#Lendo dados dos DBFs e salvando no script SQL
fornecedor = DBF('../files/source_1/Fornecedor.dbf', load=True)
for i in fornecedor.records:
    insertFornecedor(i)

cliente = DBF('../files/source_1/Cliente.dbf', load=True)
for i in cliente.records:
    insertCliente(i)

produto = DBF('../files/source_1/produto.dbf', load=True)
for i in produto.records:
    insertProduto(i)
