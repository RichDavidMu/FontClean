import cv2
import random
import glob
img_dir = r'E:\GitHub\FontClean\ShuFa2Img\OriginData' #存放未清洗图片的路径
save_dir = r'./CleanData/' #存放清洗后数据
def split(jpg_file):
    img = cv2.imread(jpg_file)
    result = img.copy()
    # 获取文件名
    file_name = jpg_file.split('\\')[-1].split('.')[-2]
    # 将图片转为灰度图
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    # 灰度图转二值图
    ret,thresh = cv2.threshold(gray,190,255,cv2.THRESH_BINARY)
    # 加深颜色
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 40))
    eroded = cv2.erode(thresh, kernel)
    # 开始分割
    contours, hierarchy = cv2.findContours(eroded, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    color = (0, 255, 0)
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(img, (x, y), (x + w, y + h), color, 1)
        temp = result[y:(y + h), x:(x + w)]
        if (temp.shape[0]+temp.shape[1] >100) & (temp.shape[0] < 1000) :
            i = random.randint(0,10)
            j = random.randint(0,10)
            temp = cv2.medianBlur(temp,5)
            #调整分割后图片的size，加上四周的空白
            temp = cv2.resize(temp,(221,221),interpolation=cv2.INTER_AREA)
            temp = cv2.cvtColor(temp,cv2.COLOR_BGR2GRAY)
            temp = cv2.copyMakeBorder(temp, 30, 30, 30, 30, cv2.BORDER_CONSTANT, value=[255, 255])
            # 生成随机文件名并保存
            cv2.imwrite(save_dir+ file_name+str(x)+str(i)+str(j) + ".jpg", temp)
for jpg_file in glob.glob(img_dir+r'/*.jpg'):
    split(jpg_file)
