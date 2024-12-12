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
CIRCLE_RADIUS = 5

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Crear la pantalla
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("La Voz")

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

# Función para generar la serie de caracteres iguales
def generate_series(correct_length):
    symbols = ['A', 'B', 'C', 'D', '1', '2', '3', '4', '@', '#', '%']
    symbol = random.choice(symbols)  # Elegir un solo símbolo aleatorio
    series = symbol * correct_length  # Repetir ese símbolo 'correct_length' veces
    return series

# Función para dibujar los círculos de estado
def draw_circles(round_counter, results):
    cols = 5  # 5 columnas
    rows = 2  # 2 filas
    circle_spacing = 10  # Espaciado entre los círculos
    circle_radius = CIRCLE_RADIUS

    for i in range(round_counter):
        row = i // cols  # Dividir el índice entre las columnas para obtener la fila
        col = i % cols   # El índice modificado para obtener la columna

        x = 50 + col * (circle_radius * 2 + circle_spacing)
        y = 30 + row * (circle_radius * 2 + circle_spacing)

        color = WHITE
        if i < len(results):
            if results[i] == 'correct':
                color = GREEN
            elif results[i] == 'incorrect':
                color = RED
        
        pygame.draw.circle(screen, color, (x, y), circle_radius)

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
        num_audio = play_audio()
        correct_length = random.randint(1, 10)  # Longitud de la serie aleatoria
        series = generate_series(correct_length)

        # Mostrar la serie de caracteres en pantalla
        text = font.render(series, True, BLACK)
        text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        screen.blit(text, text_rect)

        start_time = time.time()
        user_responded = False
        user_pressed = False

        while time.time() - start_time < time_per_round:
            screen.fill(WHITE)
            draw_circles(round_counter, results)

            # Calcular el tiempo transcurrido en milisegundos
            elapsed_time = (time.time() - start_time) * 1000  # Convertir a milisegundos
            time_text = font.render(f"{elapsed_time:.3f} ms", True, BLACK)  # Mostrar con 3 decimales
            screen.blit(time_text, (SCREEN_WIDTH - 250, 30))  # Posición superior derecha

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

                    if correct_length == num_audio:  # Condición para acertar
                        score += 1
                        results.append('correct')
                    else:  # Si no debe presionar la tecla
                        errors += 1
                        results.append('incorrect')
                    break

        # Si no presionó nada, y el número no coincide, es un acierto
        if not user_responded and correct_length != num_audio:
            score += 1
            results.append('correct')

        # Si no presionó nada y el número coincide, es un error
        if not user_responded and correct_length == num_audio:
            errors += 1
            results.append('incorrect')

        # Aumentar la dificultad reduciendo el tiempo
        if round_counter % 2 == 0:
            time_per_round = max(FINAL_TIME, time_per_round * 0.9975)  # Reduce el tiempo en un 0.25% cada 2 rondas

        # Mostrar mensaje de error si no se presiona la tecla correctamente
        if not user_pressed:
            error_message = font.render("¡Te has tardado o presionado mal!", True, BLACK)
            text_rect = error_message.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)) 
            error_rect = text_rect.move(0, 128)
            screen.blit(error_message, error_rect)

        pygame.display.flip()
        pygame.time.delay(1000)

    # Resumen final
    screen.fill(WHITE)
    accuracy = (score / TOTAL_ROUNDS) * 100
    average_reaction_time = sum(reaction_times) / len(reaction_times) if reaction_times else 0
    result_text = f"Aciertos: {score}/{TOTAL_ROUNDS} ({accuracy:.2f}%)"
    
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