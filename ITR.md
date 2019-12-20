# 통합 테스트 보고서 (Integration Test Report)
## Test 1
### 설명
단어 추가 후 프로그램 종료, 프로그램 다시 실행
### 결과
처음에는 단어가 불러와지지만, 이후 단어가 불러와지지 않는 버그 발생.

## Test 2
### 설명
다음 사전에서 단어의 뜻과 예문이 정상적으로 불러와지는지, 이것이 잘 표시되는지
### 결과
통과 

## Test 3
### 설명
단어의 '집중 단어'설정 변경이 잘 이루어지는지
### 결과
통과

## Test 4
### 설명
단어 리스트 정렬
### 결과
잘 이루어지나, 영어 정렬의 경우 대문자가 소문자보다 먼저 나오는 버그 발견

## Test 5
### 설명
설정 저장 및 불러오기, 적용
### 결과
설정은 잘 저장되고, 불러와지며, 적용된다.

## Test 6
### 설명
푸시 알림 테스트
### 결과
설정한 topic에, 설정한 시간 간격 사이에 푸시 알림을 보냄. 성공.

## 총평
### 미흡했던 구현을 수정한 결과, 원인 모를 버그들이 등장함. 따라서 발표 시에 활용한, 작동이 잘 되는 버전 또한 등록하기로 함.