# 🚀 Automated DevOps Lifecycle: Microservices Task Manager

[![CI/CD Pipeline](https://github.com/helqadiri03/Automated-DevOps-Lifecycle/actions/workflows/deploy.yml/badge.svg)](https://github.com/helqadiri03/Automated-DevOps-Lifecycle/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 📌 Overview
This project is a robust, event-driven **Microservices Task Manager** designed to demonstrate a complete **Automated DevOps Lifecycle**. It leverages modern cloud-native technologies to automate the building, testing, and deployment of a distributed application.

The system allows users to create and manage tasks through a REST API, with background processing and automated notifications handled via a message broker.

---

## 🏗️ Architecture
The system consists of several decoupled services communicating asynchronously:

```mermaid
graph TD
    Client[Client/User] -->|HTTP POST/GET| Web[Web API - Flask]
    Web -->|Store| DB[(PostgreSQL)]
    Web -->|Publish| MQ{RabbitMQ - task_events}
    
    MQ -->|Subscribe: task.created| Worker[Worker - Processor]
    MQ -->|Subscribe: task.completed| Notifier[Notifier - Webhooks]
    MQ -->|DLX| EH[Error Handler]
    
    Notifier -->|POST| External[External Webhook/n8n]
```

- **Web API (Flask)**: The entry point for task management.
- **Worker (Python)**: Asynchronous task processor.
- **Notifier (Python)**: Event-driven notification service using webhooks.
- **Error Handler (DLQ)**: Specialized consumer for failed message management.
- **PostgreSQL**: Reliable persistent storage for tasks.
- **RabbitMQ**: The message broker backbone using Topic Exchanges and Dead Letter Queues (DLQ).
- **n8n**: Workflow automation integration.

---

## 🛠️ Technology Stack
- **Backend**: Python 3.9+ (Flask, Pika, SQLAlchemy)
- **Containerization**: Docker & Docker Compose
- **Orchestration**: (Ready for Kubernetes)
- **Messaging**: RabbitMQ
- **Database**: PostgreSQL 14
- **Automation**: n8n, GitHub Actions
- **Scripting**: Bash, Makefile

---

## 🚀 Getting Started

### Prerequisites
- Docker & Docker Compose installed.
- Git installed.

### Quick Start
1. **Clone the repository:**
   ```bash
   git clone https://github.com/helqadiri03/Automated-DevOps-Lifecycle.git
   cd Automated-DevOps-Lifecycle
   ```

2. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your specific configurations
   ```

3. **Launch the infrastructure:**
   ```bash
   docker-compose up -d --build
   ```

4. **Verify services:**
   ```bash
   docker-compose ps
   ```

---

## 🔧 API Documentation
- **GET** `/tasks`: List all tasks.
- **POST** `/tasks`: Create a new task (JSON: `{"title": "...", "description": "..."}`).
- **PUT** `/tasks/<id>/complete`: Mark a task as completed.

---

## 📈 DevOps Features
- **CI/CD**: Fully automated pipeline using GitHub Actions (Linting + Deployment).
- **Scalability**: Each service can be scaled independently.
- **Resilience**: Implements retry logic and Dead Letter Queues for fault tolerance.
- **Observability**: Structured logging and service health monitoring.
- **Automation Tooling**: Included `Makefile` for simplified environment management.

### Makefile Commands
- `make up`: Start all services.
- `make logs`: View real-time logs.
- `make clean`: Deep clean the environment (volumes and images).

---

## 📄 License
Distributed under the MIT License. See `LICENSE` for more information.
