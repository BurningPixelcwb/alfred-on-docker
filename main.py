#arquivo onde está os inputs de classificação da transação
import classification

#decide pra onde vai depois de classificada a transação
if classification.tp_lancamento == 'm':
    import manual

if classification.tp_lancamento == 'n':
    import soup

##Fechando programa
print('\n######## OBRIGADO E VOLTE SEMPRE ########\n')