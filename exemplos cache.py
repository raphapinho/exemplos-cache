#!/usr/bin/env python
# coding: utf-8

# # Exemplo 5.1
# 
# Um determinado sistema de computação possui uma memória cache, MP e processador. Em
# operações normais, obtêm-se 96 acertos a cada 100 acessos do processador às memórias. Qual
# deve ser a eficiência do sistema cache/MP?

# In[2]:


percent=96
acertos = (percent/100)*100
print('A eficiência do sistema cache/MP: {}'.format(acertos))


# # Exemplo 5.2
# 
# Considere um sistema de computação com uma memória cache de 32KB de capacidade,
# constituída de linhas com 8 bytes de largura. A MP possui uma capacidade de 16MB.

# In[2]:


def convbase2(v,unid):#v=valor e unid=unidade
    convert=0
    if unid.lower() == 'b':
        convert = v
    if unid.lower() == 'kb':
        convert = v * 2 ** 10
    if unid.lower() == 'mb':
        convert = v * 2 ** 20
    if unid.lower() == 'k':
        convert = v * 1024
    if unid.lower() == 'm':
        convert = v * 1024**2
        
    for i in range(0, 255):
        if 2 ** i >= convert: return i
        
def calcBits(q, t, c):
     # q = Quantidade de células
     # t = Tamanho de cada célula
     # c = Capacidade da MP
    qntL = convbase2(q / t, "kb") # quantidade de linhas
    totBD = q * t * 1024 # total de bits para a parte de dados
    qntB = convbase2(c / t, "mb") # quantidade de blocos
    qntBL = qntB - qntL #largura do campo tag
    totBT = 2 ** qntL * qntBL # total de bits dos tags
    totB = totBD + totBT # total de bits

    return totB

print(f'Quantidade de bits: {calcBits(32, 8, 16)} -> {calcBits(32, 8, 16) / 1024}KB')
    


# # Exemplo 5.3
# 
# Cálculo do formato de endereço para as memórias cache com mapeamento direto.
# Considere uma MP com 64MB de capacidade associada a uma memória cache que possui 2K
# linhas, cada uma com largura de 16 bytes. Determine o formato do endereço para ser
# interpretado pelo sistema de controle de cache.

# In[7]:


# a mesma função convbase2 será utilizada
def calcEnd(c, ql, l):
   # c = capacidade da mp
   # ql = quantidade de linhas
   # l = largura de bloco
    capExp = convbase2(c, 'mb')
    linhaExp = convbase2(ql, 'k')
    largBlocoExp = convbase2(l, 'b')
    totBD = convbase2(c / l, 'mb')
    return [f'Byte: {largBlocoExp}', f'Linha: {int(totBD / 2)}', f'Tag: {int(capExp)}']

valores = calcEnd(64, 2, 16)

for i in range(len(valores)):
    print(valores[i]+' bits')


# # Exemplo 5.4
# Seja uma MP constituída de blocos com largura de 32 bytes, associada a uma cache com 128KB.
# Em dado instante o processador realiza um acesso, colocando o seguinte endereço (expresso
# em algarismos hexadecimais): 3FC92B6. Determine qual deverá ser o valor binário da linha que
# será localizada pelo sistema de controle da cache.
# 

# In[70]:


def dec_Bin(value):
    number = int(value)
    string = ''
    while number > 0:
        rest = int(number % 2)
        string += str(rest)
        number = (number - rest) / 2
    return string[::-1]
def tamHexToBin(v):
 # v = valor
 return len(v) * 4
def enderecoLinhaBits(lb, c, h):
 #lb = largura do bloco
#c = capacidade da memoria
 #h = endereco em hexadecimal
    tamEnderecoHex = tamHexToBin(h) # tamanho do endereço em binário
    tamCampoByte = convbase2(lb, 'b') # tamanho do campo byte
    tamCampoLinha = convbase2(c / lb, 'kb') # tamanho do campo linha
    tamCampoTag = tamEnderecoHex - (tamCampoByte + tamCampoLinha) # tamanho do campo
    enderecoBinario = decimalBinario(int(h, 16)) # endereco hexadecimal convertido p

    # faz a correção dos zeros faltantes
    if len(enderecoBinario) < tamEnderecoHex:
        while len(enderecoBinario) < tamEnderecoHex:
            tempValor = enderecoBinario[::-1]
            tempValor += '0'
            enderecoBinario = tempValor[::-1]

    return enderecoBinario[tamCampoTag:(tamCampoTag+tamCampoLinha)]

print(f'Endereço da linha: {enderecoLinhaBits(32, 128, "3FC92B6")}')


# # Exemplo 5.5
# Cálculo da quantidade de bits necessários para uma determinada memória cache. Considere um
# sistema de computação com uma memória cache de 32KB de capacidade, constituída de linhas
# com 8 bytes de largura. A MP possui uma capacidade de 16MB.
# 

# In[64]:


def quantidadeBits(cmp, ll, cc):
    # cmp = Capacidade da MP
    # ll = Largura da linha
    # cc = Capacidade da cache
    totalBitsDados = cc * ll * 1024
    larguraLinhas =convbase2(cc / ll, 'kb')
    larguraBlocos = convbase2(cmp / ll, 'mb')
    totalBitsBlocos = 2 ** larguraLinhas * larguraBlocos
    totalBits = totalBitsDados + totalBitsBlocos
    return totalBits
print(f'Quantidade de bits necessários: {quantidadeBits(16, 8, 32)}')


# # Exemplo 5.6
# Cálculo de formato de endereço para memórias cache com mapeamento associativo completo.
# Considere uma MP com 64MB de capacidade associada a uma memória cache que possui 2K
# linhas, cada uma com largura de 16 bytes. Determine o formato do endereço para ser
# interpretado pelo sistema de controle da cache.
# 

# In[65]:


def memoMap(cmp, ql, ll):
    # cmp = Capacidade da MP
    # ll = Largura da linha
    # ql = Quantidade de linhas
    tamEndereco = convbase2(cmp, 'mb')
    tamEndLinha = convbase2(ql, 'k')
    larguraBloco = convbase2(ll, 'b')
    tamEndBloco = tamEndereco - larguraBloco
    return [tamEndereco - tamEndBloco, tamEndBloco]
vetor = memoMap(64, 2, 16)
print(f'Byte: {vetor[0]} bits')
print(f'Bloco: {vetor[1]} bits')


# # Exemplo 5.7
# Seja uma MP constituída de blocos com largura de 32 bytes, associada a uma cache com 64KB.
# Em dado instante o processador realiza um acesso, colocando o seguinte endereço (expresso
# em algarismos hexadecimais): 3FC92B6. Determine qual deverá ser o valor binário do campo
# bloco que será localizado pelo sistema de controle da cache.
# 

# In[66]:



def endBloco(lb, cc, h):
    # lb = largura do bloco
    # cc = capacidade da cache
    # h = endereco em hexadecimal
    tamEnderecoBin = tamHexToBin(h)
    tamCampoByte = convbase2(lb, 'b')
    tamCampoBloco = tamEnderecoBin - tamCampoByte
    enderecoBinario = decimalBinario(int(h, 16))

    # faz a correção dos zeros faltantes
    if len(enderecoBinario) < tamEnderecoBin:
        while len(enderecoBinario) < tamEnderecoBin:
            tempValor = enderecoBinario[::-1]
            tempValor += '0'
            enderecoBinario = tempValor[::-1]

    return enderecoBinario[:tamCampoBloco]
print(f'Endereço do campo bloco: {endBloco(32, 64, "3FC92B6")}')


# # Exemplo 5.8
# Cálculo da quantidade de bits necessários para urna determinada memória cache, que funciona
# com mapeamento por conjunto de quatro.
# Considere um sistema de computação com uma memória cache de 32KB de capacidade,
# constituída de linhas com 8 bytes de largura e conjunto de 4. A MP possui uma capacidade de
# 16MB.
# 

# In[3]:


def qntBitsTotal(cc, ll, conj, cmp):
    totalBitsDados = cc * ll * 1024
    tamEndLinhas = convbase2(cc / ll, 'kb')
    tamEndConjuntos = convbase2((cc / ll) / conj, 'k')
    tamEndBlocos = convbase2(cmp / ll, 'mb')
    tamCampoTag = tamEndBlocos - tamEndConjuntos
    totalBitsTags = (2 ** tamEndLinhas / 1024) * (2 ** tamCampoTag / 1024) * 1024
    totalBits = totalBitsDados + totalBitsTags

    return int(totalBits)
print(f'Quantidade de bits necessários: {qntBitsTotal(32, 8, 4, 16)}')


# # Exemplo 5.9
# Cálculo de formato de endereço para memórias cache com mapeamento associativo por
# conjunto.
# Considere uma MP com 64MB de capacidade associada a uma memória cache que funciona
# com mapeamento associativo por conjunto de 4 e que possui ~32KB~ (128KB corrigido), com
# linhas de largura de 16 bytes. Determine o formato do endereço para ser interpretado pelo
# sistema de controle da cache
# Solução: Com os mesmos conceitos aplicados anteriormente, utiliza-se o seguinte código para
# a resolução desse exemplo:
# 

# In[68]:


def mapeamentoCampos(cmp, conj, cc, ll):
    # cmp = capacidade da mp
    # conj = valor do conjunto
    # cc = capacidade da cache
    # ll = largura da linha
    tamEnd = convbase2(cmp, 'mb')
    larguraBloco = convbase2(ll, 'b')
    larguraConjunto = convbase2(conj, 'b')
    tamEndBloco = convbase2(cmp / ll, 'm') # qntd de blocos reduzida para base 2
    tamEndLinhasCache = convbase2(cc / ll, 'k') # qntd de linhas da cache reduzid
    tamEndConjuntos = tamEndLinhasCache - larguraConjunto
    tamEndBlocoConjunto = tamEndBloco - tamEndConjuntos # qntd de blocos por conjunt

    return [tamEndBloco - tamEndConjuntos, tamEndConjuntos, larguraBloco]
vetor = mapeamentoCampos(64, 4, 128, 16)
print(f'Campo tag: {vetor[0]} bits')
print(f'Campo conjunto: {vetor[1]} bits')
print(f'Campo bloco: {vetor[2]} bits')


# # Exemplo 5.10
# Seja uma MP constituída de blocos com largura de 32 bytes, associada a urna cache com
# ~64KB~ (128KB corrigido); a cache usa mapeamento por conjunto de 4. Em dado instante o
# processador realiza um acesso, colocando o seguinte endereço (expresso em algarismos
# hexadecimais): 31C92B6. Determine qual deverá ser o valor binário do conjunto que será
# localizado pelo sistema de controle da cache.
# 

# In[71]:


def pegVBin(lb, cc, conj, h):
    tamEnderecoBin = tamHexToBin(h)
    tamConj = convbase2(conj, 'b')
    tamCampoByte = convbase2(lb, 'b')
    qntLinhas = convbase2(cc / lb, 'kb')
    tamCampoConjunto = qntLinhas - tamConj
    tamCampoTag = tamEnderecoBin - tamCampoConjunto - tamCampoByte
    enderecoBinario= decimalBinario(int(h, 16))

   # faz a correção dos zeros faltantes
    if len(enderecoBinario) < tamEnderecoBin:
        while len(enderecoBinario) < tamEnderecoBin:
            tempValor = enderecoBinario[::-1]
            tempValor += '0'
            enderecoBinario = tempValor[::-1]

    return enderecoBinario[tamCampoTag:(tamCampoTag + tamCampoConjunto)]


print(f'Binário do conjunto: {pegVBin(32, 128, 4, "31C92B6")}')
    


# In[ ]:




