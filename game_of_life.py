import pygame
import time

# ------------------------------------------------------------------------------------------------------------------------------------------------------------ Define constants
cell_size = 10
CELL_BORDER = 1
CELL_COLOR = (224, 170, 255)
cells_origin_x, cells_origin_y = 0, 0

GRID_X_CELLS, GRID_Y_CELLS = 80, 60

GRID_WIDTH, GRID_HEIGHT = GRID_X_CELLS * cell_size, GRID_Y_CELLS * cell_size
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

# ------------------------------------------------------------------------------------------------------------------------------------------------------------ Simple button class
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

# ------------------------------------------------------------------------------------------------------------------------------------------------------------ Define the next generation based on current generation
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
        if -1 < cell[0] < GRID_X_CELLS and -1 < cell[1] < GRID_Y_CELLS:
            if cell in current_gen:
                if count == 2 or count == 3:
                    next_gen.add(cell)
            else:
                if count == 3:
                    next_gen.add(cell)

    current_gen, next_gen = next_gen, current_gen

# ------------------------------------------------------------------------------------------------------------------------------------------------------------ Draw or remove cells based on mouse events
def draw_cells(event, current_gen, mode):
    x, y = event.pos
    if MARGIN < x < GRID_WIDTH + MARGIN and MARGIN < y < GRID_HEIGHT + MARGIN:
        cell_X = (x - MARGIN - cells_origin_x) // cell_size
        cell_Y = (y - MARGIN - cells_origin_y) // cell_size
        cell = (cell_X, cell_Y)
    
        if mode == "add":
            if cell not in current_gen:
                current_gen.add(cell)
        else:
            if cell in current_gen:
                current_gen.remove(cell)


def main():
    global current_gen, next_gen, num_generation, cell_size, cells_origin_x, cells_origin_y

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Game of life")
    icon = pygame.image.load("icon.png")
    pygame.display.set_icon(icon)

# ------------------------------------------------------------------------------------------------------------------------------------------------------------ Create window

    next_btn = button(BTN_WIDTH + 2 * MARGIN, GRID_HEIGHT + MARGIN + 20, BTN_WIDTH, BTN_HEIGHT, (0, 200, 0), "Next")
    clear_btn = button(WIDTH - MARGIN - BTN_WIDTH, GRID_HEIGHT + MARGIN + 20, BTN_WIDTH, BTN_HEIGHT, (200, 0, 0), "Clear")
# ------------------------------------------------------------------------------------------------------------------------------------------------------------ Create buttons
    
    current_time = time.time()

    play_btn_text = "Play"
    next_gening = False
    drawing_cells = False
    mode = "add"
    move_screen = False
    running = True
# ------------------------------------------------------------------------------------------------------------------------------------------------------------ Main loop conditions
    while running:
        screen.fill((8, 11, 22))
# ------------------------------------------------------------------------------------------------------------------------------------------------------------ Draw buttons

        events = pygame.event.get() # Event handling
        for event in events:
            if event.type == pygame.QUIT: # Quit event
                running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN: # Mouse button down event
                if event.button != 2: # Only respond to left mouse button
                    x, y = event.pos
                    if MARGIN < x < GRID_WIDTH + MARGIN and  MARGIN < y < GRID_HEIGHT + MARGIN: # Check if click is within grid area
                        drawing_cells = True
                        cell_X = (x - MARGIN - cells_origin_x) // cell_size
                        cell_Y = (y - MARGIN - cells_origin_y) // cell_size
                        cell = (cell_X, cell_Y)
                        mode = "remove" if cell in current_gen else "add"
                
                    elif play_btn.is_clicked(event.pos) and len(current_gen): # Check if play button is clicked and there are cells
                        next_gening = not next_gening
                        play_btn_text = "Pause" if next_gening else "Play"

                    elif next_btn.is_clicked(event.pos) and len(current_gen): # Check if next button is clicked and there are cells
                        next_gening = False
                        play_btn_text = "Play"
                        define_next_generation()
                        num_generation += 1

                    elif clear_btn.is_clicked(event.pos): # Check if clear button is clicked
                        next_gening = False
                        play_btn_text = "Play"
                        current_gen.clear()
                        next_gen.clear()
                        num_generation = 0
                        cell_size = 10
                        cells_origin_x, cells_origin_y = 0, 0

                elif event.button == 2: # Middle mouse button to toggle cell state
                    move_screen = True
                    pygame.mouse.get_rel()
            
            elif event.type == pygame.MOUSEBUTTONUP: # Stop drawing cells on mouse button up
                if event.button != 2:
                    drawing_cells = False
                elif event.button == 2:
                    move_screen = False

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and len(current_gen): # Spacebar toggles play/pause
                next_gening = not next_gening
                play_btn_text = "Pause" if next_gening else "Play"

            elif event.type == pygame.MOUSEWHEEL: # Mouse wheel event
                if event.y > 0:
                    if cell_size < 100:
                        cell_size += 5
                        cells_origin_x -=  (pygame.mouse.get_pos()[0] - cells_origin_x) / ((cell_size - 5) * GRID_X_CELLS) * (cell_size * GRID_X_CELLS - (cell_size - 5) * GRID_X_CELLS)
                        cells_origin_y -=  (pygame.mouse.get_pos()[1] - cells_origin_y) / ((cell_size - 5) * GRID_Y_CELLS) * (cell_size * GRID_Y_CELLS - (cell_size - 5) * GRID_Y_CELLS)
                else:
                    if cell_size != 10 :
                        cell_size -= 5
                        cells_origin_x += (pygame.mouse.get_pos()[0] - cells_origin_x) / ((cell_size + 5) * GRID_X_CELLS) * ((cell_size + 5) * GRID_X_CELLS - cell_size * GRID_X_CELLS)
                        cells_origin_y += (pygame.mouse.get_pos()[1] - cells_origin_y) / ((cell_size + 5) * GRID_Y_CELLS) * ((cell_size + 5) * GRID_Y_CELLS - cell_size * GRID_Y_CELLS)

                if cells_origin_x > 0: cells_origin_x = 0
                if cells_origin_y > 0: cells_origin_y = 0

                if cells_origin_x + cell_size * GRID_X_CELLS < GRID_WIDTH:
                    cells_origin_x += GRID_WIDTH - (cells_origin_x + cell_size * GRID_X_CELLS)
                if cells_origin_y + cell_size * GRID_Y_CELLS < GRID_HEIGHT:
                    cells_origin_y += GRID_HEIGHT - (cells_origin_y + cell_size * GRID_Y_CELLS)

        if drawing_cells: # Draw or remove cells while mouse is held down
            draw_cells(event, current_gen, mode)

        if next_gening and len(current_gen): # Automatically advance generations if playing
            if time.time() >= current_time + 0.1:
                define_next_generation()
                num_generation += 1
                current_time = time.time()
        else:
            next_gening = False
            play_btn_text = "Play"
        
        if move_screen: # Move screen with middle mouse button
            diff_mouse_x, diff_mouse_y = pygame.mouse.get_rel()
            cells_origin_x += diff_mouse_x
            cells_origin_y += diff_mouse_y
            if cells_origin_x > 0: cells_origin_x = 0
            elif cells_origin_x < GRID_WIDTH - (GRID_X_CELLS * cell_size): cells_origin_x = GRID_WIDTH - (GRID_X_CELLS * cell_size)
            if cells_origin_y > 0: cells_origin_y = 0
            elif cells_origin_y < GRID_HEIGHT - (GRID_Y_CELLS * cell_size): cells_origin_y = GRID_HEIGHT - (GRID_Y_CELLS * cell_size)

        for cell_X, cell_Y in current_gen: # Draw cells
            px = 0
            if cell_X * cell_size + MARGIN + cells_origin_x < 0: px = 1
            py = 0
            if cell_Y * cell_size + MARGIN + cells_origin_y < 0: py = 1
            pygame.draw.rect(screen, CELL_COLOR, (cell_X * cell_size + MARGIN + cells_origin_x - px, cell_Y * cell_size + MARGIN + cells_origin_y - py, cell_size, cell_size))
        
        for x in range(GRID_X_CELLS + 1): # Draw grid lines
            if 0 <= x * cell_size + cells_origin_x <= GRID_WIDTH:
                x_pos = x * cell_size - CELL_BORDER + MARGIN + cells_origin_x
                pygame.draw.line(screen, GRID_COLOR, (x_pos, MARGIN), (x_pos, GRID_HEIGHT + MARGIN), CELL_BORDER)
        for y in range(GRID_Y_CELLS + 1):
            if 0 <= y * cell_size + cells_origin_y <= GRID_HEIGHT:
                y_pos = y * cell_size - CELL_BORDER + MARGIN + cells_origin_y
                pygame.draw.line(screen, GRID_COLOR, (MARGIN, y_pos), (GRID_WIDTH + MARGIN, y_pos), CELL_BORDER)

        pygame.draw.rect(screen, (8, 11, 22), (0, 0, MARGIN, HEIGHT)) # MARGIN left
        pygame.draw.rect(screen, (8, 11, 22), (0, 0, WIDTH, MARGIN)) # MARGIN top
        pygame.draw.rect(screen, (8, 11, 22), (WIDTH - MARGIN, 0, MARGIN, HEIGHT)) # MARGIN right
        pygame.draw.rect(screen, (8, 11, 22), (0, GRID_HEIGHT + MARGIN, WIDTH, MENU_HEIGHT + MARGIN + 1)) # MARGIN bottom

        pygame.draw.rect(screen, GRID_COLOR, (MARGIN - CELL_BORDER, MARGIN - CELL_BORDER, GRID_WIDTH + CELL_BORDER, GRID_HEIGHT + CELL_BORDER), CELL_BORDER) # Draw border around grid

        play_btn = button(20, GRID_HEIGHT + MARGIN + 20, BTN_WIDTH, BTN_HEIGHT, (238, 155, 0), play_btn_text)
        play_btn.draw(screen)
        next_btn.draw(screen)
        clear_btn.draw(screen)
        
        generation_surf = pygame.font.SysFont(None, 24).render(f'Generation: {num_generation}', True, (255, 255, 255))
        screen.blit(generation_surf, (2 * BTN_WIDTH + 3 * MARGIN, GRID_HEIGHT + 2 * MARGIN + 6))
        population_surf = pygame.font.SysFont(None, 24).render(f'Population: {len(current_gen)}', True, (255, 255, 255))
        screen.blit(population_surf, (4 * BTN_WIDTH + 4 * MARGIN, GRID_HEIGHT + 2 * MARGIN + 6)) # Display generation and population info

        pygame.display.flip()  # Update the display to reflect changes

    pygame.quit() # Quit pygame when the main loop ends

if __name__ == "__main__":
    main()