import datetime
import threading
from queue import Queue
import pygame
import pygame_gui
import time

import requests
from pygame_gui.elements import UITextBox

from water_temp import get_water_temp
from weather import get_weather, get_icon_data, get_3_day_forecast

water_queue = Queue()

def next_even_wednesday(date):
    months = ['januari', 'februari', 'mars', 'april', 'maj', 'juni', 'juli', 'augusti', 'september', 'oktober', 'november', 'december']
    while date.weekday() != 2 or int(date.strftime('%V')) % 2 != 0:
        date += datetime.timedelta(days=1)

    return f'{date.day} {months[date.month-1]}'


def rot_center(image, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    x, y = image.get_rect().center
    new_rect = rotated_image.get_rect(center=image.get_rect(center=(x, y)).center)

    return rotated_image, new_rect

def get_mail():
    data = requests.get('https://portal.postnord.com/api/sendoutarrival/closest?postalCode=62436').json()
    return data['delivery'].split(',')[0]



def degrees_to_cardinal(d):
    '''
    note: this is highly approximate...
    '''
    dirs = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
            "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    ix = int((d + 11.25)/22.5)
    return dirs[ix % 16]

def update_weather():
    while True:
        pass



def main():
    pygame.init()

    pygame.display.set_caption('Quick Start')
    window_surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    # window_surface = pygame.display.set_mode((800, 480))

    background = pygame.Surface((800, 480))
    background.fill(pygame.Color('#000000'))

    manager = pygame_gui.UIManager((800, 480))

    clock = pygame.time.Clock()
    is_running = True
    start = datetime.datetime.now()
    old_min = -1
    while is_running:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    is_running = False
            manager.process_events(event)

        manager.update(time_delta)

        if old_min != datetime.datetime.now().minute:

            # Update
            weather = get_weather(57.67880768737381, 18.769248992539723)

            forecast = get_3_day_forecast(57.67880768737381, 18.769248992539723)

            weather_icon = pygame.image.load(f'./icons/{weather["weather"][0]["icon"]}.png')
            temp = weather['main']['temp']
            font = pygame.font.Font('freesansbold.ttf', 28)
            time_font = pygame.font.Font('freesansbold.ttf', 16)

            text_temp = font.render(str(temp) + '°', True, (255, 255, 255), (0, 0, 0))
            text_rect_temp = text_temp.get_rect()
            text_rect_temp.center = (175, 65)

            sunrise = weather['sys']['sunrise']
            sunrise = datetime.datetime.fromtimestamp(sunrise)
            h, m = sunrise.hour, sunrise.minute
            h = str(h) if h > 9 else '0' + str(h)
            m = str(m) if m > 9 else '0' + str(m)
            text_sunrise = font.render(f'{h}:{m}', True, (255, 255, 255), (0, 0, 0))
            text_rect_sunrise = text_sunrise.get_rect()
            text_rect_sunrise.topleft = (125, 120)

            wind_icon = pygame.image.load('./icons/wind_icon.png')
            wind_indicator = pygame.image.load('./icons/wind_indicator.png')
            angle = weather['wind']['deg']
            # wind_arrow, wind_rect = rot_center(wind_arrow, angle)
            wind_dir = degrees_to_cardinal(angle)

            wind_arrow = pygame.image.load(f'./icons/{wind_dir}.png')

            sunreise_icon = pygame.image.load('icons/sun_set.png')

            sunset = weather['sys']['sunset']
            sunset = datetime.datetime.fromtimestamp(sunset)
            h, m = sunset.hour, sunset.minute
            h = str(h) if h > 9 else '0' + str(h)
            m = str(m) if m > 9 else '0' + str(m)
            text_sunset = font.render(f'{h}:{m}', True, (255, 255, 255), (0, 0, 0))
            text_rect_sunset = text_sunset.get_rect()
            text_rect_sunset.topleft = (125, 175)
            sunset_icon = pygame.image.load('icons/sun_raise.png')

            wind_speed = weather['wind']['speed']
            wind_speed = str(wind_speed)
            wind_speed = wind_speed.replace('.', ',')
            text_wind_speed = font.render(f'{wind_speed} m/sec', True, (255, 255, 255), (0, 0, 0))
            text_wind_speed_rect = text_wind_speed.get_rect()
            text_wind_speed_rect.topleft = (360, 50)

            water_temp_icon = pygame.image.load('./icons/water_temp.png')

            # forecast
            days = []
            for d_no, day in enumerate(forecast):
                temp = day['temp']
                temp_text = font.render(f'{day["date"].day}/{day["date"].month} {str(temp)}°', True, (255, 255, 255),
                                        (0, 0, 0))
                temp_text_rect = temp_text.get_rect()
                temp_text_rect.topleft = (530, 50 + (d_no * 70))
                days.append({
                    'text': temp_text,
                    'rect': temp_text_rect,
                    'icon': day['icon']
                })

            water_temp = get_water_temp()
            water_temp_text = font.render(water_temp, True, (255, 255, 255), (0, 0, 0))
            water_temp_rect = water_temp_text.get_rect()
            water_temp_rect.topleft = (360, 120)

            old_min = datetime.datetime.now().minute
            print('update')

        window_surface.blit(background, (0, 0))
        window_surface.blit(weather_icon, (30, 35))
        window_surface.blit(text_temp, text_rect_temp)
        window_surface.blit(sunreise_icon, (30, 100))
        window_surface.blit(text_sunrise, text_rect_sunrise)
        window_surface.blit(sunset_icon, (30, 165))
        window_surface.blit(wind_icon, (250, 50))

        window_surface.blit(wind_indicator, (300, 47))

        window_surface.blit(wind_arrow, (300, 46))

        window_surface.blit(water_temp_icon, (250, 100))
        window_surface.blit(water_temp_text, water_temp_rect)

        window_surface.blit(text_wind_speed, text_wind_speed_rect)
        window_surface.blit(text_sunset, text_rect_sunset)

        for d in days:
            window_surface.blit(d['text'], d['rect'])
            icon = pygame.image.load(f'./icons/{d["icon"]}.png')
            window_surface.blit(icon, (d['rect'].x+170, d['rect'].y-10))

        trashcan = pygame.image.load('./icons/trash.png')
        window_surface.blit(trashcan, (100, 400))

        trash_text = font.render(next_even_wednesday(datetime.datetime.now()), True, (255, 255, 255), (0, 0, 0))
        trash_rect = trash_text.get_rect()
        trash_rect.topleft = (200, 410)
        window_surface.blit(trash_text, trash_rect)


        mailbox = pygame.image.load('./icons/mail.png')
        window_surface.blit(mailbox, (520, 400))
        mail_time = get_mail()

        mail_text = font.render(mail_time, True, (255, 255, 255), (0, 0, 0))
        mail_rect = mail_text.get_rect()
        mail_rect.topleft = (600, 410)
        window_surface.blit(mail_text, mail_rect)

        now = datetime.datetime.now()
        days1 = ['Mån', 'Tis', 'Ons', 'Tor', 'Fre', 'Lör', 'Sön']
        dd = now.day if now.day > 9 else f'0{now.day}'
        mm = now.month if now.month > 9 else f'0{now.month}'
        h = now.hour if now.hour > 9 else f'0{now.hour}'
        m = now.minute if now.minute > 9 else f'0{now.minute}'
        time_now = time_font.render(f'{days1[(now.weekday()) % 7]} {dd}/{mm} {h}:{m}', True, (255, 255, 0), (0, 0, 0))
        time_rect = time_now.get_rect()
        time_rect.topleft = (10, 10)
        window_surface.blit(time_now, time_rect)



        manager.draw_ui(window_surface)
        pygame.display.update()

if __name__ == '__main__':
    main()
