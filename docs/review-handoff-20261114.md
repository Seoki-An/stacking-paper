# RSS 2027 원고 검토 인계

2026-11-14 기준. Dongjun Lee 교수님의 기존 원고 코멘트를 참고하여 문법, 용어, 설명의 명확성을 검토한 뒤 남은 항목을 정리했다. 아래 제안은 교수님의 새로운 코멘트가 아니다.

## 현재 상태

- 메인 원고는 `root.tex`, 본문은 `sections/01_introduction.tex`부터 `sections/05_sequence_planning.tex`까지다.
- 최신 `root.pdf`는 총 6페이지다. 최신 컴파일에서 undefined reference 및 overfull 경고가 없었다.
- 현재 원고를 기준으로 아래 미완료 항목을 검토한다. 정의가 불명확한 알고리즘 동작은 실제 실행 코드에서 확인한 후 반영한다.
- `.ref/rss2027-review-remaining.md`에는 이전 논의가 누적되어 있지만 `.ref`는 현재 Git ignore 대상이다. 다른 작업환경에서 필요한 최신 내용은 이 문서에 정리했다.

## 남은 수정과 확인

### 1. Introduction의 문장 주어

파일 `sections/01_introduction.tex`, 첫 문단.

현재 문구는 `freestanding stacking of n irregular objects must approximate a prescribed target shape`다. 형상을 근사하고 평형을 유지하는 주체를 구조물로 쓰면 더 정확하다.

제안 문구는 `Without such support, a freestanding structure of n irregular objects must approximate a prescribed target shape ...`다. 이 수정은 아직 적용하지 않았다.

### 2. MCTS 기호 정의 — 반영 완료

파일 `sections/03_overview.tex`와 `sections/05_sequence_planning.tex`.

- MDP 정의에서 `gamma`를 discount factor로 명시했다.
- Leaf value 식의 `\depth_{\node}`를 추정에 포함되는 미래 placement 수로 정의하고, remaining search depth와 inventory에 의해 제한된다는 설명을 유지했다.
- Action Selection에서 `\node_a`가 root action `a`로 도달하는 child임을 명시했다.
- 수정 후 컴파일은 총 6페이지다.

### 3. G(a)의 경로 범위

파일 `sections/05_sequence_planning.tex`, Action Selection and Tree Reuse.

- `deepest evaluated feasible paths below a`에서 deepest가 각 root action 아래의 최대 평가 깊이를 뜻하는지 코드에서 확인한다.
- `root-only paths are eligible`가 root action 하나로 이루어진 경로를 뜻한다면 `single-action paths are eligible`로 바꾸면 더 명확하다. Root 노드만 있는 경로와 혼동될 수 있는 현재 표현을 확인한다.
- 현재 정의는 관측된 discounted return이며 bootstrap을 제외한다. 이 정의와 실제 집계 규칙의 일치를 확인한다.
- 과거 참고 문서의 SHORT/LONG simulation 및 G_val 설명을 현재 원고에 그대로 복원하지 않는다. 최신 실행 코드와 현재 G(a)의 의미를 먼저 대조한다.

### 4. 압축된 표현의 명확성

- `sections/05_sequence_planning.tex`의 `elite selection`은 높은 점수의 후보를 선택하는 역할이 드러나도록 풀어 쓸 수 있다.
- `sections/02_related_works.tex`의 `detached contact points`는 contact point를 미분 중 고정한다는 의미를 전달하도록 검토한다. BODex의 실제 처리 및 기존 finite-difference 설명과 일치시킨다.

### 5. 제출용 정리

- `root.tex`의 `Paper-ID [add your ID here]`를 실제 제출 ID로 교체해야 한다.
- 빈 `Acknowledgments` 제목을 정리해야 한다.
- 수정 후 PDF 페이지 수와 그림 배치를 다시 확인한다. 최근 몇 줄 추가만으로 7페이지가 되는 경우가 있어 분량 여유가 작다.

## 이번 논의에서 반영한 사항

- Initial Pose Sampling의 `volume bias`를 큰 부피의 물체에 더 많은 proposal attempts를 배정한다는 설명으로 수정했다. 로컬 구현 요약에는 volume-proportional allocation과 per-stone attempt cap이 명시되어 있다. 본문은 배정 방향과 역할을 간결하게 설명한다.
- 제목을 `Automated Stacking of Irregularly Shaped Stones via GPU-Accelerated Pose Optimization and Monte Carlo Tree Search`로 수정했다.
- Introduction 두 번째 문단의 방법 소개 끝에 Figure 2 참조를 넣고 뒤쪽 GPU 문단의 중복 참조를 삭제했다.
- Friction cone 설명에서 scalar function과 inequality constraint를 구분하고 단복수 오류 및 반복된 `where`를 수정했다.
- `Upper-Level Optimization on SE(3)` 소제목과 Riemannian trust-region/BFGS 문장을 정리했다.
- Physical objective의 세 항을 static equilibrium residuals, contact complementarity 위반, 큰 contact forces에 대한 penalty로 명확하게 설명했다.
- Reward 표현을 `domain-specific`으로 통일했다.
- Progressive widening은 방문 누적에 따라 candidate placement 집합을 확장한다는 문장과 인용으로 설명한다. 본문에서는 non-root 구분과 root의 CEM 세부를 생략하기로 논의했다. 상세 구현 설명에서 적용 범위를 다룬다.
- `Selection follows evaluated, feasible children using PUCT until a node is chosen for expansion.`을 추가하여 selection과 expansion을 연결했다. 다음 단락의 중복 설명은 합쳤다.
- Reservations가 widening allowance를 증가시키지 않는다는 설명을 유지했다.
- Simulation의 `fixed duration`을 `fixed time duration`으로 수정했다.
- 사용자가 disturbance 이후의 성공 조건을 확인했다. Trial은 disturbance 이전의 settled successor를 기준으로 허용 변위 안에서 다시 정지해야 한다. 이에 따라 `settle again without exceeding prescribed displacement limits relative to s'`로 설명했다.

## 후속 작업 범위

2번의 기호 정의는 반영했다. 1번의 문장 수정은 남아 있으며, 3번은 실제 코드의 경로 집계 규칙과 맞춘다. Progressive widening의 수치 설정이나 CEM 설명을 본문에 늘리는 방향은 이번 논의에서 채택하지 않았다. 코드 및 실험 결과를 새로 확인하지 않은 상태에서 성능 우위나 안정성 보장을 추가하지 않는다.

현재 문서화 단계에서는 위 미완료 항목을 원고에 자동 적용하지 않았다. Git 작업은 로컬 커밋 보관으로 진행한다.
