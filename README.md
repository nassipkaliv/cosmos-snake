to start install pygame
and run the programm

1. Введение и сюжет
Название: "Snake Game" <br> 

Жанр: Аркада с элементами приключения

Сеттинг: Фантастический мир "Квантовый лабиринт" — бесконечная сетка измерений, где обитают древние существа, порталы и магические фрукты. <br>

Сюжет: <br>

Вы — Змейка, маленький, но отважный путешественник, который оказался в Квантовом лабиринте после случайного падения через портал из своего родного леса. Лабиринт — это загадочное место, где время и пространство искажены, а порталы соединяют разные его части. Ваша цель — найти легендарный "Фрукт вечности", который, по слухам, может вернуть вас домой. Однако в лабиринте обитают стражи — движущиеся тени (враги), которые охраняют сокровища и пытаются остановить вас. Собирая магические фрукты, вы становитесь сильнее, но и привлекаете больше внимания стражей. <br>

2. Цели игры <br>
Основная цель: Набрать 100 очков, чтобы найти "Фрукт вечности" и завершить игру победой. <br>
Побочные задачи: <br>
Избегать столкновений с собственным хвостом и стражами. <br>
Использовать порталы для манёвров и сбора редких фруктов. <br>
Выживать как можно дольше, чтобы увидеть, как изменяется лабиринт. <br>
3. Механики игры <br>
3.1. Управление <br>
Игрок управляет Змейкой с помощью стрелок (вверх, вниз, влево, вправо). <br>
Змейка движется непрерывно, каждые 5 кадров обновляя позицию. <br>
3.2. Еда (Магические фрукты) <br>
Обычный фрукт (красный круг): Даёт 1 очко, ничего не меняет. <br>
Фрукт скорости (жёлтый треугольник): Удваивает скорость на 5 секунд, 2 очка. <br>
Фрукт замедления (синий квадрат): Уменьшает скорость вдвое на 5 секунд, 2 очка. <br>
Золотой фрукт (жёлтый ромб): Даёт 5 очков, редкий. <br>
Фрукт неуязвимости (розовый шестиугольник): Делает неуязвимым на 10 секунд, 3 очка, очень редкий. <br>
При сборе фрукта появляются частицы соответствующего цвета, усиливая визуальный эффект. <br>

3.3. Порталы <br>
Два портала (голубой и оранжевый, прямоугольники 30x30) на поле. <br>
При пересечении голубого портала Змейка телепортируется в оранжевый (и наоборот) с сохранением направления. <br>
Порталы остаются неподвижными, но их положение обновляется при перезапуске. <br>
3.4. Враги (Стражи) <br>
Три фиолетовых квадрата (20x20), движутся случайным образом, отскакивая от краёв. <br>
Столкновение с ними завершает игру, если Змейка не неуязвима. <br>
Скорость врагов — 2 пикселя за кадр. <br>
3.5. Прогрессия <br>
Каждые 10 очков базовая скорость увеличивается на 1, усложняя игру. <br>
При достижении 100 очков появляется финальный экран победы. <br>
4. Визуальные и звуковые элементы <br>
4.1. Визуальный стиль <br>
Фон: Темно-зелёная сетка (20x40x20) с более светлыми линиями (40x60x40), создающая ощущение глубины. <br>
Змейка: <br>
Голова — ярко-зелёная (0, 255, 0) с белым глазом, пульсирует (размер меняется на 3 пикселя). <br>
Тело — темно-зелёное (0, 150, 0) с эффектом свечения (прозрачность меняется). <br>
При неуязвимости голова становится розовой (255, 105, 180). <br>
Порталы: Голубой (0, 191, 255) и оранжевый (255, 165, 0) прямоугольники 30x30. <br>
Враги: Фиолетовые квадраты (139, 0, 139). <br>
Еда: Разные формы (круг, треугольник, квадрат, ромб, шестиугольник) с лёгкой анимацией масштаба. <br>
Частицы: Маленькие круги (2 пикселя), разлетаются при сборе фруктов. <br>
4.2. Звуки <br>
Фоновая музыка: Зацикленный трек (background_music.mp3), создающий атмосферу таинственного лабиринта. <br>
Эффекты: <br>
Сбор обычного/золотого/неуязвимого фрукта — eat.wav. <br>
Сбор фрукта скорости — speed.wav. <br>
Сбор фрукта замедления — slow.wav. <br>
Конец игры — gameover.wav.
5. Игровой процесс <br>
5.1. Начало игры <br>
Змейка появляется в центре (300, 200). <br>
Один фрукт, два портала и три врага генерируются случайно. <br>
Музыка начинает играть, Змейка движется вправо. <br>
5.2. Основной цикл <br>
Игрок управляет Змейкой, собирая фрукты для роста и очков. <br>
Использует порталы для быстрого перемещения или избегания врагов. <br>
Избегает столкновений с хвостом и врагами (кроме режима неуязвимости). <br>
Скорость растёт, делая игру сложнее. <br>
5.3. Поражение <br>
Если Змейка сталкивается с хвостом или врагом (без неуязвимости): <br>
Экран "Game Over" с текущим счётом. <br>
Проигрывается gameover.wav. <br>
Предлагается перезапуск (клавиша R). <br>
5.4. Победа <br>
При достижении 100 очков: <br>
Экран "Victory! You found the Fruit of Eternity!" с финальным счётом. <br>
Возможность перезапуска (R). <br>
6. Прогрессия и концовка <br>
6.1. Прогрессия <br>
0-30 очков: Лёгкий старт, игрок осваивает управление и порталы. <br>
30-60 очков: Увеличение скорости, больше врагов кажутся угрозой. <br>
60-90 очков: Высокая сложность, редкие фрукты становятся ключевыми. <br>
90-100 очков: Финальный рывок, напряжение максимальное. <br>
6.2. Концовка <br>
После 100 очков Змейка находит "Фрукт вечности" — огромный сияющий фрукт (в коде это финальный экран). <br>
Экран победы: "Поздравляем! Вы вернулись домой через Квантовый лабиринт!" <br>
Возможность начать заново, чтобы побить свой рекорд. <br>
