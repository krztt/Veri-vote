from idlelib.mainmenu import menudefs

import pygame
import os



pygame.init()

clock = pygame.time.Clock()
fps = 60

# file handling /storage
class Storage:
    #call all the variable
    def __init__(self):
        self.file_name = 'tally.txt'
        self.candidates = {}
        self.load_candidates()
    # loads the storage txt
    def load_candidates(self):
        if os.path.exists(self.file_name):
            with open(self.file_name, "r") as file:
                for line in file:
                    parts = line.strip().split(":")
                    if len(parts) == 2 and parts[1].isdigit():
                        name, count = parts[0], int(parts[1])
                        self.candidates[name] = count
                    else:
                        name = line.strip()
                        if name:
                            self.candidates[name] = 0
    # function that saves the name
    def save_candidate(self):
        with open(self.file_name, "w") as file:
            for name, count in self.candidates.items():
                file.write(f"{name}:{count}\n")
    # function to add a name
    def add_candidate(self, name,):
        name = name.strip()
        if name and name not in self.candidates:
            self.candidates[name] = 0
            self.save_candidate()
            print(f"Candidate '{name}' added.")
        else:
            print(f"Candidate '{name}' already exists or name is invalid.")

    # adds a vote to the chosen candidate
    def add_vote(self, name):
        name = name.strip()
        if name in self.candidates:
            self.candidates[name] += 1
            self.save_candidate()
            global mode
            mode = "vote_complete"
            print(f"Vote added for '{name}'. New count: {self.candidates[name]}")


#fonts
font = pygame.font.SysFont(None, 40)
#buttons
def draw_button(text, x, y, w, h, color, hover_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    button_rect = pygame.Rect(x, y, w, h)

    if button_rect.collidepoint(mouse):
        pygame.draw.rect(screen, hover_color, button_rect)
        if click[0] == 1 and action:
            action()
    else:
        pygame.draw.rect(screen, color, button_rect)

    text_surf = font.render(text, True, (255, 255, 255))
    text_rect = text_surf.get_rect(center=(x + w // 2, y + h // 2))
    screen.blit(text_surf, text_rect)
# function to automatically create buttons for every candidate
def draw_vote_buttons(storage_obj, start_x=100, start_y=100, button_w=250, button_h=50, gap=20):
    y = start_y
    for name in storage_obj.candidates:
        draw_button(
            f"Vote {name}",
            start_x,
            y,
            button_w,
            button_h,
            (50, 120, 180),
            (80, 150, 210),
            action=lambda n=name: storage_obj.add_vote(n)
        )
        y += button_h + gap




#pygame functions
storage = Storage()
screen_width = 800
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Vote Wisely')

# switch modes
mode = "menu"
def go_to_add():
    global mode
    mode = "add"

def go_to_vote():
    global mode
    mode = "vote"

def go_to_menu():
    global mode
    mode = "menu"
def go_to_vote_end():
    global mode
    mode = "vote_complete"


typed_name = ""

run = True
while run:
    #frame rate
    clock.tick(fps)
    screen.fill((30, 70, 30))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    # typing shortcut
        if event.type == pygame.KEYDOWN and mode == "add":
            if event.key == pygame.K_BACKSPACE:
                typed_name = typed_name[:-1]
            elif event.key == pygame.K_RETURN:
                if typed_name.strip():
                    storage.add_candidate(typed_name)
                    typed_name = ""
            else:
                typed_name += event.unicode




    #main app
    match mode:
        case "menu":
            draw_button("Nominate a candidate", 250, 120, 300, 60, (70, 130, 180), (100, 160, 210), go_to_add )
            draw_button("Vote for your candidate", 250, 250, 300, 60, (70, 130, 180), (100, 160, 210), go_to_vote)
        case "add":
            screen.fill((40, 40, 80))
            draw_button("Back to menu", 550, 20, 200, 50, (120, 60, 60), (180, 80, 80), go_to_menu)

            # Render input text
            input_box = pygame.Rect(150, 150, 500, 50)
            pygame.draw.rect(screen, (255, 255, 255), input_box, 2)

            input_surface = font.render(typed_name, True, (255, 255, 255))
            screen.blit(input_surface, (input_box.x + 10, input_box.y + 10))

            # Instructions
            hint = font.render("Type candidate name and press Enter", True, (200, 200, 200))
            screen.blit(hint, (150, 100))
        case "vote":
            screen.fill((40, 80, 80))
            draw_button("Back to menu", 550, 20, 200, 50, (120, 60, 60), (180, 80, 80), go_to_menu)
            draw_vote_buttons(storage, start_x=100, start_y=100)
        case "vote_complete":
            screen.fill((40,90,50))
            text_surface = font.render("You have voted successfully", True, (50,50,50))
            text_rect = text_surface.get_rect()
            text_rect.center = (screen_width /2 , screen_height / 2)
            screen.blit(text_surface, text_rect)
            draw_button("Back to menu", 550, 20, 200, 50, (120, 60, 60), (180, 80, 80), go_to_menu)


    pygame.display.update()

pygame.quit()

