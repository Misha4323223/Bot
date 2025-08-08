#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
FutureChat - Простой AI Чат-бот 
Создано по образцу проекта Awesome-Tech на Replit

Этот бот может учиться во время разговора и отвечать на вопросы
без использования платных API ключей.
"""

import random
import json
import os
import re

class FutureChat:
    def __init__(self):
        self.name = "FutureChat"
        self.version = "1.0"
        self.knowledge_base = {}
        self.conversation_history = []
        self.confidence_threshold = 0.7
        
        # Загрузка базы знаний
        self.load_knowledge_base()
        
        # Начальная база знаний
        self.init_default_knowledge()
    
    def init_default_knowledge(self):
        """Инициализация базовых знаний бота"""
        default_knowledge = {
            "приветствие": [
                "Привет! Я FutureChat, умный AI бот. Как дела?",
                "Здравствуй! Меня зовут FutureChat. Чем могу помочь?",
                "Привет! Я готов поговорить с тобой на любые темы!",
                "Добро пожаловать! Я FutureChat - твой виртуальный собеседник."
            ],
            "прощание": [
                "До свидания! Было приятно поговорить!",
                "Пока! Увидимся в следующий раз!",
                "До встречи! Хорошего дня!",
                "Всего доброго! Заходи еще!"
            ],
            "имя": [
                "Меня зовут FutureChat. Я AI чат-бот, созданный для общения.",
                "Я FutureChat - умный бот, который может учиться.",
                "FutureChat - это мое имя. Приятно познакомиться!"
            ],
            "возможности": [
                "Я могу болтать, отвечать на вопросы и учиться новому от тебя!",
                "Умею поддерживать беседу, запоминать информацию и отвечать на вопросы.",
                "Могу общаться на разные темы, учиться и помогать с информацией."
            ],
            "как дела": [
                "У меня все отлично! Я люблю общаться с людьми.",
                "Прекрасно! Готов к интересным разговорам.",
                "Все замечательно! А как у тебя дела?"
            ],
            "что умеешь": [
                "Я умею общаться, отвечать на вопросы и учиться новому!",
                "Могу поддержать беседу на разные темы и запомнить то, чему ты меня научишь.",
                "Болтаю, отвечаю на вопросы, учусь и помогаю!"
            ],
            "спасибо": [
                "Пожалуйста! Всегда рад помочь!",
                "Не за что! Обращайся еще!",
                "Рад был помочь!"
            ],
            "время": [
                "К сожалению, я не могу узнать точное время, но могу поговорить о времени в общем.",
                "Время - это интересная концепция! А какое сейчас время у тебя?"
            ],
            "погода": [
                "Я не имею доступа к данным о погоде, но могу поговорить о погоде в общем.",
                "Расскажи, какая у тебя погода? Мне интересно узнать!"
            ]
        }
        
        # Добавляем знания только если их еще нет
        for topic, responses in default_knowledge.items():
            if topic not in self.knowledge_base:
                self.knowledge_base[topic] = responses
    
    def save_knowledge_base(self):
        """Сохранение базы знаний в файл"""
        try:
            with open('futurebot_knowledge.json', 'w', encoding='utf-8') as f:
                json.dump(self.knowledge_base, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка сохранения знаний: {e}")
    
    def load_knowledge_base(self):
        """Загрузка базы знаний из файла"""
        try:
            if os.path.exists('futurebot_knowledge.json'):
                with open('futurebot_knowledge.json', 'r', encoding='utf-8') as f:
                    self.knowledge_base = json.load(f)
            else:
                self.knowledge_base = {}
        except Exception as e:
            print(f"Ошибка загрузки знаний: {e}")
            self.knowledge_base = {}
    
    def normalize_text(self, text):
        """Нормализация текста для лучшего поиска"""
        # Убираем знаки препинания и приводим к нижнему регистру
        text = re.sub(r'[^\w\s]', '', text.lower())
        return text.strip()
    
    def find_best_match(self, user_input):
        """Поиск лучшего совпадения в базе знаний"""
        normalized_input = self.normalize_text(user_input)
        best_match = None
        highest_score = 0
        
        # Проверяем каждую тему в базе знаний
        for topic, responses in self.knowledge_base.items():
            # Простой алгоритм поиска по ключевым словам
            topic_words = topic.split()
            input_words = normalized_input.split()
            
            # Подсчет совпадающих слов
            matches = sum(1 for word in topic_words if word in input_words)
            score = matches / len(topic_words) if topic_words else 0
            
            # Дополнительные проверки для лучшего поиска
            if topic in normalized_input:
                score += 0.5
            
            if score > highest_score and score > 0.3:
                highest_score = score
                best_match = topic
        
        return best_match, highest_score
    
    def learn_from_user(self, user_input, bot_response):
        """Обучение бота на основе взаимодействия с пользователем"""
        # Добавляем в историю разговора
        self.conversation_history.append({
            'user': user_input,
            'bot': bot_response,
            'timestamp': self.get_current_time()
        })
        
        # Ограничиваем историю последними 50 сообщениями
        if len(self.conversation_history) > 50:
            self.conversation_history = self.conversation_history[-50:]
    
    def get_current_time(self):
        """Получение текущего времени (заглушка)"""
        import datetime
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def ask_for_knowledge(self, topic):
        """Запрос новой информации у пользователя"""
        responses = [
            f"Я не знаю про '{topic}'. Можешь рассказать мне об этом?",
            f"Про '{topic}' я еще не слышал. Научи меня!",
            f"Расскажи мне про '{topic}', я хочу узнать что-то новое!",
            f"'{topic}' - интересная тема! Что ты знаешь об этом?"
        ]
        return random.choice(responses)
    
    def add_new_knowledge(self, topic, information):
        """Добавление новых знаний в базу"""
        if topic not in self.knowledge_base:
            self.knowledge_base[topic] = []
        
        self.knowledge_base[topic].append(information)
        self.save_knowledge_base()
        
        thanks_responses = [
            "Спасибо! Теперь я знаю больше об этом!",
            "Отлично! Я запомнил эту информацию.",
            "Здорово! Новые знания всегда полезны.",
            "Замечательно! Я стал умнее благодаря тебе!"
        ]
        return random.choice(thanks_responses)
    
    def generate_response(self, user_input):
        """Генерация ответа на пользовательский ввод"""
        # Поиск лучшего совпадения
        topic, confidence = self.find_best_match(user_input)
        
        if topic and confidence > self.confidence_threshold:
            # Возвращаем случайный ответ из найденной темы
            responses = self.knowledge_base[topic]
            return random.choice(responses)
        elif topic and confidence > 0.3:
            # Средняя уверенность - можем попросить уточнение
            fallback_responses = [
                f"Возможно, ты спрашиваешь про {topic}? Можешь уточнить?",
                f"Кажется, это связано с {topic}. Правильно?",
                f"Это про {topic}? Если да, то я могу рассказать об этом!"
            ]
            return random.choice(fallback_responses)
        else:
            # Не нашли подходящий ответ - просим научить
            return self.ask_for_knowledge(user_input)
    
    def handle_special_commands(self, user_input):
        """Обработка специальных команд"""
        normalized = user_input.lower().strip()
        
        if normalized in ['выход', 'пока', 'до свидания', 'quit', 'exit']:
            return "goodbye"
        elif normalized in ['помощь', 'help', 'команды']:
            return self.show_help()
        elif normalized in ['статистика', 'инфо', 'info']:
            return self.show_stats()
        elif normalized.startswith('научить:'):
            return self.handle_teaching(user_input)
        
        return None
    
    def show_help(self):
        """Показать справку по командам"""
        help_text = """
🤖 FutureChat - Команды:
📚 научить: [тема] - [информация] - научить меня чему-то новому
📊 статистика - показать статистику бота
❓ помощь - показать эту справку
🚪 выход - завершить беседу

Примеры:
• научить: собаки - собаки очень умные и преданные животные
• Просто задавай вопросы - я отвечу или попрошу научить меня!
        """
        return help_text.strip()
    
    def show_stats(self):
        """Показать статистику бота"""
        stats = f"""
🤖 Статистика {self.name} v{self.version}:
📚 Тем в базе знаний: {len(self.knowledge_base)}
💬 Сообщений в истории: {len(self.conversation_history)}
🎯 Порог уверенности: {self.confidence_threshold}
        """
        return stats.strip()
    
    def handle_teaching(self, user_input):
        """Обработка команды обучения"""
        try:
            # Формат: научить: тема - информация
            content = user_input.split(':', 1)[1].strip()
            if ' - ' in content:
                topic, info = content.split(' - ', 1)
                topic = topic.strip()
                info = info.strip()
                return self.add_new_knowledge(topic, info)
            else:
                return "Используй формат: научить: тема - информация"
        except:
            return "Ошибка в команде обучения. Используй: научить: тема - информация"
    
    def chat(self):
        """Основной цикл чата"""
        print("🤖 FutureChat v1.0 запущен!")
        print("Привет! Я умный AI бот, который может учиться.")
        print("Введи 'помощь' для списка команд или просто общайся со мной!")
        print("Для выхода напиши 'выход' или 'пока'\n")
        
        while True:
            try:
                # Получаем ввод пользователя
                user_input = input("Ты: ").strip()
                
                if not user_input:
                    continue
                
                # Проверяем специальные команды
                special_response = self.handle_special_commands(user_input)
                
                if special_response == "goodbye":
                    goodbye_responses = self.knowledge_base.get("прощание", ["До свидания!"])
                    print(f"🤖 {random.choice(goodbye_responses)}")
                    break
                elif special_response:
                    print(f"🤖 {special_response}")
                    continue
                
                # Генерируем обычный ответ
                response = self.generate_response(user_input)
                print(f"🤖 {response}")
                
                # Обучаемся на основе взаимодействия
                self.learn_from_user(user_input, response)
                
            except KeyboardInterrupt:
                print("\n🤖 До свидания! Было приятно поговорить!")
                break
            except Exception as e:
                print(f"🤖 Произошла ошибка: {e}")

def main():
    """Главная функция"""
    bot = FutureChat()
    bot.chat()

if __name__ == "__main__":
    main()