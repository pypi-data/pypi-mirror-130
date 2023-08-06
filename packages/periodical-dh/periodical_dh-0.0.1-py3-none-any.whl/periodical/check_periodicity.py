import numpy as np
def period_check(data,window:int=20,sort:bool=True):
    """This function checks the autocorrelation of a given data set to determine if it is periodic.

    Args:
        data (list): Input data it can be a list of floats or a numpy array.
        window (int, optional): Autocorrelation window. Defaults to 20.
        sort (bool, optional): It is the flag for sorting the array. Defaults to True.

    Returns:
        [type]: [description]
    """    
    dt=np.array(data).squeeze()
    coef=np.zeros((2,2))

    for idx,val in enumerate(range(0,len(dt),window)):
        i0,i1=idx*window, (idx+1)*window
        for idx2,val2 in enumerate(range(0,len(dt),window)):
            i0_1,i1_1=idx2*window, (idx2+1)*window
            if i0_1==i0 and i1_1==i1:
                continue
            try:
                coef+=np.corrcoef(dt[i0_1:i0_1+(i1-i0)],dt[i0:i1])
            except:
                pass
        
    dt_abs_diff=np.abs(np.diff(dt))

    return {'corr_matrix':coef,'corr_score':coef[0,1]/coef[1,1],'mean': np.mean(dt_abs_diff),
    'std': np.std(dt_abs_diff),'median':np.median(dt_abs_diff), 'result':f'Array has a mean of {np.mean(dt_abs_diff):.2f} and a std of {np.std(dt_abs_diff):.2f}'}
