# 서드파티 라이브러리 임포트 (알파벳 순)
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# matplotlib 라이브러리 한글 폰트 깨짐 방지 용도
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False


# 1. 데이터 불러오기 및 데이터 확인
df = pd.read_csv('sales_data.csv')

# 2. Pandas를 사용해서 데이터 전처리
# 목표: 날짜와 시간 컬럼을 분석하기 적합한 형태로 변환하고, 필요한 파생 변수(Series)를 만든다.
# 예시: order_date를 실제 날짜 형식으로, order_time을 시간 형식으로 변환하고,
# 요일이나 시간대(오전/점심/오후 등)를 나타내는 컬럼을 추가

# order_date의 dtype: 문자열(object)을 datetime64로 변경
df['order_date'] = pd.to_datetime(df['order_date'])

# order_time의 dtype: 문자열(object)을 datetime.time object로 변경
df['order_time'] = pd.to_datetime(df['order_time']).dt.time

# 요일 이름 추출 후 day_of_week 이라는 Series 추가
df['day_of_week'] = df['order_date'].dt.day_name()

# 시간 추출
df['hour'] = df['order_time'].apply(lambda x: x.hour)


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


# 3. 탐색적 데이터분석(EDA) 및 시각화
# 목표: 질문에 대한 답을 찾기 위해 데이터를 요약하고 시각적으로 표현하여 패턴을 발견한다.

# 3-1. 어떤 메뉴가 가장 잘 팔리는가?
# 분석: menu_item 별 quantity의 합계 또는 total_price의 합계를 계산한다.
# 시각화: 막대 그래프로 표현
# 가설: 아메리카노가 가장 많이 팔릴 것이다.

# menu_item별 quantity의 합계를 계산하고 내림차순 정렬
menu_sales = df.groupby('menu_item')['quantity'].sum().sort_values(
    ascending=False
)


# figure()를 사용하여 그림 창의 크기 설정
plt.figure(figsize=(10, 6))

# barplot()을 사용하여 메뉴별 총 판매 수량 시각화
sns.barplot(x=menu_sales.index, y=menu_sales.values)

# 그래프 제목과 x, y축 라벨 설정
plt.title('메뉴별 총 판매 수량')
plt.xlabel('메뉴')
plt.ylabel('판매 수량')

# x축 라벨이 겹치지 않도록 45도 회전
plt.xticks(rotation=45)
plt.show()


# 3-2. 요일별/시간대별 판매량은 어떻게 다른가?
# 분석: day_of_week나 time_slot 별 total_price의 합계를 계산한다.
# 시각화: 요일별/시간대별 막대 그래프 또는 선 그래프로 표현
# 가설: 주말이 평일보다 판매량이 높을 것이다. / 점심시간과 오후 시간대가 피크일 것이다.