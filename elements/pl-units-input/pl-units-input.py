import lxml.html
from html import escape
import chevron
import math
import prairielearn as pl
import random
import numpy
import sympy
import units


WEIGHT_DEFAULT = 1
CORRECT_ANSWER_DEFAULT = None
LABEL_DEFAULT = None
INFIX_DEFAULT = None
SUFFIX_DEFAULT = None
DISPLAY_DEFAULT = 'inline'
ALLOW_BLANK_DEFAULT = False
ALLOW_UNITLESS_DEFAULT = False
BLANK_VALUE_DEFAULT = 0
UNITLESS_VALUE_DEFAULT = 1
SIZE_DEFAULT = 35
SHOW_HELP_TEXT_DEFAULT = True

def prepare(element_html, data):
    # TODO: checks whether correct answer is valid
    element = lxml.html.fragment_fromstring(element_html)
    required_attribs = ['answers-name']
    optional_attribs = ['weight', 'correct-answer', 'label', 'infix', 'suffix', 'display', 'allow-blank', 'allow-unitless', 'blank-value', 'unitless-value', 'size', 'show-help-text']
    pl.check_attibs(element, required_attribs, optional_attribs)

    name = pl.get_string_attrib(element, 'answers-name')
    correct_answer = pl.get_string_attrib(element, 'correct-answer', CORRECT_ANSWER_DEFAULT)

    if correct_answer is not None:
        if name in data['correct_answers']:
            raise Exception('duplicate correct_answers variable name: %s' % name)
        data['correct_answers'][name] = correct_answer

    # TODO: check integer validity?

def render(element_html, data):
    # TODO: render question, submission, & answer blocks
    # TODO: config customizable attributes
    element = lxml.html.fragment_fromstring(element_html)
    name = pl.get_string_attrib(element, 'answers-name')
    first_name = name + str(1)
    last_name = name + str(2)
    label = pl.get_string_attrib(element, 'label', LABEL_DEFAULT)
    infix = pl.get_string_attrib(element, 'infix', INFIX_DEFAULT)
    suffix = pl.get_string_attrib(element, 'suffix', SUFFIX_DEFAULT)
    display = pl.get_string_attrib(element, 'display', DISPLAY_DEFAULT)
    size = pl.get_integer_attrib(element, 'size', SIZE_DEFAULT)

    if data['panel'] == 'question':
        editable = data['editable']
        raw_submitted_first_answer = data['raw_submitted_answers'].get(first_name, None)
        raw_submitted_last_answer = data['raw_submitted_answers'].get(last_name, None)

        # Get info strings
        info_params = {'format': True}
        with open('pl-units-input.mustache', 'r', encoding='utf-8') as f:
            template = f.read()
            info = chevron.render(template, info_params).strip()
            info_params.pop('format', None)
        
        html_params = {
            'question': True,
            'name': name,
            'label': label,
            'infix': infix,
            'suffix': suffix,
            'editable': editable,
            'info': info,
            'size': size,
            'show_info': pl.get_boolean_attrib(element, 'show-help-text', SHOW_HELP_TEXT_DEFAULT),
            'show_placeholder': size >= PLACEHOLDER_TEXT_THRESHOLD,
            'uuid': pl.get_uuid()
        }

        partial_score = data['partial_scores'].get(name, {'score': None})
        score = partial_score.get('score', None)
        if score is not None:
            try:
                score = float(score)
                if score >= 1:
                    html_params['correct'] = True
                elif score > 0:
                    html_params['partial'] = math.floor(score * 100)
                else:
                    html_params['incorrect'] = True
            except Exception:
                raise ValueError('invalid score' + score)
        
        html_params['display_append_span'] = html_params['show_info'] or suffix

        if display == 'inline':
            html_params['inline'] = True
        elif display == 'block':
            html_params['block'] = True
        else:
            raise ValueError('method of display "%s" is not valid (must be "inline" or "block")' % display)

        if raw_submitted_first_answer is not None:
            html_params['raw_submitted_first_answer'] = escape(raw_submitted_first_answer)
        if raw_submitted_last_answer is not None:
            html_params['raw_submitted_last_answer'] = escape(raw_submitted_last_answer)
        with open('pl-units-input.mustache', 'r', encoding='utf-8') as f:
            html = chevron.render(f, html_params).strip()

    elif data['panel'] == 'submission':
        parse_error = data['format_errors'].get(name, None)
        html_params = {
            'submission': True,
            'label': label,
            'parse_error': parse_error,
            'uuid': pl.get_uuid()
        }

        if parse_error is None and name in data['submitted_answers']:
            # Get submitted answer, raising an exception if it does not exist
            a_sub_first = data['submitted_answers'].get(first_name, None)
            a_sub_last = data['submitted_answers'].get(last_name, None)
            if a_sub_first is None:
                raise Exception('submitted number is None')
            if a_sub_last is None:
                raise Exception('submitted unit is None')
            
            # If answer is in a format generated by pl.to_json, convert it
            # back to a standard type (otherwise, do nothing)
            a_sub_first = pl.from_json(a_sub_first)
            a_sub_last = pl.from_json(a_sub_last)
            a_sub_last = pl.escape_unicode_string(a_sub_last)

            html_params['suffix'] = suffix
            html_params['first_sub'] = a_sub_first
            html_params['last_sub'] = a_sub_last
        
        elif name not in data['submitted_answers']:
            html_params['missing_input'] = True
            html_params['parse_error'] = None
        
        else:
            raw_submitted_first_answer = data['raw_submitted_answers'].get(first_name, None)
            raw_submitted_last_answer = data['raw_submitted_answers'].get(last_name, None)
            if raw_submitted_first_answer is not None:
                html_params['raw_submitted_first_answer'] = pl.escape_unicode_string(raw_submitted_first_answer)
            if raw_submitted_last_answer is not None:
                html_params['raw_submitted_last_answer'] = pl.escape_unicode_string(raw_submitted_last_answer)
        
        partial_score = data['partial_scores'].get(name, {'score': None})
        score = partial_score.get('score', None)
        if score is not None:
            try:
                score = float(score)
                if score >= 1:
                    html_params['correct'] = True
                elif score > 0:
                    html_params['partial'] = math.floor(score * 100)
                else:
                    html_params['incorrect'] = True
            except Exception:
                raise ValueError('invalid score' + score)
        
        html_params['error'] = html_params['parse_error'] or  html_params.get('missing_input', False)
        with open('pl-units-input.mustache', 'r', encoding='utf-8') as f:
            html = chevron.render(f, html_params).strip()
        
    elif data['panel'] == 'answer':
        a_tru = pl.from_json(data['correct_answers'].get(name, None))
        if a_tru is not None:
            html_params = {
                'answer': True,
                'label': label,
                'a_tru': a_tru,
                'suffix': suffix
            }
            with open('pl-units-input.mustache', 'r', encoding='utf-8') as f:
                html = chevron.render(f, html_params).strip()
        else:
            html = ''
    
    else:
        raise Exception('Invalid  panel type: %s' % data['panel'])
    
    return html

def parse(element_html, data):
    # TODO: change submitted answer to dimensionful quantity
    element = lxml.html.fragment_fromstring(element_html)
    name = pl.get_string_attrib(element, 'answers-name')
    first_name = name + str(1)
    last_name = name + str(2)
    allow_blank = pl.get_string_attrib(element, 'allow-blank', ALLOW_BLANK_DEFAULT)
    allow_unitless = pl.get_string_attrib(element, 'allow-unitless', ALLOW_UNITLESS_DEFAULT)

    a_sub_first = data['submitted_answers'].get(first_name, None)
    a_sub_last = data['submitted_answers'].get(last_name, None)

    if a_sub_first is None:
        data['format_errors'][first_name] = 'No submitted answer.'
        data['submitted_answers'][first_name] = None
        return
    if a_sub_last is None:
        data['format_errors'][last_name] = 'No submitted answer.'
        data['submitted_answers'][last_name] = None
        return
    
    if a_sub_first.strip() == '':
        if pl.get_boolean_attrib(element, 'allow-blank', ALLOW_BLANK_DEFAULT):
            a_sub_first = pl.get_integer_attrib(element, 'blank-value', BLANK_VALUE_DEFAULT)
        else:
            data['format_errors'][first_name] = 'Invalid format. The submitted answer was left blank.'
            data['submitted_answers'][first_name] = None
            return
    try:
        a_sub_parsed = pl.string_to_integer(str(a_sub_first), 10)
        if a_sub_parsed is None:
            raise ValueError('invalid submitted answer (wrong type)')
        if a_sub_parsed > 2**53 - 1 or a_sub_parsed < -((2**53) - 1):
            data['format_errors'][first_name] = 'correct answer must be between -9007199254740991 and +9007199254740991 (that is, between -(2^53 - 1) and +(2^53 - 1)).'
        a_sub_first = pl.to_json(a_sub_parsed)
    except Exception:
        data['format_errors'][first_name] = 'Invalid format.'
        data['submitted_answers'][first_name] = None
        return

    if not a_sub_last and not allow_unitless:
        data['format_errors'][last_name] = 'Invalid format. The submitted answer was left blank.'
        data['submitted_answers'][last_name] = None
        return
    
    data['submitted_answers'][name] = units.dimensionfully_quantitize(a_sub_first, a_sub_last)

def grade(element_html, data):
    # TODO: checks against correct answer
    element = lxml.html.fragment_fromstring(element_html)
    name = pl.get_string_attrib(element, 'answers-name')
    weight = pl.get_integer_attrib(element, 'weight', WEIGHT_DEFAULT)

    a_tru = pl.from_json(data['correct_answers'].get(name, None))
    if a_tru is None:
        return
    
    a_sub = data['submitted_answers'].get(name, None)
    if a_sub is None:
        data['partial_scores'][name] = {'score': 0, 'weight': weight}
        return
    a_sub = pl.from_json(a_sub)

    if a_tru == a_sub:
        data['partial_scores'][name] = {'score': 1, 'weight': weight}
    elif units.dimension(a_tru) == units.dimension(a_sub):
        data['partial_scores'][name] = {'score': 0.5, 'weight': weight}
    else:
        data['partial_scores'][name] = {'score': 0, 'weight': weight}

def test(element_html, data):
    # TODO: support pl.to_json?
    pass
