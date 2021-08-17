f = open(r'test.json', encoding='UTF-8')
lines = f.readlines()
result_lines = []
result= open(r'result.json', encoding='UTF-8', mode='w')
for line in lines:
    index = line.find('#')
    name = line[:index]
    hex_str = line[index+1 : -1]
    r = int(hex_str[0:2], 16)
    g = int(hex_str[2:4], 16)
    b = int(hex_str[4:6], 16)
    result_lines.append(f'{{"name":"{name}","rgb":[{r},{g},{b}],"hex":"#{hex_str}"}},')
result.writelines(result_lines)