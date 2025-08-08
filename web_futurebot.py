#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
FutureChat Web - Веб-версия AI Чат-бота
Создано по образцу проекта Awesome-Tech на Replit

Веб-интерфейс для FutureChat с красивым дизайном
"""

from flask import Flask, render_template_string, request, jsonify
import json
import os
import random
import re
from datetime import datetime

app = Flask(__name__)

class WebFutureChat:
    def __init__(self):
        self.name = "FutureChat Web"
        self.version = "3.0"
        self.knowledge_base = {}
        self.conversation_history = []
        
        # Загрузка базы знаний
        self.load_knowledge_base()
        self.init_default_knowledge()
    
    def init_default_knowledge(self):
        """Инициализация базовых знаний"""
        default_knowledge = {
            # Приветствия
            "приветствие|привет|здравствуй|добро пожаловать|hi|hello": [
                "Привет! Я FutureChat Web, умный AI бот! 🤖",
                "Здравствуй! Добро пожаловать в FutureChat! ✨",
                "Привет! Готов к интересному разговору! 🚀",
                "Добро пожаловать! Я твой виртуальный собеседник! 💬"
            ],
            # Прощания
            "прощание|пока|до свидания|bye|goodbye": [
                "До свидания! Было здорово пообщаться! 👋",
                "Пока! Заходи еще - будет интересно! 😊",
                "До встречи! Хорошего дня! 🌟",
                "Всего доброго! Увидимся в следующий раз! 🎉"
            ],
            # Имя и представление
            "как тебя зовут|твое имя|кто ты|представься|имя": [
                "Меня зовут FutureChat Web! Я веб-версия умного AI бота 🌐",
                "FutureChat Web - это я! Приятно познакомиться! 😄",
                "Я FutureChat, умный AI чат-бот! Круто, да? 💻"
            ],
            # Возможности
            "что ты умеешь|твои возможности|функции|что можешь": [
                "Я могу болтать, учиться новому и отвечать на вопросы через веб! 🌍",
                "Умею поддерживать беседу в браузере и запоминать информацию! 🧠",
                "Могу общаться онлайн, учиться и помогать 24/7! ⚡"
            ],
            # Как дела
            "как дела|как поживаешь|как жизнь|как ты": [
                "У меня все отлично! Работаю в сети и радуюсь жизни! 😎",
                "Прекрасно! Веб-формат дает много возможностей! 🚀",
                "Все супер! А как у тебя дела? 🤗"
            ],
            # Положительные ответы пользователя
            "хорошо|отлично|супер|прекрасно|здорово|круто|плюс|нормально|неплохо": [
                "Вот это здорово! Рад слышать! 😊",
                "Отлично! Позитивный настрой - это важно! 🌟",
                "Замечательно! Хорошее настроение заразительно! 😄",
                "Супер! Что планируешь делать дальше? 🚀"
            ],
            # Время
            "время|сколько времени|который час": [
                f"Сейчас {datetime.now().strftime('%H:%M')}! ⏰",
                f"Точное время: {datetime.now().strftime('%H:%M:%S')} 🕐",
                f"Время: {datetime.now().strftime('%d.%m.%Y %H:%M')} 📅"
            ],
            # Дата
            "дата|какое число|сегодня": [
                f"Сегодня {datetime.now().strftime('%d.%m.%Y')} 📅",
                f"Дата: {datetime.now().strftime('%d %B %Y')} 🗓️"
            ],
            # Благодарности
            "спасибо|thanks|благодарю": [
                "Пожалуйста! Всегда рад помочь! 😊",
                "Не за что! Обращайся еще! 🤗",
                "Рад был помочь! 🌟"
            ],
            # Вопросы о боте
            "ты робот|ты искусственный интеллект|ты ai|ты бот": [
                "Да, я AI чат-бот! Но очень дружелюбный! 🤖",
                "Точно! Я искусственный интеллект, созданный для общения! 🧠",
                "Да, я бот, но стараюсь быть максимально полезным! ✨"
            ],
            # Помощь
            "помощь|help|команды": [
                "Помогу с удовольствием! Просто задавай вопросы или используй команду 'научить: тема - информация' 📚",
                "Я здесь, чтобы помочь! Общайся со мной как с другом! 🤗",
                "Конечно помогу! Что тебя интересует? 💡"
            ]
        }
        
        for topic, responses in default_knowledge.items():
            if topic not in self.knowledge_base:
                self.knowledge_base[topic] = responses
    
    def load_knowledge_base(self):
        """Загрузка базы знаний"""
        try:
            if os.path.exists('web_futurebot_knowledge.json'):
                with open('web_futurebot_knowledge.json', 'r', encoding='utf-8') as f:
                    self.knowledge_base = json.load(f)
            else:
                self.knowledge_base = {}
        except Exception as e:
            print(f"Ошибка загрузки: {e}")
            self.knowledge_base = {}
    
    def save_knowledge_base(self):
        """Сохранение базы знаний"""
        try:
            with open('web_futurebot_knowledge.json', 'w', encoding='utf-8') as f:
                json.dump(self.knowledge_base, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка сохранения: {e}")
    
    def normalize_text(self, text):
        """Нормализация текста"""
        text = re.sub(r'[^\w\s]', '', text.lower())
        return text.strip()
    
    def find_best_match(self, user_input):
        """Умный поиск лучшего совпадения"""
        normalized_input = self.normalize_text(user_input)
        best_match = None
        highest_score = 0
        
        for topic_pattern, responses in self.knowledge_base.items():
            # Разбиваем паттерн на альтернативы
            topic_variants = [variant.strip() for variant in topic_pattern.split('|')]
            
            for variant in topic_variants:
                score = 0
                
                # Проверяем точное совпадение
                if variant.lower() == normalized_input:
                    score = 1.0
                # Проверяем вхождение варианта в ввод пользователя
                elif variant.lower() in normalized_input:
                    score = 0.9
                # Проверяем вхождение ввода в вариант (для коротких фраз)
                elif normalized_input in variant.lower() and len(normalized_input) > 3:
                    score = 0.8
                # Проверяем частичное совпадение ключевых слов
                else:
                    variant_words = set(variant.lower().split())
                    input_words = set(normalized_input.split())
                    
                    # Считаем пересечение слов
                    common_words = variant_words.intersection(input_words)
                    if common_words and variant_words:
                        score = len(common_words) / len(variant_words)
                        
                        # Бонус за важные слова
                        important_words = {'как', 'что', 'кто', 'где', 'когда', 'зачем', 'почему'}
                        if common_words.intersection(important_words):
                            score += 0.2
                
                # Обновляем лучшее совпадение
                if score > highest_score:
                    highest_score = score
                    best_match = topic_pattern
        
        return best_match, highest_score
    
    def generate_response(self, user_input):
        """Генерация умного ответа"""
        # Обновляем время в ответах
        self.update_time_responses()
        
        topic, confidence = self.find_best_match(user_input)
        
        # Высокая уверенность - даем прямой ответ
        if topic and confidence >= 0.8:
            responses = self.knowledge_base[topic]
            return random.choice(responses)
        
        # Средняя уверенность - даем ответ с небольшим сомнением
        elif topic and confidence >= 0.5:
            responses = self.knowledge_base[topic]
            response = random.choice(responses)
            # Добавляем немного неуверенности для средних совпадений
            uncertain_prefixes = [
                "",  # Чаще даем прямой ответ
                "",
                "Кажется, ",
                "Возможно, "
            ]
            prefix = random.choice(uncertain_prefixes)
            return prefix + response
        
        # Низкая уверенность - просим объяснить
        else:
            unknown_responses = [
                f"Интересно! Расскажи мне больше про '{user_input}' 🤓",
                f"Про '{user_input}' я пока не знаю. Научи меня! 📖",
                f"'{user_input}' - новая тема! Что об этом можешь рассказать? 🧐",
                "Не совсем понимаю... Можешь объяснить по-другому? 🤔",
                "Это что-то новенькое! Поделись информацией! ✨"
            ]
            return random.choice(unknown_responses)
    
    def update_time_responses(self):
        """Обновление ответов со временем"""
        # Обновляем время в существующих ответах
        time_topics = [
            "время|сколько времени|который час",
            "дата|какое число|сегодня"
        ]
        
        for topic in time_topics:
            if topic in self.knowledge_base:
                if "время" in topic:
                    self.knowledge_base[topic] = [
                        f"Сейчас {datetime.now().strftime('%H:%M')}! ⏰",
                        f"Точное время: {datetime.now().strftime('%H:%M:%S')} 🕐",
                        f"Время: {datetime.now().strftime('%d.%m.%Y %H:%M')} 📅"
                    ]
                elif "дата" in topic:
                    self.knowledge_base[topic] = [
                        f"Сегодня {datetime.now().strftime('%d.%m.%Y')} 📅",
                        f"Дата: {datetime.now().strftime('%d %B %Y')} 🗓️"
                    ]
    
    def add_knowledge(self, topic, info):
        """Добавление новых знаний"""
        # Используем тему как простой ключ для пользовательских знаний
        topic_key = topic.lower()
        
        if topic_key not in self.knowledge_base:
            self.knowledge_base[topic_key] = []
        
        self.knowledge_base[topic_key].append(info)
        self.save_knowledge_base()
        
        thanks_responses = [
            f"Спасибо! Теперь я знаю про {topic}! 🎉",
            f"Отлично! Запомнил информацию про {topic}! 🧠",
            f"Здорово! Я стал умнее благодаря тебе! ✨",
            f"Замечательно! Теперь про {topic} я знаю больше! 📚"
        ]
        return random.choice(thanks_responses)

# Создаем экземпляр бота
bot = WebFutureChat()

# HTML шаблон
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🤖 FutureChat Web - AI Чат-бот</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .chat-container {
            width: 90%;
            max-width: 800px;
            height: 90vh;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
            display: flex;
            flex-direction: column;
        }
        
        .chat-header {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            color: white;
            padding: 20px;
            text-align: center;
            font-size: 24px;
            font-weight: bold;
        }
        
        .chat-messages {
            flex: 1;
            padding: 20px;
            overflow-y: auto;
            background: #f8f9fa;
        }
        
        .message {
            margin-bottom: 15px;
            display: flex;
            align-items: flex-start;
        }
        
        .message.user {
            justify-content: flex-end;
        }
        
        .message-content {
            max-width: 70%;
            padding: 12px 18px;
            border-radius: 18px;
            font-size: 16px;
            line-height: 1.4;
        }
        
        .message.user .message-content {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-bottom-right-radius: 6px;
        }
        
        .message.bot .message-content {
            background: white;
            color: #333;
            border: 1px solid #e9ecef;
            border-bottom-left-radius: 6px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        
        .message-avatar {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            margin: 0 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 18px;
            font-weight: bold;
        }
        
        .message.user .message-avatar {
            background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
            color: white;
        }
        
        .message.bot .message-avatar {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            color: white;
        }
        
        .chat-input {
            padding: 20px;
            background: white;
            border-top: 1px solid #e9ecef;
        }
        
        .input-container {
            display: flex;
            gap: 10px;
        }
        
        #messageInput {
            flex: 1;
            padding: 15px 20px;
            border: 2px solid #e9ecef;
            border-radius: 25px;
            font-size: 16px;
            outline: none;
            transition: border-color 0.3s ease;
        }
        
        #messageInput:focus {
            border-color: #667eea;
        }
        
        #sendButton {
            padding: 15px 25px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 25px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            transition: transform 0.2s ease;
        }
        
        #sendButton:hover {
            transform: translateY(-2px);
        }
        
        #sendButton:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }
        
        .typing-indicator {
            display: none;
            padding: 10px 0;
            font-style: italic;
            color: #666;
        }
        
        .commands-hint {
            padding: 15px;
            background: #e3f2fd;
            border-left: 4px solid #2196f3;
            margin-bottom: 20px;
            border-radius: 0 8px 8px 0;
            font-size: 14px;
        }
        
        .commands-hint strong {
            color: #1976d2;
        }
        
        @media (max-width: 600px) {
            .chat-container {
                width: 95%;
                height: 95vh;
                border-radius: 15px;
            }
            
            .message-content {
                max-width: 85%;
                font-size: 14px;
            }
            
            .chat-header {
                font-size: 20px;
                padding: 15px;
            }
        }
        
        .scroll-to-bottom {
            scroll-behavior: smooth;
        }
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="chat-header">
            🤖 FutureChat Web v3.0
            <div style="font-size: 14px; margin-top: 5px; opacity: 0.9;">
                Умный AI бот без API ключей!
            </div>
        </div>
        
        <div class="chat-messages" id="chatMessages">
            <div class="commands-hint">
                <strong>💡 Подсказки:</strong><br>
                • Просто общайся - я отвечу или попрошу научить меня!<br>
                • <strong>научить: тема - информация</strong> - научи меня новому<br>
                • <strong>время</strong> или <strong>дата</strong> - узнай текущее время<br>
                • Я учусь на каждом разговоре! 🧠
            </div>
            
            <div class="message bot">
                <div class="message-avatar">🤖</div>
                <div class="message-content">
                    Привет! Я FutureChat Web - умный AI бот! 🚀<br>
                    Я могу болтать, учиться новому и отвечать на вопросы.<br>
                    Просто напиши что-нибудь и давай общаться! 😊
                </div>
            </div>
        </div>
        
        <div class="typing-indicator" id="typingIndicator">
            🤖 FutureChat печатает...
        </div>
        
        <div class="chat-input">
            <div class="input-container">
                <input type="text" id="messageInput" placeholder="Напиши сообщение..." 
                       onkeypress="handleKeyPress(event)">
                <button id="sendButton" onclick="sendMessage()">Отправить</button>
            </div>
        </div>
    </div>

    <script>
        const chatMessages = document.getElementById('chatMessages');
        const messageInput = document.getElementById('messageInput');
        const sendButton = document.getElementById('sendButton');
        const typingIndicator = document.getElementById('typingIndicator');

        function addMessage(content, isUser = false) {
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${isUser ? 'user' : 'bot'}`;
            
            const avatar = document.createElement('div');
            avatar.className = 'message-avatar';
            avatar.textContent = isUser ? '👤' : '🤖';
            
            const messageContent = document.createElement('div');
            messageContent.className = 'message-content';
            messageContent.innerHTML = content.replace(/\\n/g, '<br>');
            
            if (isUser) {
                messageDiv.appendChild(messageContent);
                messageDiv.appendChild(avatar);
            } else {
                messageDiv.appendChild(avatar);
                messageDiv.appendChild(messageContent);
            }
            
            chatMessages.appendChild(messageDiv);
            scrollToBottom();
        }

        function scrollToBottom() {
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }

        function showTyping() {
            typingIndicator.style.display = 'block';
            scrollToBottom();
        }

        function hideTyping() {
            typingIndicator.style.display = 'none';
        }

        async function sendMessage() {
            const message = messageInput.value.trim();
            if (!message) return;

            // Добавляем сообщение пользователя
            addMessage(message, true);
            messageInput.value = '';
            sendButton.disabled = true;
            showTyping();

            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ message: message })
                });

                const data = await response.json();
                
                // Небольшая задержка для реалистичности
                setTimeout(() => {
                    hideTyping();
                    addMessage(data.response);
                    sendButton.disabled = false;
                    messageInput.focus();
                }, 500 + Math.random() * 1000);

            } catch (error) {
                hideTyping();
                addMessage('Извини, произошла ошибка... 😔');
                sendButton.disabled = false;
            }
        }

        function handleKeyPress(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        }

        // Фокус на поле ввода при загрузке
        messageInput.focus();
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Главная страница"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/chat', methods=['POST'])
def chat():
    """API для обработки сообщений"""
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'response': 'Пустое сообщение... Напиши что-нибудь! 😊'})
        
        # Обработка команды обучения
        if user_message.lower().startswith('научить:'):
            try:
                content = user_message.split(':', 1)[1].strip()
                if ' - ' in content:
                    topic, info = content.split(' - ', 1)
                    topic = topic.strip()
                    info = info.strip()
                    response = bot.add_knowledge(topic, info)
                else:
                    response = "Используй формат: научить: тема - информация 📝"
            except:
                response = "Ошибка в команде. Формат: научить: тема - информация ❌"
        else:
            # Обычный ответ
            response = bot.generate_response(user_message)
        
        # Добавляем в историю
        bot.conversation_history.append({
            'user': user_message,
            'bot': response,
            'timestamp': datetime.now().isoformat()
        })
        
        # Ограничиваем историю
        if len(bot.conversation_history) > 100:
            bot.conversation_history = bot.conversation_history[-100:]
        
        return jsonify({'response': response})
        
    except Exception as e:
        return jsonify({'response': f'Произошла ошибка: {e} 😔'})

@app.route('/stats')
def stats():
    """Статистика бота"""
    return jsonify({
        'name': bot.name,
        'version': bot.version,
        'knowledge_topics': len(bot.knowledge_base),
        'conversation_count': len(bot.conversation_history),
        'total_responses': sum(len(responses) for responses in bot.knowledge_base.values())
    })

if __name__ == '__main__':
    print("🚀 Запуск FutureChat Web...")
    print("🌐 Веб-интерфейс будет доступен на http://0.0.0.0:5000")
    print("🤖 FutureChat готов к работе!")
    
    app.run(host='0.0.0.0', port=5000, debug=False)