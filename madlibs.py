import json
import random
import re
import types

import streamlit as st

st.markdown("""MAD LIBS

(dataset is from [a Microsoft EMNLP paper](https://www.microsoft.com/en-us/download/details.aspx?id=55593))

Fill in all the fields then click "Generate Story".
""")


# This is a double hack. Basically, I want to choose a random story
# both initially, and then again when someone presses the "new story" button.
# However, I don't want the random draw to change while the user is working.
#
# In order to do this, I use st.cache to create a "persistent namespace" object 
# that contains a global "serial number" that persists across recalculations. 
# 
# THEN I wrap the random story picker in another st.cached function 
# that takes as input the singleton serial number. And I have the "new story"
# button increment that serial number, which invalidates the cached random story.

@st.cache(allow_output_mutation=True)
def persistent_namespace():
    return types.SimpleNamespace(serial_number=0)

ns = persistent_namespace()

with open('stories.json') as f:
    stories = json.load(f)

if st.button("new story"):
    ns.serial_number += 1

@st.cache
def new_story(i: int) -> str:
    return random.choice(stories)

story = new_story(ns.serial_number)


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

parts = re.split(regex, story)

outparts = []

for i, part in enumerate(parts):
    if i % 2 == 1:
        # remove ':'
        part = part.strip(':')
        answer = st.text_input(pos.get(part, part), key=(serial.number, i))

        outparts.append(f"**{answer}**" if answer else "")
    else:
        outparts.append(part)

if all(outparts) and st.button("generate madlib"):
    st.markdown("".join(outparts))