import pygame, math

# Initialize Pygame
pygame.init()

# Set the window size
screen_size = (800, 600)
screen = pygame.display.set_mode(screen_size)

# Set the title of the window
pygame.display.set_caption("PCM Lab.")


debug = True

# Set the initial position of the dot
dot_pos = [400, 300]
dot_size = 20
dot_hp = 100

# Bullet conf

bullet_pos = None
bullet_speed = 15

# Floor conf
floor_color = "black_white"

# Menu conf
menu_background_filler = (0, 0, 255)

#Button conf
button_color = (255, 255, 255)
button2_color = (255, 255, 255)

#Mtext conf
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





# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                event_pos = event.pos
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
                if not bullet_pos and not paused:
                    bullet_pos = list(dot_pos)
                    mouse_pos = pygame.mouse.get_pos()
                    angle = math.atan2(mouse_pos[1] - dot_pos[1], mouse_pos[0] - dot_pos[0])
                    bullet_velocity = (bullet_speed * math.cos(angle), bullet_speed * math.sin(angle))
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                menu_open = not menu_open
                paused = not paused

    if not paused:
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

    #Draw HP
    font = pygame.font.Font(None, 30)
    hp_text = str(dot_hp) + " HP"
    hp_text_surface = font.render(hp_text, True, (0, 0, 0))
    hp_rect = hp_text_surface.get_rect()
    hp_rect.center = (380, 10)
    pygame.draw.rect(screen, (255, 0, 0), hp_rect)
    screen.blit(hp_text_surface, hp_rect)
    

    # Update the screen
    pygame.display.update()

    # Limit the frame rate
    clock.tick(60)

# Quit
pygame.quit()

"""
credits to https://github.com/savokbs. feel free to use it if you want to make this project better
"""
