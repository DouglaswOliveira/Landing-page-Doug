from flask import Flask, render_template, request, redirect
import urllib.parse
import re

app = Flask(__name__)

SEU_WHATSAPP = "5517982073231"

# Rota principal (home) – mantém POST do formulário
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        nome = request.form.get("nome")
        whatsapp_cliente = request.form.get("whatsapp")

        if not nome or not whatsapp_cliente:
            return redirect("/")

        # limpa caracteres do número
        whatsapp_cliente = re.sub(r"\D", "", whatsapp_cliente)

        # salva lead
        with open("leads.txt", "a", encoding="utf-8") as f:
            f.write(f"{nome} - {whatsapp_cliente}\n")

        mensagem = f"""
Olá Douglas, quero fazer minha declaração de Imposto de Renda 2026.

Nome: {nome}
WhatsApp do cliente: {whatsapp_cliente}

Gostaria de receber mais informações.
"""

        mensagem_codificada = urllib.parse.quote(mensagem)
        url = f"https://wa.me/{SEU_WHATSAPP}?text={mensagem_codificada}"

        return redirect(url)

    # Renderiza o index.html, que agora inclui a seção "Como restituir mais"
    return render_template("index.html")

# Health check
@app.route("/health")
def health():
    return "OK"

if __name__ == "__main__":
    app.run(debug=True)