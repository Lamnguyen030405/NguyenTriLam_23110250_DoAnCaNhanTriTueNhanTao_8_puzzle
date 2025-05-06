import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Định nghĩa ComboBox
class ComboBox:
    def __init__(self, x, y, width, height, options):
        self.rect = pygame.Rect(x, y, width, height)
        self.options = options  # Danh sách các tùy chọn
        self.selected_option = options[0]  # Giá trị mặc định
        self.is_open = False  # Trạng thái mở/đóng
        self.option_height = 30  # Chiều cao mỗi tùy chọn
        self.option_list = []  # Danh sách các Rect cho từng tùy chọn
        self.font = pygame.font.Font(None, 30)

    def draw(self, surface):
        # Vẽ hộp ComboBox
        pygame.draw.rect(surface, BLUE if self.is_open else GRAY, self.rect, 0)
        pygame.draw.rect(surface, BLACK, self.rect, 2)

        # Vẽ văn bản được chọn
        text = self.font.render(self.selected_option, True, BLACK)
        text_rect = text.get_rect(center=self.rect.center)
        surface.blit(text, text_rect)

        # Vẽ mũi tên thả xuống
        arrow_x = self.rect.right - 20
        arrow_y = self.rect.centery - 5
        pygame.draw.polygon(surface, BLACK, [(arrow_x, arrow_y), (arrow_x - 10, arrow_y), (arrow_x - 5, arrow_y + 5)])

        # Vẽ danh sách tùy chọn nếu mở
        if self.is_open:
            for i, option in enumerate(self.options):
                option_rect = pygame.Rect(self.rect.x, self.rect.bottom + i * self.option_height,
                                        self.rect.width, self.option_height)
                self.option_list.append(option_rect)
                color = RED if option_rect.collidepoint(pygame.mouse.get_pos()) else GRAY
                pygame.draw.rect(surface, color, option_rect)
                pygame.draw.rect(surface, BLACK, option_rect, 2)
                text = self.font.render(option, True, BLACK)
                text_rect = text.get_rect(center=option_rect.center)
                surface.blit(text, text_rect)

    def update_layout(self, x, y, width, height):
        """Cập nhật vị trí và kích thước của ComboBox"""
        self.rect.x = x
        self.rect.y = y
        self.rect.width = width
        self.rect.height = height
        self.option_height = height  # Cập nhật chiều cao mỗi tùy chọn
        self.options_rect = pygame.Rect(x, y + height, width, height * len(self.options))
        self.font = pygame.font.Font(None, int(height * 0.8))  # Cập nhật font chữ

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.is_open = not self.is_open
            elif self.is_open:
                for i, option_rect in enumerate(self.option_list):
                    if option_rect.collidepoint(event.pos):
                        self.selected_option = self.options[i]
                        self.is_open = False
                        self.option_list.clear()  # Xóa danh sách Rect sau khi chọn
                        break
                else:
                    self.is_open = False
                    self.option_list.clear()