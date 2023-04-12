import pathlib
import sys
import os
import shutil
import re
import random

'''
        папки 
    archives, video, audio, documents, images
'''

list_folder = ['archives', 'video', 'audio', 'documents', 'images']

""" 
    параметры сортировки файлов
    зображення('JPEG', 'PNG', 'JPG', 'SVG')
    відео файли('AVI', 'MP4', 'MOV', 'MKV')
    документи('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX')
    музика('MP3', 'OGG', 'WAV', 'AMR')
    архіви('ZIP', 'GZ', 'TAR')
    невідомі розширення.
"""

dict_sort = {
    'images': ['jpeg', 'png', 'jpg', 'svg'],
    'audio': ['mp3', 'ogg', 'wav', 'amr'],
    'documents': ['dov', 'docx', 'txt', 'pdf', 'xlsx', 'pptx'],
    'video': ['avi', 'mp4', 'mov', 'mkv'],
    'archives': ['zip', 'gz', 'tar']}

CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"

TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")

TRANS = {}
path_ff = None
path_folder_arhiv = None

for t, c in zip(TRANSLATION, CYRILLIC_SYMBOLS):
    TRANS[ord(c)] = t
    TRANS[ord(c.upper())] = t.upper()
                
def normalizate_(namefile):
    
    name_file = re.sub('\.\w+', '', namefile)
    name_file = re.sub('\W', '_', name_file)
    name_file = name_file.translate(TRANS)
       
    return name_file
                    
def end_sort(path_ff):
   for path_fd in path_ff.iterdir():
        if path_fd.name not in list_folder:
            if path_fd.is_dir():
                # 1 вариант  - удаляем все паки не всписке
                shutil.rmtree(path_fd)
                # 2 вариант - сначала проверка на пустату папки, потом вхождение в нее и удаление.
                # try:
                #     os.removedirs(path_fd) 
                # except:
                #     end_sort(path_fd)

def dict_sort_file(path_fd, name_file):
    
    suffix_ = path_fd.suffix[1:]
    path_name_file = name_file + path_fd.suffix
    path_file = None
    
    for key, val in dict_sort.items():
            
        if suffix_ in val:
            if key == 'archives':
                
                #  распаковка архива в папку
                global path_folder_arhiv
                path_folder_arhiv = pathlib.Path(f'{path_ff}\\{key}\\{name_file}')
                
                if not os.path.exists(path_folder_arhiv):
                    pathlib.Path.mkdir(path_folder_arhiv)
                
                # папака переноса архивного файла
                path_file_arhiv = pathlib.Path(f'{path_ff}\\{key}')
                path_file = path_file_arhiv
            else:
                path_file = pathlib.Path(f'{path_ff}\\{key}')
    
    if path_file is None:
        path_file = path_ff
    
    return pathlib.Path.joinpath(path_file, path_name_file)


def sort(path):
    
    # 2 итерация
    # по папкам и файлам и сортировка их по папкам
    for path_fd in path.iterdir():
        if path_fd.is_dir():
            if path_fd.name not in list_folder:
                sort(path_fd)
        else:
            name_file = normalizate_(path_fd.name)
            dst = dict_sort_file(path_fd, name_file)
            
            if pathlib.Path.is_file(dst):
                name_file = name_file + random.choice(name_file)
                dst = dict_sort_file(path_fd, name_file)
            
            if path_fd.suffix[1:] in dict_sort['archives']:
                # try:
                #    readr =  shutil.unpack_archive(path_fd, path_folder_arhiv)
                shutil.unpack_archive(path_fd, path_folder_arhiv)
                # except path_fd.ReadError as re:
                    # print (re)
                    
            pathlib.Path.replace(path_fd, dst)
          
                            
def star(path):
    
    global path_ff
    path_ff = pathlib.Path(path)
  
    # 1 итерация  - проврека, есть ли у нас необходимые папки видео и т.д.
    # если нет то создать, если есть то 
    list_dir =[]
    for path_fd in path_ff.iterdir():
        if path_fd.is_dir():
            list_dir.append(path_fd.name)
    
    for lf in list_folder:
        if lf not in list_dir:
            lf = f'{path_ff}\\{lf}'
            os.mkdir(lf)   
        
    sort(path_ff)

if __name__ == "__main__":
    try:
    
        if len(sys.argv) > 1:
            star(sys.argv[1])
            end_sort(path_ff)
    except IndexError: 
            print ('No path to folder. Take as parameter')

        
# path = 'E:\LessonsPython\GoIT_lesson_6\хлам'
# star(path)
# end_sort(path_ff)

