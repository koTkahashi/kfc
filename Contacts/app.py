{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Requirement already satisfied: line-bot-sdk in c:\\users\\髙橋滉\\appdata\\local\\programs\\python\\python39\\lib\\site-packages (1.19.0)\n",
      "Requirement already satisfied: requests>=2.0 in c:\\users\\髙橋滉\\appdata\\local\\programs\\python\\python39\\lib\\site-packages (from line-bot-sdk) (2.25.0)\n",
      "Requirement already satisfied: future in c:\\users\\髙橋滉\\appdata\\local\\programs\\python\\python39\\lib\\site-packages (from line-bot-sdk) (0.18.2)\n",
      "Requirement already satisfied: idna<3,>=2.5 in c:\\users\\髙橋滉\\appdata\\local\\programs\\python\\python39\\lib\\site-packages (from requests>=2.0->line-bot-sdk) (2.10)\n",
      "Requirement already satisfied: chardet<4,>=3.0.2 in c:\\users\\髙橋滉\\appdata\\local\\programs\\python\\python39\\lib\\site-packages (from requests>=2.0->line-bot-sdk) (3.0.4)\n",
      "Requirement already satisfied: certifi>=2017.4.17 in c:\\users\\髙橋滉\\appdata\\local\\programs\\python\\python39\\lib\\site-packages (from requests>=2.0->line-bot-sdk) (2020.11.8)\n",
      "Requirement already satisfied: urllib3<1.27,>=1.21.1 in c:\\users\\髙橋滉\\appdata\\local\\programs\\python\\python39\\lib\\site-packages (from requests>=2.0->line-bot-sdk) (1.26.2)\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "WARNING: You are using pip version 20.2.4; however, version 21.1.1 is available.\n",
      "You should consider upgrading via the 'c:\\users\\髙橋滉\\appdata\\local\\programs\\python\\python39\\python.exe -m pip install --upgrade pip' command.\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Requirement already satisfied: flask in c:\\users\\髙橋滉\\appdata\\local\\programs\\python\\python39\\lib\\site-packages (1.1.2)\n",
      "Requirement already satisfied: click>=5.1 in c:\\users\\髙橋滉\\appdata\\local\\programs\\python\\python39\\lib\\site-packages (from flask) (7.1.2)\n",
      "Requirement already satisfied: itsdangerous>=0.24 in c:\\users\\髙橋滉\\appdata\\local\\programs\\python\\python39\\lib\\site-packages (from flask) (1.1.0)\n",
      "Requirement already satisfied: Werkzeug>=0.15 in c:\\users\\髙橋滉\\appdata\\local\\programs\\python\\python39\\lib\\site-packages (from flask) (1.0.1)\n",
      "Requirement already satisfied: Jinja2>=2.10.1 in c:\\users\\髙橋滉\\appdata\\local\\programs\\python\\python39\\lib\\site-packages (from flask) (2.11.2)\n",
      "Requirement already satisfied: MarkupSafe>=0.23 in c:\\users\\髙橋滉\\appdata\\local\\programs\\python\\python39\\lib\\site-packages (from Jinja2>=2.10.1->flask) (1.1.1)\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "WARNING: You are using pip version 20.2.4; however, version 21.1.1 is available.\n",
      "You should consider upgrading via the 'c:\\users\\髙橋滉\\appdata\\local\\programs\\python\\python39\\python.exe -m pip install --upgrade pip' command.\n"
     ]
    }
   ],
   "source": [
    "!pip install line-bot-sdk\n",
    "!pip install flask"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "from flask import Flask, request, abort\n",
    "\n",
    "from linebot import (\n",
    "    LineBotApi, WebhookHandler\n",
    ")\n",
    "from linebot.exceptions import (\n",
    "    InvalidSignatureError\n",
    ")\n",
    "from linebot.models import (\n",
    "    MessageEvent, TextMessage, TextSendMessage,\n",
    ")\n",
    "import os"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "app = Flask(__name__)\n",
    "\n",
    "YOUR_CHANNEL_ACCESS_TOKEN = \"adCLwP6vZh5Ukj18CEzAMnh8Sh8tagXMLi1dkmtCCElGZG0SL4lkCV2EIEh/vtZM1lad6Sjw/ddFz/P3YcKZVf5jHTja34491UbpDl2DoDjG3kpTVWHBxfWs8q8OK2afBpmtRAxl0HIj5XIe+kKiGwdB04t89/1O/w1cDnyilFU=\"\n",
    "YOUR_CHANNEL_SECRET = \"4f90b0eb1ed7b83a125381cc793baf51\"\n",
    "\n",
    "line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)\n",
    "handler = WebhookHandler(YOUR_CHANNEL_SECRET)\n",
    "\n",
    "\n",
    "@app.route(\"/\")\n",
    "def hello_world():\n",
    "    return \"hello world\"\n",
    "\n",
    "@app.route(\"/callback\", methods=['POST'])\n",
    "def callback():\n",
    "    # get X-Line-Signature header value\n",
    "    signature = request.headers['X-Line-Signature']\n",
    "\n",
    "    # get request body as text\n",
    "    body = request.get_data(as_text=True)\n",
    "    app.logger.info(\"Request body: \" + body)\n",
    "\n",
    "    # handle webhook body\n",
    "    try:\n",
    "        handler.handle(body, signature)\n",
    "    except InvalidSignatureError:\n",
    "        print(\"Invalid signature. Please check your channel access token/channel secret.\")\n",
    "        abort(400)\n",
    "\n",
    "    return 'OK'\n",
    "\n",
    "\n",
    "@handler.add(MessageEvent, message=TextMessage)\n",
    "def handle_message(event):\n",
    "    line_bot_api.reply_message(\n",
    "        event.reply_token,\n",
    "        TextSendMessage(text=event.message.text))\n",
    "\n",
    "\n",
    "if __name__ == \"__main__\":\n",
    "    port = os.getenv(\"PORT\")\n",
    "    app.run(host=\"0.0.0.0\",port=port)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.9.4"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
