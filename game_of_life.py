import pygame

# Define constants
CELL_SIZE = 10
CELL_BORDER = 1
CELL_COLOR = (224, 170, 255)

GRID_X, GRID_Y = 80, 60

GRID_WIDTH, GRID_HEIGHT = GRID_X * CELL_SIZE, GRID_Y * CELL_SIZE
GRID_COLOR = (60, 9, 108)

MARGIN = 20

MENU_WIDTH = GRID_WIDTH
MENU_HEIGHT = 50

WIDTH = GRID_WIDTH - CELL_BORDER + MARGIN * 2
HEIGHT = GRID_HEIGHT + MENU_HEIGHT + CELL_BORDER + MARGIN * 2

BTN_WIDTH = 70
BTN_HEIGHT = 30

current_gen = set()
next_gen = set()
num_generation = 0

class button:
    def __init__(self, x, y, width, height, color, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.font = pygame.font.SysFont(None, 24)
        self.text_surf = self.font.render(text, True, (255, 255, 255))
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        screen.blit(self.text_surf, self.text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

def define_next_generation():
    global current_gen, next_gen
    next_gen.clear()
    neighbor_counts = {}

    for cell in current_gen:
        x, y = cell
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                neighbor = (x + dx, y + dy)
                if neighbor in neighbor_counts:
                    neighbor_counts[neighbor] += 1
                else:
                    neighbor_counts[neighbor] = 1

    for cell, count in neighbor_counts.items():
        if -1 < cell[0] < GRID_WIDTH // CELL_SIZE and -1 < cell[1] < GRID_HEIGHT // CELL_SIZE:
            if cell in current_gen:
                if count == 2 or count == 3:
                    next_gen.add(cell)
            else:
                if count == 3:
                    next_gen.add(cell)

    current_gen, next_gen = next_gen, current_gen

def draw_cells(event, screen, current_gen, mode):
    x, y = event.pos
    if MARGIN < x < GRID_WIDTH + MARGIN and MARGIN < y < GRID_HEIGHT + MARGIN:
        cell_X = (x - MARGIN) // CELL_SIZE
        cell_Y = (y - MARGIN) // CELL_SIZE
        cell = (cell_X, cell_Y)
    
        if mode == "add":
            if cell not in current_gen:
                current_gen.add(cell)
        else:
            if cell in current_gen:
                current_gen.remove(cell)
    
    for cell_X, cell_Y in current_gen:
        pygame.draw.rect(screen, CELL_COLOR, (cell_X * CELL_SIZE + MARGIN, cell_Y * CELL_SIZE + MARGIN, CELL_SIZE, CELL_SIZE))

def main():
    global current_gen, next_gen, num_generation
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Game of life")
    next_btn = button(BTN_WIDTH + 2 * MARGIN, GRID_HEIGHT + MARGIN + 20, BTN_WIDTH, BTN_HEIGHT, (0, 200, 0), "Next")
    clear_btn = button(WIDTH - MARGIN - BTN_WIDTH, GRID_HEIGHT + MARGIN + 20, BTN_WIDTH, BTN_HEIGHT, (200, 0, 0), "Clear")

    play_btn_text = "Play"
    next_gening = False
    drawing_cells = False
    running = True
    while running:
        screen.fill((8, 11, 22))
        play_btn = button(20, GRID_HEIGHT + MARGIN + 20, BTN_WIDTH, BTN_HEIGHT, (238, 155, 0), play_btn_text)
        play_btn.draw(screen)
        next_btn.draw(screen)
        clear_btn.draw(screen)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if MARGIN < event.pos[1] < GRID_HEIGHT + MARGIN:
                    drawing_cells = True
                    x, y = event.pos
                    if MARGIN < x < GRID_WIDTH + MARGIN and  MARGIN < y < GRID_HEIGHT + MARGIN:
                        cell_X = (x - MARGIN) // CELL_SIZE
                        cell_Y = (y - MARGIN) // CELL_SIZE
                        cell = (cell_X, cell_Y)
                        mode = "remove" if cell in current_gen else "add"
            
                elif play_btn.is_clicked(event.pos) and len(current_gen):
                    next_gening = not next_gening
                    play_btn_text = "Pause" if next_gening else "Play"

                elif next_btn.is_clicked(event.pos) and len(current_gen):
                    define_next_generation()
                    print(f'{"{"}"gen": {num_generation}, "population": {len(current_gen)},{"}"}')
                    num_generation += 1

                elif clear_btn.is_clicked(event.pos):
                    current_gen.clear()
                    next_gen.clear()
                    num_generation = 0
            
            elif event.type == pygame.MOUSEBUTTONUP:
                drawing_cells = False

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and len(current_gen):
                    next_gening = not next_gening
                    play_btn_text = "Pause" if next_gening else "Play"

        if drawing_cells:
            draw_cells(event, screen, current_gen, mode)

        if next_gening and len(current_gen):
            define_next_generation()
            print(f'{"{"}"gen": {num_generation}, "population": {len(current_gen)},{"}"}')
            num_generation += 1
        else:
            play_btn_text = "Play"
            next_gening = False

        generation_surf = pygame.font.SysFont(None, 24).render(f'Generation: {num_generation}', True, (255, 255, 255))
        screen.blit(generation_surf, (2 * BTN_WIDTH + 3 * MARGIN, GRID_HEIGHT + 2 * MARGIN + 6))
        population_surf = pygame.font.SysFont(None, 24).render(f'Population: {len(current_gen)}', True, (255, 255, 255))
        screen.blit(population_surf, (4 * BTN_WIDTH + 4 * MARGIN, GRID_HEIGHT + 2 * MARGIN + 6))

        for cell_X, cell_Y in current_gen:
            pygame.draw.rect(screen, CELL_COLOR, (cell_X * CELL_SIZE + MARGIN, cell_Y * CELL_SIZE + MARGIN, CELL_SIZE, CELL_SIZE))
        
        for x in range(GRID_X + 1):
            x_pos = x * CELL_SIZE - CELL_BORDER / 2 + MARGIN
            pygame.draw.line(screen, GRID_COLOR, (x_pos, MARGIN), (x_pos, GRID_HEIGHT + MARGIN), CELL_BORDER)
        for y in range(GRID_Y + 1):
            y_pos = y * CELL_SIZE - CELL_BORDER / 2 + MARGIN
            pygame.draw.line(screen, GRID_COLOR, (MARGIN, y_pos), (GRID_WIDTH + MARGIN, y_pos), CELL_BORDER)

        pygame.display.flip()  # Update the display to reflect changes

        next_gening and pygame.time.delay(100)

    pygame.quit()

if __name__ == "__main__":
    main()