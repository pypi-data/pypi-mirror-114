import click
from click_help_colors import HelpColorsGroup, HelpColorsCommand
import clipboard as cb
import random

@click.version_option('0.1.3', prog_name='main')
@click.group(
    cls=HelpColorsGroup, help_headers_color='blue', help_options_color='yellow'
)


def main():
    '''
I am TUX! Hehe
    '''
    pass

@main.command('say', help="SAY!")
@click.argument('text')
@click.option('--character', '-c')
def say(text, character):
    choice = [3,4,1,1,2,1,2]
    for i in text:
        if random.choice(choice)==1:
            text = text.replace(i, i.upper())
        else:
            text = text.replace(i, i.lower())
    if character==None:
        out = f'''
         _nnnn_                      
        dGGGGMMb     ,"{len(text)*'"'}".
       @p~qp~~qMb    | {text} |
       M(•) (•) M|   _;{len(text)*'.'}'
       @,----.JM| -'
      JS^\__/  qKL
     dZP        qKRb
    dZP          qKKb
   fZP            SMMb
   HZM            MMMM
   FqM            MMMM
 __| ".        |\dS"qML
 |    `.       | `' \Zq
_)      \.___.,|     .'
\____   )MMMMMM|   .'
'''
        click.secho(out, fg='yellow')
        cb.copy(out)
    elif character.lower()=='python':
        out = f'''
    __    __    __    __
   /  \  /  \  /  \  /  |
__/  __\/  __\/  __\/  __\______
__/  /__/  /__/  /__/  /_________
  | / \   / \   / \   / \  \____     ,"{len(text)*'"'}".
  |/   \_/   \_/   \_/   \    o \    | {text} |
                          \_____/--< _;{len(text)*'.'}'
                          '''
        click.secho(out, fg='blue')
        cb.copy(out)
    elif character.lower()=='man':
        out=f"""
                           ,-----.
                         /'       '|
                        ; ----,---- ;   ,"{len(text)*'"'}".
                        | 'o- |'o-  |   | {text} |
                        |     |_    |  _;{len(text)*'.'}'
                        |   ____,   | -.
                         \_       _/
                         | `-----' |
                     __.-;         ;-.__
                 _,-'    ; :     ; ;    `-._
              _,'                           `.
            ,'-,_____     \ :   : /     ____,-'-,
          /'         '''----.   .----'''          |
         /                   \_/                   |
        |                     |                     |
        |        ,            |            ,        |
        |        |            |            |        |
        |        \            |            /        |
        \        /\   o       |      o    /\       /
"""
        click.secho(out, fg='white')
        cb.copy(out)
    elif character.lower()=='knight':
        out=f'''
             ,;~;,     ,"{len(text)*'"'}".
                /\_    | {text} |
               (  /   _;{len(text)*'.'}'
               (()  _;  //)
               | \.\  ,,;;'\.
           __ _(  )m=(((((((((============----
         /'  ' '()/~' '.(, |
      ,;(      )||     |  ~
     ,;' \    /-(.;,   )
          ) /       ) /
         //         ||
        )_\         )_\.'''
        click.secho(out, fg='white')
        cb.copy(out)
        
@main.command('list', help="list all characters")
@click.argument('arg')
def list(arg):
    if arg=='chars':
        click.echo('tux (default)\nman\nknight\npython')
if __name__=='__main__':
    main()