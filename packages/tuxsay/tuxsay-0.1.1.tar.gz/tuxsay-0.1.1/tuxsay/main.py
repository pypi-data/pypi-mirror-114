import click
from click_help_colors import HelpColorsGroup, HelpColorsCommand


@click.version_option('0.1.1', prog_name='main')
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
    if character==None:
        click.secho(f'''
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
''', fg='yellow')
    elif character.lower()=='python':
        click.secho(f'''
    __    __    __    __
   /  \  /  \  /  \  /  |
__/  __\/  __\/  __\/  __\______
__/  /__/  /__/  /__/  /_________
  | / \   / \   / \   / \  \____     ,"{len(text)*'"'}".
  |/   \_/   \_/   \_/   \    o \    | {text} |
                          \_____/--< _;{len(text)*'.'}'
                          ''', fg='blue')
    elif character.lower()=='man':
        click.secho(f"""
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
""", fg='white')
    elif character.lower()=='knight':
        click.secho(f'''
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
        )_\         )_\.''', fg='white')

@main.command('list', help="list all characters")
@click.argument('arg')
def list(arg):
    if arg=='chars':
        click.echo('tux (default)\nman\nknight\npython')
if __name__=='__main__':
    main()