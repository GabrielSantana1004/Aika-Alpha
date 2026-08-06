from datetime import datetime

TOOL_SCHEMA = {
    "type": "function",
    "function": {
        "name": "get_current_datetime",
        "description": (
            "Retorna a data e a hora atuais. Use sempre que o usuário perguntar "
            "que horas são, que dia é hoje, ou precisar de qualquer referência "
            "temporal do momento presente."
        ),
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    },
}

DIAS_SEMANA = [
    "segunda-feira", "terça-feira", "quarta-feira", "quinta-feira",
    "sexta-feira", "sábado", "domingo",
]


def get_current_datetime(**kwargs) -> str:
    agora = datetime.now()
    dia_semana = DIAS_SEMANA[agora.weekday()]
    return f"Agora são {agora.strftime('%H:%M')} de {dia_semana}, {agora.strftime('%d/%m/%Y')}."
