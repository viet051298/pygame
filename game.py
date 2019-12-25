import pygame
import random
import sys

HEIGHT = 600
WIDTH = 600
RED = (255,0,0)
BLUE = (0,0,255)
WHITE = (255,255,255)
BLACK = (0,0,0)

class Game:
    def __init__(self):
        # Tạo dữ liệu
        pygame.init()
        self._data = [0]*9
        self.turn = 0
        self.gameExit = False
        self.first_player = "You"
        self.second_player = "Computer"
        self.display = pygame.display
        self.gameDisplay = pygame.display.set_mode((WIDTH,HEIGHT))
        self.draw_board()


    def update_data(self,pos,master):
        # cập nhật dư liệu
        if self._data[pos]==0:
            self._data[pos] = master
            return True
        return False

    def master_data(self,master):
        # Trả về dữ liệu cụ thể
        return [k+1 for k in range(0,9) if self._data[k]==master]

    def draw_board(self):
        # Tạo bảng với màu
        self.gameDisplay.fill(BLACK)
        self.display.set_caption("Caro 3x3")
        x,y = 0,0
        for i in range(3):
            x = 0
            for j in range(3):
                col = WHITE
                pygame.draw.rect(self.gameDisplay,col,[x,y,195,195])
                x += 200
            y += 200

    def message_to_screen(self,msg,col,size,t_x,t_y):
        #Hiển thị định dạng ra màn hình
        font = pygame.font.SysFont(None,size)
        text = font.render(msg,True,col)
        text_rect = text.get_rect()
        text_rect.center = (t_x,t_y)
        self.gameDisplay.blit(text,text_rect)

    def game_end(self):
        # Kiểm tra xem trò chơi kết thúc chưa
        if self.turn>=9:
            return True
        return False

    def check_winner(self):
        # Kiểm tra xem người chơi nào win trò chơi
        winner = None
        win_set = [(1,2,3),(4,5,6),(7,8,9),(1,4,7),(2,5,8),(3,6,9),(1,5,9),(3,5,7)]
        first_player = self.master_data(1)
        second_player = self.master_data(2)
        for x,y,z in win_set:
            if x in first_player and y in first_player and z in first_player:
                winner = self.first_player
            elif x in second_player and y in second_player and z in second_player:
                winner = self.second_player
        return winner

    def result(self,winner):
        # Hiển thị kết quả ra màn hình
        self.gameDisplay.fill(BLACK)
        msg1 = 'Winner is {}.'.format(winner)
        self.message_to_screen(msg1,RED,40,290,285)
        msg2 = 'Press R to continue or Q to quit.'
        self.message_to_screen(msg2,BLUE,25,290,310)
        pygame.display.update()
        again = True
        while again:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    again = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        again = False
                        self.restart()
                    if event.key == pygame.K_q:
                        again = False

    def computer_move(self):
        update = False
        while not update:
            pos = random.randint(0,8)
            update = self.update_data(pos,2)
         #Tính hàng và cột từ pos
        row = pos//3 #1
        col = pos-3*(pos//3) #0
        self.message_to_screen('X',BLACK,100,100+(200*col),100+(200*row))
        self.turn += 1

                        

    def __events(self):
        # kiểm tra các sự kiện bàn phím và chuột
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.gameExit = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                col,row = event.pos
                if(row<600 and col<600):
                    col,row = col//200,row//200
                    pos = col+row*3
                    updated = self.update_data(pos,1)
                    if updated:
                        self.message_to_screen('O',BLACK,100,100+(200*col),100+(200*row))
                        self.turn += 1

    def __update(self):
        # Cập nhật dữ liệu ra màn hình
        if self.turn%2==1 and self.turn<9:
            self.computer_move()
        self.display.update()
        gameEnd = game.game_end()
        winner = game.check_winner()
        if gameEnd or (not winner is None):
            self.gameExit = True
            self.result(winner)
            
    def run(self):
        # Chạy game
        while not self.gameExit:
            self.__events()
            self.__update()
        # Giải phóng pygame và thoát khỏi trò chơi
        pygame.quit()
        sys.exit()
            

    def restart(self):
        # Khởi động lại trò chơi
        self.__init__()


if __name__=='__main__':
    # Tạo trò chơi
    game = Game()
    game.run()