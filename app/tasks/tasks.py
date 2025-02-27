from pathlib import Path
from PIL import Image
from app.tasks.celery import celery


@celery.task
def process_pic(
    path: str,    #путь до фото
):
    """
    Сжимаем фото
    """
    im_path = Path(path)    #конвертируем строчку в путь
    im = Image.open(im_path)    #открыть картинку по пути
    im_resized_1000_500 = im.resize((1000, 500))    #урезаем картинку
    im_resized_200_100 = im.resize((200, 100))
    im_resized_1000_500.save(f"app/static/images/resized_1000_500_{im_path.name}")    #сохраняем картинку (.name - расширение)
    im_resized_200_100.save(f"app/static/images/resized_200_100_{im_path.name}")
