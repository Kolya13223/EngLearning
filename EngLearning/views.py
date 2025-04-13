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
    stats = words_work.get_words_stats()
    return render(request, "stats.html", stats)

def check_test(request):
    if request.method == 'POST':
        cache.clear()
        words = words_work.get_words_and_its_translation()

        # Обрабатываем ответы с проверкой ошибок
        correct = 0
        # results = []
        # errors = []

        for i in range (0,len(words)) :
            word = words[i]
            selected_option_id = request.POST[f'answer_{i}']
            print(selected_option_id)
            print(word.id_of_answer)
            if (int(selected_option_id) == int(word.id_of_answer)):
                print('correct')
                correct = correct + 1
        # Успешная обработка
        return render(request, "result.html",context={"correct": correct,
                                                      'percentage': round((correct / len(words)) * 100)})


def check_words(request):
    words = words_work.get_words_and_its_translation()
    print(len(words))
    return render(request, "check_words.html", context={"words": words})
