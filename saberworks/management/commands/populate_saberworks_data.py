from django.core.management import BaseCommand

from saberworks.models import Game, TagType, Tag

class Command(BaseCommand):
    help = 'Populates initial saberworks.net data'

    games = [
        ['Jedi Knight', 'jk', 'Dark Forces II: Jedi Knight', 'blue'],
        ['Mysteries of the Sith', 'mots', 'Mysteries of the Sith', 'cyan'],
        ['Jedi Outcast', 'jo', 'Jedi Outcast', 'geekblue'],
        ['Jedi Academy', 'ja', 'Jedi Academy', 'gold'],
        ['Doom', 'doom', 'Doom', 'green'],
    ]

    tag_types = [
        ['mode', '#F0F0F0'],
        ['type', '#F0F0F0'],
        ['asset', '#F0F0F0'],
        ['tool', '#F0F0F0'],
        ['patch', '#F0F0F0'],
    ]

    tags = [
        ['texture', 'blue', 'asset'],
        ['model', 'cyan', 'asset'],
        ['map', 'geekblue', 'type'],
        ['mod', 'gold', 'type'],
        ['level-editor', 'green', 'tool'],
        ['gob', 'lime', 'tool'],
        ['graphics', 'magenta', 'patch'],
        ['capture-the-flag', 'orange', 'mode'],
        ['kill-the-fool-with-the-ysalamiri', 'purple', 'mode'],
        ['multiplayer', 'red', 'mode'],
        ['single-player', 'volcano', 'mode'],
    ]

    def handle(self, *args, **options):
        for game in self.games:
            game_row = Game(
                name=game[0],
                slug=game[1],
                description=game[2],
                color=game[3],
            )

            game_row.save(force_insert=True)

        for tag_type in self.tag_types:
            tt_row = TagType(
                slug=tag_type[0],
                color=tag_type[1],
            )

            tt_row.save(force_insert=True)

        for tag in self.tags:
            tt = TagType.objects.get(slug=tag[2])

            tag_row = Tag(
                slug=tag[0],
                color=tag[1],
                type=tt,
            )

            tag_row.save(force_insert=True)
