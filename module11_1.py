from time import sleep
import requests
from requests import exceptions
from PIL import Image, ImageTk
from io import BytesIO
import tkinter as tk
from tkinter import messagebox


class MyApp(tk.Tk):
    '''
    Приложение демонстрирует работу различных библиотек (tkinter, requests, pillow) путем создания
    рабочего окна, загрузки изображения и выполнения некоторых манипуляций с ним. Интерфейс
    интуитивно понятен.

    Пожалуйста не бойтесь, здесь нет вредоносного кода!
    '''

    # Параметры рабочего окна
    _WINDOW_TITLE = 'МоЁ д/з # 11.1'
    _WINDOW_WIDTH = 450
    _WINDOW_HEIGHT = 450

    # Текст подсказки
    _LABEL_TEXT = 'Нажмите сюда'

    # Параметры загрузки изображения и манипуляции с ним
    _IMAGE_URL = r'http://www.python.org/static/opengraph-icon-200x200.png'
    _IMAGE_TARGET_WIDTH = 140
    _IMAGE_TARGET_HEIGHT = 140
    _IMAGE_SIZE_DELTA = 1.75
    _IMAGE_INTERFRAME_DELAY = 0.05
    _IMAGE_SMALLEST_SIZE = (1, 1)
    _IMAGE_GROWING_STARTING_ANGLE = 180
    _IMAGE_GROWING_TARGET_ANGLE = -180 - 360 * 3
    _IMAGE_CYCLE_TIMEOUT = 500

    def __init__(self):
        super().__init__()

        self.__labels = list()
        self.__current_label = None
        self.__is_terminating = False

        try:
            self.__prepare_main_layout()
        except RuntimeError:
            self.destroy()
        else:
            self.protocol('WM_DELETE_WINDOW', self.__on_destroy)
            self.mainloop()

    def __prepare_main_layout(self):
        pos_x = (self.winfo_screenwidth() // 2) - (self._WINDOW_WIDTH // 2)
        pos_y = (self.winfo_screenheight() // 2) - (self._WINDOW_HEIGHT // 2)

        self.title(self._WINDOW_TITLE)

        self.geometry(f'{self._WINDOW_WIDTH}x{self._WINDOW_HEIGHT}+{pos_x}+{pos_y}')
        self.resizable(False, False)

        self._image = self._download_image()

        self.__init_image_area()

    def __init_image_area(self):
        self.__labels.clear()

        self.rowconfigure(tuple(range(3)), weight=1, uniform="labels")
        self.columnconfigure(tuple(range(3)), weight=1, uniform="labels")

        for row_n in range(3):
            for col_n in range(3):
                label = tk.Label(self, relief="groove", borderwidth=3, text=self._LABEL_TEXT)
                label.bind("<Button-1>", lambda event: self.__move_image(event.widget))
                label.grid(column=col_n, row=row_n, sticky="news")
                self.__labels.append(label)

    def __image_animate(self, label, is_growing=True):
        size = self._IMAGE_SMALLEST_SIZE
        size_delta = self._IMAGE_SIZE_DELTA
        target_size = (self._IMAGE_TARGET_WIDTH, self._IMAGE_TARGET_HEIGHT)
        starting_angle = self._IMAGE_GROWING_STARTING_ANGLE
        target_angle = self._IMAGE_GROWING_TARGET_ANGLE

        if not is_growing:
            size = target_size
            size_delta = 1 / size_delta
            target_size = self._IMAGE_SMALLEST_SIZE
            starting_angle = 0
        angle = 0

        while True:
            if size == target_size:
                if is_growing:
                    photo_image = ImageTk.PhotoImage(self._image)
                    label.configure(image=photo_image)
                    label.image = photo_image
                else:
                    label.configure(image='')
                    label.image = None
                break

            # Формула изменения угла поворота
            # Сделал посложнее, чтобы картинка вращалась повеселее
            angle = starting_angle + target_angle * size[0] / target_size[0] if is_growing \
                else angle - 120 * (1 - 1 / size[0])

            # Крутим, вертим...
            image = self._image.rotate(angle)
            # Изменяем размер...
            image.thumbnail(size)
            photo_image = ImageTk.PhotoImage(image)
            label.configure(image=photo_image)
            label.image = photo_image

            self.update_idletasks()

            size = tuple(param * size_delta for param in size)
            if (is_growing and size > target_size) or (not is_growing and size < target_size):
                size = target_size

            sleep(self._IMAGE_INTERFRAME_DELAY)

    def __image_animate_all(self, angle):
        image = self._image.rotate(angle)
        photo_image = ImageTk.PhotoImage(image)
        for label in self.__labels:
            label.configure(image=photo_image)
            label.image = photo_image

        self.update_idletasks()

        if angle == -330:
            angle = 0
        else:
            angle -= 30

        self.after(100, self.__image_animate_all, angle)

    def __move_image(self, *args):
        if isinstance(args[0], int):
            # Не спрашивайте что это :-/
            return

        new_label = args[0]
        label = self.__current_label

        if label is not None:
            if label == new_label:
                return
            self.__image_animate(label, False)

        self.__current_label = new_label
        self.__image_animate(new_label)

    def _download_image(self):
        try:
            # Пробуем загрузить изображение
            # В случае возникновения ошибок предлагаем повторить попытку или завершить приложение
            # Позволяет продолжить работу в случае возникновения временных проблем со связью
            r = requests.get(self._IMAGE_URL)
            image_data = BytesIO(r.content)
            # Подгоняем размер изображения под размер окна
            resized = Image.open(image_data).resize((self._IMAGE_TARGET_WIDTH, self._IMAGE_TARGET_HEIGHT))
        except Exception as e:
            retry = messagebox.askretrycancel(
                title='Ошибка загрузки изображения',
                message=f'При попытке загрузки изображения:\n{self._IMAGE_URL} '
                        f'произошла ошибка:\n{e}\n\n'
                        'Повторить попытку?'
            )
            if retry:
                return self._download_image()
            else:
                raise RuntimeError

        return resized

    def __cycle_move_image(self):
        if self.__is_terminating:
            return

        i = iter(self.__labels)
        if self.__current_label in i:
            self.__move_image(next(i, self.__labels[0]))
        else:
            self.__move_image(self.__labels[0])

        self.after(self._IMAGE_CYCLE_TIMEOUT, self.__cycle_move_image)

    def __on_destroy(self):
        if self.__is_terminating:
            return

        for label in self.__labels:
            label.configure(text='')

        self.__cycle_move_image()

        answer = messagebox.askquestion(title='Как оно?', message='Зачёт? ;-)')
        self.__is_terminating = True

        if answer == 'yes':
            self.__image_animate_all(0)
            messagebox.showinfo(title='Эмоции', message='Ура!!!')

        self.destroy()


if __name__ == '__main__':
    app = MyApp()
