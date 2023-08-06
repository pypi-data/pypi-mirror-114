def check_prime(x):
    is_prime = True # 是質數
    for i in range(2, x):
        if x%i == 0:
            is_prime = False
            break
        
    return is_prime

# print 9x9 table
def generate_9x9_table(row, column):
    for i in range(1, row+1):
        for j in range(1, column+1):
            print(f'{i}x{j}={i*j:2d}', end='  ')
        print()

# print 9x9 table V2
def generate_9x9_table_v2(row, column):
    result = ''
    for i in range(1, row+1):
        for j in range(1, column+1):
            result += f'{i}x{j}={i*j:2d}  '
        result += '\n'
    return result
    
def calculate_BMI(height, weight=80): 
    '''
    功能:計算BMI
    輸入參數:身高(cm)、體重(kg)
    輸出：BMI、評論
    作者：Michael
    '''
    if not str(height).isdigit():
        return 0, "height input error." 
#     if not str(weight).isdigit():
#         return 0, "weight input error." 
    if not isinstance(weight, float) and not isinstance(weight, int):
        return 0, "weight input error." 
    
    BMI=float(weight)/(float(height)/100)**2
        
    message = ''
    if BMI<18.5:
        message = '過輕'
    elif BMI<24:
        message = '正常'
    elif BMI<27:
        message = '過重'
    elif BMI<30:
        message = '輕度肥胖'
    elif BMI<35:
        message = '中度肥胖'
    else:
        message = '重度肥胖'
    
    return round(BMI, 1), message
    
    
def sum_list(list1=[1,2,3]):
    total = 0
    for i in list1:
        total += i
        
    return total

def bubble_Sort(list2):
    for i in range(len(list2)):
        for j in range(0,len(list2)-1):
            if list2[j]>list2[j+1]:
                list2[j],list2[j+1]=list2[j+1],list2[j]
    return list2

