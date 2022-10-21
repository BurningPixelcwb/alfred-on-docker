
import libs
import functions.queries
import functions.functions as funcs
from bs4 import BeautifulSoup
from lxml import etree
import requests
import classification

# INSERE A URL DA NOTA FISCAL
print('######## AGORA QUE ESTÁ TUDO CERTO, BASTA COLAR O LINK DO TICKET! ########\n')
print('Insira a URL da nota fiscal eletronica:')
url_nfe = input()

HEADERS = ({'User-Agent':
			'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
			(KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',\
			'Accept-Language': 'en-US, en;q=0.5'})

webpage = requests.get(url_nfe, headers=HEADERS)
soup = BeautifulSoup(webpage.content, "html.parser")
dom = etree.HTML(str(soup))

q = soup.find_all('span', {'class':'Rqtd'})

##Pandas
##Series para lista de compra
df_cod_prod = libs.pd.Series([])
df_item_comprado = libs.pd.Series([])
df_quantidade = libs.pd.Series([])
df_medida = libs.pd.Series([])
df_preco = libs.pd.Series([])
df_valor_total = libs.pd.Series([])

#Series para: Local da compra
df_local_compra = libs.pd.Series([])

#Series para: Consumidor

#Series para: Info Gerais

transacao = libs.pd.DataFrame()

ticket = libs.pd.DataFrame()

#resolvendo estabelecimento
estabelecimento = dom.xpath('//*[@id="u20"]')[0].text

#definindo data do lançamento do ticket
dt_lancamento = libs.datetime.today().strftime('%Y-%m-%d-%H:%M:%S')

#resolvendo endereço da compra
endereco = dom.xpath('//*[@id="conteudo"]/div[2]/div[3]')[0].text


#recuperando informações da compra
item_comprado = dom.xpath('//span[@class="txtTit2"]')

cod_produto = dom.xpath('//span[@class="RCod"]')

# Tratando xpath de quandtidade
Rqtd = soup.find_all('span', {'class':'Rqtd'})
quantidade = funcs.clear_fields_from_xpath(Rqtd, '\nQtde.:')

# Tratando xpath de medida
run = soup.find_all('span', {'class':'RUN'})
medida = funcs.clear_fields_from_xpath(run, '\nUN:')

# Tratando xpath de preço
rvlunit = soup.find_all('span', {'class':'RvlUnit'})
preco = funcs.clear_vl_unit(rvlunit, '\nVl. Unit.:')

valor_total = dom.xpath('//span[@class="valor"]')

compras = len(item_comprado)

for i in range(compras):
    ##print(cod_produto[i].text + " : " + item_comprado[i].text + " : " +  quantidade[i].text + " : " +  medida[i].text + " : " + valor_total[i].text)
    
    df_cod_prod[i] = cod_produto[i].text
    
    df_item_comprado[i] = item_comprado[i].text

    df_quantidade[i] = quantidade[i]

    df_medida[i] = medida[i]

    df_preco[i] = preco[i]

    df_valor_total[i] = valor_total[i].text
    

#Cria um data frame
ticket_lancamento = {
    'fk_id_conta': classification.escolha_id_conta
    , 'fk_id_tp_transacao': classification.escolha_id_tipo_transacao
    , 'fk_id_sub_categoria': [classification.escolha_id_sub_categoria]
    , 'url_nfe': url_nfe
    , 'estabelecimento': estabelecimento
    , 'endereco_compra': endereco
    , 'dt_ticket': dt_lancamento
    , 'dt_lancamento': dt_lancamento
}
df_transacao = libs.pd.DataFrame(data=ticket_lancamento)

##insere lancamento
functions.queries.insert_trancao(df_transacao)

##Resgata as contas registradas em BD
url_cara = functions.queries.get_last_transacao()
fk_id_transacao = url_cara.at[0,'id_transacao']

#criando DataFrame de ticket
ticket.insert(0, "cod_prod", df_cod_prod)
ticket.insert(1, "item_comprado", df_item_comprado)
ticket.insert(2, "quantidade", df_quantidade)
ticket.insert(3, "medida", df_medida)
ticket.insert(4, "preco", df_preco)
ticket.insert(5, "valor_total", df_valor_total)
ticket.insert(6, "fk_id_transacao", fk_id_transacao)


#Limpando coluna: cod_prod
ticket['cod_prod'] = ticket['cod_prod'].str.replace('Código: ', '')
ticket['cod_prod'] = ticket['cod_prod'].str.replace('(', '')
ticket['cod_prod'] = ticket['cod_prod'].str.replace(')', '')


#Limpando coluna: quantidade
ticket['quantidade'] = ticket['quantidade'].str.replace('Qtde.:', '')
ticket['quantidade'] = ticket['quantidade'].str.replace(',', '.')


#Limpando coluna: medida
ticket['medida'] = ticket['medida'].str.replace('UN: ', '')

#Limpando coluna: preco
ticket['preco'] = ticket['preco'].str.replace('Vl. Unit.: ', '')
ticket['preco'] = ticket['preco'].str.replace(',', '.')


#Limpando coluna: valor_total
ticket['valor_total'] = ticket['valor_total'].str.replace(',', '.')

print(ticket)

functions.queries.set_ticket(ticket)