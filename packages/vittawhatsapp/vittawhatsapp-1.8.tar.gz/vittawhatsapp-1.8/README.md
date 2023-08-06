
## Instalacao

VittaWhatsapp esta disponivel no PyPi:

```bash
python3 -m pip install vittawhatsapp
```

```bash
pip3 install vittawhatsapp
```

```bash
pip install vittawhatsapp
```


## Clonar Repositorio



## Features

- Envia messagem para grupos e contatos do Whatsapp
- Envia imagens para grupos e contatos do Whatsapp

## Uso

```py
import vittawhatsapp

# Envia mensagem para um contato as 13:30
vittawhatsapp.enviarwhats("+5511999999999", "Ola", 13, 30)

# Envia a mesma mensagem e fecha a Aba depois de 2 segundos
vittawhatsapp.enviarwhats("+5511999999999", "Ola", 13, 30, 15, True, 2)

# Envia uma mensagem a um grupo a meia noite
vittawhatsapp.enviarwhats_para_grupo("AB123CDEFGHijklmn", "Oi a todos!", 0, 0)

# Envia uma imagem a um grupo com a mensagem Ola
vittawhatsapp.enviarwhats_imagem("AB123CDEFGHijklmn", "Images/exemplo.png", "Ola")

# Envia uma imagem a um contato
vittawhatsapp.enviarwhats_imagem("+5511999999999", "Images/exemplo.png")

```


## Licença

MIT.
