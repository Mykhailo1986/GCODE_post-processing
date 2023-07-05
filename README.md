## Post-Processing Script for PrusaSlicer.
(It should work on other slicing software based on Slic3r as well, not just PrusaSlicer. )

This post-processing script adds utility for the following features:

- Linear Advance: Adjusts the extrusion flow rate during printing to improve the quality of printed objects.
- AcrWeider: It's a G-Code post-processing tool that converts multiple line commands into arc commands. This effectively reduces the G-Code size, giving you smoother prints and faster print times.
- Fan Multiply Option: Allows multiplying the fan speed to enhance cooling during printing.
- Model Inspection Stops: Inserts pause commands in the G-code to enable closer inspection of the printed model at specific layers.

## Installation

1. Download the latest release of the post-processing script from the [GitHub repository](https://github.com/Mykhailo1986/GCODE_post-processing/releases).
2. Extract the contents of the downloaded ZIP file to a convenient location on your computer.

## Usage

~~1. Launch PrusaSlicer and import your 3D model.
~2. Configure your print settings as desired.
~3. In PrusaSlicer, navigate to **Print Settings** -> **Output Options** -> **Post-processing scripts**.
~5. Click Open to add the script to your PrusaSlicer configuration.
~6. Adjust any parameters or settings within the script if required.
~7. Slice your model as usual and export the G-code.

**Just drag the G-code file onto the executable file.**

## Contributing

Contributions to this post-processing script are welcome. If you have any bug fixes, improvements, or new feature ideas, please submit them as pull requests on the [GitHub repository](https://github.com/Mykhailo1986/GCODE_post-processing).

## License

This post-processing script is licensed under the [MIT License](https://chat.openai.com/LICENSE). Feel free to modify and distribute it as per the terms of the license.

## Contact

If you have any questions, issues, or suggestions, please contact the project maintainer:

- Mykhailo Kucher
- Email: [I_am_Misha@i.ua](mailto:I_am_misha@i.ua)
- GitHub: [Mykhailo1986](https://github.com/Mykhailo1986)

---
Українська:


Скрипт пост-обробки G-Code після слайсеру (Тестувалось на PursaSlicer)

Цей скрипт пост-обробки надає доступ до наступних функцій:

- Linear Advance: Налаштовує швидкість подачі екструзії під час друку для покращення якості надрукованих об'єктів.
- AcrWeider: Це інструмент пост-обробки G-коду, який перетворює кілька рядкових команд на дугові команди. Це ефективно зменшує розмір G-коду, забезпечуючи більш плавний друк і скорочення часу друку.- 
- Опція контролю швидкості вентилятора: Дозволяє повністю контролювати швидкість вентилятора на вибраних шарах, для покращення охолодження під час друку.
- Зупинки для перевірки моделі: Вставляє команди паузи в G-код та відвід каретки, для детальнішого огляду надрукованої моделі на певних шарах.

## Установка

1. Завантажте останню версію сценарію пост-обробки з [сховища GitHub](https://github.com/Mykhailo1986/GCODE_post-processing/releases).
2. Розпакуйте вміст завантаженого ZIP-файлу в зручне місце на вашому комп'ютері.

## Використання

~~1. Запустіть PrusaSlicer та імпортуйте вашу 3D-модель. 
~2. Налаштуйте параметри друку за бажанням. ~
~3. В PrusaSlicer перейдіть до **Параметри друку** -> **Параметри виводу** -> **Сценарії пост-обробки**. ~
~4. Клацніть кнопку **Додати сценарій** та перейдіть до розташування, де ви розпакували файли сценарію пост-обробки. 
~5.  Клацніть **Відкрити**, щоб додати сценарій до конфігурації PrusaSlicer. 
~6.  За необхідності налаштуйте будь-які параметри або налаштування в межах сценарію.
~7.  Наріжте вашу модель, як зазвичай, і експортуйте G-код.

**Просто перетягніть файл G-коду на виконавчий файл.**

## Участь

Участь у цьому проекті по пост-обробці є бажаним. Якщо у вас є ідеї що до  виправлення помилок, поліпшення або нові ідеї щодо функціоналу, будь ласка, надішліть їх у вигляді запитів на злиття (pull requests) у [сховище GitHub](https://github.com/Mykhailo1986/GCODE_post-processing).

## Ліцензія

Цей сценарій пост-обробки має ліцензію [MIT License](https://chat.openai.com/LICENSE). Ви можете вільно змінювати та поширювати його відповідно до умов ліцензії.

## Контактна інформація

Якщо у вас виникли питання, проблеми або пропозиції, будь ласка, зв'яжіться з утримувачем проекту:

- Михайло Кучер
- Електронна пошта: [I_am_Misha@i.ua](mailto:I_am_misha@i.ua)
- GitHub: [Mykhailo1986](https://github.com/Mykhailo1986)
