#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
FutureChat Advanced - Продвинутый AI Чат-бот с ChatterBot
Создано по образцу проекта Awesome-Tech на Replit

Использует библиотеку ChatterBot для более умных ответов
"""

import os
import sys
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer

class AdvancedFutureChat:
    def __init__(self):
        self.bot_name = "FutureChat Advanced"
        self.version = "2.0"
        
        # Создаем чат-бота с настройками
        try:
            self.chatbot = ChatBot(
                'FutureChat',
                storage_adapter='chatterbot.storage.SQLStorageAdapter',
                database_uri='sqlite:///futurebot_database.sqlite3',
                logic_adapters=[
                    {
                        'import_path': 'chatterbot.logic.BestMatch',
                        'default_response': 'Извини, я не понимаю. Можешь объяснить по-другому?',
                        'maximum_similarity_threshold': 0.90
                    },
                    'chatterbot.logic.TimeLogicAdapter',
                    'chatterbot.logic.MathematicalEvaluationAdapter'
                ]
            )
            
            self.setup_training()
            
        except Exception as e:
            print(f"Ошибка при создании бота: {e}")
            print("Переключаемся на простой режим...")
            self.chatbot = None
    
    def setup_training(self):
        """Настройка и обучение бота"""
        try:
            # Создаем тренеры
            corpus_trainer = ChatterBotCorpusTrainer(self.chatbot)
            list_trainer = ListTrainer(self.chatbot)
            
            # Обучение на английском корпусе (если доступен)
            try:
                print("🎓 Обучаю бота на английских данных...")
                corpus_trainer.train("chatterbot.corpus.english.greetings")
                corpus_trainer.train("chatterbot.corpus.english.conversations")
            except Exception as e:
                print(f"Английский корпус недоступен: {e}")
            
            # Обучение на русском языке (кастомные данные)
            print("🎓 Обучаю бота русскому языку...")
            russian_conversations = [
                "Привет",
                "Привет! Как дела?",
                "Как дела?",
                "Хорошо, спасибо! А у тебя?",
                "Как тебя зовут?",
                "Меня зовут FutureChat. Я умный AI бот.",
                "Что ты умеешь?",
                "Я могу болтать, отвечать на вопросы и учиться новому!",
                "Расскажи что-нибудь интересное",
                "Знаешь ли ты, что AI развивается очень быстро? Каждый день появляются новые возможности!",
                "Какая сегодня погода?",
                "Я не имею доступа к данным о погоде, но могу поговорить на эту тему.",
                "Сколько будет 2+2?",
                "2+2 равно 4",
                "Что такое искусственный интеллект?",
                "ИИ - это технология, которая позволяет машинам имитировать человеческое мышление.",
                "Расскажи анекдот",
                "Почему программисты любят темные темы? Потому что свет привлекает баги!",
                "Спасибо",
                "Пожалуйста! Всегда рад помочь!",
                "Пока",
                "До свидания! Было приятно поговорить!",
                "Ты умный?",
                "Я стараюсь быть полезным и учусь каждый день!",
                "Что ты знаешь о Python?",
                "Python - отличный язык программирования! Простой и мощный.",
                "Помоги мне",
                "Конечно! Расскажи, с чем тебе нужна помощь.",
                "Ты робот?",
                "Да, я AI чат-бот, созданный для общения с людьми.",
                "Какой сейчас год?",
                "Я знаю, что сейчас 2024-2025 год, но точную дату узнать не могу."
            ]
            
            # Обучение по парам
            for i in range(0, len(russian_conversations), 2):
                if i + 1 < len(russian_conversations):
                    list_trainer.train([
                        russian_conversations[i],
                        russian_conversations[i + 1]
                    ])
            
            print("✅ Обучение завершено!")
            
        except Exception as e:
            print(f"Ошибка при обучении: {e}")
    
    def get_response(self, user_input):
        """Получение ответа от бота"""
        if self.chatbot is None:
            return "Извини, бот недоступен. Попробуй простую версию."
        
        try:
            response = self.chatbot.get_response(user_input)
            confidence = response.confidence
            
            # Если уверенность низкая, предлагаем альтернативу
            if confidence < 0.5:
                alternative_responses = [
                    f"Не совсем понимаю... Возможно: {response}",
                    f"Может быть: {response}. Это то, что ты имел в виду?",
                    "Можешь переформулировать вопрос?",
                    "Я еще учусь понимать такие вопросы. Попробуй спросить по-другому."
                ]
                import random
                return random.choice(alternative_responses)
            
            return str(response)
            
        except Exception as e:
            return f"Ошибка при генерации ответа: {e}"
    
    def handle_special_commands(self, user_input):
        """Обработка специальных команд"""
        normalized = user_input.lower().strip()
        
        if normalized in ['выход', 'пока', 'до свидания', 'quit', 'exit']:
            return "goodbye"
        elif normalized in ['помощь', 'help']:
            return self.show_help()
        elif normalized in ['инфо', 'info', 'версия']:
            return self.show_info()
        elif normalized.startswith('обучить:'):
            return self.handle_training(user_input)
        
        return None
    
    def show_help(self):
        """Показать справку"""
        help_text = f"""
🤖 {self.bot_name} v{self.version} - Справка:

📚 обучить: [вопрос] - [ответ] - научить новому диалогу
ℹ️  инфо - информация о боте  
❓ помощь - эта справка
🚪 выход - завершить разговор

Особенности:
• Использует ChatterBot для умных ответов
• Может решать простые математические примеры
• Говорит время (на английском)
• Учится на разговорах

Примеры:
• обучить: Как погода? - Сегодня солнечно и тепло!
• Сколько будет 15 + 27?
• What time is it?
        """
        return help_text.strip()
    
    def show_info(self):
        """Показать информацию о боте"""
        info_text = f"""
🤖 {self.bot_name} v{self.version}

🧠 Движок: ChatterBot Library
💾 База данных: SQLite
🌍 Языки: Русский + English
🎯 Алгоритмы: BestMatch, Time, Math
📚 Обучение: Корпус + Кастомные данные

Статус: {"✅ Активен" if self.chatbot else "❌ Ошибка"}
        """
        return info_text.strip()
    
    def handle_training(self, user_input):
        """Обработка команды обучения"""
        if self.chatbot is None:
            return "Обучение недоступно - бот не инициализирован."
        
        try:
            content = user_input.split(':', 1)[1].strip()
            if ' - ' in content:
                question, answer = content.split(' - ', 1)
                question = question.strip()
                answer = answer.strip()
                
                # Обучаем бота новому диалогу
                trainer = ListTrainer(self.chatbot)
                trainer.train([question, answer])
                
                return f"✅ Отлично! Теперь я знаю, что на '{question}' нужно отвечать: '{answer}'"
            else:
                return "Используй формат: обучить: вопрос - ответ"
        except Exception as e:
            return f"Ошибка при обучении: {e}"
    
    def chat(self):
        """Основной цикл чата"""
        print(f"🤖 {self.bot_name} v{self.version} запущен!")
        print("Привет! Я продвинутый AI бот с машинным обучением.")
        print("Введи 'помощь' для команд или просто общайся!")
        print("Для выхода: 'выход' или 'пока'\n")
        
        if self.chatbot is None:
            print("⚠️  ВНИМАНИЕ: ChatterBot недоступен. Ограниченная функциональность.\n")
        
        while True:
            try:
                user_input = input("Ты: ").strip()
                
                if not user_input:
                    continue
                
                # Проверяем специальные команды
                special_response = self.handle_special_commands(user_input)
                
                if special_response == "goodbye":
                    print("🤖 До свидания! Надеюсь, наш разговор был полезным!")
                    break
                elif special_response:
                    print(f"🤖 {special_response}")
                    continue
                
                # Получаем ответ от бота
                response = self.get_response(user_input)
                print(f"🤖 {response}")
                
            except KeyboardInterrupt:
                print("\n🤖 Пока! Было приятно пообщаться!")
                break
            except Exception as e:
                print(f"🤖 Произошла ошибка: {e}")

def main():
    """Главная функция"""
    bot = AdvancedFutureChat()
    bot.chat()

if __name__ == "__main__":
    main()