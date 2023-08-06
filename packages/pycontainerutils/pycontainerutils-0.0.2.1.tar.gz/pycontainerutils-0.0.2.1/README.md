# pycontainerutils
## Installation
`pip install pycontainerutils`

## Example

### version 
추후 release로 이동 
0.0.0.0  
3번째 - 기능 추가  
4번째 - 버그 수정  

0.0.0.1  
- pypi 테스트

0.0.0.2  
- test code test

0.0.0.3  
- db adaper  

0.0.0.4  
- logger  

0.0.0.5  
- scheduler  

0.0.0.5  
- scheduler
0.0.0.6  == 0.0.1.0
- check_delete_insert_df

0.0.1.1
- check_delete_insert_df
- 위험성 감소
 
0.0.1.2
- info console 추가
- 간단히 info만 확인하는 용으로 사용

0.0.1.3
- DB handler에서 db 연결부분 분리 - psycopg2를 사용하여 재정의
- 로그 이중 발생 문제 해결 
- https://stackoverflow.com/questions/18900888/how-to-turn-sqlalchemy-logging-off-completely

0.0.1.4
- check_delete_insert_df에서 많은 로그가 보이는 걸 조절
- DBAdapter에서 logger level 추가 

0.0.1.5
- check_delete_insert_df 로그에 \n 추가

0.0.2.0
- check_delete_insert_df log level -> debug
- api client

0.0.2.1
- db handler에서 연결 방식을 sqlalchemy 으로 변경