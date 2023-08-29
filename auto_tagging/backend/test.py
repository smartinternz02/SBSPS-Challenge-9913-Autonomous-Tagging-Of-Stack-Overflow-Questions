from tagPredictor import getTags

title = 'How to learn python?'
body = "I'm trying to learn java , but also interested in C#. What to learn first?"

question = title + " " +body

predicted_tags = getTags([question])

for tags_tuple in predicted_tags:
    for tag in tags_tuple:
        print(tag)
