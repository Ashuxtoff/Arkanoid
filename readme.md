# Игра "Arkanoid"
***
Версия 1.0

Автор: Шукстов Александр [ashuxtoff@yandex.ru](ashuxtoff@yandex.ru)

Ревью выполнил: Чикунов Антон [https://anytask.org/accounts/profile/achikunov](https://anytask.org/accounts/profile/achikunov)

## Описание
***
Данное приложение является реализацией игры "Arkanoid"

## Требования
***
* Python версии не ниже 3.5.2
* PyGame версии не ниже 1.9.4

## Состав
***
* Модули `GameObjects/`
* Изображения `Images/`
* Файлы озвучки `Sounds/`
* Уровни `Levels/`
* Тесты `Tests/`

## Особенности
***
* 3 уровня прочности блоков
* Музыкальное споровождение во время непосредственного прохождения игры
* Изменение громкости клавишами "Вверх" и "Вниз"
* Несколько уровней, прохождение которых в аркадном режиме есть цель игры
* Счетчик количества жизней и очков игры
* Меню перед началом игры и после окончания игрового цикла
* Выбор имени игрока из меню (по дефолту имя Player)
* Доступ к таблице рекордов игроков
* 4 уровня сложности, регулирующих количество исходных жизней и скорость мяча
* Читы. Включение читов по клавише "С". Доступны читы: увеличение скорости мяча (F), уменьшение скорости мяча (S), удвоить очки за каждый удар мяча о блок (D) увеличить количество жизней на 1 (L) 

## Подробности реализации
***
В директории GameObjects хранятся объекты игры: мяч, доска, кирпичи, меню, карта, кнопки меню, образец игры, сама игра, а так же таблица рекордов и используемый шрифт.
В директории Images хранятся изображения объектов
В директории Levels хранятся уровни в их текстовом представлении
В директории Sounds хранятся файлы озвучки
В директории Tests хранятся тесты на логику игры