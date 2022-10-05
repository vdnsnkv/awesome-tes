# Awesome Task Exchange System 

Доска в Miro с моделью данных и доменами: 

https://miro.com/app/board/uXjVPR1o6IM=/

## Домены и сервисы
- User Domain
  - User Service — аутентификация и авторизация пользователей, роли
- Tasks Domain
  - Task Tracker Service — управление задачами
- Finance Domain
  - Balance Service — управление транзакциями и балансами пользователей
  - Payments Service — выплаты балансов
- Technical Domain
  - Email Service — отправляет письма
  - Analytics Service — собирает аналитику по системе

### User Service
Продьюсит:
- Бизнес-события
  - —
- CUD-события
  - User.Created — добавление нового пользователя в систему
  - User.Updated — изменение данных пользователя (email, имя, роль)
  - User.Deleted — удаление пользователя из системы

### Task Tracker Service
Продьюсит:
- Бизнес-события
  - Task.Added — добавлена новая задача в систему
  - Task.Assigned — задача была назначена на пользователя
  - Task.Done — задача была выполнена пользователем
- CUD-события
  - Task.Created
  - Task.Updated

Консьюмит:
  - User.Created
  - User.Updated
  - User.Deleted

### Balance Service
Продьюсит:
- Бизнес-события
  - —
- CUD-события
  - Transaction.Created — появилась новая транзакция

Консьюмит:
  - Task.Added
  - Task.Assigned
  - Task.Done
  - User.Created
  - User.Updated
  - User.Deleted
  - User.BalancePaid

### Payments Service
Продьюсит:
- Бизнес-события
  - User.BalancePaid
- CUD-события
  - —

### Analytics Service

Консьюмит:
  - Transaction.Created 
  - User.Created
  - User.Updated
  - User.Deleted
  

### Email Service

Только отправляет письма из очереди на отправку
