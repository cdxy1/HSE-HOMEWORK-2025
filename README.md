# Домашние задание

## 🔧 Что сделали

- Поиск релевантных видео с YouTube API
- Сбор данных о видео, метаданных и комментариев
- Вычисление производных признаков: длительность, частота слов, тональность комментариев и др.
- Визуализация: просмотры, длительность, активность по времени и др.
- Регрессионное моделирование для оценки значимости факторов

## 🧱 Структура
```
.
├── pyproject.toml
├── ruff.toml
├── src
│   ├── config.py
│   ├── main.py
│   └── utils
│       │   
│       ├── data_collector.py
│       ├── data_processing.py
│       ├── report_generator.py
│       ├── statistical_analysis.py
│       ├── visualization.py
│       └── youtube_api.py
└── uv.lock
```
## 🛠️ Зависимости

- pandas, numpy, matplotlib, seaborn
- scikit-learn, scipy, isodate
- google-api-python-client
### Dev
- ruff
- uv

## 🚀 Запуск

В модуле config.py требуется ввести свой API-ключ от YouTube Data API, также в нем есть константа MAX_VIDEOS_DEFAULT, где требуется ввест количество видео (дефолт 120).

```bash
python3 -m venv .venv
source .venv/bin/activate # для linux/macos
.venv\Scripts\activate # для windows
pip install -r requirements.txt
python3 .src/main.py
```

## 📈 Вывод

Файл с результатами сохраняется в `.xlsx`, визуализации строятся автоматически и появляются в корне проекта.
