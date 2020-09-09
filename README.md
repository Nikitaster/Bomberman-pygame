# Bomberman

## Preview
<img src="./preview.gif" width="50%" />

## Start
```bash
  python -m venv venv
  source venv/bin/activate
  pip install --upgrade pip
  pip install -r main_information/requirements.txt 
  python run.py
```

## Main concepts

Numbers -> Blocks:
'0' -> 'Grass'(aka void block)
'1' -> 'Bedrock'(aka unbreakable block)
'2' -> 'Bricks'

## Movement
(Direction - 'en.char'/'ru.char'/'arrow'):
Right - 'D'/'В'/'>'
Left - 'A'/'Ф'/'<'
Up - 'W'/'Ц'/'^'
Down - 'S'/'Ы'/'v'

Spawn bomb -> 'E'/'У'
