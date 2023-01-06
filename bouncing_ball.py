"""
Phân tích các đối tượng trong game
* Đối tượng quả bóng:
    - Thuộc tính:
        + Tọa độ
        + Góc di chuyển
        + Tốc độ di chuyển (có thể set cố định hoặc tăng dần theo thời gian)
        + Màu sắc
        + Kích thước (bán kính)
        
    - Phương thức:
        + Di chuyển
        + Kiểm tra xem chạm tường hay chưa
        + Kiểm tra xem chạm vào thanh paddle
        + Kiểm tra xem rơi xuống đất chưa
        
* Đối tượng thanh paddle:
    - Thuộc tính:
        + Tọa độ 4 điểm 
        + Chiều dài, chiều rộng
        + Màu sắc 
        + Hướng di chuyển
        
    - Phương thức:
        + Di chuyển: Binding với sự kiện ấn 2 nút mũi tên trái phải để di chuyển thanh paddle

Flow của chương trình: 
Người dùng điều khiển thanh paddle sang trái phải bằng phím mũi tên trên bàn phím
Quả bóng sẽ di chuyển theo góc nhất định và đổi hướng khi chạm vào các vật chắn như biên ngang, biên dọc, paddle. 
    - Nếu chạm vào biên ngang thì quả bóng đổi hướng di chuyển, là hướng đối xứng với hướng cũ
    - Tương tự với biên dọc 
    - Nếu chạm vào paddle thì sẽ đổi góc phụ thuộc vào hướng di chuyển của thanh paddle
    - Nếu quả bóng bay xuống đất thì kết thúc lượt chơi và để người chơi lựa chọn chơi lại
    - Cách tính điểm: Chạm vào paddle thì được cộng 1 điểm hoặc là tăng điểm theo thời gian chơi
    
    
* Note:
- Sử dụng  widget Canvas để tạo các đối tượng đồ họa (đối tượng quả bóng, đối tượng paddle)
- Cách di chuyển của quả bóng:
    + Ban đầu quả bóng sẽ di chuyển mỗi bước theo trục x 3 pixel, theo trục y 3 pixel (3, 3)
    + Khi chạm vào Paddle thì sẽ di chuyển mỗi bước theo trục x là 3 pixel, theo trục y là -3 pixel
    + Khi chạm vào Biên phải thì sẽ di chuyển mỗi bước theo trục x là -3 pixel, theo trục y là -3 pixel
    + Khi chạm vào Biên trên thì sẽ di chuyển mỗi bước theo trục x là -3 pixel, theo trục y là 3 pixel
    + Khi chạm vào Biên trái thì di chuyển mỗi bước theo trục x 3 pixel, theo trục y 3 pixel


"""

from tkinter import *
import time


def create_circle(can_vas, x, y, r, color = "blue"):
    return can_vas.create_oval(x-r,y-r,x+r,y+r,fill=color)

def check_va_cham(toa_do_hcn1, toa_do_hcn2):
    if (toa_do_hcn2[0] >= toa_do_hcn1[2]) or (toa_do_hcn2[1] > toa_do_hcn1[3]):
        return False
    if (toa_do_hcn1[0] >= toa_do_hcn2[2]) or (toa_do_hcn1[1] > toa_do_hcn2[3]):
        return False
    return True

class Ball:
    def __init__(self, canvas, paddle, color = "red"):
        self.canvas = canvas
        self.id = create_circle(self.canvas,15,15,10,color)
        # x, y dùng để xác định góc di chuyển của quả bóng
        self.x = 3
        self.y = 3
        self.is_hitting_bottom = False
        self.canvas_width = self.canvas.winfo_width()
        self.canvas_height = self.canvas.winfo_height()
        self.paddle = paddle
        self.score = 0
        
    def draw(self):
        # Mỗi bước sẽ kiểm tra quả bóng chạm vào các vật chắn chưa
        
        pos = self.canvas.coords(self.id)
        # (pos[0], pos[1]) là điểm top-left, (pos[2], pos[3]) là điểm bottom-right
        
        # Kiểm tra quả bóng chạm vào biên trái chưa?
        if pos[0] <= 0:
            self.x = 3
        
        # Kiểm tra quả bóng chạm vào biên phải chưa?
        if pos[2] >= 500:
            self.x = -3
            
        # Kiểm tra quả bóng chạm vào biên trên chưa?
        if pos[1] <= 0:
            self.y = 3
        
        # Kiểm tra quả bóng đã chạm và paddle chưa?
        if check_va_cham(pos, self.canvas.coords(self.paddle.id)):
            self.y = -3
            self.score += 1
            label_score.config(text = "Điểm = " + str(self.score))
            
        
        # Kiểm tra quả bóng có rơi xuống đất hay không?
        if pos[3] >= 300:
            self.is_hitting_bottom = True
        
        if self.is_hitting_bottom == False:
            self.canvas.move(self.id, self.x, self.y)
        
class Paddle:
    def __init__(self, canvas, color = "blue"):
        self.canvas = canvas
        self.color = color
        self.id = self.canvas.create_rectangle(210,250,300,260,fill=self.color)
        self.x = -3
        
    def draw(self):
        self.canvas.move(self.id, self.x, 0)
        self.canvas.bind_all("<KeyPress-Left>", self.move_left)
        self.canvas.bind_all("<KeyPress-Right>", self.move_right)
    
    def move_left(self, event):
        self.x = -3
    
    def move_right(self, event):
        self.x = 3

def stop_game():
    top_level.destroy() # tắt chương trình
    root.destroy()

def continue_game():
    ball.is_hitting_bottom = False
    pos = canvas.coords(ball.id)
    canvas.move(ball.id, - pos[0] +30, - pos[1] +30)
    ball.x=3
    ball.y=3
    ball.score = 0
    label_score.config(text = "Điểm = 0")
    global is_show
    is_show = False
    top_level.destroy()
    

root = Tk()
canvas = Canvas(root, height=300, width=500)
label_score = Label(root, text = "Điểm = 0")
canvas.pack()
label_score.pack()
paddle = Paddle(canvas)
ball = Ball(canvas, paddle)
root.update()

is_show = False

while True:
    if ball.is_hitting_bottom == False:
        ball.draw()
        paddle.draw()
    else:
        if is_show == False:
            top_level = Toplevel(root)
            label = Label(top_level, text = "Bạn có muốn tiếp tục chơi không?")
            btn_yes = Button(top_level, text = "Có", command=continue_game)
            btn_no = Button(top_level, text = "Không", command=stop_game)
            label.grid(row=0, column=0, columnspan=2)
            btn_yes.grid(row=1, column=0)
            btn_no.grid(row=1, column=1)
            is_show = True
                      
    
    root.update_idletasks()
    root.update()
    time.sleep(0.1)


















































