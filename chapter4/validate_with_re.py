import re


def validate_price(value: str):
    '''
    valueが価格として正しい文字列（数字とカンマのみ含む文字列）であるかどうかを判別し、
    正しくない値の場合はValueErrorを発生させる
    '''
    if not re.search(r'^[0-9,]+$', value):#数字とカンマのみを含む正規表現にマッチするかをチェックする
        raise ValueError(f'Invalid price: {value}')

validate_price('3,000')
validate_price('無料')#価格として正しくないので例外