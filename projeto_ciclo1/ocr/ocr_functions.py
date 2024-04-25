import cv2 as cv
import pytesseract
import numpy as np
from controllers.logs_controllers import Log


class Ocr:
    @classmethod
    def perspective(self, img1, img2):
        try:
            h, w, _ = img1.shape
            orb = cv.ORB_create(5000)

            keypoints1, descriptors1 = orb.detectAndCompute(img1, None)
            keypoints2, descriptors2 = orb.detectAndCompute(img2, None)
            bf = cv.BFMatcher(cv.NORM_HAMMING)
            matches = list(bf.match(descriptors2, descriptors1))
            matches.sort(key=lambda x: x.distance)

            per = 35
            matches_filter = matches[:int(len(matches)*per/100)]

            src_points = np.float32(
                [keypoints2[m.queryIdx].pt for m in matches_filter]).reshape(-1, 1, 2)
            dst_points = np.float32(
                [keypoints1[m.trainIdx].pt for m in matches_filter]).reshape(-1, 1, 2)

            m, _ = cv.findHomography(src_points, dst_points, cv.RANSAC, 5.0)
            img_scan = cv.warpPerspective(img2, m, (w, h))

            return img_scan
        except Exception as e:
            Log.insert_system_log(e)
            return False
        
        
    @classmethod
    def labels(self, img, roi, filter):
        try:
            img_show = img.copy()
            img_mask = np.zeros_like(img_show)
            data = []
            kernel = np.ones((3, 3))

            for x, r in enumerate(roi):
                cv.rectangle(img_mask, (r[0][0], r[0][1]), (r[1][0], r[1][1]), (0, 0, 255), cv.FILLED)
                img_show = cv.addWeighted(img_show, 1, img_mask, 1, 0)

                img_cut = img[r[0][1]:r[1][1], r[0][0]:r[1][0]]
                img_gray = cv.cvtColor(img_cut, cv.COLOR_BGR2GRAY)
                
                if filter == 'Tratamento de Ruido':
                    img_dilate = cv.dilate(img_gray, (kernel), iterations=1)
                    img_erode = cv.erode(img_dilate, (kernel), iterations=1)
                    _, img_threshhold = cv.threshold(img_erode, 127, 255, cv.THRESH_BINARY)
                else:
                    _, img_threshhold = cv.threshold(img_gray, 127, 255, cv.THRESH_BINARY)

                data.append({r[2]: pytesseract.image_to_string(img_threshhold, lang='por')})

            return data, img_show
        except Exception as e:
            Log.insert_system_log(e)
            return False





