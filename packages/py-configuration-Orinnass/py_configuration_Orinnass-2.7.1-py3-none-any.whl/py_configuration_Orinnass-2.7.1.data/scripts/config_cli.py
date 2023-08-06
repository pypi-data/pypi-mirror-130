"""
Модуль для работы с конфигурацией из командной строки
"""
from sys import argv
from os import getenv, walk
from os.path import exists as path_exists, isfile, join as path_join
from json import dumps as json_dump, loads as json_load
import argparse
from config import __version__

new_element = None
root_template = None

# TODO: добавить типы переменных


def __dump_json__(file_path, json):
    with open(file_path, 'w') as file:
        file.write(json_dump(json, indent=3))


def __wait_confirmation__(message: str) -> bool:
    print(message)
    answer = input()
    if answer.lower() != "yes" and answer.lower() != 'y':
        return False
    return True


def __parse_element__(element, name_parent_element, parent_element):
    global new_element
    global root_template
    if element.get('$ref'):
        path_element = element['$ref'].split('/')
        for i in path_element:
            match i:
                case "#":
                    element = root_template
                case _:
                    element = element[i]
        __parse_element__(element, name_parent_element, parent_element)
    else:
        if element['type'] == 'object':
            parent_element[name_parent_element] = {}
            parent_element = parent_element[name_parent_element]
            for i in element['required']:
                __parse_element__(element['properties'][i], i, parent_element)
        else:
            parent_element[name_parent_element] = element.get('default')


def __update_add_command__(**kwargs):
    params = kwargs['params']
    template = kwargs['template']
    with open(params.config_file, 'r') as config_file:
        config = json_load(config_file.read())
    for i in params.elements:
        if i not in template['properties']:
            print(f'Элемента {i} нет в шаблоне')
            return
        if i in config.keys() and __wait_confirmation__(f'{i} элемент уже есть в конфигурации, перезаписать (y/n)'):
            continue
        global new_element
        new_element = {}
        __parse_element__(template['properties'][i], i, new_element)
        config[i] = new_element[i]

    __dump_json__(params.config_file, config)
    print(f"{'Элемент добавлен' if len(params.elements) == 1 else 'Элементы добавлены'}")


def __update_delete_command__(**kwargs):
    params = kwargs['params']
    with open(params.config_file, 'r') as config_file:
        config = json_load(config_file.read())

    for i in params.elements:
        if i in config.keys():
            del config[i]
            print(f"{i} элемент удален")
        else:
            print(f"{i} элемент отсутсвует в конфиге")

    __dump_json__(params.config_file, config)

    print('Удаление выполнено')


def create_command(params):
    """
    Функция создания конфига из шаблона
    """
    # TODO: сделать чтение конфига лога из шаблона
    if not getenv('TEMPLATE_CONFIG', default=None):
        print("Не определена переменная окружения TEMPLATE_CONFIG")
        return
    template = json_load(open(getenv("TEMPLATE_CONFIG")).read())

    if params.list_elements:
        message = "Список доступных элементов: "
        for i in template['properties']:
            message += f"{i}, "
        print(message[:-2])
        return
    if path_exists(params.config_file) and \
            not __wait_confirmation__('Файл конфигурации уже существует, перезаписать его? (y/n)'):
        return
    if params.elements:
        elements = params.elements
        elements.append('logging')
    else:
        elements = ['logging']
    config = {}
    global root_template
    root_template = template

    for i in elements:
        if i not in template['properties']:
            print(f'Элемента {i} нет в шаблоне')
            return
        global new_element
        new_element = {}
        __parse_element__(template['properties'][i], i, new_element)
        config[i] = new_element[i]

    __dump_json__(params.config_file, config)
    print('Конфигурация создана')


def update_command(params):
    """
    Функция обновления конфига
    """
    if not getenv('TEMPLATE_CONFIG', default=None):
        print("Не определена переменная окружения TEMPLATE_CONFIG")
        return
    if not path_exists(params.config_file) and not isfile(params.config_file):
        print("Указанного файла не существует")
        return

    template = json_load(open(getenv("TEMPLATE_CONFIG")).read())
    update_methods = {
        "add": __update_add_command__,
        "delete": __update_delete_command__
    }
    update_methods[params.update_command](params=params, template=template)


def merge_template(params):
    """
    Функция слияние файлов шаблона
    """
    with open(params.merge_file) as merge_file:
        merge = json_load(merge_file.read())
    with open(params.template_file) as template_file:
        template = json_load(template_file.read())

    blocks = ["properties", "definitions"]
    for block in blocks:
        if merge.get(block):
            merge_properties = merge[block]
            for i in merge_properties.keys():
                if i in template[block]:
                    user_input = input(f"{i} уже есть в шаблоне в блоке {block} перезаписать? (y/n)")
                    if user_input.lower() != 'y':
                        continue
                template[block][i] = merge_properties[i]
    if merge.get("required"):
        for i in merge["required"]:
            if i not in template["required"]:
                template["required"].append(i)

    __dump_json__(params.template_file, template)

    print("Конфигурация объединена")


def merge_all_templates(params):
    """
    Функция поиска всех файлов для шаблона и слияние с шаблоном
    """
    for i in walk(params.dir_find):
        for file in i[2]:
            if file == "merge_template.json":
                merge_file = path_join(i[0], file)
                user_input = input(f"Найден файл для слияние: {merge_file}. Выполняем слияние? (y,n)")
                if user_input.lower() == 'y':
                    print(f"Слияние файла: {merge_file}")
                    params.merge_file = merge_file
                    merge_template(params)

    print("Поиск и слияние завершено")


def create_template(params):
    """
    Функция создания базового шаблона
    """
    __dump_json__(params.template_file, {"definitions": {}, "type": "object", "properties": {},
                                         "required": [], "additionalProperties": False})
    print("Конфигурация создана")


methods = {
    "create": create_command,
    "update": update_command,
    "merge-template": merge_template,
    "merge-all-templates": merge_all_templates,
    "create-template": create_template
}


def create_parse():
    """
    Команда создания парсинга аргументов
    """
    parser = argparse.ArgumentParser(add_help=False)

    parent_group = parser.add_argument_group(title="Параметры")
    parent_group.add_argument('--version', action='version', help='Вывести номер версии',
                              version='%(prog)s {}'.format(__version__))
    parent_group.add_argument("--help", "-h", action="help", help="Справка")

    subparsers = parser.add_subparsers(dest="command", title="Возможные команды",
                                       description="Команды, которые должны быть в качестве первого параметра %(prog)s")

    # region create command
    create_command_parser = subparsers.add_parser("create", add_help=False)
    create_command_parser.add_argument('config_file')
    create_command_parser.add_argument('-e', '--elements', nargs='+', help="Элементы, которые нужно добавить в конфиг. "
                                                                           "Для работы этого параметра требуется "
                                                                           "указать переменную окружения "
                                                                           "TEMPLATE_CONFIG")
    create_command_parser.add_argument('--list-elements', action='store_true', default=False)
    create_command_parser.add_argument('-h', '--help', action='help', help='Справка')
    # endregion

    # region update command
    update_command_parser = subparsers.add_parser('update', add_help=False)
    update_command_parser.add_argument('config_file')
    update_command_parser.add_argument('update_command', choices=['add', 'delete'])
    update_command_parser.add_argument('elements', nargs='+')
    update_command_parser.add_argument('-h', '--help', action='help', help='Справка')
    # endregion

    # region merge template
    attach_template_parser = subparsers.add_parser('merge-template', add_help=False)
    attach_template_parser.add_argument("merge_file")
    attach_template_parser.add_argument("template_file")
    # endregion

    # region merge all templates
    merge_all_template = subparsers.add_parser("merge-all-templates", add_help=False)
    merge_all_template.add_argument("dir_find")
    merge_all_template.add_argument("template_file")
    # endregion

    # region create base template
    create_template_parser = subparsers.add_parser("create-template", add_help=False)
    create_template_parser.add_argument("template_file")
    # endregion

    return parser


if __name__ == '__main__':
    main_parser = create_parse()
    parsed_params = main_parser.parse_args(argv[1:])

    methods[parsed_params.command](parsed_params)
