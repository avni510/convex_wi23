import numpy as np

def build(b):
    b1, b2, b3, b4, b5 = b

    #find possible x1 vals: 
    # candidate = []
    # candidate.append(b5/(b3-32))
    # candidate.append(b4/(b2-32))
    if b4/(b2-32) > b5/(b3-32): 
        if np.sqrt(b4 + b5) <= b5/(b3 - 32):
            x1 = (np.sqrt(b4 + b5)) #in this case, no better objective function value than this for this piece of the function, over all +ve x, and this function lower bounds the other 2, so global optima
        else:#in this case, any x1 value less than b5/(b3 - 32) is worse than picking this value (because the derivative is negative in the region for x1 smaller than this)
            if np.sqrt(b4) < b5/(b3-32): 
                x1 = (b5/(b3-32)) # in this case, no better value than b5/(b3-32) because deriv is positive in whole region. This x1 val also lower bounds the region to the right, so global opt
            elif np.sqrt(b4) < b4/(b2-32):
                x1 = (np.sqrt(b4)) # in this case, no better value than b4 (deriv of convex function is 0). The value at b5/(b3-32) is worse, and anything smaller is worse (see above)
            else: #in this case, any x1 val less than b4/(b2-32) is worse, because derivative is negative throughout both other regions
                x1 = (b4/(b2-32)) #deriv here is positive always, so take smallest value in region
    else: 
        if np.sqrt(b4 + b5) <= b4/(b2 - 32):
            x1 = (np.sqrt(b4 + b5)) #in this case, no better objective function value than this, for this region, and this function lower bounds the other 2, so global optima
        else:#in this case, any x1 value less than b5/(b3 - 32) is worse than picking this value (because the derivative is negative in the region for x1 smaller than this)
            if np.sqrt(b5) < b4/(b2-32): 
                x1 = (b4/(b2-32)) # in this case, no better value than b4/(b3-32) because deriv is positive in whole region. This x1 val also lower bounds the region to the right, so global opt
            elif np.sqrt(b5) < b5/(b3-32):
                x1 = (np.sqrt(b5)) # in this case, no better value than b5 (deriv of convex function is 0). The value at b4/(b3-32) is worse, and anything smaller is worse (see above)
            else: #in this case, any x1 val less than b4/(b2-32) is worse, because derivative is negative throughout both other regions
                x1 = (b5/(b3-32)) #deriv here is positive always, so take smallest value in region

    #now account for upper bound of b1 #todo - check this doesn't break things
    x1_lb = max(b4/(b2), b5/b3, b1 - 32)
    if b1 < x1_lb: 
        # print('infeasible')
        return -1, -1, -1, -1
    
    x1 = min(b1, x1)
    x1 = max(x1, x1_lb)
    
    x2 = max(b4/x1, b2-32)

    x3 = max(b5/x1, b3-32)


    return x1 + x2 + x3, x1, x2, x3
        