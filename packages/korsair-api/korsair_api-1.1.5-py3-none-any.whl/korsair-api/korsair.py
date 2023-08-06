import requests
import pandas as pd

CONST_SHOWNUM = 7 # 한 번에 출력할 data숫자.
CONST_MAX_COLUMNS = 20 # 최대 columns 개수
CONST_MAX_ROWS = 10000 # 최대 rows 개수
CONST_MAX_WIDTH = 1000 # 한 줄에 출력 가능한 최대 데이터 크기
CONST_URL = 'http://korsair.kisti.re.kr/api/'

pd.set_option('display.max_columns', CONST_MAX_COLUMNS)
pd.set_option('display.max_rows',CONST_MAX_ROWS)
pd.set_option('display.width', CONST_MAX_WIDTH)
# pd.set_option('display.max_colwidth', None) # 셀 안의 데이터 생략 방지. 단,정렬이 안됨

#에러 위치에 따른 예제코드 출력
def get_error_message(func):
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

#df가 비어있는지 확인
def check_empty(df):
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
    

#api요청을 통해 데이터 get
def get_data(requestUrl, func):
    response = requests.get(requestUrl)
    if(response.status_code != 200):
        get_error_message(func)
        return None
    return response.json()

#df에서 정수 및 실수 값을 필터
def extract_data(df, column, num):
    if(check_empty(df) == True): return
    if((column == 'cadd_score') or (column == 'allele_freq') or (column == 'allele_count') or (column == 'site_quality')):
        data = df[column].apply(pd.to_numeric, errors='coerce')
        return df[data > num]
    elif(column == 'rsid'):
        print('Try the extract_none_rsid function')
    elif(column == 'filter'):
        print('Try the extract_filter function')
    else:
        print('The column you are looking for does not exist')

# rsid의 None 데이터 길이를 출력
def extract_none_rsid(df):
    if(check_empty(df) == True): return
    length = len(df[df['rsid'].isnull()])
    print('[rsid is the number of null values] : ' + str(length) + '\n')
    return length

# filter열 중에서 조건에 맞는 값 추출
def extract_filter(df, value):
    if(check_empty(df) == True): return
    filterToUpper = df['filter'].astype(str).apply(str.upper)
    value = df[filterToUpper.str.contains(value.upper(), na = False)]
    if value.empty:
        print('No values ​​are filtered out. Please check the parameters')
        return
    return value

#variant api
def get_variant(chro, pos, ref, alt):
    queryString = 'chr=' + str(chro) + '&pos=' + str(pos) + '&ref=' + str(ref) + '&alt=' + str(alt)
    requestUrl = CONST_URL + "variant/?" + queryString
    data = get_data(requestUrl, 'get_variant')
    if (data == None): return
    df = pd.DataFrame.from_dict(data, orient='columns')
    return df

#variant_id api
def get_variant_id(rsid):
    requestUrl = CONST_URL + 'variant/' + str(rsid)
    response = requests.get(requestUrl)
    data = get_data(requestUrl, 'get_variant_id')
    if (data == None): return
    df = pd.DataFrame.from_dict(data, orient='columns')
    return df

#gene api
def get_gene(gene_id):
    requestUrl = CONST_URL + 'gene/' + str(gene_id)
    data = get_data(requestUrl, 'get_gene')
    if (data == None): return
    df = pd.DataFrame.from_dict(data, orient='columns')
    return df

#region api
def get_region(chro, start, end):
    queryString = 'chr=' + str(chro) + '&start=' + str(start) + '&end=' + str(end)
    requestUrl = CONST_URL + "region/?" + queryString
    data = get_data(requestUrl, 'get_region')
    if (data == None): return 
    df = pd.DataFrame.from_dict(data, orient='columns')
    return df

