import cv2 as cv
import pytesseract
import numpy as np


path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
pytesseract.pytesseract.tesseract_cmd = path

def perspective(img1, img2):
    
    # Altura e largura da imagem base
    h, w, _ = img1.shape
    
    #Pontos de interesse
    orb = cv.ORB_create(5000)

    # Detectar pontos-chave e calcular descritores para a primeira imagem
    keypoints1, descriptors1 = orb.detectAndCompute(img1, None)
    
    # Visualização
    # img_points = cv.drawKeypoints(img1, keypoints1, None)
    # img_points = cv.resize(img_points, (640, 840))
    # cv.imshow("image", img_points)
    # cv.waitKey(0)
    
    # Detectar pontos-chave e calcular descritores para a segunda imagem
    keypoints2, descriptors2 = orb.detectAndCompute(img2, None)

    # Inicializar o BFMatcher
    bf = cv.BFMatcher(cv.NORM_HAMMING)

    # Realizar a correspondência entre os descritores das duas imagens
    matches = list(bf.match(descriptors2, descriptors1))

    # Ordenar as correspondências com base na distância
    matches.sort(key=lambda x: x.distance)

    # Selecionar uma porcentagem das melhores correspondências
    per = 35
    matches_filter = matches[:int(len(matches)*per/100)]

    # Visualização
    # Desenhar as correspondências na imagem de saída
    # img_match = cv.drawMatches(img2, keypoints2, img1,keypoints1, matches_filter, None, flags=2)
    # Exibir a imagem com as correspondências
    # img_match_resized = cv.resize(img_match , (840, 640))
    # cv.imshow("image", img_match_resized)
    # cv.waitKey(0)

    src_points = np.float32(
        [keypoints2[m.queryIdx].pt for m in matches_filter]).reshape(-1, 1, 2)
    dst_points = np.float32(
        [keypoints1[m.trainIdx].pt for m in matches_filter]).reshape(-1, 1, 2)

    m, _ = cv.findHomography(src_points, dst_points, cv.RANSAC, 5.0)
    img_scan = cv.warpPerspective(img2, m, (w, h))

    # Visualização
    # img_scan_resized = cv.resize(img_scan, (420, 640))
    # cv.imshow("image", img_scan_resized)
    # cv.waitKey(0)
    
    return img_scan


def labels(img, roi, filter):
    
    # Visualozação
    img_show = img.copy()
    img_mask = np.zeros_like(img_show)
    data = []
    kernel = np.ones((3, 3))

    for x, r in enumerate(roi):
        cv.rectangle(img_mask, (r[0][0], r[0][1]), (r[1][0], r[1][1]), (0, 0, 255), cv.FILLED)
        img_show = cv.addWeighted(img_show, 1, img_mask, 1, 0)

        img_cut = img[r[0][1]:r[1][1], r[0][0]:r[1][0]]
        
        # Visualização
        # cv.imshow("image", img_cut)
        # cv.waitKey(0)
        
        img_gray = cv.cvtColor(img_cut, cv.COLOR_BGR2GRAY)
        
        #('Padrão', 'Filtro1')
        if filter == 'Tratamento de Ruido':
            img_dilate = cv.dilate(img_gray, (kernel), iterations=1)
            img_erode = cv.erode(img_dilate, (kernel), iterations=1)
            _, img_threshhold = cv.threshold(img_erode, 127, 255, cv.THRESH_BINARY)
        else:
            _, img_threshhold = cv.threshold(img_gray, 127, 255, cv.THRESH_BINARY)

        
        data.append({r[2]: pytesseract.image_to_string(img_threshhold, lang='por')})
        # Visualização
        # cv.imshow("image", img_cut)
        # cv.waitKey(0)

        # cv.imshow("image", img_threshhold)
        # cv.waitKey(0)

    return data, img_show





