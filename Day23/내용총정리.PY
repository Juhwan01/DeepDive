import pandas as pd
import numpy as np
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (BaggingClassifier, RandomForestClassifier, 
                             VotingClassifier, ExtraTreesClassifier)
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report
import warnings
warnings.filterwarnings('ignore')

print("와인 품질 예측 시스템 - 결정트리 vs 앙상블 모델 비교")
print("=" * 60)

# 1. 데이터 로드 및 전처리
wine = load_wine()
X, y = wine.data, wine.target

# 이진 분류로 변환 (고품질 vs 일반품질)
y_binary = (y >= 1).astype(int)

X_train, X_test, y_train, y_test = train_test_split(
    X, y_binary, test_size=0.3, random_state=42, stratify=y_binary
)

print(f"데이터 정보:")
print(f"   전체 샘플 수: {len(X)}")
print(f"   특성 수: {X.shape[1]}")
print(f"   훈련 데이터: {len(X_train)}, 테스트 데이터: {len(X_test)}")
print(f"   고품질 와인 비율: {y_binary.mean():.2%}")

# 2. 지니불순도 계산 함수

def calculate_gini_impurity(y):
    if len(y) == 0:
        return 0
    
    from collections import Counter
    counts = Counter(y)
    impurity = 1.0
    
    for count in counts.values():
        probability = count / len(y)
        impurity -= probability ** 2
    
    return impurity

print(f"\n1단계: 지니불순도 계산")
print("-" * 40)
print(f"전체 데이터 지니불순도: {calculate_gini_impurity(y_train):.3f}")
print(f"클래스 0만 있을 때 지니불순도: {calculate_gini_impurity([0]*10):.3f}")
print(f"클래스가 균등 분포일 때 지니불순도: {calculate_gini_impurity([0]*5 + [1]*5):.3f}")

# 3. 단일 결정트리 분석 (과적합 vs 규제)
print(f"\n2단계: 단일 결정트리 분석")
print("-" * 40)

# 과적합된 결정트리
tree_overfit = DecisionTreeClassifier(random_state=42)
tree_overfit.fit(X_train, y_train)

# 규제된 결정트리 (규제 파라미터 활용)
tree_regularized = DecisionTreeClassifier(
    max_depth=5, 
    min_samples_leaf=10, 
    min_samples_split=20,
    random_state=42
)
tree_regularized.fit(X_train, y_train)

print(f"과적합 트리:")
print(f"   훈련 정확도: {accuracy_score(y_train, tree_overfit.predict(X_train)):.3f}")
print(f"   테스트 정확도: {accuracy_score(y_test, tree_overfit.predict(X_test)):.3f}")
print(f"   트리 깊이: {tree_overfit.get_depth()}")

print(f"규제된 트리:")
print(f"   훈련 정확도: {accuracy_score(y_train, tree_regularized.predict(X_train)):.3f}")
print(f"   테스트 정확도: {accuracy_score(y_test, tree_regularized.predict(X_test)):.3f}")
print(f"   트리 깊이: {tree_regularized.get_depth()}")

# 4. 배깅과 OOB 평가
print(f"\n3단계: 배깅과 OOB 평가")
print("-" * 40)

bagging_clf = BaggingClassifier(
    DecisionTreeClassifier(max_depth=5),
    n_estimators=100,
    oob_score=True,  # OOB 평가
    random_state=42
)
bagging_clf.fit(X_train, y_train)

print(f"배깅 분류기:")
print(f"   OOB 점수: {bagging_clf.oob_score_:.3f}")
print(f"   테스트 정확도: {accuracy_score(y_test, bagging_clf.predict(X_test)):.3f}")

# 5. 랜덤 포레스트와 특성 중요도
print(f"\n4단계: 랜덤 포레스트와 특성 중요도")
print("-" * 40)

rf_clf = RandomForestClassifier(
    n_estimators=100,
    max_depth=5,
    max_features='sqrt',  # 특성 선택
    oob_score=True,
    random_state=42
)
rf_clf.fit(X_train, y_train)

print(f"랜덤 포레스트:")
print(f"   OOB 점수: {rf_clf.oob_score_:.3f}")
print(f"   테스트 정확도: {accuracy_score(y_test, rf_clf.predict(X_test)):.3f}")

# 특성 중요도 분석 (feature_importances_)
feature_importance = rf_clf.feature_importances_
feature_names = wine.feature_names

print(f"\n특성 중요도 Top 5:")
top_indices = np.argsort(feature_importance)[-5:][::-1]
for i, idx in enumerate(top_indices, 1):
    print(f"   {i}. {feature_names[idx]}: {feature_importance[idx]:.3f}")

# 6. 투표식 분류기 (직접투표 vs 간접투표)
print(f"\n5단계: 투표식 분류기")
print("-" * 40)

# 직접 투표 (hard voting)
voting_hard = VotingClassifier(
    estimators=[
        ('tree', tree_regularized),
        ('rf', rf_clf),
        ('svm', SVC(random_state=42))
    ],
    voting='hard'
)
voting_hard.fit(X_train, y_train)

# 간접 투표 (soft voting) - 확률 기반
voting_soft = VotingClassifier(
    estimators=[
        ('tree', tree_regularized),
        ('rf', rf_clf),
        ('svm', SVC(probability=True, random_state=42)),
        ('lr', LogisticRegression(random_state=42, max_iter=1000))
    ],
    voting='soft'
)
voting_soft.fit(X_train, y_train)

print(f"투표식 분류기 (직접 투표): {accuracy_score(y_test, voting_hard.predict(X_test)):.3f}")
print(f"투표식 분류기 (간접 투표): {accuracy_score(y_test, voting_soft.predict(X_test)):.3f}")

# 7. 모든 모델 성능 비교
print(f"\n6단계: 전체 모델 성능 비교")
print("-" * 40)

models = {
    '단일 결정트리 (과적합)': tree_overfit,
    '단일 결정트리 (규제)': tree_regularized,
    '배깅': bagging_clf,
    '랜덤 포레스트': rf_clf,
    '투표식 (직접)': voting_hard,
    '투표식 (간접)': voting_soft
}

results = []
for name, model in models.items():
    # 교차 검증
    cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='accuracy')
    test_score = accuracy_score(y_test, model.predict(X_test))
    
    results.append({
        '모델': name,
        'CV 평균': cv_scores.mean(),
        'CV 표준편차': cv_scores.std(),
        '테스트 정확도': test_score
    })

# 결과 출력
for result in results:
    print(f"{result['모델']:20s}: CV={result['CV 평균']:.3f}(±{result['CV 표준편차']:.3f}), "
          f"Test={result['테스트 정확도']:.3f}")

# 8. 편향-분산 트레이드오프 확인
print(f"\n7단계: 편향-분산 트레이드오프 분석")
print("-" * 40)

single_tree_cv_std = [r for r in results if '단일 결정트리 (규제)' in r['모델']][0]['CV 표준편차']
ensemble_cv_std = [r for r in results if '랜덤 포레스트' in r['모델']][0]['CV 표준편차']

print(f"단일 결정트리 분산 (CV 표준편차): {single_tree_cv_std:.3f}")
print(f"랜덤 포레스트 분산 (CV 표준편차): {ensemble_cv_std:.3f}")
print(f"분산 감소 효과: {((single_tree_cv_std - ensemble_cv_std) / single_tree_cv_std * 100):.1f}%")

# 9. 예측 확률 분석 (predict_proba 개념)
print(f"\n8단계: 예측 확률 분석")
print("-" * 40)

sample_wine = X_test[:3]
true_labels = y_test[:3]

print("샘플 3개에 대한 각 모델의 예측 확률:")
for i in range(3):
    print(f"\n샘플 {i+1} (실제: {'고품질' if true_labels[i] == 1 else '일반품질'}):")
    
    # 확률을 제공하는 모델들만
    prob_models = {
        '랜덤 포레스트': rf_clf,
        '투표식 (간접)': voting_soft
    }
    
    for name, model in prob_models.items():
        if hasattr(model, 'predict_proba'):
            proba = model.predict_proba(sample_wine[i:i+1])[0]
            prediction = model.predict(sample_wine[i:i+1])[0]
            print(f"   {name:15s}: 예측={'고품질' if prediction == 1 else '일반품질'}, "
                  f"확률=[{proba[0]:.2f}, {proba[1]:.2f}]")

# 10. 최종 결론
print(f"\n9단계: 최종 분석")
print("-" * 40)

best_result = max(results, key=lambda x: x['테스트 정확도'])
print(f"최고 성능 모델: {best_result['모델']}")
print(f"테스트 정확도: {best_result['테스트 정확도']:.3f}")

print(f"\n주요 발견사항:")
single_tree_acc = [r for r in results if '단일 결정트리 (규제)' in r['모델']][0]['테스트 정확도']
rf_acc = [r for r in results if '랜덤 포레스트' in r['모델']][0]['테스트 정확도']
print(f"   1. 앙상블 vs 단일 모델 성능 향상: +{(rf_acc - single_tree_acc)*100:.1f}%p")
print(f"   2. 과적합 방지: 규제된 트리가 더 안정적")
print(f"   3. OOB 평가: 별도 검증 세트 없이도 성능 추정 가능")
print(f"   4. 특성 중요도: {feature_names[top_indices[0]]}가 가장 중요")

print(f"\n학습 내용 확인:")
print(f"   - 지니불순도 계산 및 이해")
print(f"   - 결정트리 규제 파라미터 효과")
print(f"   - 배깅의 분산 감소 효과")
print(f"   - OOB 평가의 실용성")
print(f"   - 랜덤 포레스트의 성능 향상")
print(f"   - 투표식 분류기의 직접/간접 투표 차이")
print(f"   - 특성 중요도를 통한 모델 해석")
print(f"   - 편향-분산 트레이드오프 확인")