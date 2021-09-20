import pyfiglet
import pathlib

sample_text = "hello world!"

fontdir = pathlib.Path(pyfiglet.__file__).parent.joinpath('fonts')

fig = pyfiglet.Figlet(width=80*4)

for fontfn in fontdir.glob('*.flf'):
    fontname, _, _ = fontfn.name.rpartition('.flf')
    try:
        fig.setFont(font=fontname)
        print(f'--- font: {fontname} ---')
        print(fig.renderText(sample_text))
    except pyfiglet.FontNotFound:
        print(f'%%%%%% {fontname} not found!! %%%%%%')
