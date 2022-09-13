from cProfile import label
import re
import os
dirname = os.path.dirname(__file__)
dirlist = os.listdir(dirname + '/text')
# 0(m + n) time where m is number of files and n is the number of words in file
# 0(n) space where n is wordCount?
# grab each individual .txt file
def getInfo():
    result = []
    for file in dirlist:
        wordCount = {
        "maxCount": {
            "word": [],
            "frequency": 0
        }
    }
        if '.txt' in file:
            # open and read file
            content = open(os.path.join(dirname + '/text',file), 'r')

            # read file and create regex to only grab words
            content = content.read()

            # regex finds 1 or more alphabet char + 0 or more ' (for conjunctions), but only matches if that's then followed by more alphabet chars
            reggie = "[a-zA-Z]+['/_]*[a-zA-Z]+"
            content = re.findall(reggie, content)
            length = len(content)

            for entry in content:
                # exclusions (uncomment if needed)
                # if entry == 'the' or entry == 'of' or entry == 'to' or entry == 'for' or entry == 'and':
                #     continue

                # if entry hasnt been initialized, create it and add one to freq value
                wordCount.setdefault(entry, 0)
                wordCount[entry] += 1

                # if current word is greater than stored frequency, replace maxcount frequency and word
                if wordCount["maxCount"]["frequency"] < wordCount[entry]:
                    wordCount["maxCount"]["frequency"] = wordCount[entry]
                    wordCount["maxCount"]["word"] = [entry]
                elif wordCount["maxCount"]["frequency"] == wordCount[entry]:
                    wordCount["maxCount"]["word"].append(entry)


            # set up ratio - if len/wordCount has only a .0 for decimal, it can be simplified, else if cant. set up ratio accordingly
            if length / wordCount["maxCount"]["frequency"] == 1:
                ratio = '1:1'
            elif int(length / wordCount["maxCount"]["frequency"]) == length / wordCount["maxCount"]["frequency"]:
                ratio = str(wordCount["maxCount"]["frequency"] % length) + ':' + str(int(length / wordCount["maxCount"]["frequency"]))
            else:
                ratio = str(wordCount["maxCount"]["frequency"]) + ':' + str(length)
            result.append({
                "label": wordCount["maxCount"]["word"],
                "count": wordCount["maxCount"]['frequency'],
                "length": length
                })
    return result

info = getInfo()

import matplotlib.pyplot as plt
import numpy as np


labels = []
word_total = []
most_common = []

for prop in info:
    labels.append(prop["label"][0])
    word_total.append(prop["length"])
    most_common.append(prop["count"])


x = np.arange(len(labels))  # the label locations
width = 0.35  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(x - width/2, word_total, width, label='Total length')
rects2 = ax.bar(x + width/2, most_common, width, label='Most common word')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Paper')
ax.set_title('Word frequency map')
ax.set_xticks(x, labels)
ax.legend()

ax.bar_label(rects1, padding=3)
ax.bar_label(rects2, padding=3)

fig.tight_layout()

plt.show()