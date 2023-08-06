import os
import time

from vittawhatsapp.vitta.vitta import check_number


def format_message(message: str) -> str:
    msg_l = message.split(" ")
    new = []
    for x in msg_l:
        if "\n" in x:
            x = x.replace("\n", "")
            new.append(x) if not len(x) == 0 else None

        elif len(x) != 0:
            new.append(x)

    return " ".join(new)


def log_message(_time: time.struct_time, receiver: str, message: str) -> None:

    if not os.path.exists("vw_log.txt"):
        file = open("vw_log.txt", "w+")
        file.close()

    message = format_message(message)

    with open("vw_log.txt", "a", encoding="utf-8") as file:
        if check_number(receiver):
            file.write(
                f"Data: {_time.tm_mday}/{_time.tm_mon}/{_time.tm_year}\nHorário: {_time.tm_hour}:{_time.tm_min}\n"
                f"Whatsapp: {receiver}\nMensagem: {message}"
            )
        else:
            file.write(
                f"Data: {_time.tm_mday}/{_time.tm_mon}/{_time.tm_year}\nHorário: {_time.tm_hour}:{_time.tm_min}\n"
                f"ID do grupo: {receiver}\nMensagem: {message}"
            )
        file.write("\n--------------------\n")
        file.close()


def log_image(_time: time.struct_time, path: str, receiver: str, caption: str) -> None:

    if not os.path.exists("vw_log.txt"):
        file = open("vw_log.txt", "w+")
        file.close()

    caption = format_message(caption)

    with open("vw_log.txt", "a", encoding="utf-8") as file:
        if check_number(number=receiver):
            file.write(
                f"Data: {_time.tm_mday}/{_time.tm_mon}/{_time.tm_year}\nHorário: {_time.tm_hour}:{_time.tm_min}\n"
                f"Whatsapp: {receiver}\nImagem: {path}\nCapitura: {caption}"
            )

        else:
            file.write(
                f"Data: {_time.tm_mday}/{_time.tm_mon}/{_time.tm_year}\nHorário: {_time.tm_hour}:{_time.tm_min}\n"
                f"ID do grupo: {receiver}\nImagem: {path}\nCaptura: {caption}"
            )
        file.write("\n--------------------\n")
        file.close()
