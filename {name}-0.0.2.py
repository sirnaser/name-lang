import re

variables = {'main': ''}
print('main : \n')

def concat_once(text):
    for m in re.finditer(r'\{(?!-)([^{}]*?)\}', text):
        name = m.group(1)
        if name.endswith('.file'):
            try:
                with open(name) as file:
                    value = file.read()
            except Exception:
                print('file read error:', name)
                continue
        elif name in variables:
            value = variables[name]
        else:
            continue
        return text[:m.start()] + value + text[m.end():], True
    return text, False

def concat(text):
    changed = True
    while changed:
        text, changed = concat_once(text)
    return text

while True:
    code = input('> ')
    if code.strip().endswith(':'):
        while line := input():
            if line.startswith('\t') or line.startswith(' '*4):
                code += '\n' + line
            else:
                break
        if line:
            print(': ignored\n')
            continue

    lines = code.split('\n')
    while lines:
        line = lines.pop(0)

        if ':' not in line:
            line, changed = concat_once(line)
            if changed:
                lines = line.split('\n') + lines
            continue

        name, _, value = line.partition(':')
        name = concat(name.strip())
        value = concat(value.strip())

        if value: value += '\n'
        while lines:
            if lines[0].startswith('\t'):
                line = lines.pop(0)[1:]
            elif lines[0].startswith(' '*4):
                line = lines.pop(0)[4:]
            else:
                break
            value += concat(line) + '\n'
        value = value[:-1].replace('{-', '{')

        if name.endswith('.file'):
            try:
                with open(name, 'w') as file:
                    file.write(value)
            except Exception:
                print('file write error:', name)
        else:
            variables[name] = value

    variables['main'] += code.replace('{', '{-') + '\n'
    # print('variables:', variables)