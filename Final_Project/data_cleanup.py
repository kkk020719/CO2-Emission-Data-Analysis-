#Kevin Zhao 260952439
def find_delim(s):
    """
    (str) -> str
    Take a string as input as a single line
    returns the most common delimeter within the range of ('\t', ',', ' ', '-')
    
    >>> find_delim("cat\tdog bat\tcrab-cod")
    '\t'
    >>> find_delim("4 5 6")
    ' '
    >>> find_delim("4,5,6")
    ','
    """
    count = 0
    delimiters = ['\t', ',', ' ', '-']
    for delimiter in delimiters:
        if delimiter not in s:
            continue
        if s.count(delimiter) > count:
            count = s.count(delimiter) #record the count of each delimeter
            most_deli = delimiter
    
    if count == 0:
        raise AssertionError("There are no delimeters in the given string")
    return most_deli

def clean_one(input_, output_):
    
    """
    (str,str) -> int
    
    takes input two strings representing a file to read from and another representing a file to write on
    replace most common delimeter in each line of the original file and replace with a tab
    returns the number of lines written into the other file
    
    >>> clean_one('small_raw_co2_data.txt', 'small_tab_sep_co2_data.tsv')
    10
    >>> clean_one('read_here.txt', 'write_here.tsv')
    55
    >>> clean_one('data1.txt', 'data2.tsv')
    10232
    """
    
    
    input_file = open(input_, "r", encoding="utf-8")
    output_file = open(output_, "w", encoding="utf-8")
    line_count = 0
    for line in input_file:
        most_common = find_delim(line)#finding the most common delimeter
        output_file.write(line.replace(most_common, "\t"))#change the line and write it to the file
        line_count += 1
    input_file.close()
    output_file.close()
    return line_count

def whether_is_number(s):
    
    """
    (str) -> bool
    
    helper function to check whether the string is consist of characters other than alphabets(a-z)
    
    >>> whether_is_number('34')
    True
    >>> whether_is_number('')
    True
    >>> whether_is_number('ef3')
    False
    """
    
    
    if s == '' or s == '\n':#the case when a line is ending with empty string(population missing) or when co2 is missing
        return True #this is True because we want to verify whether the string is made of characters
                    #and every other cases will be treated as if it is like a number
    
    for char in s:
        if char in ['\n','',',','.']: #edge cases to consider(to skip) #between numbers, ',' or '.' might appear
            continue
        try:
            int(char)#try to convert it to int
        except ValueError:
            return False
    
    return True
        
def final_clean(input_, output_):
    
    """
    (str,str) -> int
    
    takes two strings as input: one is the file name to read from and another is file name to write on
    change each of the line to 5 columns, each column representing a data of the country
    change all the , to .
    return the total number of lines written into the output file
    
    >>> final_clean('small_tab_sep_co2_data.tsv', 'small_clean_co2_data.tsv')
    10
    >>> final_clean('large_tab_sep_co2_data.tsv', 'large_clean_co2_data.tsv')
    17452
    >>> final_clean('data1.txt', 'data2.tsv')
    10232 
    """
    
    input_file = open(input_, "r", encoding="utf-8")
    output_file = open(output_, "w", encoding="utf-8")
    line_count = 0
    final = []
    for line in input_file:
        splitted = line.split("\t")
        if len(splitted) == 5 or len(splitted) == 4: #chekcing whether already 5 colums
            if "," in line:
                output_file.write(("\t").join(splitted).replace(",", ".")) #replace the , with .
                line_count += 1
                continue
            else:
                output_file.write(("\t").join(splitted))
                line_count += 1
                continue
            
        elif whether_is_number(splitted[2]) == False: #chekcing if its the case of long country name
            final.append(splitted[0]) #first add the iso code
            for data in splitted[::-1]:
                if whether_is_number(data) == False: #finding the last index of the country name by iterating backwards
                    name_index = splitted.index(data)
                    break
            final.append(" ".join(splitted[1:name_index+1])) #joining the long country name
            final.append(splitted[name_index+1]) #the year
            del splitted[0:name_index+2]
            if len(splitted) == 2: #if the last two data fit in the columns of 2
                final += splitted
                output_file.write(("\t").join(final).replace(",", "."))
                line_count += 1
                final = []
            else: #if still don't fit in the columns
                final.append(".".join(splitted[:-1]))
                final.append(splitted[-1])
                output_file.write('\t'.join(final))
                line_count += 1
                final = []
        else: #the cases of splitting co2 emission for example (3.125)
            final += splitted[:3] #adding the iso, name and year
            del splitted[:3]
            final.append(".".join(splitted[:-1])) #joining the splitted co2 emission with .
            final.append(splitted[-1])
            output_file.write('\t'.join(final))
            line_count += 1
            final = []
            
    input_file.close()
    output_file.close()
    return line_count
