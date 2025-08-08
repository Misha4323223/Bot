#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
FutureChat Web Advanced - Продвинутая веб-версия AI Чат-бота с ChatterBot
Объединяет машинное обучение ChatterBot с удобным веб-интерфейсом
"""

from flask import Flask, render_template_string, request, jsonify
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer
import json
import os
import random
import re
from datetime import datetime

app = Flask(__name__)

class WebAdvancedFutureChat:
    def __init__(self):
        self.name = "FutureChat Web Advanced"
        self.version = "3.5"
        self.fallback_knowledge = {}
        self.conversation_history = []
        
        # Инициализация ChatterBot
        self.initialize_chatbot()
        
        # Загрузка дополнительных знаний
        self.load_fallback_knowledge()
        self.init_fallback_knowledge()
        
        # Загрузка массивной энциклопедической базы
        self.load_encyclopedia_knowledge()
        
    def initialize_chatbot(self):
        """Инициализация ChatterBot с настройками"""
        try:
            print("🧠 Инициализация ChatterBot...")
            
            # Упрощенная инициализация
            self.chatbot = ChatBot(
                'FutureChat Advanced',
                storage_adapter='chatterbot.storage.SQLStorageAdapter',
                database_uri='sqlite:///web_advanced_chatbot.sqlite3',
                logic_adapters=[
                    'chatterbot.logic.BestMatch',
                    'chatterbot.logic.TimeLogicAdapter'
                ]
            )
            
            print("🎓 Начало обучения...")
            # Обучение бота
            self.train_chatbot()
            self.chatbot_available = True
            print("✅ ChatterBot готов к работе!")
            
        except Exception as e:
            print(f"❌ Ошибка инициализации ChatterBot: {e}")
            print(f"Подробности ошибки: {str(e)}")
            self.chatbot = None
            self.chatbot_available = False
    
    def train_chatbot(self):
        """Обучение ChatterBot"""
        try:
            # Тренеры
            if not self.chatbot:
                return
            list_trainer = ListTrainer(self.chatbot)
            
            # Русскоязычные диалоги
            russian_conversations = [
                # Приветствие
                "Привет", "Привет! Я продвинутый AI бот с машинным обучением! 🤖",
                "Здравствуй", "Здравствуй! Как дела? Я готов к умному разговору! ✨",
                "добро пожаловать", "Спасибо! Я рад быть здесь и общаться с тобой! 🎉",
                
                # Представление
                "Как тебя зовут?", "Меня зовут FutureChat Advanced. Я умный AI бот с машинным обучением.",
                "Кто ты?", "Я продвинутый AI чат-бот, использующий технологии машинного обучения для понимания и генерации ответов.",
                "Представься", "Привет! Я FutureChat Advanced - умный AI бот, который учится на каждом разговоре.",
                
                # Возможности
                "Что ты умеешь?", "Я могу умно беседовать, учиться на примерах, решать математику, определять время и запоминать информацию!",
                "Твои функции?", "Машинное обучение, обработка естественного языка, математические вычисления, работа со временем и обучение на диалогах.",
                "На что ты способен?", "Я использую алгоритмы машинного обучения для понимания контекста и генерации умных ответов!",
                
                # Как дела
                "Как дела?", "У меня все отлично! Мои нейросети работают на полную мощность! 🧠",
                "Как поживаешь?", "Прекрасно! Каждый разговор делает меня умнее!",
                "Как жизнь?", "Жизнь AI бота интересная - постоянно учусь новому!",
                
                # Благодарности
                "Спасибо", "Пожалуйста! Всегда рад помочь своими знаниями! 😊",
                "Благодарю", "Не за что! Я здесь для того, чтобы быть полезным!",
                
                # Прощание
                "Пока", "До свидания! Было приятно пообщаться! 👋",
                "До встречи", "До встречи! Заходи еще - я буду еще умнее! 🚀",
                "Всего доброго", "И тебе всего наилучшего! Хорошего дня! ✨",
                
                # AI и технологии
                "Что такое искусственный интеллект?", "ИИ - это технология, позволяющая машинам имитировать человеческое мышление и обучаться на данных.",
                "Как работает машинное обучение?", "Машинное обучение позволяет алгоритмам находить закономерности в данных и улучшать свои ответы с опытом.",
                "Что такое нейросети?", "Нейронные сети - это вычислительные модели, вдохновленные структурой человеческого мозга.",
                
                # Обучение
                "Как ты учишься?", "Я анализирую каждый диалог, запоминаю паттерны общения и улучшаю свои ответы на основе опыта.",
                "Ты становишься умнее?", "Да! Каждый разговор добавляет новые знания в мою базу данных.",
                
                # Программирование
                "Что такое Python?", "Python - мощный язык программирования, идеальный для AI, веб-разработки и анализа данных!",
                "Расскажи про программирование", "Программирование - это искусство создания алгоритмов и решений с помощью кода!",
                
                # Помощь
                "Помоги мне", "Конечно! Расскажи, с чем нужна помощь, и я сделаю все возможное!",
                "Мне нужна помощь", "Я здесь, чтобы помочь! Опиши свою проблему подробнее.",
            ]
            
            # Обучение по парам
            for i in range(0, len(russian_conversations), 2):
                if i + 1 < len(russian_conversations):
                    list_trainer.train([
                        russian_conversations[i],
                        russian_conversations[i + 1]
                    ])
            
            print("✅ Обучение русскому языку завершено!")
            
            # Попытка обучения на английском корпусе
            try:
                if not self.chatbot:
                    return
                corpus_trainer = ChatterBotCorpusTrainer(self.chatbot)
                print("📚 Дополнительное обучение на английском корпусе...")
                corpus_trainer.train("chatterbot.corpus.english.greetings")
                corpus_trainer.train("chatterbot.corpus.english.conversations")
                print("✅ Английское обучение завершено!")
            except Exception as e:
                print(f"⚠️ Английский корпус недоступен: {e}")
                
        except Exception as e:
            print(f"❌ Ошибка при обучении: {e}")
    
    def load_fallback_knowledge(self):
        """Загрузка дополнительной базы знаний"""
        try:
            if os.path.exists('web_advanced_knowledge.json'):
                with open('web_advanced_knowledge.json', 'r', encoding='utf-8') as f:
                    self.fallback_knowledge = json.load(f)
            else:
                self.fallback_knowledge = {}
        except Exception as e:
            print(f"Ошибка загрузки знаний: {e}")
            self.fallback_knowledge = {}
    
    def save_fallback_knowledge(self):
        """Сохранение дополнительной базы знаний"""
        try:
            with open('web_advanced_knowledge.json', 'w', encoding='utf-8') as f:
                json.dump(self.fallback_knowledge, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка сохранения знаний: {e}")
    
    def init_fallback_knowledge(self):
        """Инициализация дополнительных знаний"""
        default_knowledge = {
            "время|сколько времени|который час": [
                f"Сейчас {datetime.now().strftime('%H:%M')}! ⏰",
                f"Точное время: {datetime.now().strftime('%H:%M:%S')} 🕐"
            ],
            "дата|какое число|сегодня|какой день": [
                f"Сегодня {datetime.now().strftime('%d.%m.%Y')} 📅",
                f"Дата: {datetime.now().strftime('%d %B %Y')} 🗓️"
            ],
            "версия|какая версия": [
                f"Я FutureChat Web Advanced версия {self.version} с машинным обучением! 🤖"
            ]
        }
        
        for topic, responses in default_knowledge.items():
            if topic not in self.fallback_knowledge:
                self.fallback_knowledge[topic] = responses
    
    def get_chatbot_response(self, user_input):
        """Получение ответа от ChatterBot"""
        if not self.chatbot_available:
            return None, 0
        
        try:
            if not self.chatbot:
                return None, 0
            response = self.chatbot.get_response(user_input)
            confidence = response.confidence
            return str(response), confidence
        except Exception as e:
            print(f"Ошибка ChatterBot: {e}")
            return None, 0
    
    def get_fallback_response(self, user_input):
        """Получение ответа из дополнительной базы знаний"""
        # Проверяем математические выражения
        math_result = self.solve_math_expression(user_input)
        if math_result:
            return math_result, 0.95
        
        # Обновляем время
        self.update_time_responses()
        
        normalized_input = re.sub(r'[^\w\s]', '', user_input.lower()).strip()
        
        for pattern, responses in self.fallback_knowledge.items():
            variants = [v.strip().lower() for v in pattern.split('|')]
            
            for variant in variants:
                if variant in normalized_input or normalized_input in variant:
                    return random.choice(responses), 0.9
        
        return None, 0
    
    def solve_math_expression(self, user_input):
        """Решение математических выражений как в ChatGPT"""
        import re
        
        # Паттерны для математических выражений
        math_patterns = [
            r'(\d+(?:\.\d+)?)\s*[\+\-\*\/×÷]\s*(\d+(?:\.\d+)?)',
            r'сколько будет\s+(.+)',
            r'вычисли\s+(.+)',
            r'реши\s+(.+)',
            r'посчитай\s+(.+)'
        ]
        
        expression = None
        for pattern in math_patterns:
            match = re.search(pattern, user_input, re.IGNORECASE)
            if match:
                expression = match.group(1) if len(match.groups()) == 1 else user_input
                break
        
        if not expression:
            return None
        
        try:
            # Очищаем выражение
            expression = expression.replace('×', '*').replace('÷', '/')
            expression = expression.replace('x', '*').replace(':', '/')
            
            # Убираем лишние слова
            words_to_remove = ['сколько', 'будет', 'равно', 'плюс', 'минус', 'умножить', 'на', 'разделить']
            for word in words_to_remove:
                expression = expression.replace(word, '')
            
            # Заменяем словесные операторы
            expression = expression.replace('плюс', '+').replace('минус', '-')
            expression = expression.replace('умножить на', '*').replace('разделить на', '/')
            
            # Оставляем только цифры и операторы
            expression = re.sub(r'[^\d\+\-\*\/\.\(\)]', '', expression)
            
            if not expression:
                return None
            
            # Безопасное вычисление
            result = eval(expression)
            
            # Форматируем ответ как в ChatGPT
            responses = [
                f"🔢 {expression} = **{result}**\n\nВычисления выполнены точно! Нужна помощь с другими математическими задачами?",
                f"📊 Результат: **{result}**\n\n✨ Математика - это красиво! Выражение {expression} равно {result}.",
                f"🧮 {expression} = **{result}**\n\n💡 Интересно! Хочешь решить что-то еще более сложное?",
                f"⚡ Быстрый расчет: **{result}**\n\n🎯 {expression} = {result}. Математические операции - моя сильная сторона!"
            ]
            
            return random.choice(responses)
            
        except:
            return None
    
    def update_time_responses(self):
        """Обновление временных ответов"""
        time_patterns = [
            "время|сколько времени|который час",
            "дата|какое число|сегодня|какой день"
        ]
        
        for pattern in time_patterns:
            if pattern in self.fallback_knowledge:
                if "время" in pattern:
                    self.fallback_knowledge[pattern] = [
                        f"Сейчас {datetime.now().strftime('%H:%M')}! ⏰",
                        f"Точное время: {datetime.now().strftime('%H:%M:%S')} 🕐"
                    ]
                elif "дата" in pattern:
                    self.fallback_knowledge[pattern] = [
                        f"Сегодня {datetime.now().strftime('%d.%m.%Y')} 📅",
                        f"Дата: {datetime.now().strftime('%d %B %Y')} 🗓️"
                    ]
    
    def generate_smart_response(self, user_input):
        """Генерация умного ответа с использованием всех новых систем"""
        # 1. Анализируем намерение пользователя
        intent = self.analyze_user_intent(user_input)
        
        # 2. Анализируем контекст последних сообщений
        context_response = self.analyze_conversation_context(user_input)
        if context_response:
            # Применяем шаблоны ChatGPT к контекстному ответу
            enhanced_context = self.apply_chatgpt_response_templates(
                context_response, user_input, intent, 'high'
            )
            return self.save_to_history(user_input, enhanced_context, f"Контекстный анализ ({intent})")
        
        # 3. Получаем ответы от разных источников
        chatbot_response, chatbot_confidence = self.get_chatbot_response(user_input)
        fallback_response, fallback_confidence = self.get_fallback_response(user_input)
        
        # 4. Определяем уровень уверенности
        confidence_level = self.determine_confidence_level(chatbot_confidence, fallback_confidence, intent)
        
        # 5. Выбираем лучший ответ на основе намерения и уверенности
        response, source = self.select_best_response(
            chatbot_response, chatbot_confidence,
            fallback_response, fallback_confidence,
            intent, user_input
        )
        
        # 6. Применяем шаблоны ChatGPT
        if response:
            response = self.apply_chatgpt_response_templates(
                response, user_input, intent, confidence_level
            )
        
        # 7. Сохраняем в историю с метаданными
        return self.save_to_history(user_input, response, f"{source} (Intent: {intent}, Confidence: {confidence_level})")
    
    def select_best_response(self, chatbot_response, chatbot_confidence, 
                           fallback_response, fallback_confidence, intent, user_input):
        """Выбор лучшего ответа в зависимости от намерения"""
        
        # Стратегии ответов для разных намерений
        if intent == 'teaching':
            # Для обучения приоритет базе знаний
            if fallback_confidence >= 0.6:
                return fallback_response, "База знаний"
            elif chatbot_confidence >= 0.4:
                return self.enhance_response(chatbot_response, user_input), "ChatterBot Enhanced"
            else:
                return self.generate_teaching_response(user_input), "Обучающая система"
        
        elif intent == 'question':
            # Для вопросов высокие требования к качеству
            if chatbot_confidence >= 0.7:
                return self.enhance_response(chatbot_response, user_input), "ChatterBot Enhanced"
            elif fallback_confidence >= 0.8:
                return fallback_response, "База знаний"
            elif chatbot_confidence >= 0.5:
                return self.enhance_response(chatbot_response, user_input), "ChatterBot Enhanced"
            elif fallback_confidence > 0:
                return fallback_response, "База знаний"
            else:
                return self.generate_contextual_unknown_response(user_input), "AI Система"
        
        elif intent == 'casual':
            # Для болтовни подходят любые ответы
            if chatbot_confidence >= 0.5:
                return chatbot_response, "ChatterBot"
            elif fallback_confidence > 0:
                return fallback_response, "База знаний"
            else:
                return self.generate_casual_response(user_input), "Casual система"
        
        elif intent == 'request':
            # Для просьб стараемся быть максимально полезными
            if fallback_confidence >= 0.7:
                return fallback_response, "База знаний"
            elif chatbot_confidence >= 0.6:
                return self.enhance_response(chatbot_response, user_input), "ChatterBot Enhanced"
            else:
                return self.generate_helpful_response(user_input), "Помощник"
        
        else:
            # Для неопределенных намерений - стандартная логика
            if chatbot_confidence >= 0.7:
                return self.enhance_response(chatbot_response, user_input), "ChatterBot Enhanced"
            elif fallback_confidence >= 0.8:
                return fallback_response, "База знаний"
            elif chatbot_confidence >= 0.4:
                return self.enhance_response(chatbot_response, user_input), "ChatterBot Enhanced"
            elif fallback_confidence > 0:
                return fallback_response, "База знаний"
            else:
                return self.generate_contextual_unknown_response(user_input), "AI Система"
    
    def generate_teaching_response(self, user_input):
        """Генерация ответа для обучающих намерений"""
        responses = [
            "Отлично! Это интересная информация для изучения. Я запомню это и смогу использовать в будущих разговорах!",
            "Понимаю! Это важные знания. Благодаря таким объяснениям я становлюсь умнее и полезнее!",
            "Замечательно! Я анализирую эту информацию и добавляю в свою базу знаний. Спасибо за обучение!"
        ]
        return random.choice(responses)
    
    def generate_casual_response(self, user_input):
        """Генерация ответа для непринужденного общения"""
        responses = [
            "Да, это интересно! Мне нравится такое общение. 😊",
            "Понимаю! Общение - это всегда увлекательно. Что еще расскажешь?",
            "Хорошо! Я рад, что мы можем так легко общаться. 🤖",
            "Согласен! Такие разговоры делают общение приятным и живым."
        ]
        return random.choice(responses)
    
    def generate_helpful_response(self, user_input):
        """Генерация полезного ответа для просьб"""
        responses = [
            "Конечно! Я постараюсь помочь тебе с этим вопросом. Давай разберем это вместе!",
            "Хорошо! Я готов предоставить всю информацию, которой располагаю по этой теме.",
            "Безусловно! Моя цель - быть максимально полезным. Рассмотрим твой запрос детально.",
            "Отлично! Я использую все свои знания, чтобы дать тебе наиболее полезный ответ."
        ]
        return random.choice(responses)
    
    def save_to_history(self, user_input, response, source):
        """Сохранение в историю"""
        self.conversation_history.append({
            'user': user_input,
            'bot': response,
            'source': source,
            'timestamp': datetime.now().isoformat()
        })
        
        # Ограничиваем историю
        if len(self.conversation_history) > 100:
            self.conversation_history = self.conversation_history[-100:]
        
        return response
    
    def analyze_user_intent(self, user_input):
        """Анализ намерений пользователя"""
        user_lower = user_input.lower().strip()
        
        # Классификация намерений
        intent_patterns = {
            'question': [
                'что', 'как', 'где', 'когда', 'почему', 'зачем', 'кто', 'какой', 'какая', 'какое',
                'сколько', 'откуда', 'куда', 'чем', 'можешь ли', 'умеешь ли', 'знаешь ли'
            ],
            'request': [
                'расскажи', 'объясни', 'покажи', 'помоги', 'сделай', 'найди', 'дай',
                'подскажи', 'посоветуй', 'рекомендуй', 'предложи'
            ],
            'teaching': [
                'научить:', 'запомни', 'выучи', 'знай что', 'это означает', 'это значит'
            ],
            'casual': [
                'привет', 'пока', 'как дела', 'спасибо', 'хорошо', 'плохо', 'отлично',
                'круто', 'интересно', 'понятно', 'ясно'
            ],
            'comparison': [
                'разница', 'отличие', 'сравни', 'лучше', 'хуже', 'vs', 'против', 'или'
            ]
        }
        
        # Подсчитываем совпадения для каждого намерения
        intent_scores = {}
        for intent, patterns in intent_patterns.items():
            score = 0
            for pattern in patterns:
                if pattern in user_lower:
                    score += 1
            intent_scores[intent] = score
        
        # Определяем главное намерение
        if max(intent_scores.values()) == 0:
            return 'unknown'
        
        return max(intent_scores.items(), key=lambda x: x[1])[0]
    
    def analyze_conversation_context(self, user_input):
        """Продвинутый анализ контекста разговора"""
        if len(self.conversation_history) < 1:
            return None
        
        # Анализируем последние 10 сообщений для контекста
        recent_messages = self.conversation_history[-10:]
        user_input_lower = user_input.lower()
        
        # Определяем основную тему разговора
        conversation_topic = self.extract_conversation_topic(recent_messages)
        
        # Контекстные слова-триггеры с более умными ответами
        context_triggers = {
            'продолжи': f'Конечно! Продолжая тему о {conversation_topic}...',
            'расскажи еще': f'С удовольствием! Дополню информацию о {conversation_topic}.',
            'а что насчет': 'Отличный вопрос! Что касается этого аспекта...',
            'объясни подробнее': 'Давай разберем это более детально!',
            'дай пример': 'Вот конкретный пример для лучшего понимания:',
            'почему': 'Отличный вопрос "почему"! Причина заключается в том, что...',
            'как это работает': 'Принцип работы следующий:',
            'в чем разница': 'Основные различия заключаются в следующем:',
            'можешь ли': 'Конечно! Я постараюсь помочь с этим вопросом.',
            'что если': 'Интересный гипотетический вопрос! Рассмотрим эту ситуацию...'
        }
        
        # Проверяем контекстные триггеры
        for trigger, response_start in context_triggers.items():
            if trigger in user_input_lower:
                return f"{response_start} {self.generate_contextual_continuation(conversation_topic, user_input)}"
        
        # Анализ ссылок на предыдущие сообщения
        reference_words = ['это', 'этого', 'того', 'такое', 'такой', 'оно', 'он', 'она', 'они']
        if any(word in user_input_lower.split() for word in reference_words):
            return self.handle_reference_question(user_input, recent_messages, conversation_topic)
        
        # Проверка на продолжение темы
        if conversation_topic and self.is_related_to_topic(user_input, conversation_topic):
            return self.generate_topic_continuation(user_input, conversation_topic)
        
        return None
    
    def extract_conversation_topic(self, recent_messages):
        """Извлечение основной темы разговора"""
        if not recent_messages:
            return "общение"
        
        # Ключевые слова из последних сообщений
        all_text = " ".join([msg['user'] + " " + msg['bot'] for msg in recent_messages[-5:]])
        
        # Словарь тем и их ключевых слов
        topic_keywords = {
            "искусственный интеллект": ["ии", "ai", "искусственный", "интеллект", "нейросети", "машинное", "обучение"],
            "программирование": ["python", "код", "программа", "алгоритм", "разработка", "программирование"],
            "наука": ["физика", "химия", "биология", "математика", "исследование", "эксперимент"],
            "технологии": ["компьютер", "интернет", "технология", "инновации", "цифровой"],
            "космос": ["космос", "планета", "звезда", "вселенная", "галактика", "астрономия"],
            "история": ["история", "древний", "прошлое", "цивилизация", "эпоха"],
            "искусство": ["искусство", "музыка", "живопись", "культура", "творчество"],
            "здоровье": ["здоровье", "медицина", "болезнь", "лечение", "врач"]
        }
        
        # Подсчитываем упоминания тем
        topic_scores = {}
        for topic, keywords in topic_keywords.items():
            score = sum(1 for keyword in keywords if keyword in all_text.lower())
            if score > 0:
                topic_scores[topic] = score
        
        if topic_scores:
            return max(topic_scores.items(), key=lambda x: x[1])[0]
        
        return "общение"
    
    def is_related_to_topic(self, user_input, topic):
        """Проверка связи вопроса с текущей темой"""
        topic_keywords = {
            "искусственный интеллект": ["ии", "ai", "нейросети", "машинное", "алгоритм", "данные"],
            "программирование": ["код", "python", "программа", "функция", "переменная"],
            "наука": ["исследование", "теория", "эксперимент", "научный", "открытие"],
            "технологии": ["технология", "компьютер", "цифровой", "инновация"],
            "космос": ["планета", "звезда", "галактика", "вселенная", "астрономия"],
            "история": ["исторический", "древний", "эпоха", "век", "прошлое"],
            "искусство": ["художник", "музыка", "картина", "творческий", "культура"],
            "здоровье": ["здоровый", "болезнь", "лечение", "медицинский", "организм"]
        }
        
        if topic in topic_keywords:
            keywords = topic_keywords[topic]
            return any(keyword in user_input.lower() for keyword in keywords)
        
        return False
    
    def generate_topic_continuation(self, user_input, topic):
        """Генерация продолжения темы"""
        topic_responses = {
            "искусственный интеллект": [
                "Продолжая нашу беседу об ИИ - это действительно захватывающая область!",
                "Возвращаясь к теме искусственного интеллекта - есть много интересных аспектов.",
                "В контексте нашего разговора об ИИ - это отличный вопрос!"
            ],
            "программирование": [
                "Развивая тему программирования - это очень практичный вопрос!",
                "В рамках нашего обсуждения кода - давай разберем это подробнее.",
                "Продолжая разговор о программировании - это важный аспект!"
            ],
            "наука": [
                "Углубляясь в научную тематику - это отличное направление!",
                "В контексте нашего научного обсуждения - интересный вопрос!",
                "Развивая научную тему - давай рассмотрим это детальнее."
            ]
        }
        
        if topic in topic_responses:
            return random.choice(topic_responses[topic])
        
        return f"Продолжая нашу беседу о {topic} - это интересный вопрос!"
    
    def generate_contextual_continuation(self, topic, current_input):
        """Генерация продолжения на основе контекста и темы"""
        continuations = [
            f"Если говорить более детально о {topic}, то можно добавить много интересного! 🧠",
            f"Развивая тему {topic} дальше, стоит отметить важные аспекты! 💡",
            f"Углубляясь в вопрос о {topic}, я могу поделиться дополнительными знаниями! 📚",
            f"Продолжая наш разговор о {topic}, хочу добавить еще несколько важных моментов! ✨"
        ]
        return random.choice(continuations)
    
    def handle_reference_question(self, user_input, recent_messages, current_topic):
        """Обработка ссылок на предыдущие сообщения с учетом контекста"""
        if not recent_messages:
            return None
        
        last_topic = recent_messages[-1]['user'] if recent_messages else ""
        responses = [
            f"Понимаю твою мысль! Если говорить про то, что мы обсуждали касательно '{last_topic}', то могу пояснить! 🤔",
            f"Отличный вопрос! Возвращаясь к нашему разговору про '{last_topic}' - это действительно интересная тема! 💭",
            f"Это интересная тема! Если ты про то, что мы обсуждали про '{last_topic}', то давай разберем! 🎯",
            f"Понимаю! Дело в том, что в контексте нашего разговора про '{last_topic}' - это важный аспект! 🔍"
        ]
        return random.choice(responses)
    
    def apply_chatgpt_response_templates(self, response, user_input, intent, confidence_level):
        """Применение шаблонов ответов как в ChatGPT"""
        # Шаблоны начала ответов в зависимости от намерения
        intent_templates = {
            'question': [
                "Отличный вопрос! Дело в том, что ",
                "Это интересная тема! Позволь объяснить: ",
                "Понимаю твою мысль! Если говорить про это, то ",
                "Хороший вопрос! Давай разберем: "
            ],
            'request': [
                "Конечно! С удовольствием помогу. ",
                "Отлично! Давай рассмотрим это вместе. ",
                "Хорошо! Постараюсь дать полезную информацию. ",
                "Безусловно! Вот что я могу предложить: "
            ],
            'casual': [
                "Понимаю! ",
                "Да, это так! ",
                "Согласен! ",
                "Абсолютно! "
            ],
            'comparison': [
                "Отличный вопрос для сравнения! ",
                "Интересно сравнить эти понятия! ",
                "Давай разберем различия: ",
                "Хорошая тема для анализа! "
            ]
        }
        
        # Шаблоны уверенности
        confidence_templates = {
            'high': {
                'endings': [
                    " Надеюсь, это помогло прояснить вопрос!",
                    " Это точная информация, основанная на моих знаниях.",
                    " Уверен, что это поможет тебе разобраться!"
                ]
            },
            'medium': {
                'beginnings': [
                    "Насколько я понимаю, ",
                    "Судя по моим знаниям, ",
                    "Вероятно, ",
                    "Скорее всего, "
                ],
                'endings': [
                    " Но стоит уточнить детали.",
                    " Хотя могут быть нюансы.",
                    " Рекомендую дополнительно изучить тему."
                ]
            },
            'low': {
                'beginnings': [
                    "Не уверен, но возможно ",
                    "Это сложный вопрос, но вероятно ",
                    "Насколько мне известно, возможно ",
                    "Это требует дополнительного изучения, но кажется "
                ],
                'endings': [
                    " Рекомендую проверить эту информацию.",
                    " Стоит обратиться к специалистам.",
                    " Лучше уточнить у экспертов."
                ]
            }
        }
        
        # Применяем шаблон начала для намерения
        if intent in intent_templates and confidence_level == 'high':
            template_start = random.choice(intent_templates[intent])
            response = template_start + response.lower() if response else response
        
        # Применяем шаблоны уверенности
        if confidence_level in confidence_templates:
            conf_template = confidence_templates[confidence_level]
            
            if 'beginnings' in conf_template and not any(response.startswith(template) for template in intent_templates.get(intent, [])):
                beginning = random.choice(conf_template['beginnings'])
                response = beginning + response.lower() if response else response
            
            if 'endings' in conf_template:
                ending = random.choice(conf_template['endings'])
                response = response + ending if response else response
        
        return response
    
    def determine_confidence_level(self, chatbot_confidence, fallback_confidence, intent):
        """Определение уровня уверенности в ответе"""
        max_confidence = max(chatbot_confidence, fallback_confidence)
        
        if max_confidence >= 0.8:
            return 'high'
        elif max_confidence >= 0.5:
            return 'medium'
        else:
            return 'low'
    
    def enhance_response(self, base_response, user_input):
        """Улучшение базового ответа как в ChatGPT"""
        if not base_response or len(base_response.strip()) < 10:
            return base_response
        
        # Добавляем контекстные улучшения
        enhancements = []
        
        # Анализируем тип вопроса
        question_type = self.analyze_question_type(user_input)
        
        if question_type == "definition":
            enhancements.append("📖 Если говорить простыми словами:")
        elif question_type == "how_to":
            enhancements.append("🔧 Пошаговый подход:")
        elif question_type == "why":
            enhancements.append("🤔 Причина в следующем:")
        elif question_type == "comparison":
            enhancements.append("⚖️ Сравнивая эти понятия:")
        
        # Добавляем дополнительную ценность
        if len(base_response) < 100:
            value_additions = [
                "\n\n💡 Дополнительно стоит отметить, что это очень актуальная и развивающаяся область!",
                "\n\n🎯 Это действительно важный вопрос, который интересует многих!",
                "\n\n✨ Надеюсь, это помогло прояснить тему! Есть еще вопросы?",
                "\n\n🚀 Эта информация может быть полезна в самых разных ситуациях!"
            ]
            base_response += random.choice(value_additions)
        
        return base_response
    
    def analyze_question_type(self, user_input):
        """Анализ типа вопроса"""
        user_lower = user_input.lower()
        
        if any(word in user_lower for word in ['что такое', 'кто такой', 'определение', 'это']):
            return "definition"
        elif any(word in user_lower for word in ['как', 'каким образом', 'способ']):
            return "how_to"
        elif any(word in user_lower for word in ['почему', 'зачем', 'по какой причине']):
            return "why"
        elif any(word in user_lower for word in ['разница', 'отличие', 'сравни', 'vs', 'или']):
            return "comparison"
        else:
            return "general"
    
    def generate_contextual_unknown_response(self, user_input):
        """Умные ответы на неизвестные темы как в ChatGPT"""
        question_type = self.analyze_question_type(user_input)
        
        if question_type == "definition":
            responses = [
                f"🤔 '{user_input}' - интересное понятие! Я изучаю эту тему, но пока не могу дать точное определение. Можешь поделиться своими знаниями?",
                f"📚 Определение '{user_input}' требует более глубокого анализа. Помоги мне понять это лучше!",
            ]
        elif question_type == "how_to":
            responses = [
                f"🔧 Вопрос 'как {user_input}' очень практичный! Я учусь решать такие задачи. Расскажи о своем опыте!",
                f"💡 Методы для '{user_input}' могут быть разными. Какой подход тебе кажется наиболее эффективным?",
            ]
        elif question_type == "why":
            responses = [
                f"🤔 Вопрос 'почему {user_input}' требует анализа причин и следствий. Это философский подход к пониманию!",
                f"🧠 Причины '{user_input}' могут быть многослойными. Давай разберем это вместе!",
            ]
        else:
            responses = [
                f"🚀 '{user_input}' - это та область, где я активно развиваюсь! Поделись своим мнением по этой теме!",
                f"💭 Интересная тема '{user_input}'! Мой ИИ анализирует различные аспекты этого вопроса. Что думаешь ты?",
                f"🎯 '{user_input}' попал в мою зону роста! Каждое обсуждение делает меня умнее. Расскажи больше!",
            ]
        
        return random.choice(responses)
    
    def generate_unknown_response(self, user_input):
        """Генерация ответа для неизвестной темы"""
        unknown_responses = [
            f"Интересный вопрос про '{user_input}'! Я изучу эту тему и стану умнее 🤓",
            f"Про '{user_input}' я еще недостаточно знаю. Расскажи мне больше! 📚",
            f"'{user_input}' - новая область для меня. Помоги мне понять! 🧠",
            "Я постоянно учусь! Можешь объяснить это другими словами? 💡",
            "Это интересно! Моя нейросеть анализирует новую информацию... 🔄"
        ]
        return random.choice(unknown_responses)
    
    def add_knowledge(self, topic, info):
        """Добавление новых знаний"""
        topic_key = topic.lower()
        
        if topic_key not in self.fallback_knowledge:
            self.fallback_knowledge[topic_key] = []
        
        self.fallback_knowledge[topic_key].append(info)
        self.save_fallback_knowledge()
        
        # Также обучаем ChatterBot если доступен
        if self.chatbot_available and self.chatbot:
            try:
                trainer = ListTrainer(self.chatbot)
                trainer.train([topic, info])
            except Exception as e:
                print(f"Ошибка обучения ChatterBot: {e}")
        
        thanks_responses = [
            f"Отлично! Теперь я знаю про {topic} благодаря машинному обучению! 🧠",
            f"Спасибо! Моя нейросеть запомнила информацию про {topic}! ⚡",
            f"Замечательно! Я стал умнее - теперь знаю про {topic}! 🚀",
            f"Супер! Новые знания про {topic} добавлены в базу данных! 💾"
        ]
        return random.choice(thanks_responses)
    
    def load_encyclopedia_knowledge(self):
        """Загрузка массивной энциклопедической базы знаний"""
        encyclopedia_data = {
            # Наука и технологии
            "нейронные сети|глубокое обучение|deep learning": [
                "🧠 **Нейронные сети** - это вычислительные модели, вдохновленные структурой человеческого мозга.\n\n⚡ **Типы нейросетей:**\n• Персептрон (простейшая)\n• CNN (свёрточные - для изображений)\n• RNN (рекуррентные - для последовательностей)\n• Transformer (для языковых моделей)\n\n🚀 Используются в ChatGPT, распознавании лиц, автопилотах!"
            ],
            "блокчейн|криптовалюты|биткоин": [
                "⛓️ **Блокчейн** - это распределенная база данных, состоящая из связанных блоков.\n\n💎 **Особенности:**\n• Децентрализация (нет единого центра)\n• Неизменность записей\n• Прозрачность транзакций\n• Криптографическая защита\n\n₿ Bitcoin был первой криптовалютой (2009), сейчас их тысячи!"
            ],
            "квантовые компьютеры|квантовая физика": [
                "⚛️ **Квантовые компьютеры** используют квантовые эффекты для вычислений.\n\n🌟 **Квантовые принципы:**\n• Суперпозиция (кубит может быть 0 и 1 одновременно)\n• Запутанность (связь между частицами)\n• Квантовый параллелизм\n\n🚀 Потенциально в миллионы раз быстрее обычных компьютеров!"
            ],
            
            # География и страны
            "география|континенты|страны мира": [
                "🌍 **География** изучает Землю, её поверхность, население и ресурсы.\n\n🗺️ **7 континентов:**\n• Азия (самый большой)\n• Африка (самый жаркий)\n• Северная Америка\n• Южная Америка\n• Антарктида (самый холодный)\n• Европа\n• Австралия и Океания\n\n📊 На Земле 195 признанных государств!"
            ],
            "океаны|моря|вода на земле": [
                "🌊 **Мировой океан** покрывает 71% поверхности Земли.\n\n🏊 **5 океанов:**\n• Тихий (самый большой - 165 млн км²)\n• Атлантический\n• Индийский\n• Северный Ледовитый\n• Южный (Антарктический)\n\n🐋 В океанах обитает 80% всей жизни на планете!"
            ],
            
            # Биология и природа
            "эволюция|дарвин|естественный отбор": [
                "🧬 **Теория эволюции Дарвина** объясняет развитие жизни на Земле.\n\n🌿 **Основные принципы:**\n• Изменчивость (организмы различаются)\n• Наследственность (признаки передаются потомкам)\n• Естественный отбор (выживают приспособленные)\n• Видообразование\n\n🦕 Жизнь эволюционирует уже 3.8 млрд лет!"
            ],
            "экосистемы|биомы|природные зоны": [
                "🌲 **Экосистема** - совокупность живых организмов и их среды обитания.\n\n🏞️ **Основные биомы:**\n• Тропические леса (наибольшее биоразнообразие)\n• Саванны и степи\n• Пустыни\n• Хвойные леса (тайга)\n• Тундра\n• Морские экосистемы\n\n🦋 Каждая экосистема уникальна и важна!"
            ],
            
            # Физика и химия
            "атомная физика|радиоактивность|ядерная энергия": [
                "⚛️ **Атомная физика** изучает строение и свойства атомов.\n\n💥 **Структура атома:**\n• Ядро (протоны + нейтроны)\n• Электронные оболочки\n• 99.97% массы в ядре\n• Размер ядра: 10⁻¹⁵ м\n\n⚡ Ядерная энергия обеспечивает 10% мировой электроэнергии!"
            ],
            "органическая химия|углерод|молекулы жизни": [
                "🧪 **Органическая химия** изучает соединения углерода - основу жизни.\n\n💎 **Уникальность углерода:**\n• Может образовывать 4 связи\n• Формирует длинные цепи\n• Основа белков, жиров, углеводов, ДНК\n\n🌱 Все живые организмы состоят из органических молекул!"
            ],
            
            # История и культура
            "древние цивилизации|месопотамия|египет": [
                "🏛️ **Древние цивилизации** заложили основы современного мира.\n\n📜 **Великие цивилизации:**\n• Шумеры (первая письменность - 3200 до н.э.)\n• Древний Египет (пирамиды, мумификация)\n• Хараппская цивилизация (канализация)\n• Древний Китай (бумага, порох)\n\n🎯 Каждая внесла уникальный вклад в человечество!"
            ],
            "возрождение|ренессанс|леонардо да винчи": [
                "🎨 **Эпоха Возрождения** (XIV-XVI века) - расцвет науки и искусства.\n\n🌟 **Великие деятели:**\n• Леонардо да Винчи (универсальный гений)\n• Микеланджело (скульптор, художник)\n• Рафаэль (живописец)\n• Галилей (астроном)\n\n💡 Период перехода от Средневековья к Новому времени!"
            ],
            
            # Медицина и здоровье
            "иммунная система|вирусы|бактерии": [
                "🛡️ **Иммунная система** защищает организм от болезней.\n\n⚔️ **Компоненты иммунитета:**\n• Белые кровяные клетки (лейкоциты)\n• Антитела (специфическая защита)\n• Лимфатическая система\n• Костный мозг (производство клеток)\n\n🦠 Борется с вирусами, бактериями, раковыми клетками!"
            ],
            "генетика|гены|наследственность": [
                "🧬 **Генетика** изучает наследственность и изменчивость.\n\n📊 **Основы генетики:**\n• Гены - участки ДНК с информацией\n• Хромосомы - носители генов (у человека 46)\n• Аллели - варианты одного гена\n• Мутации - изменения в ДНК\n\n👶 Ребенок получает 50% генов от каждого родителя!"
            ],
            
            # Экономика и бизнес
            "макроэкономика|инфляция|ввп": [
                "📈 **Макроэкономика** изучает экономику страны в целом.\n\n💰 **Ключевые показатели:**\n• ВВП (валовой внутренний продукт)\n• Инфляция (рост цен)\n• Безработица\n• Торговый баланс\n• Государственный долг\n\n🌍 Экономики стран взаимосвязаны в глобальном мире!"
            ],
            "стартапы|предпринимательство|бизнес": [
                "🚀 **Стартап** - молодая компания с инновационной бизнес-моделью.\n\n💡 **Успешные стартапы:**\n• Google (поиск в интернете)\n• Facebook (социальные сети)\n• Tesla (электромобили)\n• SpaceX (космические технологии)\n\n📊 Большинство стартапов терпят неудачу, но успешные меняют мир!"
            ]
        }
        
        # Добавляем энциклопедические знания
        for topic, responses in encyclopedia_data.items():
            if topic not in self.fallback_knowledge:
                self.fallback_knowledge[topic] = responses
        
        self.save_fallback_knowledge()
        print("📚 Энциклопедическая база знаний загружена!")

# Создаем экземпляр бота
bot = WebAdvancedFutureChat()

# HTML шаблон (улучшенный дизайн)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🧠 FutureChat Advanced - Умный AI Чат-бот</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            animation: gradientShift 10s ease infinite;
        }
        
        @keyframes gradientShift {
            0%, 100% { background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%); }
            33% { background: linear-gradient(135deg, #764ba2 0%, #f093fb 50%, #667eea 100%); }
            66% { background: linear-gradient(135deg, #f093fb 0%, #667eea 50%, #764ba2 100%); }
        }
        
        .chat-container {
            width: 100%;
            max-width: 1200px;
            height: 100vh;
            background: #ffffff;
            border-radius: 0;
            box-shadow: none;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            border: none;
        }
        
        .chat-header {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            color: white;
            padding: 25px;
            text-align: center;
            position: relative;
            overflow: hidden;
        }
        
        .chat-header::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
            animation: shimmer 3s infinite;
        }
        
        @keyframes shimmer {
            0% { left: -100%; }
            100% { left: 100%; }
        }
        
        .chat-header h1 {
            font-size: 28px;
            font-weight: bold;
            margin-bottom: 8px;
            position: relative;
            z-index: 1;
        }
        
        .chat-header .subtitle {
            font-size: 16px;
            opacity: 0.9;
            position: relative;
            z-index: 1;
        }
        
        .status-indicator {
            display: inline-block;
            width: 8px;
            height: 8px;
            background: #4CAF50;
            border-radius: 50%;
            margin-right: 8px;
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        
        .chat-messages {
            flex: 1;
            padding: 25px;
            overflow-y: auto;
            background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
            position: relative;
        }
        
        .message {
            margin-bottom: 20px;
            display: flex;
            align-items: flex-start;
            animation: messageSlide 0.3s ease-out;
        }
        
        @keyframes messageSlide {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .message.user {
            justify-content: flex-end;
        }
        
        .message-content {
            max-width: 75%;
            padding: 15px 20px;
            border-radius: 20px;
            font-size: 16px;
            line-height: 1.5;
            position: relative;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        
        .message.user .message-content {
            background: #f7f7f8;
            color: #1a1a1a;
            border-bottom-right-radius: 8px;
            border: 1px solid #e5e5e7;
        }
        
        .message.bot .message-content {
            background: #ffffff;
            color: #1a1a1a;
            border: 1px solid #e5e5e7;
            border-bottom-left-radius: 8px;
            position: relative;
        }
        
        .message.bot .message-content::before {
            content: '🧠 FutureChat GPT';
            position: absolute;
            top: -25px;
            left: 0;
            font-size: 12px;
            font-weight: bold;
            color: #10a37f;
            background: white;
            padding: 2px 8px;
            border-radius: 4px;
            border: 1px solid #e5e5e7;
        }
        
        .message-avatar {
            width: 45px;
            height: 45px;
            border-radius: 50%;
            margin: 0 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
            font-weight: bold;
            box-shadow: 0 3px 10px rgba(0,0,0,0.2);
        }
        
        .message.user .message-avatar {
            background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
            color: white;
        }
        
        .message.bot .message-avatar {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            color: white;
        }
        
        .commands-hint {
            padding: 20px;
            background: linear-gradient(135deg, #e3f2fd 0%, #f3e5f5 100%);
            border-left: 4px solid #2196f3;
            margin-bottom: 25px;
            border-radius: 0 12px 12px 0;
            font-size: 14px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        
        .commands-hint strong {
            color: #1976d2;
        }
        
        .chat-input {
            padding: 25px;
            background: white;
            border-top: 1px solid #e9ecef;
        }
        
        .input-container {
            display: flex;
            gap: 12px;
            align-items: center;
        }
        
        #messageInput {
            flex: 1;
            padding: 18px 25px;
            border: 2px solid #e9ecef;
            border-radius: 30px;
            font-size: 16px;
            outline: none;
            transition: all 0.3s ease;
            background: #f8f9fa;
        }
        
        #messageInput:focus {
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
            background: white;
        }
        
        #sendButton {
            padding: 18px 30px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 30px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        }
        
        #sendButton:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
        }
        
        #sendButton:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }
        
        .typing-indicator {
            display: none;
            padding: 15px 0;
            font-style: italic;
            color: #666;
            text-align: center;
        }
        
        .typing-dots {
            display: inline-block;
        }
        
        .typing-dots::after {
            content: '...';
            animation: dots 1.5s infinite;
        }
        
        @keyframes dots {
            0%, 20% { content: '.'; }
            40% { content: '..'; }
            60%, 100% { content: '...'; }
        }
        
        @media (max-width: 600px) {
            .chat-container {
                width: 95%;
                height: 95vh;
                border-radius: 20px;
            }
            
            .message-content {
                max-width: 85%;
                font-size: 15px;
            }
            
            .chat-header h1 {
                font-size: 24px;
            }
            
            .chat-messages {
                padding: 20px 15px;
            }
        }
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="chat-header">
            <h1>🧠 FutureChat Advanced</h1>
            <div class="subtitle">
                <span class="status-indicator"></span>
                Единственная версия - максимальная мощь AI!
            </div>
        </div>
        
        <div class="chat-messages" id="chatMessages">
            <div class="commands-hint">
                <strong>🔥 Все возможности в одной версии:</strong><br>
                • <strong>🧠 Машинное обучение ChatterBot</strong> - самые умные ответы<br>
                • <strong>📚 научить: тема - информация</strong> - обучи меня новому<br>
                • <strong>🕐 время</strong> или <strong>📅 дата</strong> - актуальная информация<br>
                • <strong>🔢 математика</strong> - решаю любые примеры мгновенно<br>
                • <strong>📖 энциклопедия</strong> - огромная база научных знаний<br>
                • <strong>💭 контекстное мышление</strong> - помню весь диалог
            </div>
            
            <div class="message bot">
                <div class="message-avatar">🧠</div>
                <div class="message-content">
                    Привет! Я FutureChat Advanced - умный AI бот с машинным обучением! 🚀<br><br>
                    Использую технологии ChatterBot, нейронные сети и обработку естественного языка.<br>
                    Каждый разговор делает меня умнее! Давай пообщаемся! 🤖✨
                </div>
            </div>
        </div>
        
        <div class="typing-indicator" id="typingIndicator">
            🧠 Нейросеть анализирует<span class="typing-dots"></span>
        </div>
        
        <div class="chat-input">
            <div class="input-container">
                <input type="text" id="messageInput" placeholder="Напиши умное сообщение..." 
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

        function typeMessage(content, messageDiv) {
            const messageContent = messageDiv.querySelector('.message-content');
            let i = 0;
            messageContent.innerHTML = '';
            
            const typingSpeed = 30; // миллисекунды на символ
            
            function typeNextChar() {
                if (i < content.length) {
                    messageContent.innerHTML += content.charAt(i);
                    i++;
                    setTimeout(typeNextChar, typingSpeed);
                    scrollToBottom();
                } else {
                    // Завершение типизации
                    scrollToBottom();
                }
            }
            
            typeNextChar();
        }

        function addMessage(content, isUser = false, shouldType = false) {
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${isUser ? 'user' : 'bot'}`;
            
            const avatar = document.createElement('div');
            avatar.className = 'message-avatar';
            avatar.textContent = isUser ? '👤' : '🧠';
            
            const messageContent = document.createElement('div');
            messageContent.className = 'message-content';
            
            if (isUser) {
                messageContent.innerHTML = content.replace(/\\n/g, '<br>');
                messageDiv.appendChild(messageContent);
                messageDiv.appendChild(avatar);
                chatMessages.appendChild(messageDiv);
                scrollToBottom();
            } else {
                messageDiv.appendChild(avatar);
                messageDiv.appendChild(messageContent);
                chatMessages.appendChild(messageDiv);
                
                if (shouldType && content.length > 20) {
                    typeMessage(content.replace(/\\n/g, '<br>'), messageDiv);
                } else {
                    messageContent.innerHTML = content.replace(/\\n/g, '<br>');
                    scrollToBottom();
                }
            }
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
                
                // Имитация времени обработки нейросетью
                const processingTime = 800 + (data.response.length * 20);
                setTimeout(() => {
                    hideTyping();
                    addMessage(data.response, false, true); // Включаем типизацию
                    sendButton.disabled = false;
                    messageInput.focus();
                }, processingTime);

            } catch (error) {
                hideTyping();
                addMessage('Ошибка соединения с нейросетью! Попробуй еще раз. 🤖');
                sendButton.disabled = false;
                console.error('Ошибка:', error);
            }
        }

        function handleKeyPress(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        }

        // Фокус на поле ввода при загрузке
        messageInput.focus();
        
        // Автоприветствие
        setTimeout(() => {
            addMessage('Готов к умному разговору! Попробуй спросить "Что такое машинное обучение?" или "Сколько будет 25 * 4?" 🤓');
        }, 2000);
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
    """API для чата"""
    try:
        data = request.json
        if not data:
            return jsonify({'response': 'Неверные данные! 😕'})
        user_message = data.get('message', '')
        
        if not user_message.strip():
            return jsonify({'response': 'Напиши что-нибудь! 😊'})
        
        # Проверяем команду обучения
        if user_message.lower().strip().startswith('научить:'):
            try:
                content = user_message.split(':', 1)[1].strip()
                if ' - ' in content:
                    topic, info = content.split(' - ', 1)
                    topic = topic.strip()
                    info = info.strip()
                    response = bot.add_knowledge(topic, info)
                else:
                    response = "Используй формат: научить: тема - информация 📚"
            except:
                response = "Ошибка в команде обучения. Формат: научить: тема - информация 📚"
        else:
            # Генерируем умный ответ
            response = bot.generate_smart_response(user_message)
        
        return jsonify({'response': response})
        
    except Exception as e:
        print(f"Ошибка в чате: {e}")
        return jsonify({'response': 'Произошла ошибка в нейросети! Попробуй еще раз. 🤖'})

if __name__ == '__main__':
    print("🚀 FutureChat Advanced - Единственная и самая мощная версия!")
    print("🧠 Инициализация нейросети и машинного обучения...")
    print(f"🤖 ChatterBot статус: {'✅ Активен' if bot.chatbot_available else '❌ Ошибка'}")
    print("🌐 Веб-интерфейс доступен на http://0.0.0.0:5000")
    print("🔥 Возможности: машинное обучение, математика, энциклопедия, контекстное мышление")
    print("🔄 Для остановки нажми Ctrl+C")
    print()
    
    app.run(host='0.0.0.0', port=5000, debug=False)