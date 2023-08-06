import time
import webbrowser as web
from datetime import datetime
from typing import Optional
from urllib.parse import quote

import pyautogui as pg

from vittawhatsapp.vitta import vitta, excecoes, log

pg.FAILSAFE = False

vitta.check_connection()


def enviarwhats_instantaneo(
    phone_no: str,
    message: str,
    wait_time: int = 15,
    tab_close: bool = False,
    close_time: int = 3,
) -> None:

    if not vitta.check_number(number=phone_no):
        raise excecoes.CountryCodeException('Código de país incorreto!')

    web.open(f"https://web.whatsapp.com/send?phone={phone_no}&text={quote(message)}")
    time.sleep(4)
    pg.click(vitta.WIDTH / 2, vitta.HEIGHT / 2)
    time.sleep(wait_time - 4)
    pg.press("enter")
    log.log_message(_time=time.localtime(), receiver=phone_no, message=message)
    if tab_close:
        vitta.close_tab(wait_time=close_time)


def enviarwhats(
    phone_no: str,
    message: str,
    time_hour: int,
    time_min: int,
    time_sec: int = 0,
    wait_time: int = 15,
    tab_close: bool = False,
    close_time: int = 3,
) -> None:

    if not vitta.check_number(number=phone_no):
        raise excecoes.CountryCodeException("Código de país incorreto!")

    if time_hour not in range(25) or time_min not in range(60) or time_sec not in range(60):
        raise Warning("Formato incorreto!")

    current_time = time.localtime()
    left_time = datetime.strptime(
        f"{time_hour}:{time_min}:{time_sec}", "%H:%M:%S"
    ) - datetime.strptime(
        f"{current_time.tm_hour}:{current_time.tm_min}:{current_time.tm_sec}",
        "%H:%M:%S",
    )

    if left_time.seconds < wait_time:
        raise excecoes.CallTimeException(
            "Call Time must be Greater than Wait Time as WhatsApp Web takes some Time to Load!"
        )

    sleep_time = left_time.seconds - wait_time
    print(
        f"Em {sleep_time} segundos o Whatsapp irá abrir e em {wait_time} segundos a mensagem será enviada!"
    )
    time.sleep(sleep_time)
    vitta.send_message(message=message, receiver=phone_no, wait_time=wait_time)
    log.log_message(_time=current_time, receiver=phone_no, message=message)
    if tab_close:
        vitta.close_tab(wait_time=close_time)


def enviarwhats_para_grupo(
    group_id: str,
    message: str,
    time_hour: int,
    time_min: int,
    wait_time: int = 15,
    tab_close: bool = False,
    close_time: int = 3,
) -> None:
    """Send WhatsApp Message to a Group at a Certain Time"""

    if time_hour not in range(25) or time_min not in range(60):
        raise Warning("Invalid Time Format!")

    current_time = time.localtime()
    left_time = datetime.strptime(
        f"{time_hour}:{time_min}:0", "%H:%M:%S"
    ) - datetime.strptime(
        f"{current_time.tm_hour}:{current_time.tm_min}:{current_time.tm_sec}",
        "%H:%M:%S",
    )

    if left_time.seconds < wait_time:
        raise excecoes.CallTimeException(
            "Call Time must be Greater than Wait Time as WhatsApp Web takes some Time to Load!"
        )

    sleep_time = left_time.seconds - wait_time
    print(
        f"In {sleep_time} Seconds WhatsApp will open and after {wait_time} Seconds Message will be Delivered!"
    )
    time.sleep(sleep_time)
    vitta.send_message(message=message, receiver=group_id, wait_time=wait_time)
    log.log_message(_time=current_time, receiver=group_id, message=message)
    if tab_close:
        vitta.close_tab(wait_time=close_time)


def enviarwhats_imagem(
    receiver: str,
    img_path: str,
    caption: str = "",
    wait_time: int = 15,
    tab_close: bool = False,
    close_time: int = 3,
) -> None:

    if (not receiver.isalnum()) and (not vitta.check_number(number=receiver)):
        raise excecoes.CountryCodeException("Country Code Missing in Phone Number!")

    current_time = time.localtime()
    vitta.send_image(
        path=img_path, caption=caption, receiver=receiver, wait_time=wait_time
    )
    log.log_image(_time=current_time, path=img_path, receiver=receiver, caption=caption)
    if tab_close:
        vitta.close_tab(wait_time=close_time)


def abrir_navegador() -> bool:

    try:
        web.open("https://web.whatsapp.com")
    except web.Error:
        return False
    else:
        return True
