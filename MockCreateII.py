import re
import os

def GetNumOfInputs(inputs):
    template = 0
    count = 0
    for c in inputs:
        if c == '<':
            template += 1
        if c == ',' and template == 0:
            count = count + 1
        if c == '>':
            template -= 1

    if len(inputs) == 0:
        count = 0
    else:
        count += 1

    return count

interfaceFilePath = input("Enter interface path:")
turtleMock = True if input(
    "Which type of mock do you want to generate? \n    google mock: 1\n    turtle mock: 2\n") == '2' else False
interfaceFolderPath = os.path.dirname(interfaceFilePath)

inputHeader = open(interfaceFilePath)
interfaceStr = ""
for line in inputHeader:
    interfaceStr += line

commentStarRgx = re.compile(r"/[*].*?[*]/", flags=re.DOTALL)
commentBackSpaceRgx = re.compile(r"//.*")
voidFuncRgx = re.compile(r"\(\s*void\s*\)")
cleanedInterfaceStr = re.sub(commentStarRgx, '', interfaceStr)
cleanedInterfaceStr = re.sub(commentBackSpaceRgx, '', cleanedInterfaceStr)
cleanedInterfaceStr = re.sub(voidFuncRgx, '( )', cleanedInterfaceStr)
dtor = re.compile(r"\s*virtual\s+~\w+\s*\(\s*\)\s*.*?;")
cleanedInterfaceStr = re.sub(dtor, '', cleanedInterfaceStr)
print(cleanedInterfaceStr)

classRe = re.compile(
    r"class\s+(\w+)\s*.*?{\s*public:\s*(.*?)}", flags=re.DOTALL)
classInc = classRe.search(cleanedInterfaceStr)

# print(classInc.group(1))
# print(classInc.group(2))
functionsRe = re.compile(
    r"virtual\s+(.*?)\s+(\w+)\s*\(\s*(.*?)\s*\)\s*(\w*)\s*=\s*0\s*;", flags=re.DOTALL)
funcMatches = functionsRe.findall(classInc.group(2))

className = classInc.group(1)[1:]
# print(className)
outputFile = open(interfaceFolderPath + '/Mock' + className + '.h', 'w')
print('#include "I'+className+'.h"')
print()
outputFile.writelines(['#include "I' + className + '.h"\n', '\n'])

if turtleMock: # trutle mock
    classDclr = 'MOCK_BASE_CLASS(Mock' + className+ ', I' + className+')'
    print(classDclr)
    print('{')
    outputFile.writelines([classDclr + '\n', '{\n'])

    for func in funcMatches:
        returnType = func[0]
        methodName = func[1]
        inputs = func[2]
        isConst = (func[3] == 'const')
        numberOfInputs = str(GetNumOfInputs(inputs))

        if isConst:
            print('    MOCK_CONST_METHOD('+ methodName + ', ' +
                  numberOfInputs + ', ' + returnType+'(' + inputs + '));')
            outputFile.write('    MOCK_CONST_METHOD(' + methodName + ', ' +
                             numberOfInputs + ', ' + returnType + '(' + inputs + '));\n')
        else:
            print('    MOCK_NON_CONST_METHOD('+methodName+', ' +
                  numberOfInputs+', '+returnType+'('+inputs+'));')
            outputFile.write('    MOCK_NON_CONST_METHOD('+methodName +
                             ', '+numberOfInputs+', '+returnType+'('+inputs+'));\n')

else:  # google mock
    classDclr = 'class Mock' + className + ': public I' + className
    print(classDclr)
    print('{')
    outputFile.writelines([classDclr + '\n', '{\n'])
    for func in funcMatches:
        returnType = func[0]
        methodName = func[1]
        inputs = '(' + func[2] + ')'
        isConst = (func[3] == 'const')
        specs = '(' + ('const, ' if isConst else '') + 'virtual)'
        returnType = '(' + returnType + ')' if re.search(',', returnType) else returnType
        mockFunc = 'MOCK_METHOD(' + returnType + ', ' + methodName + ', ' + inputs + ', ' + specs + ');'
        print('  ' + mockFunc)
        outputFile.write('    ' + mockFunc + '\n')

print('};')
outputFile.write('};')

inputHeader.close()
outputFile.close()

input()
