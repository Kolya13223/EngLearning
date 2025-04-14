class Word:
    def __init__(self, word: str, translation: str, id: int):
        self.word = word
        self.translation = translation
        self.id_of_answer = id


def get_words_for_table():
    words = []
    with open("./data/words.csv", "r", encoding="utf-8") as f:
        cnt = 1
        for line in f.readlines()[1:]:
            word, definition, source = line.split(";")
            words.append([cnt, word, definition])
            cnt += 1
    return words


def get_words_and_its_translation():
    words = []
    with open("./data/words.csv", "r", encoding="utf-8") as f:
        counter = 0
        for line in f.readlines()[1:]:
            counter = counter + 1
            word, translation, source = line.split(";")
            new_word = Word(word, translation, counter)
            words.append(new_word)
    return words


def write_word(new_word, new_definition):
    new_word_line = f"{new_word};{new_definition};user"
    with open("./data/words.csv", "r", encoding="utf-8") as f:
        existing_words = [l.strip("\n") for l in f.readlines()]
        title = existing_words[0]
        old_words = existing_words[1:]
    words_sorted = old_words + [new_word_line]
    words_sorted.sort()
    new_words = [title] + words_sorted
    with open("./data/words.csv", "w", encoding="utf-8") as f:
        f.write("\n".join(new_words))


def create_and_write_res(pecantege):
    data = [f'1;{pecantege};{pecantege}']
    with open("./data/stats.csv", "w", encoding="utf-8") as file:
        file.write('\n'.join(data))


def update_stat_res(pecantege):
    file_path = "./data/stats.csv"
    with open(file_path, 'r', encoding='utf-8') as file:
        line = file.readline().strip()
        count_of_iters, _, max_res = map(int, line.split(';'))
    # Записываем обновленные данные
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(f"{count_of_iters + 1};{pecantege};{max(pecantege, max_res)}")


def get_words_stats(is_there_file):
    db_words = 0
    user_words = 0
    defin_len = []
    if is_there_file:
        file_path = "./data/stats.csv"
        with open(file_path, 'r', encoding='utf-8') as file:
            line = file.readline().strip()
            count_of_iters, prev_precentage, max_res = map(int, line.split(';'))

        with open("./data/words.csv", "r", encoding="utf-8") as f:
            for line in f.readlines()[1:]:
                word, define, added_by = line.split(";")
                words = define.split()
                defin_len.append(len(words))
                if "user" in added_by:
                    user_words += 1
                elif "db" in added_by:
                    db_words += 1
        stats = {
            "count_of_iters": count_of_iters,
            "prev_precentage": prev_precentage,
            "max_res": max_res,
            "words_all": db_words + user_words,
            "words_own": db_words,
            "words_added": user_words,
            "words_avg": sum(defin_len) / len(defin_len),
            "words_max": max(defin_len),
            "words_min": min(defin_len)
        }
    else:

        with open("./data/words.csv", "r", encoding="utf-8") as f:
            for line in f.readlines()[1:]:
                word, define, added_by = line.split(";")
                words = define.split()
                defin_len.append(len(words))
                if "user" in added_by:
                    user_words += 1
                elif "db" in added_by:
                    db_words += 1
        stats = {
            "words_all": db_words + user_words,
            "words_own": db_words,
            "words_added": user_words,
            "words_avg": sum(defin_len) / len(defin_len),
            "words_max": max(defin_len),
            "words_min": min(defin_len)
        }
    return stats
