import warnings

import matplotlib.pyplot as plt

warnings.filterwarnings("ignore")

plt.rcParams["font.family"] = "DejaVu Sans"
plt.rcParams["axes.unicode_minus"] = False

API_KEY = "AIzaSyAfS1NURr-J-hHScqhjYpW8yGFmpxfjjP4"

SEARCH_TERMS = [
    "астрология гороскоп",
    "знаки зодиака предсказания",
    "астролог консультация",
    "гороскоп сегодня",
    "астрология прогноз",
    "таро астрология",
    "нумерология астрология",
]

ASTRO_TERMS = [
    "гороскоп",
    "зодиак",
    "астрология",
    "предсказание",
    "прогноз",
    "овен",
    "телец",
    "близнецы",
    "рак",
    "лев",
    "дева",
    "весы",
    "скорпион",
    "стрелец",
    "козерог",
    "водолей",
    "рыбы",
    "планета",
    "луна",
    "солнце",
    "венера",
    "марс",
    "юпитер",
    "таро",
    "карты",
    "предсказание",
    "судьба",
    "энергия",
]

POSITIVE_WORDS = ["спасибо", "классно", "отлично", "супер", "круто", "правда", "точно"]
NEGATIVE_WORDS = ["плохо", "неправда", "ерунда", "глупость", "бред", "фигня"]

MAX_VIDEOS_DEFAULT = 120
MAX_COMMENTS_PER_VIDEO = 20
COMMENTS_ANALYSIS_LIMIT = 50
BATCH_SIZE = 50
