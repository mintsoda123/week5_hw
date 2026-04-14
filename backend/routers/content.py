from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import os

from database import get_db
import models
import schemas
from auth import get_current_user

router = APIRouter(prefix="/content", tags=["content"])

FREE_USAGE_LIMIT = int(os.getenv("FREE_USAGE_LIMIT", "5"))

# Week 5 딥러닝 컨텐츠 데이터
SECTIONS = [
    {
        "id": "regularization",
        "title": "🛡️ 1. Regularization (규제)",
        "description": "과적합을 방지하는 핵심 기법들을 학습합니다",
        "content": """## Regularization이란?

모델이 훈련 데이터에 과도하게 맞춰져서(Overfitting) 새로운 데이터에 대한 성능이 떨어지는 것을 막기 위한 기법들입니다.

### L1/L2 Regularization
- **L1**: 가중치의 절대값 합을 손실 함수에 추가 → 일부 가중치를 0으로 만들어 희소성(Sparsity) 유도
- **L2**: 가중치의 제곱 합을 손실 함수에 추가 → 가중치를 전반적으로 작게 만듦

### Dropout
학습 시 무작위로 일부 뉴런을 꺼버려서(0으로 만듦) 특정 뉴런에 의존하는 것을 방지합니다.
- 매 학습 배치마다 다른 뉴런이 비활성화됩니다
- 앙상블 효과를 가져옵니다

### Batch Normalization
각 층의 입력을 정규화(평균 0, 분산 1)하여 학습을 안정화하고 속도를 높입니다.
- Internal Covariate Shift 문제를 해결합니다
- 학습률을 높게 설정할 수 있습니다

### 결과 해석
- **None**: 규제 없을 때 검증 손실이 훈련 손실보다 높아짐 (과적합)
- **Dropout/L2**: 검증 손실이 안정적으로 유지됨""",
        "code_example": """import tensorflow as tf
from tensorflow.keras import layers, regularizers

# L2 Regularization
model_l2 = tf.keras.Sequential([
    layers.Dense(256, activation='relu',
                 kernel_regularizer=regularizers.l2(0.001)),
    layers.Dense(128, activation='relu',
                 kernel_regularizer=regularizers.l2(0.001)),
    layers.Dense(1, activation='sigmoid')
])

# Dropout
model_dropout = tf.keras.Sequential([
    layers.Dense(256, activation='relu'),
    layers.Dropout(0.3),  # 30% 뉴런 무작위 비활성화
    layers.Dense(128, activation='relu'),
    layers.Dropout(0.3),
    layers.Dense(1, activation='sigmoid')
])

# Batch Normalization
model_bn = tf.keras.Sequential([
    layers.Dense(256),
    layers.BatchNormalization(),
    layers.Activation('relu'),
    layers.Dense(128),
    layers.BatchNormalization(),
    layers.Activation('relu'),
    layers.Dense(1, activation='sigmoid')
])""",
        "result_description": "규제 기법 적용 시 검증 손실(Validation Loss)이 훈련 손실과 비슷한 수준을 유지합니다."
    },
    {
        "id": "overfitting",
        "title": "⚖️ 2. Overfitting vs Underfitting",
        "description": "모델 복잡도와 성능의 관계를 이해합니다",
        "content": """## Overfitting vs Underfitting

### Underfitting (과소적합)
모델이 너무 단순해서 데이터의 패턴을 제대로 학습하지 못한 상태입니다.
- 훈련 데이터에서도 성능이 낮습니다
- 바이어스(Bias)가 높습니다
- 해결책: 모델 복잡도 증가, 더 많은 특성 사용

### Overfitting (과적합)
모델이 너무 복잡해서 훈련 데이터의 노이즈까지 학습해버린 상태입니다.
- 훈련 데이터에서는 성능이 매우 좋지만 테스트 데이터에서는 성능이 낮습니다
- 분산(Variance)이 높습니다
- 해결책: Regularization, 데이터 증강, 조기 종료(Early Stopping)

### Balanced (적절한 모델)
모델의 복잡도가 데이터에 적절하여 일반화 성능이 좋은 상태입니다.
- 훈련 손실과 검증 손실이 비슷합니다
- 바이어스-분산 트레이드오프를 잘 맞춘 상태입니다

### 학습 곡선으로 진단하기
- Overfit 모델: 훈련 손실 ↓, 검증 손실 ↑ (큰 gap)
- Underfit 모델: 훈련 손실과 검증 손실 모두 높음
- 적절한 모델: 두 손실 모두 낮고 비슷함""",
        "code_example": """import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import Ridge

# 데이터 생성
np.random.seed(42)
X = np.linspace(0, 2*np.pi, 30).reshape(-1, 1)
y = np.sin(X).ravel() + np.random.normal(0, 0.2, 30)

# Underfitting (degree=1), Balanced (degree=4), Overfitting (degree=15)
for degree, label in [(1, 'Underfit'), (4, 'Balanced'), (15, 'Overfit')]:
    poly = PolynomialFeatures(degree=degree)
    X_poly = poly.fit_transform(X)

    model = Ridge(alpha=0.001)
    model.fit(X_poly, y)

    print(f"{label} (degree={degree}): 훈련 R² = {model.score(X_poly, y):.3f}")""",
        "result_description": "Overfit 모델은 훈련 데이터 점들을 지나치게 구불구불하게 따라가며, 검증 손실이 매우 높습니다."
    },
    {
        "id": "data_augmentation",
        "title": "🖼️ 3. Data Augmentation (데이터 증강)",
        "description": "데이터 부족 문제를 해결하는 이미지 증강 기법",
        "content": """## Data Augmentation이란?

데이터가 부족할 때, 기존 이미지를 다양하게 변형하여 데이터의 양과 다양성을 늘리는 기법입니다.

### 왜 필요한가?
- 딥러닝 모델은 대량의 데이터를 필요로 합니다
- 실제로는 데이터 수집이 어렵거나 비용이 많이 듭니다
- 증강을 통해 같은 이미지에서 다양한 학습 데이터를 생성할 수 있습니다

### 주요 증강 기법
1. **Random Flip**: 좌우/상하 뒤집기
2. **Random Rotation**: 임의 각도 회전
3. **Random Zoom**: 확대/축소
4. **Random Brightness/Contrast**: 밝기/대비 조절
5. **Random Crop**: 임의 영역 자르기
6. **Cutout/Mixup**: 고급 증강 기법

### 언제 사용해야 하는가?
- 학습 데이터가 부족할 때
- 모델이 특정 위치/방향에 과적합될 때
- 모델의 일반화 성능을 높이고 싶을 때

### 주의사항
증강은 학습 데이터에만 적용하고, 검증/테스트 데이터에는 적용하지 않습니다.""",
        "code_example": """import tensorflow as tf
from tensorflow.keras import layers
import matplotlib.pyplot as plt

# 데이터 증강 레이어 정의
data_augmentation = tf.keras.Sequential([
    layers.RandomFlip("horizontal_and_vertical"),
    layers.RandomRotation(0.2),          # ±20% 회전
    layers.RandomZoom(0.2),              # ±20% 줌
    layers.RandomBrightness(0.2),        # 밝기 조절
    layers.RandomContrast(0.2),          # 대비 조절
])

# 모델에 증강 레이어 포함
model = tf.keras.Sequential([
    data_augmentation,                   # 학습 시에만 적용
    layers.Conv2D(32, (3, 3), activation='relu'),
    layers.MaxPooling2D(),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D(),
    layers.Flatten(),
    layers.Dense(64, activation='relu'),
    layers.Dense(10, activation='softmax')
])

# 증강 효과 시각화
def visualize_augmentation(image, augmentation_layer):
    plt.figure(figsize=(10, 10))
    for i in range(9):
        augmented = augmentation_layer(tf.expand_dims(image, 0))
        plt.subplot(3, 3, i + 1)
        plt.imshow(augmented[0].numpy().astype('uint8'))
        plt.axis('off')
    plt.show()""",
        "result_description": "하나의 이미지가 회전, 뒤집기, 확대/축소를 통해 다양한 형태로 변형됩니다."
    },
    {
        "id": "transfer_learning",
        "title": "🧠 4. Transfer Learning (전이 학습)",
        "description": "사전 학습된 모델의 지식을 활용하는 방법",
        "content": """## Transfer Learning이란?

이미 대량의 데이터(예: ImageNet 1.2M 장)로 학습된 모델의 지식을 가져와서, 내가 가진 적은 데이터의 문제 해결에 활용하는 방법입니다.

### 핵심 개념

#### Feature Extraction (특성 추출)
사전 학습된 모델의 합성곱 층(Convolutional Base)을 **고정(Freeze)**하고,
내 데이터에 맞는 분류기(Classifier)만 새로 학습합니다.
- 빠른 학습 속도
- 적은 데이터로도 좋은 성능
- 새 층만 학습하므로 GPU 메모리 효율적

#### Fine-tuning (미세 조정)
사전 학습된 모델의 상위 층(도메인 특화된 특성)도 함께 미세하게 학습합니다.
- Feature Extraction보다 높은 성능 가능
- 충분한 데이터 필요
- 작은 학습률 사용 (기존 지식 망각 방지)

### 주요 사전 학습 모델
| 모델 | 파라미터 | 특징 |
|------|---------|------|
| MobileNetV2 | 3.4M | 모바일/엣지 최적화 |
| ResNet50 | 25.6M | 잔차 연결, 안정적 |
| EfficientNetB0 | 5.3M | 최고 효율성 |
| VGG16 | 138M | 간단한 구조 |

### 언제 사용하는가?
- 데이터가 적을 때 (수백 ~ 수천 장)
- ImageNet과 유사한 도메인 (자연 이미지)
- 빠른 프로토타입이 필요할 때""",
        "code_example": """import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras import layers, models

# 1. 사전 학습된 MobileNetV2 불러오기
base_model = MobileNetV2(
    input_shape=(224, 224, 3),
    include_top=False,          # 분류 레이어 제거
    weights='imagenet'          # ImageNet 가중치 사용
)

# 2. Feature Extraction: 기본 층 고정 (Freeze)
base_model.trainable = False

# 3. 새로운 분류기 추가
model = models.Sequential([
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.Dense(128, activation='relu'),
    layers.Dropout(0.5),
    layers.Dense(10, activation='softmax')   # 10개 클래스 분류
])

# 4. 컴파일
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

print(f"전체 파라미터: {model.count_params():,}")
print(f"학습 가능 파라미터: {sum([tf.size(w).numpy() for w in model.trainable_weights]):,}")

# 5. Fine-tuning (선택): 상위 30개 층 학습 활성화
base_model.trainable = True
fine_tune_at = len(base_model.layers) - 30
for layer in base_model.layers[:fine_tune_at]:
    layer.trainable = False

# 작은 학습률로 재컴파일
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=1e-5),  # 매우 작은 학습률
    loss='categorical_crossentropy',
    metrics=['accuracy']
)""",
        "result_description": "MobileNetV2 기반 모델 구조에서 학습 가능한 파라미터가 전체의 극히 일부임을 확인할 수 있습니다."
    },
    {
        "id": "mnist_cnn",
        "title": "✍️ 5. MNIST CNN 실습",
        "description": "CNN으로 손글씨 숫자를 인식하는 모델을 구현합니다",
        "content": """## MNIST CNN 실습

### CNN (Convolutional Neural Network)이란?
이미지 처리에 특화된 딥러닝 구조로, 이미지의 공간적 구조를 활용합니다.

### 핵심 레이어

#### Conv2D (합성곱 레이어)
이미지에서 특징(Edge, 텍스처, 패턴 등)을 추출합니다.
- 작은 필터(커널)가 이미지 전체를 슬라이딩하며 특성맵(Feature Map) 생성
- 파라미터 공유로 효율적인 학습

#### MaxPooling2D (최대 풀링)
특성맵의 크기를 줄이면서 가장 중요한 특징만 남깁니다.
- 공간적 불변성(Translation Invariance) 제공
- 과적합 방지, 연산량 감소

#### Flatten & Dense (완전 연결층)
추출된 특징을 1D로 펼쳐서 최종 분류를 수행합니다.

### MNIST 데이터셋
- 0~9 손글씨 숫자 이미지
- 훈련: 60,000장, 테스트: 10,000장
- 이미지 크기: 28×28 픽셀, 흑백

### 모델 구조
```
Input (28, 28, 1)
→ Conv2D(32, 3×3) → (26, 26, 32)
→ MaxPooling2D → (13, 13, 32)
→ Conv2D(64, 3×3) → (11, 11, 64)
→ MaxPooling2D → (5, 5, 64)
→ Conv2D(64, 3×3) → (3, 3, 64)
→ Flatten → (576,)
→ Dense(64)
→ Dense(10, softmax) → 10개 클래스
```""",
        "code_example": """import tensorflow as tf
from tensorflow.keras import layers, models
import matplotlib.pyplot as plt
import numpy as np

# 1. 데이터 로드 및 전처리
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
x_train = x_train.reshape(-1, 28, 28, 1).astype('float32') / 255.0
x_test = x_test.reshape(-1, 28, 28, 1).astype('float32') / 255.0

# 2. CNN 모델 구성
model = models.Sequential([
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.Flatten(),
    layers.Dense(64, activation='relu'),
    layers.Dense(10, activation='softmax')
])

# 3. 모델 요약
model.summary()

# 4. 컴파일
model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

# 5. 학습
history = model.fit(
    x_train, y_train,
    epochs=10,
    validation_split=0.1,
    batch_size=128,
    callbacks=[
        tf.keras.callbacks.EarlyStopping(patience=3, restore_best_weights=True)
    ]
)

# 6. 평가
test_loss, test_acc = model.evaluate(x_test, y_test)
print(f'테스트 정확도: {test_acc:.4f}')  # 보통 99% 이상

# 7. 예측 시각화
predictions = model.predict(x_test[:5])
for i in range(5):
    print(f"실제: {y_test[i]}, 예측: {np.argmax(predictions[i])}")""",
        "result_description": "CNN 모델은 약 10 에폭 학습 후 MNIST 테스트 데이터에서 99% 이상의 정확도를 달성합니다."
    }
]


@router.get("/", response_model=list)
def get_content_list(current_user: models.User = Depends(get_current_user)):
    """모든 섹션 목록 반환 (상세 내용 제외)"""
    return [
        {
            "id": s["id"],
            "title": s["title"],
            "description": s["description"],
        }
        for s in SECTIONS
    ]


@router.get("/{section_id}", response_model=schemas.SectionContent)
def get_section(
    section_id: str,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """섹션 내용 반환 (사용량 추적)"""
    section = next((s for s in SECTIONS if s["id"] == section_id), None)
    if not section:
        raise HTTPException(status_code=404, detail="섹션을 찾을 수 없습니다.")

    # 이미 열람한 섹션인지 확인
    existing_log = db.query(models.UsageLog).filter(
        models.UsageLog.user_id == current_user.id,
        models.UsageLog.section_id == section_id
    ).first()

    if not existing_log:
        # 처음 보는 섹션 - 사용량 체크
        if not current_user.is_premium and current_user.usage_count >= FREE_USAGE_LIMIT:
            raise HTTPException(
                status_code=402,
                detail={
                    "message": "무료 사용 횟수를 초과했습니다. 프리미엄으로 업그레이드하세요.",
                    "usage_count": current_user.usage_count,
                    "free_limit": FREE_USAGE_LIMIT
                }
            )
        # 사용량 기록
        log = models.UsageLog(user_id=current_user.id, section_id=section_id)
        db.add(log)
        current_user.usage_count += 1
        db.commit()

    return section


@router.get("/usage/status", response_model=schemas.UsageStatus)
def get_usage_status(current_user: models.User = Depends(get_current_user)):
    """현재 사용량 상태 반환"""
    remaining = max(0, FREE_USAGE_LIMIT - current_user.usage_count)
    return {
        "usage_count": current_user.usage_count,
        "free_limit": FREE_USAGE_LIMIT,
        "is_premium": current_user.is_premium,
        "remaining": remaining if not current_user.is_premium else 999,
        "can_access": current_user.is_premium or current_user.usage_count < FREE_USAGE_LIMIT
    }


@router.post("/usage/reset")
def reset_usage(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    """사용량 초기화 (테스트용)"""
    db.query(models.UsageLog).filter(models.UsageLog.user_id == current_user.id).delete()
    current_user.usage_count = 0
    db.commit()
    return {"message": "사용량이 초기화되었습니다."}
