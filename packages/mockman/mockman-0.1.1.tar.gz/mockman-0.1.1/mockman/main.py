import random
import clipboard as cb
import click
from click_help_colors import HelpColorsGroup, HelpColorsCommand

@click.version_option('0.1.1', prog_name='main')
@click.group(
    cls=HelpColorsGroup, help_headers_color='blue', help_options_color='yellow'
)
def main():
    '''
Generate Mocked Text
    '''
    pass

@main.command('mock', help='Mock Text')
@click.argument('text', nargs=1)
def mock(text):
    choice = [1,3,4,5,2,2]
    for i in text:
        if random.choice(choice)==1:
            text = text.replace(i, i.upper())
        else:
            text = text.replace(i, i.lower())
    cb.copy(text)
    click.secho(text, fg='yellow')

if __name__=='__main__':
    main()