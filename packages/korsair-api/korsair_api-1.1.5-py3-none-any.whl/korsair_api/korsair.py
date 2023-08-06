import requests
import pandas as pd

_CONST_MAX_COLUMNS = 20 # 최대 columns 개수
_CONST_MAX_ROWS = 10000 # 최대 rows 개수
_CONST_MAX_WIDTH = 1000 # 한 줄에 출력 가능한 최대 데이터 크기
_CONST_URL = 'http://korsair.kisti.re.kr/api/'

pd.set_option('display.max_columns', _CONST_MAX_COLUMNS)
pd.set_option('display.max_rows',_CONST_MAX_ROWS)
pd.set_option('display.width', _CONST_MAX_WIDTH)
# pd.set_option('display.max_colwidth', None) # 셀 안의 데이터 생략 방지. 단,정렬이 안됨


''' 
    에러가 발생한 함수에 맞게 예제 코드를 출력해 주는 함수

    @ param
        string func = 에러가 발생한 함수의 이름
    
    @ Return
        not thing
    
    @ Author
        강성범(qkfka9045@gmail.com)

    @ Date
        2021.07.30
''' 
def _get_error_message(func):
    print('There is no data to be retrieved.\n')
    print('[Simple Example]')

    if(func == 'get_variant'):
        print("get_variant('chr7', 140787574, 'C', 'T')")
    elif (func == 'get_variant_id'):
        print("get_variant_id('rs397507456')")
    elif (func == 'get_gene'):
        print("get_gene('CHD8')")
    elif (func == 'get_region'):
        print("get_region(17, 7676272, 7675994)")
    else:
        print('parameter error')


''' 
    파라미터인 df의 타입을 확인하고 비어있는지 확인

    @ param
        variable df = pandas라이브러리를 통해 만들어진 dataframe
    
    @ Return
        boolean
    
    @ Author
        강성범(qkfka9045@gmail.com)

    @ Date
        2021.07.30
''' 
def _check_empty(df):
    type_parameter = str(type(df))
    if(type_parameter == "<class 'pandas.core.frame.DataFrame'>"):
        if(df.empty):
            print('The parameter is empty')
            return True
        else:
            return False
    else:
        print('Not a valid df type')
        return True
    

''' 
    api를 통해 데이터를 받아오는데, 정상적으로 받아오지 않을경우(200이 아닐때) None반환

    @ param
        string requestUrl   = api요청 url
        string func         = _get_data를 호출한 함수의 이름
    
    @ Return
        json
    
    @ Author
        강성범(qkfka9045@gmail.com)

    @ Date
        2021.07.30
''' 
def _get_data(requestUrl, func):
    response = requests.get(requestUrl)
    if(response.status_code != 200):
        _get_error_message(func)
        return None
    return response.json()

''' 
    실수 값을 가지는 열(cadd_score, allele_freq, allele_count, site_quality)을 특정값(num)이상의 값만 확인할 수 있도록 필터링해 주는 함수

    @ param
        variable df   = get_variant, get_variant_id, get_gene, get_region 중 하나의 함수를 통해 얻은 값
        string column = 'cadd_score', 'allele_freq', 'allele_count', 'site_quality' 중 하나의 값
        int num       = column중에서 num 이상의 숫자를 가진 값을 필터링
    
    @ Return
        pandas.dataframe
    
    @ Author
        강성범(qkfka9045@gmail.com)

    @ Date
        2021.07.30
''' 
def extract_data(df, column, num):
    if(_check_empty(df) == True): return
    if((column == 'cadd_score') or (column == 'allele_freq') or (column == 'allele_count') or (column == 'site_quality')):
        data = df[column].apply(pd.to_numeric, errors='coerce')
        return df[data >= num]
    elif(column == 'rsid'):
        print('Try the extract_none_rsid function')
    elif(column == 'filter'):
        print('Try the extract_filter function')
    else:
        print('The column you are looking for does not exist')

''' 
    rsid의 None 데이터 길이 반환

    @ param
        variable df = pandas라이브러리를 통해 만들어진 dataframe
    
    @ Return
        int
    
    @ Author
        강성범(qkfka9045@gmail.com)

    @ Date
        2021.07.30
''' 
def extract_none_rsid(df):
    if(_check_empty(df) == True): return
    length = len(df[df['rsid'].isnull()])
    print('[rsid is the number of null values] : ' + str(length) + '\n')
    return length

''' 
    # filter열 중에서 조건에 맞는 값('PASS', 'LCR', 'ExcessHet', 'VQSRTrancheSNP99.00to99.90+') 추출

    @ param
        variable df  = pandas라이브러리를 통해 만들어진 dataframe
        string value = 'PASS', 'LCR', 'ExcessHet', 'VQSRTrancheSNP99.00to99.90+'중에 하나의 값
    
    @ Return
        pandas.dataframe
    
    @ Author
        강성범(qkfka9045@gmail.com)

    @ Date
        2021.07.30
''' 
def extract_filter(df, value):
    if(_check_empty(df) == True): return
    filterToUpper = df['filter'].astype(str).apply(str.upper)
    value = df[filterToUpper.str.contains(value.upper(), na = False)]
    if value.empty:
        print('No values ​​are filtered out. Please check the parameters')
        return
    return value

''' 
    # (http://korsair.kisti.re.kr/api/variant/) Api에서 값을 받아와 반환

    @ param
        String chro = chromosome
        int pos = position
        string ref = reference allele
        string alt = alternative allele
    
    @ Return
        pandas.dataframe
    
    @ Author
        강성범(qkfka9045@gmail.com)

    @ Date
        2021.07.30
''' 
def get_variant(chro, pos, ref, alt):
    queryString = 'chr=' + str(chro).lower() + '&pos=' + str(pos) + '&ref=' + str(ref).upper() + '&alt=' + str(alt).upper()
    requestUrl = _CONST_URL + "variant/?" + queryString
    data = _get_data(requestUrl, 'get_variant')
    if (data == None): return
    df = pd.DataFrame.from_dict(data, orient='columns')
    return df

''' 
    # (http://korsair.kisti.re.kr/api/variant/{rsid}) Api에서 값을 받아와 반환

    @ param
        string rsid = dbSNP rsid
    
    @ Return
        pandas.dataframe
    
    @ Author
        강성범(qkfka9045@gmail.com)

    @ Date
        2021.07.30
''' 
def get_variant_id(rsid):
    requestUrl = _CONST_URL + 'variant/' + str(rsid)
    data = _get_data(requestUrl, 'get_variant_id')
    if (data == None): return
    df = pd.DataFrame.from_dict(data, orient='columns')
    return df

''' 
    # (http://korsair.kisti.re.kr/api/gene/{gene_id}) Api에서 값을 받아와 반환

    @ param
        string gene_id = gene_id
    
    @ Return
        pandas.dataframe
    
    @ Author
        강성범(qkfka9045@gmail.com)

    @ Date
        2021.07.30
''' 
def get_gene(gene_id):
    requestUrl = _CONST_URL + 'gene/' + str(gene_id).upper()
    data = _get_data(requestUrl, 'get_gene')
    if (data == None): return
    df = pd.DataFrame.from_dict(data, orient='columns')
    return df

''' 
    # (http://korsair.kisti.re.kr/api/region/) Api에서 값을 받아와 반환

    @ param
        String chro = chromosome
        int start = start position
        int end = end position
    
    @ Return
        pandas.dataframe
    
    @ Author
        강성범(qkfka9045@gmail.com)

    @ Date
        2021.07.30
''' 
def get_region(chro, start, end):
    queryString = 'chr=' + str(chro).lower() + '&start=' + str(start) + '&end=' + str(end)
    requestUrl = _CONST_URL + "region/?" + queryString
    data = _get_data(requestUrl, 'get_region')
    if (data == None): return 
    df = pd.DataFrame.from_dict(data, orient='columns')
    return df