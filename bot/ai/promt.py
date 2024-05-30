CUT_TEXT_PROMT = {
    "request": "Очень внимательно изучи документы и верни только те части, которые относятся к медицинским анализам и их результатам. Верни только части оригинального текста с анализами.",
}

OBSEVATION_GET_VAUES_PROMT = {
    # "request": "Very carefully parse all values within all observations tests you will find in all docuemetns and return the results in JSON format using 'response_format' schema.",
    "request": "Очень внимательно разбери все значения во всех исследованиях, которые найдешь во всех документах, и верни результаты в формате JSON, используя схему 'response_format'.",
    "response_format": {
        "_type": "object",
        "_properties": {
            "results": {
                "_type": "array",
                "_items": {
                    "_type": "object",
                    "_properties": {
                        "name": {
                            "_type": "string",
                            "_description": "Название исследования",
                        },
                        "value": {
                            "_type": "string",
                            "_description": "Данные результата исследования из входных данных",
                        },
                    },
                },
            },
        },
    },
}

OBSERVATION_INTERPRETATION_PROMT = {
    # "request": "Analyse all observations results and return addition information about each one based on 'response_format' in JSON.",
    "request": "Проанализируй все результаты анализов из документов, которые были отправлены порциями в сообщениях выше и согласно последним научным данным верни дополнительную информацию и заключение о каждом из анализов на основе 'response_format' в JSON. Обработай только результаты с отклонениями от нормы!",
    "response_format": {
        "_type": "object",
        "_properties": {
            "results": {
                "_type": "array",
                "_items": {
                    "_type": "object",
                    "_properties": {
                        "name": {
                            "_type": "string",
                            "_description": "Название исследования",
                        },
                        "value": {
                            "_type": "string",
                            "_description": "Данные результата исследования из входных данных",
                        },
                        "normsMan": {
                            "_type": "string",
                            "_description": "Нормы по данному исследованию для мужчин",
                        },
                        "normsWoman": {
                            "_type": "string",
                            "_description": "Нормы по данному исследованию для женщин",
                        },
                        "description": {
                            "_type": "string",
                            "_description": "Подробное описание исследования с пояснением простым языком на что влияет этот показатель. Минимум 100 символов",
                        },
                        "reasons": {
                            "_type": "string",
                            "_description": "Причины, по которым могло бы быть нарушение показателя. Максимум 3 причины",
                        },
                        "conclusion": {
                            "_type": "string",
                            "_description": "Напиши краткое заключение по результату исследования и рекомендации для улучшения параметра если он не в норме. Минимум 100 символов",
                        },
                        "conclusion_code": {
                            "_type": "union",
                            "_values": ["+", "-"],
                            "_description": "+ если результат в норме, - если результат не в норме",
                        },
                    },
                },
            },
        },
    },
}
