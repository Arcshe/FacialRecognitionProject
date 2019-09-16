from tkinter import *
import cv2
from PIL import Image,ImageTk


cascadePath = "haarcascade_frontalface_alt.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)

smileCascadePath = "haarcascade_smile.xml"
smilefaceCascade = cv2.CascadeClassifier(smileCascadePath)

font = cv2.FONT_HERSHEY_SIMPLEX

BoardROI = cv2.imread('timg.png')
BoardROI = cv2.cvtColor(BoardROI, cv2.COLOR_BGR2RGB)

# -------------这个是退出按钮的函数-----------------
def button_out():
    camera.release()
    cv2.destroyAllWindows()
    root.destroy()

# -------------这个是更换遮盖图片的函数-------------
id = 1

def button_picture():
    global id
    global temping
    global temping1
    global BoardROI
    if id == 1:
        id = 2

        btn_picture['image'] = temping1
        BoardROI = cv2.imread('huaji.png')
        BoardROI = cv2.cvtColor(BoardROI, cv2.COLOR_BGR2RGB)
    elif id == 2:
        id = 1
        btn_picture['image'] = temping
        BoardROI = cv2.imread('timg.png')
        BoardROI = cv2.cvtColor(BoardROI, cv2.COLOR_BGR2RGB)


def video_loop():
    success, img = camera.read()  # 从摄像头读取照片
    if success:
        # cv2.waitKey(10)
        cv2image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)#转换颜色从BGR到RGBA
        # ------------------------接下来为图像处理代码-----------------------
        # 灰度
        gray = cv2.cvtColor(cv2image, cv2.COLOR_BGR2GRAY)
        # 均衡化
        gray = cv2.equalizeHist(gray)
        # 人脸识别
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(int(minW), int(minH)),
        )
        # 人脸区域图片代替
        for (x, y, w, h) in faces:
            # global BoardROI
            cv2.rectangle(cv2image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            global BoardROI
            BoardROI = cv2.resize(src=BoardROI, dsize=(h, w))
            roi_color = img[y:y + h, x:x + w]
            smile = smilefaceCascade.detectMultiScale(
                roi_color,
                scaleFactor=1.1,
                minNeighbors=35,
                minSize=(25, 25),
                flags=cv2.CASCADE_SCALE_IMAGE
            )
            for (x2, y2, w2, h2) in smile:
                cv2image[y:y + h, x:x + w] = BoardROI
        # ----------------------接下来是图像显示-----------------------------
        current_image = Image.fromarray(cv2image)#将图像转换成Image对象
        imgtk = ImageTk.PhotoImage(image=current_image)
        panel.imgtk = imgtk
        panel.config(image=imgtk)
        root.after(1, video_loop)


camera = cv2.VideoCapture(0)    #摄像头
camera.set(3, 640) # set video widht
camera.set(4, 480) # set video height

# Define min window size to be recognized as a face
minW = 0.1*camera.get(3)
minH = 0.1*camera.get(4)

root = Tk()
root.title("人脸替换")

panel = Label(root)  # initialize image panel
panel.pack(padx=10, pady=10)
root.config(cursor="arrow")
# 图片更换按钮
temping = PhotoImage(file = "timg.png")
temping1 = PhotoImage(file = "huaji.png")
btn_picture = Button(root, image = temping, command=button_picture, width = 50, height = 50)
btn_picture.pack()

# 退出按钮
btn_out = Button(root, text="退出!", command=button_out)
btn_out.pack(fill="both", expand=True, padx=10, pady=10)

video_loop()

root.mainloop()
# 当一切都完成后，关闭摄像头并释放所占资源
camera.release()
cv2.destroyAllWindows()