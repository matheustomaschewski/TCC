import matplotlib.pyplot as plt

f = open("Bottom.txt", "r") # Abre o arquivo Gerber

lerlinhas = f.readlines() # Lê o arquivo e armazena numa lista organizada por linhas

# Determinação do AM - Aperture Macro
listaAM = str()
for g in range(len(lerlinhas)): # Percorre cada linha da lista
    linha = lerlinhas[g] # Transforma a linha da lista numa string iterável
    if 'AM' in linha:
        listaAM = str(listaAM + linha[linha.find(",")+1:linha.find("\n")])
        AMType = int(linha[linha.find("*")+1:linha.find(",")]) # Tipo de 'Primitive'. Ex.: 0,1,20,21,4,5,6,7. Pág. 56
        AMName = linha[linha.find("M")+1:linha.find("*")] # Nome da variável
    
pos=[] # Determinar em quais linhas está o nome da variável (Ex.: DIL003), para determinar as linhas com os parâmetros
i=0
for x in range(len(lerlinhas)):
    linha = lerlinhas[x]
    if AMName in linha:
        pos.insert(i,x)
        i=i+1
            
for x in range(pos[0]+1,pos[1]-1): # Cria uma lista com todos os parâmetros do respectivo AM
    linha = lerlinhas[x]
    listaAM = str(listaAM + linha[:-1])
    
AMCoord = listaAM.split(",") # Transforma a string numa lista
    
Exposure = int(AMCoord[0]) # 0 para branco e 1 para preto
NVertices = int(AMCoord[1]) # número de vértices do polígono 
Rotacao = AMCoord[-1] # Rotação em graus
          
# Cria lista de ferramentas
ferramenta = []
i=0
for h in range(len(lerlinhas)):
    if 'ADD' in lerlinhas[h]:
        ferramenta.insert(i,lerlinhas[h])
        i=i+1            

# Realiza uma busca para determinar a unidade de medida, considerando não saber em qual linha está esta informação
for i in range(len(lerlinhas)):
    if "IN" in lerlinhas[i]:
        unimedida = "Polegada"
        pol = 25.4
        break
    else:
        unimedida = "Milímetro"
        pol = 1

# Busca a linha onde está o Format Specification. FS informa número de inteiros e casas decimais        
for j in range(len(lerlinhas)): 
    if "FSLA" in lerlinhas[j]:
        break

formatspec = lerlinhas[j] # Format specification - atributo do Gerber para casas de decimais e inteiros

inteiroX = int(formatspec[formatspec.find("X")+1]) # Inteiros
decimalX = int(formatspec[formatspec.find("X")+2]) # Casas após a vírgula
inteiroY = int(formatspec[formatspec.find("Y")+1])
decimalY = int(formatspec[formatspec.find("Y")+2])

##########################################################

# Busca por coordenadas em todo o arquivo
k=0
q=0
xold = 0
yold = 0
for k in range(len(lerlinhas)): # Faz leitura linha a linha
    linha = lerlinhas[k] # Transforma a linha da lista em uma string de linha única
    if 'G54' in linha: # Verifica se há troca de ferramenta na linha atual
        formato = linha[linha.find("D"):linha.find("*")] # Determina qual a ferramenta. Ex.: ADD10, ADD11
        for q in range(len(ferramenta)):
            if formato in ferramenta[q]:
                shape = ferramenta[q]
                shapetype = shape[shape.find("ADD")+5]
                if shapetype == 'C':
                    jstyle = 'round'
                    cstyle = 'round'
                    raio = float(shape[shape.find(",")+1:shape.find("*")])
                    linew = raio
                    cor = 'black'
                else:
                    if shapetype == 'R':
                        jstyle = 'miter'
                        cstyle = 'butt'
                        linewx = float(shape[shape.find(",")+1:shape.find("X")])
                        linewy = float(shape[shape.find("X")+1:shape.find("*")])
                        linew = linewx
                        cor = 'black'
                         
    if 'X' == linha[0]: # Verifica se o primeiro caracter da String é 'X'. Se for, é uma coordenada.
        x = int(linha[linha.find("X")+1:linha.find("Y")])/(10**(decimalX))
        y = int(linha[linha.find("Y")+1:linha.find("D")])/(10**(decimalY))
        op = linha[linha.find("D")+1:linha.find("*")]
        if op == "01": # Plotar
            fig1 = plt.figure(1, frameon=False)
            plt.axis('Equal')
            plt.plot([xold, x],[yold, y], color=cor, linewidth = linew*pol, solid_joinstyle=jstyle, solid_capstyle=cstyle)
        else:
            if op =="02": # Mover
                plt.figure(2)
                plt.axis('Equal')
                plt.plot([xold, x],[yold, y], color=cor, linewidth = linew*pol, solid_joinstyle=jstyle, solid_capstyle=cstyle)
            else:
                if op == "03": # Replicar
                    plt.figure(1)
                    
                    if shapetype == 'C':
                        circle = plt.Circle((x, y), radius=raio/2, color=cor)
                        plt.gca().add_patch(circle)
                        plt.axis('Equal')
                    if shapetype == 'R':
                        rectangle = plt.Rectangle((x-(linewx/2),y-(linewy/2)),linewx,linewy, color=cor)
                        plt.gca().add_patch(rectangle)
                        plt.axis('Equal')
                    if shapetype == 'D':
                        pontos=AMCoord[2:len(AMCoord)-1]   
                        points=[] # Pontos do polígono
                        for i in range(NVertices):
                            AMx = x+float(pontos[2*i])
                            AMy = y+float(pontos[2*i+1])
                            temp = [AMx,AMy]
                            points.append(temp) # Concatena os pontos numa lista para usar no plt.Polygon(Args*). Ex.: [[x,y],[x1,y1],...]
                            
                        outline = plt.Polygon(points,color=cor)
                        plt.gca().add_patch(outline)
                        plt.axis('Equal')
                    else:
                        circle = plt.Circle((x, y), radius=raio/3, color="White")
                        plt.gca().add_patch(circle)
                   
        xold = x
        yold = y
                    
f.close()
fig1.savefig('placateste.png')
