import os
import re
def fileSort(path = str(), extensions=list()):
    """
    
    Sorts image files in a directory based on numeric and alphabetic criteria and returns the sorted list.

    Parameters
    ----------
    path : str, optional
        The path to the directory containing the files to be sorted. If not provided, the current working directory ('./') is used.
    extensions : list, optional
        A list of file extensions to include in the sorting. Defaults to common image formats
        (e.g., ['.jpg', '.png', '.jpeg', '.tif', '.tiff', '.nii', '.JPG', '.JPEG', '.TIFF', '.TIF', '.NII']).

    Returns
    -------
    list
        A list of sorted file names:
        - Files with numeric names are sorted numerically, followed by alphabetic sorting within their group.
        - Files without numeric values are sorted alphabetically.
        - Non-matching files (i.e., files without the specified extensions) are excluded.
    
    Notes
    -----
    - Files that do not match the provided extensions are listed as "not found" in the console.
    - Numeric sorting ensures files with numbers (e.g., "file2.png", "file10.png") are ordered naturally.
    - Alphabetic sorting applies to files without numeric values or as a secondary criterion within numeric groups.
    - Relies on helper functions (`contains_digit_optimized`, `split_image_string`, `natural_keys`, and `create_final_list`) to process numeric values and sort efficiently.
    
    Examples
    --------
    >>> fileSort(path="./images", extensions=[".jpg", ".png"])
    ['file1.jpg', 'file2.jpg', 'file10.jpg', 'image_a.png', 'image_b.png']

    >>> fileSort(path="./dataset")
    ['IMG001.jpg', 'IMG002.jpg', 'PIC10.png', 'PIC20.png']
    
    >>> fileSort()  # Defaults to current directory and common image formats
    ['IMG1.jpg', 'IMG10.jpg', 'IMG2.jpg', 'photo_a.png', 'photo_b.png']
    
    Warnings
    --------
    - Prints a warning to the console if no matching files are found or if the directory is empty.
    - Returns -1 if no files with the specified extensions exist in the directory.
    
    """
    if len(extensions) == 0:
        extensions = ['.jpg', '.png', '.jpeg', '.tif', '.tiff', '.nii', '.JPG', '.JPEG', '.TIFF', '.TIF', '.NII']

    control_1_sentence ='filename.endswith(\'' + extensions[0] + '\')'
    for z in range(1, len(extensions)):
        control_1_sentence += ' or filename.endswith(\'' + extensions[z] + '\')'
    if(path==''):
        path='./'
    path = os.listdir(path)

    list_not = list()
    img_list = []
    for filename in path:
       if eval(control_1_sentence):
           img_list.append(filename)
       else:
           list_not.append(filename)
    if len(list_not) > 0:
        print(str(list_not)+' files not found.')
    digits = list()
    digits_temp = list()
    non_numeric_list = [filename for filename in img_list if not re.search(r'\d', filename)] # MOVED!
    if(len(img_list)==0):
        print('no files !!!')
        return -1
    control_1 = 0
    result = contains_digit_optimized(img_list)
    if result == True:
        control_1 += 1
    control_5 = split_image_string(img_list)
    int_counts = []
    for sublist in control_5:
        if isinstance(sublist, list):  # Sadece alt listeleri kontrol et
            int_count = sum(1 for item in sublist if isinstance(item, int))
            int_counts.append(int_count)
        else:
            int_counts.append(0)  # Eğer alt liste değilse 0 ekle
    max_int_value = max(int_counts)
    if(control_1==0):
        list_final = sorted(img_list, key=str.lower)
        print('filename without digits ! \nFiles are sorted alphabetically.')
        return list_final
    elif(control_1>0): # 1
        list_zeros=list()
        for control_1_value in range(0,max_int_value):
            maxx = -1
            for i in range(len(img_list)):
                index = natural_keys(img_list[i])
                control_2 = 0
                for ii2 in range(len(index)):
                    if type(index[ii2]) == int:
                        if (control_2 == control_1_value):
                            if (index[ii2] > maxx):
                                maxx = index[ii2]
                        control_2+=1
            list_zeros.append(len(str(maxx)))
        if non_numeric_list:
            non_numeric_list = sorted(non_numeric_list, key=str.lower)
            img_list = [filename for filename in img_list if re.search(r'\d', filename)]
        for i in range(len(img_list)):
            index = natural_keys(img_list[i])
            check_3 = 0
            list2=''
            for ii in range(len(index)):
                if type(index[ii]) == int:
                    if(check_3>0):
                        number_zeros=list_zeros[check_3-1]-len(str(index[ii]))
                        for j in range(0,number_zeros):
                            list2 += '0'
                        list2 += str(index[ii])
                    else:
                        list2 += str(index[ii])
                    check_3+=1
            digits.append(int(list2))
            digits_temp.append(int(list2))
        digits.sort()
        list_final = create_final_list(img_list, digits, digits_temp, non_numeric_list) #
    return list_final
    

def create_final_list(img_list, digits, digits_temp, non_numeric_list = None):
    """
    
    Creates a final sorted list of items by aligning the numeric indices of `digits` with the
    temporary list `digits_temp`, and optionally appends non-numeric items to the result.

    Parameters:
    ----------
    img_list : list
        A list of file names or items to be sorted.
    digits : list
        A list of numeric values that represent the intended sorting order.
    digits_temp : list
        A temporary list used to match the indices of `digits`.
    non_numeric_list : list, optional
        A list of non-numeric items to be appended to the final result (default is None).

    Returns:
    -------
    list
        A final sorted list that includes items from `img_list` arranged numerically
        based on `digits` and optionally includes items from `non_numeric_list`.

    Examples:
    --------
    >>> img_list = ["file3.png", "file1.png", "file2.png"]
    >>> digits = [3, 1, 2]
    >>> digits_temp = [1, 2, 3]
    >>> create_final_list(img_list, digits, digits_temp)
    ['file1.png', 'file2.png', 'file3.png']

    >>> create_final_list(img_list, digits, digits_temp, ["extra_file.txt"])
    ['file1.png', 'file2.png', 'file3.png', 'extra_file.txt']
    
    """
    
    list_final = list()
    for c in range(len(img_list)):
        v = digits_temp.index(digits[c])
        list_final.append(img_list[v])
        
    if non_numeric_list is not None:
        list_final.extend(non_numeric_list)
        
    return list_final


def contains_digit_optimized(strings):
    """
    
    Checks if any string in the given iterable contains at least one numeric digit (0-9).

    Parameters:
    ----------
    strings : iterable
        An iterable (e.g., list or tuple) containing elements to check for numeric digits.

    Returns:
    -------
    bool
        Returns `True` if at least one string in the iterable contains a numeric digit,
        otherwise returns `False`.

    Notes:
    ------
    - The function only checks elements of type `str`. Non-string elements are ignored.
    - Stops at the first occurrence of a numeric digit, making it efficient for large iterables.

    Examples:
    --------
    >>> contains_digit_optimized(["apple", "banana", "cherry123"])
    True

    >>> contains_digit_optimized(["apple", "banana", "cherry"])
    False

    >>> contains_digit_optimized(["apple", 123, "no_digits_here"])
    False
    
    """
    for s in strings:
        if isinstance(s, str) and any(char.isdigit() for char in s):
            return True  # Returns True when the first digit is found.
    return False  # If no digit is found in any element, False is returned.


def split_image_string(image_string):
    """
    
    Splits and processes a list of image file names by removing file extensions,
    extracting alphabetic and numeric parts, and returning structured lists.

    Parameters:
    ----------
    image_string : list
        A list of image file names (e.g., ["IMG123.jpg", "PIC45.jpg"]) to process.

    Returns:
    -------
    list
        A list of processed sublists where each sublist contains:
        - Alphabetic parts as strings.
        - Numeric parts as integers.

    Notes:
    ------
    - The `.jpg` extension is removed from each file name.
    - Uses regular expressions to extract alphabetic sequences (`[A-Z]+`) and numeric sequences (`\d+`).
    - Numeric parts are converted to integers for easier processing later.

    Examples:
    --------
    >>> split_image_string(["IMG123.jpg", "PIC45.jpg"])
    [['IMG', 123], ['PIC', 45]]

    >>> split_image_string(["A12B34.jpg", "C56D78.jpg"])
    [['A', 12, 'B', 34], ['C', 56, 'D', 78]]
    
    """
    result_list = list()
    for i in image_string:
        cleaned_string = i.replace(".jpg", "") # Remove *.jpg extension
        parts = re.findall(r'[A-Z]+|\d+', cleaned_string) # Split string with regular expressions
        result = [int(part) if part.isdigit() else part for part in parts] # Convert numbers (digits) to integer type
        result_list.append(result)
    return result_list


def atoi(text):
    """
    
    Converts a numeric string to an integer, or returns the string as is if it is not numeric.

    Parameters:
    ----------
    text : str
        The input string to check and possibly convert.

    Returns:
    -------
    int or str
        - If the input `text` is numeric (e.g., "123"), returns it as an integer (123).
        - If the input `text` is not numeric (e.g., "hello"), returns it unchanged as a string.

    Notes:
    ------
    - This function is typically used as a helper in sorting algorithms to handle mixed
      alphanumeric strings where numeric parts need to be sorted as integers.

    Examples:
    --------
    >>> atoi("123")
    123

    >>> atoi("hello")
    'hello'

    >>> atoi("42")
    42
    
    """
    return int(text) if text.isdigit() else text


def natural_keys(text):
    """
    
    Generates a key for natural (human-friendly) sorting by splitting the input string into numeric and non-numeric parts.

    Parameters:
    ----------
    text : str
        The input string to be processed for natural sorting.

    Returns:
    -------
    list
        A list of parts where numeric substrings are converted to integers, and non-numeric substrings remain as strings.

    Notes:
    ------
    - Relies on the `atoi` function to handle numeric conversion.
    - Useful for sorting strings with mixed alphanumeric content, such as file names or labels,
      where numeric parts should be compared numerically rather than lexicographically.

    Examples:
    --------
    >>> natural_keys("file10")
    ['file', 10, '']

    >>> natural_keys("file2")
    ['file', 2, '']

    >>> sorted(["file2", "file10", "file1"], key=natural_keys)
    ['file1', 'file2', 'file10']
    
    """
    return [ atoi(c) for c in re.split('(\d+)',text) ]
