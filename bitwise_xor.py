import cv2


fig1 = cv2.imread('img-original2.jpg')  # Leitura das imagens
fig2 = cv2.imread('spec.jpg')

fig1resz = cv2.resize(fig1, (772,712)) # Redimensionar imagens
fig2resz = cv2.resize(fig2, (772,712))

fig1gray = cv2.cvtColor(fig1resz, cv2.COLOR_BGR2GRAY) # Conversão para escala de cinza
fig2gray = cv2.cvtColor(fig2resz, cv2.COLOR_BGR2GRAY)

ret,thresh1 = cv2.threshold(fig1gray,220,255,cv2.THRESH_BINARY)  # Converter a imagem em binários
ret,thresh2 = cv2.threshold(fig2gray,220,255,cv2.THRESH_BINARY)

res1 =cv2.bitwise_xor(thresh1, thresh2)

cv2.imshow('Resultado', res1)

cv2.waitKey(0)
cv2.destroyAllWindows()