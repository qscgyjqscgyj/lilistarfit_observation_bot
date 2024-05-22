def normalize_gpt_4o_result(result):
    return {
        "name": result.get('name', '-'),
        "value": result.get('value', '-'),
        "normsMan": result.get('normsMan', '-'),
        "normsWoman": result.get('normsWoman', '-'),
        "description": result.get('description', '-'),
        "reasons": result.get('reasons', '-'),
        "conclusion": result.get('conclusion', '-'),
        "conclusion_code": result.get('conclusion_code', '-')
    }
