def test1():
    return ('tina test 0801 !!')
def joke():
    return ('Make Taiwan Great Again !!')
    
def check_prime(x):
    is_prime = True # 是質數
    for i in range(2, x):
        if x%i == 0:
            is_prime = False
            print(f'{x} is not prime')
            break
    else:
        print(f'{x} is prime')
                 
    #return is_prime       
    
    
def generate_9x9_table(row, column):
    for i in range(1, row+1):
        for j in range(1, column+1):
            print(f'{i}x{j}={i*j:2d}',end='\t')
        print()
            
        
            #print(f'{i}x{j}={i*j:2d}', end='  ')
    print()