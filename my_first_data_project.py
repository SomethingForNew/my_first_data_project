# import pandas as pd
import pandas as pd

# 1. 데이터 불러오기 및 데이터 확인
df = pd.read_csv('sales_data.csv')
# 상위 5개 row 확인
# print(df.head())

# 데이터 타입, 결측치 등 정보 확인
# 처음 하는 프로젝트기에 결측치가 없는 데이터로 진행
print(df.info())


# 데이터 전처리
# 목표: 날짜와 시간 컬럼을 분석하기 적합한 형태로 변환 하고, 필요한 파생 변수(Series)를 만든다.
# 예시: order_date를 실제 날짜 형식으로, order_time을 시간 형식으로 변환하고, 요일이나 시간대(오전/점심/오후 등)를 나타내는 컬럼을 추가
# 참고사항: 데이터프레임에서는 컬럼을 Series 라고 부른다.

# order_date의 dtype: 문자열 object를 -> datetime64로 변경
# order_time이 dtype: 문자열 obejct를 -> datetime.tiem object 로 변경 -> 왜? 어떤 효율을 위해서인지 모르겠음

df['order_date'] = pd.to_datetime(df['order_date'])
df['order_time'] = pd.to_datetime(df['order_time']).dt.time
df['day_of_week'] = df['order_date'].dt.day_name() # 요일 이름 추출 후 day_of_week 이라는 Series 추가
df['hour'] = df['order_time'].apply(lambda x: x.hour) # 시간 추출


# 시간대를 분류하는 함수
def categorize_time(hour: int) -> str:
    """주어진 시간(시)을 바탕으로 시간대를 분류합니다.

    Args:
        hour (int): 0부터 23까지의 정수 형태의 시간(시).

    Returns:
        str: 분류된 시간대 ('오전', '점심', '오후', '저녁' 중 하나).
    """
    if 6 <= hour < 12:
        return '오전'
    elif 12 <= hour < 13:
        return '점심'
    elif 13 <= hour < 18:
        return '오후'
    else:
        return '저녁'

df['time_slot'] = df['hour'].apply(categorize_time)

print(df.head())