from flask import Flask, request, render_template_string
import random
import string
import urllib.parse

app = Flask(__name__)

# =====================================
# LINK PIX NUBANK
# =====================================

PIX_LINK = "https://nubank.com.br/cobrar/30tc9u/6a0525af-9012-4be3-aff3-5b7e0be02390"

# =====================================
# WHATSAPP DO BARBEIRO
# =====================================

WHATSAPP = "5511930268285"

# =====================================
# AGENDAMENTOS
# =====================================

agendamentos = []

# =====================================
# GERAR CÓDIGO
# =====================================

def gerar_codigo():

    letras = string.ascii_uppercase
    numeros = string.digits

    codigo = "ROOTS-"

    for i in range(3):
        codigo += random.choice(letras)

    for i in range(3):
        codigo += random.choice(numeros)

    return codigo

# =====================================
# HTML
# =====================================

HTML = """

<!DOCTYPE html>
<html lang="pt-br">

<head>

<meta charset="UTF-8">

<title>Barbearia Roots</title>

<style>

body{
    background:#111;
    color:white;
    font-family:Arial;
    text-align:center;
    padding:40px;
}

.container{
    max-width:400px;
    margin:auto;
    background:#1b1b1b;
    padding:30px;
    border-radius:20px;
}

h1{
    color:red;
}

input, button{
    width:100%;
    padding:15px;
    margin-top:10px;
    border:none;
    border-radius:10px;
    font-size:16px;
}

button{
    background:red;
    color:white;
    cursor:pointer;
    font-weight:bold;
}

button:hover{
    opacity:0.9;
}

.codigo{
    font-size:40px;
    color:red;
    margin-top:20px;
    font-weight:bold;
}

.erro{
    background:red;
    padding:15px;
    border-radius:10px;
    margin-top:20px;
}

a{
    text-decoration:none;
}

</style>

</head>

<body>

<div class="container">

<h1>BARBEARIA ROOTS</h1>

<form method="POST">

<input type="text" name="nome" placeholder="Seu nome" required>

<input type="date" name="data" required>

<input type="time" name="horario" required>

<button type="submit">
CONTINUAR
</button>

</form>

{% if erro %}

<div class="erro">
{{ erro }}
</div>

{% endif %}

{% if mostrar_pix %}

<h2>Pagamento PIX</h2>

<a href="{{ pix }}" target="_blank">

<button>
PAGAR PIX R$0,50
</button>

</a>

<form method="POST">

<input type="hidden" name="nome" value="{{ nome }}">
<input type="hidden" name="data" value="{{ data }}">
<input type="hidden" name="horario" value="{{ horario }}">

<button type="submit" name="pago" value="1">
JÁ PAGUEI
</button>

</form>

{% endif %}

{% if codigo %}

<h2>AGENDAMENTO CONFIRMADO</h2>

<p><strong>Cliente:</strong> {{ nome }}</p>

<p><strong>Data:</strong> {{ data }}</p>

<p><strong>Horário:</strong> {{ horario }}</p>

<p>Seu código:</p>

<div class="codigo">
{{ codigo }}
</div>

<a href="{{ whatsapp }}" target="_blank">

<button>
ENVIAR NO WHATSAPP
</button>

</a>

{% endif %}

</div>

</body>
</html>

"""

# =====================================
# ROTA PRINCIPAL
# =====================================

@app.route("/", methods=["GET", "POST"])

def home():

    if request.method == "POST":

        nome = request.form["nome"]
        data = request.form["data"]
        horario = request.form["horario"]

        # VERIFICAR HORÁRIO DUPLICADO

        for agendamento in agendamentos:

            if agendamento["data"] == data and agendamento["horario"] == horario:

                return render_template_string(
                    HTML,
                    erro="Já existe uma pessoa nesse horário."
                )

        # CLIENTE PAGOU

        if request.form.get("pago"):

            codigo = gerar_codigo()

            agendamentos.append({
                "nome": nome,
                "data": data,
                "horario": horario,
                "codigo": codigo
            })

            # MENSAGEM CERTINHA WHATSAPP

            mensagem = f"""Novo Agendamento Barbearia Roots

Cliente: {nome}
Data: {data}
Horario: {horario}
Codigo: {codigo}
"""

            mensagem = urllib.parse.quote(mensagem)

            link_whats = f"https://wa.me/{WHATSAPP}?text={mensagem}"

            return render_template_string(
                HTML,
                codigo=codigo,
                nome=nome,
                data=data,
                horario=horario,
                whatsapp=link_whats
            )

        # MOSTRAR PIX

        return render_template_string(
            HTML,
            mostrar_pix=True,
            nome=nome,
            data=data,
            horario=horario,
            pix=PIX_LINK
        )

    return render_template_string(HTML)

# =====================================
# INICIAR SITE
# =====================================

app.run(debug=True)
