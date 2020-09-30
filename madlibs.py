import json
import random
import re
import dataclasses

import streamlit as st

st.markdown("""MAD LIBS

(dataset is from [a Microsoft EMNLP paper](https://www.microsoft.com/en-us/download/details.aspx?id=55593))

Fill in all the fields then click "Generate Story".
""")


with open('stories.json') as f:
    stories = json.load(f)


@dataclasses.dataclass
class GameState:
    story: str
    game_number: int = 0


def persistent_game_state() -> GameState:
    session_id = st.report_thread.get_report_ctx().session_id
    session = st.server.server.Server.get_current()._get_session_info(session_id).session
    if not hasattr(session, '_gamestate'):
        setattr(session, '_gamestate', GameState(random.choice(stories)))

state = persistent_game_state()


if st.button("new story"):
    state.story = random.choice(stories)
    state.game_number += 1

pos = {
 'cc': 'Coordinating conjunction',
 'cd': 'Cardinal number',
 'dt': 'Determiner',
 'ex': 'Existential there',
 'fw': 'Foreign word',
 'in': 'Preposition or subordinating conjunction',
 'jj': 'Adjective',
 'jjr': 'Adjective, comparative',
 'jjs': 'Adjective, superlative',
 'ls': 'List item marker',
 'md': 'Modal',
 'nn': 'Noun, singular or mass',
 'nns': 'Noun, plural',
 'nnp': 'Proper noun, singular',
 'nnps': 'Proper noun, plural',
 'pdt': 'Predeterminer',
 'pos': 'Possessive ending',
 'prp': 'Personal pronoun',
 'prp$': 'Possessive pronoun',
 'rb': 'Adverb',
 'rbr': 'Adverb, comparative',
 'rbs': 'Adverb, superlative',
 'rp': 'Particle',
 'sym': 'Symbol',
 'to': 'to',
 'uh': 'Interjection',
 'vb': 'Verb, base form',
 'vbd': 'Verb, past tense',
 'vbg': 'Verb, gerund or present participle',
 'vbn': 'Verb, past participle',
 'vbp': 'Verb, non-3rd person singular present',
 'vbz': 'Verb, 3rd person singular present',
 'wdt': 'Wh-determiner',
 'wp': 'Wh-pronoun',
 'wp$': 'Possessive wh-pronoun',
 'wrb': 'Wh-adverb',
 # others
 'animal': 'Animal',
 'body': 'Body part',
 'body_plural': 'Body part, plural',
 'food': 'Food',
 'liquid': 'Liquid',
 }


regex = "<.*?::(.*?)/>"

parts = re.split(regex, state.story)

outparts = []

for i, part in enumerate(parts):
    if i % 2 == 1:
        # remove ':'
        part = part.strip(':')
        # use two-part key so that new stories get new text boxes
        answer = st.text_input(pos.get(part, part), key=(state.game_number, i))

        outparts.append(f"**{answer}**" if answer else "")
    else:
        outparts.append(part)

if all(outparts) and st.button("generate madlib"):
    st.markdown("".join(outparts))