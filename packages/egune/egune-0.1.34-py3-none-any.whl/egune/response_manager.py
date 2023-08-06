import egune 
from egune.requests import FormQuestionTypes
import yaml
import random
import re

def questionsParser(a, key, b):
    def isQuestion(obj):
        if obj is dict:
            if obj['type'] is not None:
                return True
        return False

    if isQuestion(a) and isQuestion(b):
        if key not in a:
            a[key] = b
        else:
            if not b['templates']:
                if not a[key]: 
                  raise ValueError("Need more templates")
                return a[key]
            else:
                a[key]['templates'] = list(set(a[key]['templates'] + b['templates']))
    return b

def typeParser(val):
    qtype = val['type']
    if qtype == 'Open':
        return None, egune.FormQuestionTypes.Open
    elif qtype == 'MultiSelect':
        return val['options'], egune.FormQuestionTypes.MultiSelect
    elif qtype == 'Date':
        return None, egune.FormQuestionTypes.Date
    elif qtype == 'Checkbox':
        return val['options'], egune.FormQuestionTypes.Checkbox
    raise ValueError("Invalid Form Question Type")

class ResponseManager:
    def __init__(self, config_path):
        self.config = yaml.safe_load(open(config_path, "r"))
        self.response = self.config['responses']

    def ResponseSelect(self, template):
        return random.sample(template, 1)

    def ResponseFormatter(self, result, data):
        result = re.sub(r"\$\{([^\$]*)\}", "%(\\1)s", result)
        return result % data

    def prep_text(self, templates, data):
        return self.ResponseFormatter(self.ResponseSelect(templates), data)

    def responder(self, key, data):
        if key in self.response:
            currentKey = self.response[key]
            currentTypes = currentKey['type']
            currentData = currentKey['required_data']
            checkKeysExist = all(item in data.keys() for item in currentData)
            if checkKeysExist is True:
                currentTemp = currentKey.get('templates')
                if currentTypes == "Tell":
                    return egune.Tell(self.prep_text(currentTemp, data))
                elif currentTypes == "Fail":
                    return egune.Fail(self.prep_text(currentTemp, data))
                elif currentTypes == "YesNoQuestion":
                    yes_action = currentKey['constants']['yes_action']
                    no_action = currentKey['constants']['no_action']
                    return egune.YesNoQuestion(self.prep_text(currentTemp, data), yes_action, no_action)
                elif currentTypes == "MultiSelectQuestion":
                    handler = currentKey['constants']['handler']
                    options = data.get('options', currentKey['constants'].get('options', []))
                    return egune.MultiSelectQuestion(self.prep_text(currentTemp, data), options, handler)
                elif currentTypes == "OpenQuestion":
                    question = self.prep_text(currentTemp, data)
                    handler = currentKey['constants']['handler']
                    return egune.OpenQuestion(question, handler)
                elif currentTypes == "ButtonQuestion":
                    options = data.get('options', currentKey['constants'].get('options', []))
                    question = self.prep_text(currentTemp, data)
                    return egune.ButtonQuestion(question, options)
                elif currentTypes == "Success":
                    return egune.Success(self.prep_text(currentTemp, data))
                elif currentTypes == "TellCustom":
                    return egune.TellCustom(**currentKey['constants']) 
                elif currentTypes == "CheckboxQuestion":
                    handler = currentKey['constants']['handler']
                    options = data.get('options', currentKey['constants'].get('options', []))
                    question = self.prep_text(currentTemp, data)
                    return egune.CheckboxQuestion(question, options, handler)  
                elif currentTypes == "Form":
                    f = egune.Form('some_form_example_title',"some_form_example_handler")
                    questions = data['questions']
                    currentQuestion = currentKey['questions']
                    for key, value in questions.items():
                        finalTemplate = questionsParser(currentQuestion, key, value)['templates']
                        options, convertedType = typeParser(value)
                        f.add_question(key, FormQuestionTypes(convertedType), finalTemplate, options)
                    return f
        else:
            return egune.Tell("Key олдсонгүй")
