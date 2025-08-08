#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
FutureChat - Главный файл запуска
Выбор между разными версиями AI чат-бота

Версии:
1. Простая версия (консоль)
2. Продвинутая версия с ChatterBot (консоль) 
3. Веб-версия (браузер)
"""

import sys
import os

def show_menu():
    """Показать меню выбора версии"""
    print("🤖 FutureChat - AI Чат-бот без API ключей!")
    print("=" * 50)
    print("Выбери версию для запуска:")
    print()
    print("1️⃣  Простая версия (консоль)")
    print("   ✅ Быстрый запуск")
    print("   ✅ Может учиться во время разговора") 
    print("   ✅ Базовая логика поиска")
    print()
    print("2️⃣  Продвинутая версия (консоль)")
    print("   ✅ Использует ChatterBot AI")
    print("   ✅ Машинное обучение")
    print("   ✅ Решает математику, говорит время")
    print()
    print("3️⃣  Веб-версия (браузер) 🌟 РЕКОМЕНДУЕТСЯ")
    print("   ✅ Красивый веб-интерфейс")
    print("   ✅ Работает в браузере")
    print("   ✅ Современный дизайн")
    print("   ✅ Эмодзи и анимации")
    print()
    print("0️⃣  Выход")
    print("=" * 50)

def run_simple_version():
    """Запуск простой версии"""
    print("🚀 Запуск простой версии FutureChat...")
    try:
        from simple_futurebot import main
        main()
    except ImportError as e:
        print(f"❌ Ошибка импорта: {e}")
    except Exception as e:
        print(f"❌ Ошибка запуска: {e}")

def run_advanced_version():
    """Запуск продвинутой версии"""
    print("🚀 Запуск продвинутой версии с ChatterBot...")
    try:
        from advanced_chatbot import main
        main()
    except ImportError as e:
        print(f"❌ Ошибка импорта ChatterBot: {e}")
        print("💡 Попробуй простую версию (вариант 1)")
    except Exception as e:
        print(f"❌ Ошибка запуска: {e}")

def run_web_version():
    """Запуск веб-версии"""
    print("🚀 Запуск веб-версии FutureChat...")
    print("🌐 Откроется веб-интерфейс на http://localhost:5000")
    print("🔄 Для остановки нажми Ctrl+C")
    print()
    try:
        # Импортируем и запускаем веб-версию
        import web_futurebot
    except ImportError as e:
        print(f"❌ Ошибка импорта Flask: {e}")
    except Exception as e:
        print(f"❌ Ошибка запуска веб-сервера: {e}")

def main():
    """Главная функция"""
    while True:
        try:
            show_menu()
            choice = input("\nВведи номер версии (1-3) или 0 для выхода: ").strip()
            
            if choice == "1":
                run_simple_version()
            elif choice == "2":
                run_advanced_version()
            elif choice == "3":
                run_web_version()
                break  # Веб-версия блокирует выполнение
            elif choice == "0":
                print("👋 До свидания!")
                break
            else:
                print("❌ Неверный выбор. Попробуй еще раз.")
                
        except KeyboardInterrupt:
            print("\n👋 До свидания!")
            break
        except Exception as e:
            print(f"❌ Произошла ошибка: {e}")

if __name__ == "__main__":
    main()