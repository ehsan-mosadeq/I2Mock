import re
import os

def GetNumOfInputs(inputs):
    template = 0
    count = 0
    for c in inputs:
        if c == '<':
            template += 1
        if c == ',' and template == 0 :
            count = count + 1
        if c == '>':
            template -= 1
    
    if len(inputs) == 0:
        count = 0
    else:
        count +=1

    return count


address = input("Enter interface path:")
dirName = os.path.dirname(address);
a = open(address)

loadedFile="";
for l in a:
    loadedFile += l;

commentStar = re.compile(r"/[*].*?[*]/", flags = re.DOTALL);
commentBks = re.compile(r"//.*");
voidFunc = re.compile(r"\(\s*void\s*\)");
removedComments = re.sub(commentStar, '', loadedFile);
removedComments = re.sub(commentBks, '', removedComments);
removedComments = re.sub(voidFunc, '( )', removedComments);
dtor = re.compile(r"\s*virtual\s+~\w+\s*\(\s*\)\s*.*?;")
removedDtor = re.sub(dtor,'',removedComments)
print(removedDtor)

classRe = re.compile(r"class\s+(\w+)\s*.*?{\s*public:\s*(.*?)}", flags = re.DOTALL)
classInc = classRe.search(removedDtor);

#print(classInc.group(1))
#print(classInc.group(2))
functionsRe = re.compile(r"virtual\s+(.*?)\s+(\w+)\s*\(\s*(.*?)\s*\)\s*(\w*)\s*=\s*0\s*;", flags = re.DOTALL)
funcMatches = functionsRe.findall(classInc.group(2))

className = classInc.group(1)[1:]
#print(className)
outputFile = open(dirName + '/Mock' + className + '.h', 'w') 
print ('#include "I'+className+'.h"')
print ()
print ('MOCK_BASE_CLASS(Mock'+className+', I'+className+')')
print ('{')
outputFile.write('#include "I'+className+'.h"\n')
outputFile.write('\n')
outputFile.write('MOCK_BASE_CLASS(Mock'+className+', I'+className+')\n')
outputFile.write('{\n')

for func in funcMatches:
    returnType = func[0]
    methodName = func[1]
    inputs = func[2]
    isConst = (func[3] == 'const')
    numberOfInputs = str(GetNumOfInputs(inputs))
    
    if isConst:
        print('	MOCK_CONST_METHOD('+methodName+', '+numberOfInputs+', '+returnType+'('+inputs+'));')
        outputFile.write('	MOCK_CONST_METHOD('+methodName+', '+numberOfInputs+', '+returnType+'('+inputs+'));\n')
    else:
        print('	MOCK_NON_CONST_METHOD('+methodName+', '+numberOfInputs+', '+returnType+'('+inputs+'));')
        outputFile.write('	MOCK_NON_CONST_METHOD('+methodName+', '+numberOfInputs+', '+returnType+'('+inputs+'));\n')
print ('};')
#-----------------------------------------------------------------------
for func in funcMatches:
    returnType = func[0]
    methodName = func[1]
    inputs = func[2]
    isConst = (func[3] == 'const')
    
    if isConst:
        mockFunc = 'MOCK_METHOD((' + returnType + '), ' + methodName + ', (' + inputs + '));'
        #outputFile.write('	MOCK_CONST_METHOD('+funcName+', '+numberOfInputs+', '+returnType+'('+inputs+'));\n')
    
print ('};')
#------------------------------------------------------------------------
outputFile.write('};')
a.close()
outputFile.close()
input();
