# RSS 2027 원고 검토 인계

2026-11-14 기준. Dongjun Lee 교수님의 기존 원고 코멘트를 참고하여 문법, 용어, 설명의 명확성을 검토한 뒤 남은 항목을 정리했다. 아래 제안은 교수님의 새로운 코멘트가 아니다.

## 현재 상태

- 메인 원고는 `root.tex`, 본문은 `sections/01_introduction.tex`부터 `sections/05_sequence_planning.tex`까지다.
- 최신 `root.pdf`는 총 6페이지다. 최신 컴파일에서 undefined reference 및 overfull 경고가 없었다.
- 아래 본문 검토 항목은 반영 완료했다. 현재는 교수님께 공유할 원고이며, 사용자가 최종 PDF 상태를 확인했다. 제출용 템플릿 정리는 추후로 보류한다.
- `.ref/rss2027-review-remaining.md`에는 이전 논의가 누적되어 있지만 `.ref`는 현재 Git ignore 대상이다. 다른 작업환경에서 필요한 최신 내용은 이 문서에 정리했다.

## 검토 항목별 처리 상태

### 1. Introduction의 문장 주어 — 반영 완료

파일 `sections/01_introduction.tex`, 첫 문단.

`Without such support, a freestanding structure of n irregular objects must approximate a prescribed target shape ...`로 수정하여 형상을 근사하고 평형을 유지하는 주체를 구조물로 명시했다.

### 2. MCTS 기호 정의 — 반영 완료

파일 `sections/03_overview.tex`와 `sections/05_sequence_planning.tex`.

- MDP 정의에서 `gamma`를 discount factor로 명시했다.
- Leaf value 식의 `\depth_{\node}`를 추정에 포함되는 미래 placement 수로 정의하고, remaining search depth와 inventory에 의해 제한된다는 설명을 유지했다.
- Action Selection에서 `\node_a`가 root action `a`로 도달하는 child임을 명시했다.
- PUCT 식 앞에서 부모 `\node_p`, action `a`, 자식 `\node`의 관계를 정의하고, `P(\node_p,a)`가 action prior임을 명시했다.
- 수정 후 컴파일은 총 6페이지다.

### 3. G(a)의 경로 범위 — 코드 확인 및 반영 완료

파일 `sections/05_sequence_planning.tex`, Action Selection and Tree Reuse.

- stacking-apps의 `search/mcts/search.py`에 있는 `_deepest_feasible_return`과 `_final_select`를 확인했다. 각 root action의 subtree 안에서 최대 평가 깊이를 우선하고, 같은 깊이의 실행 가능한 경로 중 최대 discounted return을 사용한다. 서로 다른 root action 사이에 최대 깊이를 우선하는 규칙은 아니다.
- 경로가 root action `a`부터 시작하며 search horizon 안에 있음을 명시했다. 실제 관측 보상 `r_{\node}`를 합산하고 heuristic leaf estimate `\hat V`는 제외한다.
- 모호한 `root-only paths are eligible` 대신 후속 feasible 경로가 없으면 `G(a)=r_{\node_a}`라고 명시했다.
- 과거 참고 문서의 SHORT/LONG simulation 및 G_val 설명은 복원하지 않는다.

### 4. 압축된 표현의 명확성 — 반영 완료

- `sections/05_sequence_planning.tex`의 `elite selection`을 `top-scoring proposals`로 바꿨다.
- `sections/02_related_works.tex`의 BODex 설명은 coarse 단계의 finite differences와 fine 단계에서 link-frame contact coordinates를 고정한 미분을 구분하도록 수정했다. World-frame contact point 자체를 고정한다는 의미로 쓰지 않는다.

### 5. 제출용 정리 — 교수님 공유 단계에서는 보류

- 사용자는 현재 교수님께만 보낼 예정이므로 제출용 템플릿은 그대로 두기로 했다.
- 실제 제출 전에는 `root.tex`의 Paper-ID placeholder, 빈 `Acknowledgments` 제목, 템플릿 PDF 메타데이터(`Homer Simpson`, 임시 제목 등)를 정리한다. 메타데이터는 본문에 표시되지 않지만 Paper-ID와 빈 제목은 표시된다.
- 최신 빌드는 총 6페이지이며 사용자가 최종 PDF 상태를 확인했다. 추가 본문 수정 시에는 페이지 수를 다시 확인한다. 분량 여유가 작다.

## 이번 논의에서 반영한 사항

- Initial Pose Sampling의 `volume bias`를 큰 부피의 물체에 더 많은 proposal attempts를 배정한다는 설명으로 수정했다. 로컬 구현 요약에는 volume-proportional allocation과 per-stone attempt cap이 명시되어 있다. 본문은 배정 방향과 역할을 간결하게 설명한다.
- 제목을 `Automated Stacking of Irregularly Shaped Stones via GPU-Accelerated Pose Optimization and Monte Carlo Tree Search`로 수정했다.
- Introduction 두 번째 문단의 방법 소개 끝에 Figure 2 참조를 넣고 뒤쪽 GPU 문단의 중복 참조를 삭제했다.
- Friction cone 설명에서 scalar function과 inequality constraint를 구분하고 단복수 오류 및 반복된 `where`를 수정했다.
- `Upper-Level Optimization on SE(3)` 소제목과 Riemannian trust-region/BFGS 문장을 정리했다.
- Physical objective의 세 항을 static equilibrium residuals, contact complementarity 위반, 큰 contact forces에 대한 penalty로 명확하게 설명했다.
- Reward 표현을 `domain-specific`으로 통일했다.
- Progressive widening은 방문 누적에 따라 candidate placement 집합을 확장한다는 문장과 인용으로 설명한다. 본문에서는 non-root 구분과 root의 CEM 세부를 생략하기로 논의했다. 상세 구현 설명에서 적용 범위를 다룬다.
- Batched Selection 첫머리는 `We follow evaluated, feasible children using PUCT to select nodes for batched expansion.`으로 바꿨다. 배치 구성 동작을 먼저 설명하고 그림의 색 경로와 expansion requests를 연결하며, 뒤의 중복 selection 설명은 삭제했다.
- Reservations가 widening allowance를 증가시키지 않는다는 설명을 유지했다.
- Simulation의 `fixed duration`을 `fixed time duration`으로 수정했다.
- 사용자가 disturbance 이후의 성공 조건을 확인했다. Trial은 disturbance 이전의 settled successor를 기준으로 허용 변위 안에서 다시 정지해야 한다. 이에 따라 `settle again without exceeding prescribed displacement limits relative to s'`로 설명했다.
- Section 5 도입은 현재 배치가 이후 배치에 미치는 영향을 고려하는 MCTS 탐색과 병렬 평가를 설명한다. 실행·재계획 설명은 Action Selection and Tree Reuse로 옮겨, 선택한 배치를 실행하고 관측된 successor를 새 root로 삼는다고 명시했다.
- Simulation의 정지 조건은 `requires a minimum time duration and sustained low kinetic energy`로 정리했다. 구현 세부인 `mass-normalized`와 정의가 모호한 `invalid contacts`는 본문에서 생략했다. 코드의 contact validation은 허용치를 넘는 침투 및 지지 접촉 수 부족을 검사하며, 코드 자체는 변경하지 않았다.
- Reward Design 첫머리에 `We define the reward function used to evaluate placements in MCTS.`를 추가했다. 보상식 도입에서는 normalization scales를 가중치에 흡수한다는 구현 설명을 생략하고 `For feasible transitions, the reward is defined as`로 정리했다.
- MCTS 비교 그림의 별도 본문 해설은 분량 제한을 고려해 추가하지 않기로 했다. 비교 조건과 결과는 기존 캡션으로 전달한다.

## 후속 작업 범위

이번에 합의한 본문 수정은 완료했다. 제출용 정리는 현재 작업 범위에서 보류한다. Progressive widening의 수치 설정이나 CEM 설명을 본문에 늘리는 방향은 이번 논의에서 채택하지 않았다. 코드 및 실험 결과를 새로 확인하지 않은 상태에서 성능 우위나 안정성 보장을 추가하지 않는다.

이번 갱신은 검토 문서에 완료 사항과 보류 결정을 기록하는 작업이다. 커밋은 별도 요청 시 진행한다.
