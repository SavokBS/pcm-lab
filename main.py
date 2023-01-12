import pygame, math

# Initialize Pygame
pygame.init()

# Set the window size
screen_size = (800, 600)
screen = pygame.display.set_mode(screen_size)

# Set the title of the window
pygame.display.set_caption("PCM Lab. | v2 | by savokbs in 2023")


debug = False

# Set the initial position of the dot
dot_pos = [400, 300]
dot_size = 20
dot_hp = 100

# Bullet conf

bullet_pos = None
bullet_speed = 5

# Floor conf
floor_color = "black_white"

# Menu conf
menu_background_filler = (0, 0, 255)

#Button conf
button_color = (255, 255, 255)
button2_color = (255, 255, 255)

# Mtext conf
mtext_color = (255, 255, 255)


# Set initial state for menu
menu_open = False
paused = False

# Create the clock to track FPS
clock = pygame.time.Clock()


# Create a button with a rectangle and text
font = pygame.font.Font(None, 30)
button_text = "Change Floor Color"
button_text_surface = font.render(button_text, True, (0, 0, 0))
button_rect = button_text_surface.get_rect()
button_rect.center = (400, 300)


# Chat conf
chat_open = True
chat_active = False
user_input = "Write something..."
previous_user_input = user_input
chat_color_inactive = pygame.Color('lightskyblue3')
chat_color_active = pygame.Color('dodgerblue2')
chat_color = chat_color_inactive
bubble_start_time = pygame.time.get_ticks()
dudka = False
# Main game loop
running = True
while running:
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            event_pos = event.pos
            if chat_input_box.collidepoint(event_pos):
                # Toggle the chat_active variable.
                user_input = ""
                chat_active = not chat_active
            else:
                chat_active = False
            сhat_color = chat_color_active if chat_active else chat_color_inactive
            
            
            # Change the current color of the input box.
            
            if event.button == 1:
                if button_rect.collidepoint(event_pos) and paused:
                    # Change the color of the floor
                    if floor_color == "black_white":
                        floor_color = "black"
                        menu_background_filler = (255, 255, 255)

                    elif floor_color == "black":
                        floor_color = "white"
                        menu_background_filler = (0, 0, 0)
                    else:
                        floor_color = "black_white"
                        menu_background_filler = (0, 0, 255)
                        button_color = (255, 255, 255)
                if button2_rect.collidepoint(event_pos) and paused:
                    if debug:
                        debug = False
                    else:
                        debug = True
                        
                # When LMB is clicked, create a new bullet at the position of the dot
                if not bullet_pos and not paused and not chat_active:
                    bullet_pos = list(dot_pos)
                    mouse_pos = pygame.mouse.get_pos()
                    angle = math.atan2(mouse_pos[1] - dot_pos[1], mouse_pos[0] - dot_pos[0])
                    bullet_velocity = (bullet_speed * math.cos(angle), bullet_speed * math.sin(angle))
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                menu_open = not menu_open
                paused = not paused
            if event.key == pygame.K_c:
                chat_open = not chat_open
            if chat_active:
                if event.key == pygame.K_RETURN:
                    print(user_input)
                    dudka = True
                    previous_user_input = user_input
                    bubble_start_time = pygame.time.get_ticks()
                    user_input = "Write something..."
                    chat_active = False
                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                else:
                    if len(user_input) < 21:
                        user_input += event.unicode

    if not paused and not chat_active:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            dot_pos[1] -= 5
        if keys[pygame.K_s]:
            dot_pos[1] += 5
        if keys[pygame.K_a]:
            dot_pos[0] -= 5
        if keys[pygame.K_d]:
            dot_pos[0] += 5
        if keys[pygame.K_SPACE]:
            dot_size = 30


    #Handle coords
    
    if dot_pos[0] < 0:
        dot_pos[0] = 800 - 1
    if dot_pos[0] > 800:
        dot_pos[0] = 1
    if dot_pos[1] < 0:
        dot_pos[1] = 600 -1
    if dot_pos[1] > 600:
        dot_pos[1] = 1


    # Create a menu background
    menu_background = pygame.Surface((200, 300))
    
    menu_background.fill(menu_background_filler)
    menu_rect = menu_background.get_rect()
    menu_rect.center = (screen_size[0] // 2, screen_size[1] // 2)


    # Create a button with a rectangle and text
    font = pygame.font.Font(None, 30)
    button2_text = f"Debug: {debug}"
    button2_text_surface = font.render(button2_text, True, (0, 0, 0))
    button2_rect = button2_text_surface.get_rect()
    button2_rect.center = (400, 250)

    


    # Create menu text
    font = pygame.font.Font(None, 30)
    mtext_text = f"PCM Lab"
    mtext_text_surface = font.render(mtext_text, True, (0, 0, 0))
    mtext_rect = mtext_text_surface.get_rect()
    mtext_rect.center = (400, 160)
    

    # Draw the floor
    if floor_color == "black_white":
        for x in range(0, 800, 40):
            for y in range(0, 600, 40):
                color = (255, 255, 255) if (x + y) % 80 == 0 else (0, 0, 0)
                pygame.draw.rect(screen, color, (x, y, 40, 40))
    elif floor_color == "black":
        screen.fill((0,0,0))
    else:
        screen.fill((255,255,255))
    
    # Draw the dot
    pygame.draw.circle(screen, (255, 0, 0), dot_pos, dot_size)


    # Draw the chat
    if chat_open:
        chat_input_box = pygame.Rect(50, 500, 350, 25)
        pygame.draw.rect(screen, chat_color, chat_input_box)
        chat_input_box_round = pygame.Rect(50, 500, 350, 25)
        pygame.draw.rect(screen, (0,0,0), chat_input_box_round,2)
        
        # Draw the chat text
        
        txt_surface = font.render(user_input, True, (255, 255, 255))
        screen.blit(txt_surface, (chat_input_box.x+5, chat_input_box.y+5))


    current_time = pygame.time.get_ticks()
    

    if dudka:
        if current_time - bubble_start_time < 5 * 1000: # 5 seconds
            chat_output_box = pygame.Rect(dot_pos[0]-160, dot_pos[1]-50, 350, 25)
            pygame.draw.rect(screen, (255,255,255), chat_output_box)
            chat_output_box_round = pygame.Rect(dot_pos[0]-160, dot_pos[1]-50, 350, 25)
            pygame.draw.rect(screen, (0,0,0), chat_output_box_round,2)
            txt_surface = font.render(previous_user_input, True, (0,0,0))
            screen.blit(txt_surface, (chat_output_box.x+5, chat_output_box.y+5))
        

    if menu_open:
        # Draw the menu background
        screen.blit(menu_background, menu_rect)
        # Draw the button
        pygame.draw.rect(screen, button_color, button_rect)
        screen.blit(button_text_surface, button_rect)

        # Draw the button2
        pygame.draw.rect(screen, button2_color, button2_rect)
        screen.blit(button2_text_surface, button2_rect)

        # Draw menu text
        pygame.draw.rect(screen, mtext_color, mtext_rect)
        screen.blit(mtext_text_surface,mtext_rect)
    
    

    if dot_size == 30:
        pygame.time.wait(200)
        dot_size = 20

    if bullet_pos:
        # Move the bullet
        if not paused:
            bullet_pos[0] += bullet_velocity[0]
            bullet_pos[1] += bullet_velocity[1]
        # Draw the bullet
        pygame.draw.circle(screen, (0, 0, 255), bullet_pos, 5)
        # Check if bullet is out of screen
        if bullet_pos[0] > 800 or bullet_pos[0] < 0 or bullet_pos[1] > 600 or bullet_pos[1] < 0:
            bullet_pos = None
        else:
            bullet_rect = pygame.Rect(bullet_pos[0]-5, bullet_pos[1]-5, 10, 10)
            dot_rect = pygame.Rect(dot_pos[0]-20, dot_pos[1]-20, 40, 40)
            # check if bullet hit the dot
            if bullet_rect.colliderect(dot_rect):
                if not paused:
                    dot_hp -= 1

    if debug:
        # Draw the FPS count
        fps = int(clock.get_fps())
        fps_text = str(fps)
        font = pygame.font.Font(None, 30)
        fps_surface = font.render(fps_text, True, (0, 0, 0))
        pygame.draw.rect(screen, (0, 0, 255), (5, 5, 35, 30))
        screen.blit(fps_surface, (10, 10))

        # Draw coords
        coords_text = str(dot_pos[0]) + ", " + str(dot_pos[1])
        font = pygame.font.Font(None, 30)
        coords_surface = font.render(coords_text, True, (0, 0, 0))
        pygame.draw.rect(screen, (0, 0, 255), (700, 5, 710, 30))
        screen.blit(coords_surface, (710, 10))

        # Draw ticks
        ticks_text = str(pygame.time.get_ticks()) + " ticks"
        font = pygame.font.Font(None, 30)
        ticks_surface = font.render(ticks_text, True, (0, 0, 0))
        pygame.draw.rect(screen, (0, 0, 255), (300, 5, 200, 30))
        screen.blit(ticks_surface, (350, 10))



    # #Draw HP
    # font = pygame.font.Font(None, 30)
    # hp_text = str(dot_hp) + " HP"
    # hp_text_surface = font.render(hp_text, True, (0, 0, 0))
    # hp_rect = hp_text_surface.get_rect()
    # hp_rect.center = (380, 10)
    # pygame.draw.rect(screen, (255, 0, 0), hp_rect)
    # screen.blit(hp_text_surface, hp_rect)
    

    # Update the screen
    pygame.display.update()

    # Limit the frame rate
    clock.tick(60)

# Quit
pygame.quit()

"""
credits to https://github.com/savokbs. feel free to use it if you want to make this project better
"""
