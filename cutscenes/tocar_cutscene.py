import pygame, cv2

def tocar_cutscene_cv2(video_path, audio_path, screen):
    # Inicializa o mixer de som do pygame
    pygame.mixer.init()
    pygame.mixer.music.load(audio_path)
    pygame.mixer.music.play()

    # Abre o vídeo com OpenCV
    cap = cv2.VideoCapture(video_path)

    clock = pygame.time.Clock()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Redimensiona para o tamanho da tela
        frame = cv2.resize(frame, (1200, 800))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))

        screen.blit(surface, (0, 0))
        pygame.display.update()
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cap.release()
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    cap.release()
                    pygame.mixer.music.stop()
                    return

    cap.release()
    pygame.mixer.music.stop()