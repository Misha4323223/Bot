# FutureChat Advanced - Project Documentation

## Overview

This repository contains **FutureChat Advanced** - a powerful AI chatbot with machine learning capabilities. The project has been simplified to contain only the most advanced version, eliminating all simpler alternatives.

**Key Features:**
- ChatterBot machine learning for intelligent responses
- Intent analysis and contextual understanding
- Mathematical computation engine
- Encyclopedia knowledge base
- Real-time web interface with typing animations
- No external API keys required - fully self-contained

## Recent Changes (2025-08-08)

- **Major Refactoring:** Removed all simple versions (main.py, simple_futurebot.py, advanced_chatbot.py, web_futurebot.py)
- **Consolidated:** Renamed web_advanced_chatbot.py to main.py as the single entry point
- **Enhanced:** Updated README.md to reflect the new single-version architecture
- **Improved:** Updated web interface headers and descriptions

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **HTML/CSS/JavaScript** embedded directly in Python Flask template
- **Responsive design** with gradient backgrounds and animations
- **Real-time chat interface** with typing indicators and message animations
- **Mobile-first approach** with adaptive layouts

### Backend Architecture
- **Flask web framework** serving on port 5000
- **ChatterBot integration** for machine learning responses
- **Multi-source response system:** ChatterBot + Fallback knowledge + Encyclopedia
- **Intent analysis engine** for understanding user queries
- **Context-aware conversation** tracking dialogue history

### Data Storage
- **SQLite database** for ChatterBot training data and conversations
- **JSON files** for fallback knowledge and encyclopedia data
- **In-memory conversation history** with 100-message limit
- **Automatic persistence** of learned information

### Authentication & Authorization
- Authentication mechanisms to be identified based on implementation
- User management and session handling approaches to be documented
- Security patterns and access control methods to be specified

## External Dependencies

### Third-party Services
- External APIs and service integrations to be documented
- Payment processors, analytics, or other service providers to be identified

### Database Systems
- Primary database technology to be specified
- Any additional data storage solutions to be documented

### Development Tools
- Build tools, package managers, and development dependencies to be listed
- Testing frameworks and deployment tools to be identified

---

*Note: This documentation will be updated with specific details once the repository contents are analyzed.*