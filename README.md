# WarTunderDiscordRPC
Это консольная программа для отображения в Discord подробной информации для игры War Tunder на основе получаемых данных, доступных по адресу 8111
## Фото
<img width="420" height="136" alt="image" src="https://github.com/user-attachments/assets/662e6322-fb9f-44d7-bd8c-ecd3ca941637" />
<img width="420" height="136" alt="image" src="https://github.com/user-attachments/assets/e9b582a9-8a2f-4827-a899-8488b5a9e663" />
<img width="420" height="136" alt="image" src="https://github.com/user-attachments/assets/49aedc3c-5e28-4d57-a831-45cdbd1d85f2" />
<img width="420" height="136" alt="image" src="https://github.com/user-attachments/assets/1a62edbc-21d1-4905-9950-01c3f431d989" />

## Настройки по умолчанию
```
{
  "refresh_time": 7,
  "large_img": "main_logo",
  "alt_presence": false,
  "lang": "ru",
  "vehicle_details": true,
  "left_tank_state": "speed",
  "right_tank_state": "crew",
  "left_air_state": "spd",
  "right_air_state": "alt",
}
```
## Объяснение настроек
refresh_time - Интервал обновления статуса в секундах Рекомендовано `7` Минимально `5`

large_img - `"main_logo"` пока что только есть одно фото

alt_presence - `true`: Параметры техники показываются в тексте картинки, `false`: Параметры техники показываются в основном статусе

lang - Язык интерфейса программы и отображения дополнительной информации discord `"ru"`: русский, `"en"` англиский

vehicle_details - `"speed"`: Скорость (км/ч), `"false"`: ничего не выводит

right_tank_state - `"rpm"`: Обороты двигателя, `"crew"`: Экипаж (текущий/максимальный), `"false"`: ничего не выводит

left_air_state - `"spd"`: Скорость TAS (км/ч), `"ias"`: Скорость IAS (км/ч), `"false"`: ничего не выводит

right_air_state - `"alt"`: Высота (м), `"fuel"`: Топливо (кг), `"false"` ничего не выводит
## Как запустить
1. Скачайте [WarThunderDiscordRPC.exe](https://github.com/MoTyaZ1/WarTunder-DiscordRichPresence/releases/tag/v1.0.0)
2. Скачайте [settings.json](https://github.com/MoTyaZ1/WarTunder-DiscordRichPresence/releases/tag/v1.0.0)
3. запустите WarThunderDiscordRPC.exe
4. (не обязательно) откройте любым редактором settings.json для настройки консольной программы
## Ответы
Это моя первая программа 

Портировать консольную программу на Linux и macOS не буду

Протестированно было на Windows 11 Pro - 25H2 26220.7523 и Windows 10 Pro - 22H2 19045.6456
