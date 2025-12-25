# WarTunderDiscordRPC
Это консольная программа для отображения в Discord подробной информации для игры War Tunder на основе получаемых данных, доступных по адресу 8111

[![pypresence](https://img.shields.io/badge/using-pypresence-00bb88.svg?style=for-the-badge&logo=discord&logoWidth=20)](https://github.com/qwertyquerty/pypresence)
## Фото
**Статус, когда игра не запущена:**

<img width="448" height="159" alt="Game launching" src="https://github.com/user-attachments/assets/0086fecc-9d8e-40e8-b38b-0c5bc1cfd05f" />

**Статус, когда вы зашли в игру но не в бою:**

<img width="448" height="159" alt="Hangar" src="https://github.com/user-attachments/assets/b52858c8-e4db-4d2b-8bc1-af9510b257ca" />

**Статус, когда вы в бою на танке:**

<img width="448" height="159" alt="Ground" src="https://github.com/user-attachments/assets/0ef26c4d-86f4-49e1-b67e-dcf0d4a49f83" />

**Статус, когда вы в бою на самолёте:**

<img width="448" height="159" alt="Air" src="https://github.com/user-attachments/assets/e00e69f6-1cef-479f-8065-2824ecdda780" />

## Как запустить
1. Скачайте [WarThunderDiscordRPC.exe](https://github.com/MoTyaZ1/WarTunder-DiscordRichPresence/releases/tag/v1.2.0)
2. Скачайте [settings.json](https://github.com/MoTyaZ1/WarTunder-DiscordRichPresence/releases/tag/v1.2.0)
3. Запустите WarThunderDiscordRPC.exe
4. (Не обязательно) Откройте любым редактором settings.json для настройки консольной программы
## Как сделать автозапуск для Steam версии
1. Зайдите в Steam и откройте вкладку "БИБЛИОТЕКА"
2. Найдите вашу игру "War Tunder"
3. Откройте свойста "War Tunder"
4. В открытой вкладке "Общие" в "ПАРАМЕТРЫ ЗАПУСКА" скопируйте и вставте ```rpc.bat %COMMAND%```
5. Создайте rpc.txt с этим сожержанием:
```
@echo off
start beac_wt_mlauncher.exe
WarThunderDiscordRPC.exe
pause
```
6. Переименуйте rpc.txt в rpc.bat
7. Скачайте и поместите [WarThunderDiscordRPC.exe](https://github.com/MoTyaZ1/WarTunder-DiscordRichPresence/releases/tag/v1.2.0) и [settings.json](https://github.com/MoTyaZ1/WarTunder-DiscordRichPresence/releases/tag/v1.2.0) в корневую папку игры

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

large_img - `"main_logo"` (пока что только есть одно фото, у меня нету идей какую фотографию ещё добавить)

alt_presence - `true`: Параметры техники показываются в тексте картинки, `false`: Параметры техники показываются в основном статусе

lang - Язык интерфейса программы и отображения дополнительной информации discord `"ru"`: русский, `"en"` англиский

vehicle_details - `"speed"`: Скорость (км/ч), `"false"`: ничего не выводит

right_tank_state - `"rpm"`: Обороты двигателя, `"crew"`: Экипаж (текущий/максимальный), `"false"`: ничего не выводит

left_air_state - `"spd"`: Скорость TAS (км/ч), `"ias"`: Скорость IAS (км/ч), `"false"`: ничего не выводит

right_air_state - `"alt"`: Высота (м), `"fuel"`: Топливо (кг), `"false"`: ничего не выводит
## Ответы
Это моя первая программа 

Портировать консольную программу на Linux и особенно для macOS не буду (как минимум долгое время)

Протестированно было на Windows 11 Pro - 25H2 26220.7523 и Windows 10 Pro - 22H2 19045.6456
