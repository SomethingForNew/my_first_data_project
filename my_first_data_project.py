# 표준 라이브러리 임포트는 없다고 가정

# 서드파티 라이브러리 임포트 (알파벳 순)
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# 로컬 애플리케이션/라이브러리 특정 임포트는 없다고 가정

# matplotlib 라이브러리 한글 폰트 깨짐 방지 용도
plt.rcParams['font.family'] ='Malgun Gothic'
plt.rcParams['axes.unicode_minus'] =False


# 1.데이터 불러오기 및 데이터 확인
df = pd.read_csv('sales_data.csv')

# 상위 5개 row 확인
# print(df.head())

# 데이터 타입, 결측치 등 정보 확인
# 처음 하는 프로젝트기에 결측치가 없는 데이터로 진행
# print(df.info())


# 2.Pandas를 사용해서 데이터 전처리 
# 목표: 날짜와 시간 컬럼을 분석하기 적합한 형태로 변환 하고, 필요한 파생 변수(Series)를 만든다.
# 예시: order_date를 실제 날짜 형식으로, order_time을 시간 형식으로 변환하고, 요일이나 시간대(오전/점심/오후 등)를 나타내는 컬럼을 추가
# 참고사항: 데이터프레임에서는 컬럼을 Series 라고 부른다.

# order_date의 dtype: 문자열 object를 -> datetime64로 변경
# order_time이 dtype: 문자열 obejct를 -> datetime.tiem object 로 변경 -> 왜? 어떤 효율을 위해서인지 모르겠음
df['order_date'] = pd.to_datetime(df['order_date'])
df['order_time'] = pd.to_datetime(df['order_time']).dt.time
df['day_of_week'] = df['order_date'].dt.day_name() # 요일 이름 추출 후 day_of_week 이라는 Series 추가

# Pandas의 apply()는 DataFrame이나 Series에 사용자 정의함수, 내장 함수, 람다 함수 를 적용할 때 사용한다.
# 각 햏, 각 열 또는 각 요소에 복잡한 연산을 적용해야 할때 유용하게 활용된다.
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


# 3.탐색적 데이터분석(EDA) 및 시각화
# 목표: 질문에 대한 답을 찾기 위해 데이터를 요약하고, 시각적으로 표현하여 패턴을 발견한다.

# 3-1.어떤 메뉴가 가장 잘 팔리는가?
# 분석: menu_item 별 quantity의 합계 또는 total_price의 합계를 계산한다.
# 시각화: 막대 그래프로 표현
# 가설: 아메리카노가 가장 많이 팔릴 것이다.

"""
groupby를 하게 되면 DataFrameGroupBy 객체는 그룹화된 데이터를 직접 보여주지는 않고 그룹별로 특정 연산을 수행 할 수 있도록 준비된 객체가 된다.
sort_value()는 말그대로 sort다 default option이 오름차순이다. ascending=Falase를 이용하면 내림차순이 가능하다.
"""
menu_sales = df.groupby('menu_item')['quantity'].sum().sort_values(ascending=False)


"""
figure()는 Matplotlib의 전체 그림 창을 나타낸다. 이 안에 하나 이상의 서브플롯(Axes)이 포함 될 수 있다.
figure()는 제목, 전체크기등을 설정하는데 사용한다.
figsize 매개변수를 사용하여 그림의 크기를 인치 단위로 지정할 수 있다.
"""
plt.figure(figsize=(10, 6))


# sns.barplot(x=menu_sales.index, y=menu_sales.values)
# plt.title('메뉴별 총 판매 수량')
# plt.xlabel('메뉴')
# plt.ylabel('판매 수량')
# plt.xticks(rotation=45)
# plt.show()


# 3-2.요일별/시간대별 판매량은 어떻게 다른가?
# 분석: day_of_week나 time_slot 별 total_price의 합계를 계산한다.
# 시각화: 요일별/시간대별 막대 그래프 또는 선 그래프로 표현
# 가설: 주말이 평일보다 판매량이 높을 것이다. / 점심시간과 오후 시간대가 피크일 것이다.
