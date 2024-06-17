from time import sleep

# Запуск дополнительных тестов
# Если требуется проверка задания строго по ТЗ, установите значение в False
EXTRA_TESTS = True

# Возраст взрослого человека
ADULT_AGE = 18

# Скорость воспроизведения видео
DEFAULT_PLAY_SPEED = 1

class Video:
    """
    Видео и возрастные ограничения на его просмотр
    """
    def __init__(self, title, duration, time_now = 0, adult_mode = False):
        self.title = title
        self.duration = duration
        self.time_now = time_now
        self.adult_mode = adult_mode

    def __str__(self):
        return f'{self.title}'

    def authorize(self, user):
        """
        Проверка соответствия возраста пользователя возрастным ограничениям видео
        :param user: объект User
        :return: True, если просмотр разрешен; False - в противном случае
        """
        return True if not self.adult_mode or user.age >= ADULT_AGE else False

    def advance(self, play_speed):
        """
        Воспроизвести следующий фрагмент видео с заданной скоростью (заданный размер фрагмента).
        Например, при play_speed = 3, за одну реальную секунду будут воспроизведены три секунды видео.
        :param play_speed: скорость воспроизведения - размер фрагмента за одну реальную секунду (int)
        :return: фактический размер воспроизведенного фрагмента (int)
        """
        fragment_size = play_speed
        if self.time_now + play_speed > self.duration:
            fragment_size = self.duration - self.time_now

        for step in range(fragment_size):
            self.time_now += 1
            print(self.time_now, end=' ')
            sleep(1 / play_speed)

        return fragment_size

    def rewind(self, watch_start = 0):
        """
        Перемотка видео на заданное время
        :param watch_start: заданное время (int) (по-умолчанию - 0, т.е. начало видео)
        :return: None
        """
        if 0 <= watch_start <= self.duration:
            self.time_now = watch_start

class User:
    """
    Пользователь (Зритель)
    """
    def __init__(self, nickname, password, age):
        self.nickname = nickname
        self.password = hash(password)
        self.age = age

    def __str__(self):
        return f'{self.nickname}'

    def authenticate(self, password):
        """
        Проверка правильности ввода пароля
        :param password: введенный пароль (str)
        :return: True, если пароль совпадает; False - в противном случае
        """
        return self.password == hash(password)

class UrTube:
    """
    Платформа для показа видео
    """
    def __init__(self):
        self.users = dict()
        self.videos = dict()
        self.current_user = None

    def __str__(self):
        output = 'Список видео:\n'
        for video_title, video in self.videos.items():
            output += f'\t{str(video)}\n'
        output += 'Список пользователей:'
        for i, user_nickname in enumerate(self.users):
            output += f'{', ' if i > 0 else ' '}{user_nickname}'
        output += f'\nТекущий пользователь: {self.current_user}'
        return output

    def log_in(self, login, password):
        """
        Пытается найти пользователя в users с такими же логином и паролем.
        Если такой пользователь существует, то current_user меняется на найденного.
        :param login: имя пользователя (str)
        :param password: введенный пароль (str)
        :return: True, если пользователь найден и введен правильный пароль; False - в противном случае
        """
        if login in self.users and self.users[login].authenticate(password):
            self.current_user = self.users[login]
            return True
        return False

    def register(self, nickname, password, age):
        """
        Добавляет пользователя в список, если пользователя не существует (с таким же nickname).
        Если существует, выводит на экран: "Пользователь {nickname} уже существует".
        После регистрации, вход выполняется автоматически.
        :param nickname: имя пользователя (str)
        :param password: введенный пароль (str)
        :param age: возраст (int)
        :return: True, если пользователь добавлен; False - в противном случае
        """
        if nickname in self.users:
            print(f'Пользователь {nickname} уже существует')
            return False

        self.users[nickname] = User(nickname, password, age)
        self.current_user = self.users[nickname]
        return True

    def log_out(self):
        """
        Сброс текущего пользователя на None.
        :return: None
        """
        self.current_user = None

    def add(self, *videos):
        """
        Добавляет объекты Video в videos, если с таким же названием видео ещё не существует.
        В противном случае ничего не происходит.
        :param videos: неограниченное кол-во объектов Video
        :return: кол-во (int) добавленных видео
        """
        added = 0
        for video in videos:
            if video.title not in self.videos:
                self.videos[video.title] = video
                added += 1

        return added

    def get_video(self, title):
        """
        Возвращает объект Video, соответствующий заданному названию
        :param title: Название видео (str)
        :return: если видео с указанным названием существует, возвращает объект Video; None - в противном случае
        """
        return self.videos.get(title)

    def get_videos(self, search_string):
        """
        Поиск названий видео по заданной подстроке без учета регистра символов
        :param search_string: строка (str) поиска
        :return: список (list) найденных видео
        """
        found = list()
        for video_title in self.videos:
            if search_string.lower() in video_title.lower():
                found.append(video_title)
        return found

    def watch_video(self, title, play_speed = DEFAULT_PLAY_SPEED):
        """
        Запуск просмотра после проверки соответствия возраста пользователя запрашиваемому видео
        :param title: Строка (str) с названием видео
        :return: None
        """
        if not self.current_user:
            print("Войдите в аккаунт, чтобы смотреть видео")
            return

        video = self.get_video(title)
        if not video:
            return

        if not video.authorize(self.current_user):
            print(f"Вам нет {ADULT_AGE} лет, пожалуйста покиньте страницу")
            return

        for video_second in range(video.time_now, video.duration, play_speed):
            play_speed = video.advance(play_speed)

        print('Конец видео')
        video.rewind()


ur = UrTube()
v1 = Video('Лучший язык программирования 2024 года', 200)
v2 = Video('Для чего девушкам парень программист?', 10, adult_mode=True)

# Добавление видео
if not ur.add(v1, v2):
    print('Не удалось добавить видео в UrTube')
    exit(1)

# Проверка поиска
print(ur.get_videos('лучший'))
print(ur.get_videos('ПРОГ'))

# Проверка на вход пользователя и возрастное ограничение
ur.watch_video('Для чего девушкам парень программист?')
ur.register('vasya_pupkin', 'lolkekcheburek', 13)
ur.watch_video('Для чего девушкам парень программист?')
ur.register('urban_pythonist', 'iScX4vIJClb9YQavjAgF', 25)
ur.watch_video('Для чего девушкам парень программист?')

if EXTRA_TESTS:
    # Просмотр видео 18+ с трехкратной скоростью (почувствуйте ритм жизни кроликов!)
    ur.watch_video('Для чего девушкам парень программист?', 3)
    # Разгонимся еще быстрее. Бесконечность - не предел!
    ur.watch_video('Лучший язык программирования 2024 года', 300)

# Проверка входа в другой аккаунт
ur.register('vasya_pupkin', 'F8098FM8fjm9jmi', 55)
print(ur.current_user)

# Попытка воспроизведения несуществующего видео
ur.watch_video('Лучший язык программирования 2024 года!')

if EXTRA_TESTS:
    # Проверяем корректность выхода с платформы
    ur.log_out()
    ur.watch_video('Лучший язык программирования 2024 года!')

# Попытка входа с неправильным паролем
if EXTRA_TESTS and ur.log_in('vasya_pupkin', 'lol'):
    print(ur.current_user)
