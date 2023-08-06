def extend_bed(cls, extension):
    return cls


def extend_cli(cls, extension):
    '''Add CLI commands to create extension and validator templates.'''

    from os import mkdir
    from os.path import join, dirname, abspath

    from string import Template


    class CLI(cls):
        def __init__(self):
            super().__init__()

            self.template_path = join(dirname(__file__), 'templates')

        def dev(self, name, extension=False, validator=False, destination='.'):
            '''create an extension or validator template in a given location (current directory by default)'''

            if bool(extension) == bool(validator):
                print('Run "sci dev -e NAME" to create an extension or "sci dev -v NAME" to create a validator.')

            else:
                destination_path = abspath(join(destination, name))

                mkdir(destination_path)

                if extension:
                    source_template = Template(open(join(self.template_path, 'extension.py')).read())

                    with open(join(destination_path, '%s.py' % name), 'w') as source:
                        source.write(source_template.safe_substitute(extension=name))

                    print('Extension "%s" created in %s' % (name, destination_path))

                elif validator:
                    source_template = Template(open(join(self.template_path, 'validator.py')).read())

                    with open(join(destination_path, '%s.py' % name), 'w') as source:
                        source.write(source_template.safe_substitute(validator=name))

                    print('Validator "%s" created in %s' % (name, destination_path))

    return CLI
