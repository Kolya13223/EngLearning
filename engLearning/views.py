"""
Модуль с представлениями (views) для приложения.

Содержит обработчики запросов, включая:
- Отображение страниц (страница курсов, профиля и т.д.)
- API-эндпоинты для взаимодействия с фронтендом
- Логику авторизации и регистрации
"""
import os
from typing import Any
from django.shortcuts import render
from django.core.cache import cache
from . import words_work



def index(request):
    return render(request, "index.html")


def words_list(request):
    words = words_work.get_words_for_table()
    return render(request, "word_list.html", context={"words": words})


def word_add(request: object) -> Any:
    return render(request, "word_add.html")


def send_word(request):
    if request.method == "POST":
        cache.clear()
        user_name = request.POST.get("name")
        new_word = request.POST.get("new_word", "")
        new_definition = request.POST.get("new_definition", "").replace(";", ",")
        context = {"user": user_name}
        if len(new_definition) == 0:
            context["success"] = False
            context["comment"] = "Описание должно быть не пустым"
        elif len(new_word) == 0:
            context["success"] = False
            context["comment"] = "Термин должен быть не пустым"
        else:
            context["success"] = True
            context["comment"] = "Ваш термин принят"
            words_work.write_word(new_word, new_definition)
        if context["success"]:
            context["success-title"] = ""
        return render(request, "word_request.html", context)
    else:
        word_add(request)


def show_stats(request):
    file_path = "./data/stats.csv"
    if os.path.exists(file_path):
        is_there_file = 1
        stats = words_work.get_words_stats(is_there_file)
        return render(request, "statsWithPrevRes.html", stats)
    else:
        is_there_file = 0
        stats = words_work.get_words_stats(is_there_file)
        return render(request, "statsWithoutPrevRes.html", stats)


def check_test(request):
    if request.method == 'POST':
        cache.clear()
        words = words_work.get_words_and_its_translation()
        # Обрабатываем ответы с проверкой ошибок
        correct = 0
        for i in range(0, len(words)):
            word = words[i]
            selected_option_id = request.POST[f'answer_{i}']
            print(selected_option_id)
            print(word.id_of_answer)
            if int(selected_option_id) == int(word.id_of_answer):
                print('correct')
                correct = correct + 1
        pecantege = round((correct / len(words)) * 100)
        file_path = "./data/stats.csv"
        if os.path.exists(file_path):
            # Уже были попытки
            with open(file_path, 'r', encoding='utf-8') as file:
                first_line = file.readline()
                parts = first_line.strip().split(';')
                prev_prcentage = int(parts[2])
            words_work.update_stat_res(pecantege)
            return render(request, "resultWithPrevRes.html",
                          context={"correct": correct,
                                   "numOfWords": len(words),
                                   'percentage': pecantege,
                                   'prev_percentage': prev_prcentage})
        else:
            # первая попытка
            words_work.create_and_write_res(pecantege)
            return render(request, "resultWithoutPrevRes.html", context={"correct": correct,
                                                                         "numOfWords": len(words),
                                                                         'percentage': pecantege})


def check_words(request):
    words = words_work.get_words_and_its_translation()
    return render(request, "check_words.html", context={"words": words})
