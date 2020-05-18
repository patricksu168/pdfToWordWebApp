import os
from prettytable import PrettyTable
import re
import slate3k as slate

specialWords = [
    'nil',
    'replacement value',
    'only',
    'not insured',
    'policy limit',
    'months',
    '$',
    '%'
]

nonValues = [
    'section',
    'sum',
    ':',
    'below',
    'limits as per policy wording',
    'limit as per policy wording',
    'residence'
]

def extractFile(filePath, start, end, s, e):
    #pdfFileObj = open(filePath, 'rb')
    #pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

    with open(filePath, 'rb') as f:
        extract = slate.PDF(f)
    readTable(extract, start, end)
    readParagraph(extract, s, e)

def readTable(extract, start, end):
    names = []
    values = []

    for i in range(start, end):
        currentPage = extract[i].split('\n\n')
        currentPage = currentPage[1:len(currentPage) - 2]
        nameInput = []
        valueInput = []
        for j in range(0, len(currentPage)):
            if any(word in currentPage[j].lower() for word in specialWords):
                nameInput = currentPage[0:j]
                valueInput = currentPage[j:]
                break
        j = 0
        while j < len(valueInput):
            if not any(word in valueInput[j].lower() for word in specialWords):
                while not any(word in valueInput[j].lower() for word in specialWords):
                    nameInput.append(valueInput.pop(j))
                    if j == len(valueInput): break
            else:
                j += 1

        tempNames = []
        tempValues = []
        for j in range(0, len(nameInput)):
            #(nameInput[j])
            paragraphs = nameInput[j].split("\n")
            for l in range(0, len(paragraphs)):
                line = paragraphs[l]
                #print(line)
                tempNames.append((line))
                value = ""
                if any(word in line.lower() for word in nonValues) and "total" not in line.lower():
                    value = ""
                    #print("case 1")
                elif ')' in line and '(' not in line:
                    value = ""
                    #print("case 2")
                elif ',' in line and i != 0 and ',' in paragraphs[l - 1] and line != paragraphs[l - 1]:
                    #print("case 3")
                    value = ""
                elif not re.search('[a-zA-Z]', line):
                    if l != 0 and not re.search('[a-zA-Z]', paragraphs[l-1]):
                        value = 'value'
                        tempValues[len(tempValues) - 1] = 'value'
                        #print("case 4")
                    else:
                        value = ""
                elif re.search("^[0-9]+\.", line) and ':' not in paragraphs[l-1]:
                    value = ""
                else:
                    value = 'value'
                    #print("case 5")
                tempValues.append(value)
        splitValues = []
        for v in valueInput:
            v = v.split("\n")
            for b in v:
                if "page" not in b.lower() and '\x0c' not in b.lower(): splitValues.append(b)
        for i in range(0, len(tempValues)):
            if tempValues[i] == "value" and splitValues:
                tempValues[i] = splitValues.pop(0)
        for v in range(0, len(tempValues)):
            if tempValues[v] == 'value': tempValues[v] = ''
        names += tempNames.copy()
        values += tempValues.copy()
        #print("\n".join(str(v) for v in list(zip(names, values))))
    #print("\n".join(str(v) for v in list(zip(names, values))))
    #print("names: " + str(len(names)) + " values: " + str(len(values)))

    tableWriter = PrettyTable()

    tableWriter.field_names = [" ", "  "]
    tableWriter.add_column(" ", names)
    tableWriter.add_column("  ", values)

    # tableWriter.set_style((MSWORD_FRIENDLY))
    tableWriter.align = "l"
    tableWriter.header = False
    tableWriter.border = False

    #print(tableWriter)

    if os.path.exists(os.path.join(os.getcwd(),'upload','output.docx')):
        os.remove(os.path.join(os.getcwd(),'upload','output.docx'))
    with open(os.path.join(os.getcwd(),'upload','output.docx'), 'w') as f:
        f.write(tableWriter.get_string())
        f.write("\n")

def readParagraph(extract, start, end):
    for j in range(start, end):

        currentPage = extract[j].split('\n\n')
        currentPage = currentPage[1:]

        index = 0
        while index < len(currentPage):
            if re.search("^[0-9]+\.", currentPage[index]):
                bulletPoints = currentPage[index].split("\n")
                content = currentPage[index + 1].split("\n")
                for i in range(0, len(bulletPoints)):
                    #print(currentPage[index] + ", " + currentPage[bulletListEnd])
                    bulletPoints[i] += content[i]
                currentPage = currentPage[0:index] + bulletPoints + currentPage[index + 2:]
                index += len(bulletPoints) - 1
            if "page" in currentPage[index].lower():
                currentPage.pop(index)
            index += 1
        with open(os.path.join(os.getcwd(),'upload','output.docx'), 'a+') as f:
            f.write("\n".join(currentPage))


def concatSpltNumString(list):
    removelist = []
    for i in range(1, len(list)):
        l = list[i]
        k = list[i - 1]
        if l[0].isdigit() or l[0] == ',':
            if k[len(k) - 1].isdigit() or k[len(k) - 1] == ',':
                list[i] = k + l
                removelist.append(i - 1)
    for i in range(len(removelist) - 1, -1, -1):
        list.pop(removelist[i])
    return list

if __name__ == "__main__":
    extractFile('sample2.pdf', 1, 4, 5, 10)