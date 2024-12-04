import pygame
import random
import time
import os
from pygame.locals import *

# Inicializa pygame y pygame.mixer
pygame.init()
pygame.mixer.init()

# Constantes
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FONT_SIZE = 50
INITIAL_TIME = 2  # segundos
FINAL_TIME = 1  # segundos
TOTAL_ROUNDS = 10
CIRCLE_RADIUS = 20

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Crear la pantalla
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Juego de Reacción")

# Cargar la fuente
font = pygame.font.Font(None, FONT_SIZE)

# Función para reproducir un número aleatorio en audio usando pygame.mixer
def play_audio():
    num = random.randint(1, 10)
    audio_path = f"assets/audio/{num}.mp3"  # Asumimos que los audios están en la carpeta "audio"
    
    # Verificar si el archivo de audio existe
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"El archivo de audio {audio_path} no se encuentra.")
    
    # Cargar y reproducir el archivo de audio
    sound = pygame.mixer.Sound(audio_path)
    sound.play()

    # Esperar a que termine la reproducción
    while pygame.mixer.get_busy():
        pygame.time.Clock().tick(10)
    
    return num

# Función para generar la serie de caracteres aleatorios
def generate_series():
    symbols = ['A', 'B', 'C', 'D', '1', '2', '3', '4', '@', '#', '%']
    length = random.randint(1, 10)
    series = random.choices(symbols, k=length)
    return ''.join(series), length

# Función para dibujar los círculos de estado
def draw_circles(round_counter, results):
    # Asegurarse de que la cantidad de resultados no exceda la cantidad de rondas
    for i in range(round_counter):
        x = 50 + i * (CIRCLE_RADIUS * 2 + 10)
        y = 30
        color = WHITE  # Por defecto, blanco
        if i < len(results):
            if results[i] == 'correct':
                color = GREEN
            elif results[i] == 'incorrect':
                color = RED
        pygame.draw.circle(screen, color, (x, y), CIRCLE_RADIUS)

# Función principal del juego
def main():
    score = 0
    errors = 0
    reaction_times = []
    results = []  # Guardamos los resultados (correcto, incorrecto) de cada intento
    time_per_round = INITIAL_TIME
    round_counter = 0

    while round_counter < TOTAL_ROUNDS:
        round_counter += 1
        screen.fill(WHITE)

        # Generar la serie y el número de audio
        series, correct_length = generate_series()
        num_audio = play_audio()

        # Mostrar la serie de caracteres en pantalla
        text = font.render(series, True, BLACK)
        text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        screen.blit(text, text_rect)

        # Contador de tiempo
        start_time = time.time()
        user_responded = False
        user_pressed = False

        # Mostrar el tiempo restante en la parte superior derecha
        while time.time() - start_time < time_per_round:
            screen.fill(WHITE)
            draw_circles(round_counter, results)  # Dibuja los círculos de estado
            time_left = time_per_round - (time.time() - start_time)
            time_text = font.render(f"{int(time_left)}", True, BLACK)
            screen.blit(time_text, (SCREEN_WIDTH - 100, 30))  # Posición superior derecha

            # Actualizar la pantalla
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    return
                if event.type == KEYDOWN and event.key == K_SPACE:
                    user_pressed = True
                    user_responded = True
                    reaction_time = time.time() - start_time
                    reaction_times.append(reaction_time)
                    if correct_length == num_audio:
                        score += 1
                        results.append('correct')
                    else:
                        errors += 1
                        results.append('incorrect')
                    break

        if not user_responded:
            errors += 1
            results.append('incorrect')

        # Aumentar la dificultad reduciendo el tiempo
        if round_counter % 2 == 0:
            time_per_round = max(FINAL_TIME, time_per_round * 0.75)

        # Mostrar el tiempo restante o un mensaje de error
        if not user_pressed:
            error_message = font.render("¡Te has tardado o presionado mal!", True, BLACK)
            screen.blit(error_message, (SCREEN_WIDTH / 4, SCREEN_HEIGHT / 2 + 60))

        pygame.display.flip()
        pygame.time.delay(1000)

    # Resumen final
    screen.fill(WHITE)
    accuracy = (score / TOTAL_ROUNDS) * 100
    average_reaction_time = sum(reaction_times) / len(reaction_times) if reaction_times else 0
    result_text = f"Aciertos: {score}/{TOTAL_ROUNDS} ({accuracy:.2f}%)"
    reaction_time_text = f"Tiempo promedio de reacción: {average_reaction_time:.3f} segundos"
    error_text = f"Errores: {errors} ({100 - accuracy:.2f}%)"
    
    result = font.render(result_text, True, BLACK)
    reaction_text = font.render(reaction_time_text, True, BLACK)
    error_percentage = font.render(error_text, True, BLACK)

    screen.blit(result, (SCREEN_WIDTH / 4, SCREEN_HEIGHT / 3))
    screen.blit(reaction_text, (SCREEN_WIDTH / 4, SCREEN_HEIGHT / 3 + 60))
    screen.blit(error_percentage, (SCREEN_WIDTH / 4, SCREEN_HEIGHT / 3 + 120))

    pygame.display.flip()
    pygame.time.delay(3000)

    pygame.quit()

if __name__ == "__main__":
    main()