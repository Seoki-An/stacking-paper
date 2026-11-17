# RSS 2027 1차 제출 논의 인계

작성일: 2026-11-17 (Asia/Seoul)

이 문서는 다른 저장소/새 대화에서 논의를 이어가기 위한 기록이다. **공식 규정, 원고에서 확인한 사실, 조언 및 잠정 평가를 구분**한다. 이 파일만으로 새 저장소의 원고가 동일하다고 가정하지 말고 실제 파일을 확인한다.

## 1. 연구와 사용자 의도

- 논문 제목: **Automated Stacking of Irregularly Shaped Stones via GPU-Accelerated Pose Optimization and Monte Carlo Tree Search**.
- 대상은 **RSS 2027 Stage 1 초기 제출**이다. 최종 완성 논문의 기준을 그대로 적용하면 안 된다.
- 사용자는 최초에 `root.pdf`를 선입견 없이 읽고, TE-SDF (RSS 2026) 및 *Uncertain Pose Estimation during Contact Tasks using Differentiable Contact Features* (RSS 2023)와 비교한 채택 가능성 판단을 요청했다.
- 사용자는 GPU 가속을 의도적으로 제목과 기여에 포함했다. 이를 단순 구현상의 편의로 치부하지 말고, 실제 계산 분해와 병렬화 설계의 기여를 평가해야 한다.
- 사용자가 원한 것은 합격 보장이 아니라, 1차 규정에 맞는 현실적인 평가와 5쪽 안에서 실행 가능한 개선 방향이다.
- sampling 및 reward 설명을 과도하게 줄인 다음 재현성 부족을 지적하는 식의 상충하는 조언을 피한다.

## 2. 공식 출처와 확인 범위

2026-11-17에 FAQ와 CFP 전문을 웹에서 다시 확인했다.

- Author FAQ: https://roboticsconference.org/information/author-faq/
- Call for Papers: https://roboticsconference.org/information/cfp/
- Reviewer Guidelines: https://roboticsconference.org/information/reviewer-guidelines/
- CFP에서 연결한 LaTeX template: https://roboticsconference.org/docs/paper-template-latex.tar.gz

아래 규정은 확인 당시 내용이다. 새 대화에서 변경 여부가 중요한 판단을 할 때는 다시 확인한다. Reviewer Guidelines의 점수 설명은 앞선 대화에서 확인했으나, 11월 17일 관련 연구 구성 판단은 FAQ와 CFP에 근거했다.

### 2.1 Stage 1의 성격과 분량

- Stage 1은 단순 position paper나 연구 아이디어 요약이 아니라 **semi-complete technical research paper**다.
- 구체적인 문제 정의, 검증 가능한 가설, 엄밀하게 정의된 방법론, 얻고자 하는 과학적 통찰이 필요하다.
- CFP는 실험이나 경험적 검증이 없거나 예비 단계일 수 있음을 명시한다. 결과가 미완성이라는 이유만으로 최종 논문 수준의 감점을 해서는 안 된다.
- 수학적 이론 기여만 허용하는 것이 아니다. 시스템 구조와 실험 설계도 가능하며, 그 선택을 이끄는 가설을 명시해야 한다.
- 본문 최대 5쪽 + 참고문헌 1쪽. FAQ 3번은 참고문헌을 exactly 1 page로 표현한다.
- 본문 PDF에 넣는 appendix도 본문 5쪽에 포함된다.
- Stage 1에서는 별도 보충자료를 받지 않고, 외부 웹사이트·영상·코드 저장소의 내용도 심사에 반영하지 않는다. 핵심 평가 근거를 본문 안에 둔다.
- FAQ 6번은 모든 결과와 ablation을 압축하기보다 문제·가설·핵심 방법론에 집중하고, novelty 확립에 직접 필요한 관련 문헌만 다루도록 안내한다.

### 2.2 Extension Charter와 최종 판단

- 초기 심사에서 AC와 리뷰어가 필요한 설명, 평가, 방법론 확장을 Metareview로 제시한다.
- 저자가 rebuttal에서 응답하면 AC가 이를 반영해 최종 Extension Charter를 만든다.
- Charter는 최종 논문을 위해 수행할 실험·증명·검증 등을 구체화하는 요구사항이다.
- 결과나 벤치마크를 많이 추가하는 것 자체가 충족 조건은 아니다. 요구된 질문에 답하는 검증을 충분한 수준으로 수행해야 한다.
- CFP는 Charter 이행과 과학적으로 가치 있는 통찰을 최종 심사에서 확인한다고 설명한다. 실험 목록을 실행하면 자동 채택된다는 뜻은 아니다.
- 성능이 낮은 결과 자체로 탈락시키지는 않지만, 낮은 성능을 보고하는 것만으로 가치 있는 negative result가 되지는 않는다. 실패 원인을 구별하는 엄밀한 실험과 의미 있는 분석이 필요하다.
- 기존에 준비한 실험이 있어도 Charter에 따라 새로운 실험이 필요할 수 있다.

확인 당시 일정:

| 단계 | 날짜 |
| --- | --- |
| 초기 원고 제출 | 2026-12-04, 23:59 AoE |
| 초기 결정: reject 또는 rebuttal 초청 | 2027-02-05 |
| Rebuttal 마감 | 2027-02-12 |
| Reject 또는 Charter 수행 초청 / 확정 Charter | 2027-02-26 |
| 최종 원고 제출 | 2027-04-16 |
| 보충자료 제출 | 2027-04-19 |
| 최종 채택 통보 | 2027-04-30 |

주의: CFP 일정표의 “Decision Stage 2”는 2월 26일의 Charter 수행 초청 결정을 가리킨다. 본문에서 말하는 Stage 2 최종 원고 제출과 혼동하지 않는다.

## 3. 독립 Related Work 섹션이 필수인가?

공식 문구와 해석을 구분한 결론:

1. CFP는 Stage 1 설명에서 `the related work section`이라는 표현을 쓰며, 중심 문제와 novelty에 직접 연결되는 문헌만 인용하도록 안내한다.
2. FAQ 6번도 novelty 확립에 직접 필요한 관련 연구만 압축하라고 한다.
3. **독립된 Related Work 제목, 섹션 번호 또는 특정 배치를 반드시 사용하라는 명시적 규정은 두 문서에 없다.**
4. 반대로 독립 섹션 생략을 명시적으로 허용한다는 문장도 없다. 따라서 “공식적으로 생략 허용이 확인됐다”고 단정하지 않는다.
5. Introduction에 핵심 관련 연구와 차별점을 통합하는 구성은 문구상 합리적인 해석이다. 독립 제목이 없다는 이유만으로 규정 위반이라고 판정할 근거는 찾지 못했다.
6. Stage 2에는 완전하고 포괄적인 related work section을 제공하도록 기대한다고 CFP가 명시한다. 이 요구를 Stage 1에 그대로 적용하지 않는다.

## 4. 현재 원고에서 확인한 구성

원래 작업 저장소:

`E:\03 논문작성\04 RSS - Stone Stacking\latex`

주요 파일:

- `root.tex`, `root.pdf`, `references.bib`
- `sections/01_introduction.tex`
- `sections/02_related_works.tex`
- `sections/03_overview.tex`
- `sections/04_pose_optimization.tex`
- `sections/05_sequence_planning.tex`

11월 17일에는 위 파일 중 `root.tex`, Introduction, Related Works, Preliminaries and Overview의 소스를 다시 읽었다. 이때 원고 전체를 새로 정밀 심사하거나 PDF 전체 레이아웃을 다시 검사한 것은 아니다.

`root.tex`는 위 01–05 섹션을 포함한다. 별도 implementation/experiments/conclusion 파일의 input은 주석 처리되어 있다. 이것만으로 실험이나 demonstration이 전혀 없다고 해석하면 안 된다. Abstract는 예비 최적화·탐색 예시와 physical stacking demonstration을 언급하고, Introduction에서 예비 결과 그림을 포함한다.

### 4.1 Introduction의 핵심 내용

- 목표 형상을 채우면서 자립 구조의 안정성을 유지하는 문제와 형식적 목적식을 제시한다.
- Johns 및 Liu 계열의 stacking 방법과 비교해, 구조 전체의 힘·토크 평형을 연속 pose refinement에 이용하는 점과 미래 배치 순서를 명시적으로 탐색하는 점을 설명한다.
- Contact-aware manipulation/grasp 분야의 bilevel formulation을 기반으로 삼는다고 밝힌다.
- DSF와 관련 충돌 검출을 이용한 미분, 구조 전체 contact force 최적화, MCTS 계층적 expansion, domain-specific reward를 소개한다.
- GPU 기여는 **구조 내부의 bodywise contact-force ADMM 병렬화와 독립 후보 간 pose optimization/simulation 배칭**으로 설명한다.
- 기여 목록은 pose optimization, MCTS, GPU evaluation의 세 항목이다.

### 4.2 Related Works의 현재 세 소절

1. **Robotic Packing and Stone Stacking**: Wang/Hauser, Johns, Liu, Menezes 등을 비교한다.
2. **Contact-Aware Pose Optimization**: Contact Factor Graph, GraspQP, BODex를 다루고, DSF 접촉 기하 미분과 구조 전체 평형이라는 제안 방법의 특성을 설명한다.
3. **Simulation-Based Sequential Manipulation Planning**: PMBS의 GPU simulation 배칭을 짚고, 제안 방법은 simulation 전에 구조 전체 contact force 최적화를 포함하는 병렬 pose refinement를 추가한다고 설명한다.

이 비교 문장들이 논문별 차이를 정확하게 기술하는지에 대한 완전한 문헌 재검증은 이번 구성 논의에서 수행하지 않았다. 새로운 novelty 평가를 하려면 원 논문과 대조해야 한다. 최초 요청의 TE-SDF 비교 역시 이 인계 문서만으로 완료된 검증으로 취급하지 않는다.

## 5. 가장 최근 조언 — 아직 원고에 적용하지 않음

사용자는 “현재 1차 제출에서는 어떻게 하는 게 낫겠느냐”고 물었다. 다음은 에이전트의 추천이며, 사용자가 확정하거나 수정 실행을 지시한 상태는 아니다.

**독립 Related Work 섹션은 유지하되, 세 subsection 제목을 없애고 짧은 세 문단으로 정리한다. Introduction과의 중복을 줄인다.**

이유:

- 현재 Introduction은 이미 문제 정의, 목적식, 선행연구, 방법 소개, 기여를 포함해 길다. 관련 연구 전체를 합치면 논지와 기여가 묻힐 수 있다.
- Related Works에는 novelty 방어에 필요한 직접 비교가 있다. 이를 눈에 띄게 남기는 것이 유리하다고 판단했다.
- Johns/Liu 설명, bilevel 관련 소개, GPU 관련 소개가 두 섹션에서 겹친다. 이 중복을 우선 줄일 수 있다.
- 독립 섹션이 규정상 필수여서 유지하자는 판단은 아니다.

권장 구성:

| 부분 | 방향 |
| --- | --- |
| Introduction | 문제와 핵심 한계 → 제안 접근 및 검증할 가설 → 세 기여 |
| Related Work | stacking / contact optimization / GPU MCTS의 직접 비교를 세 문단으로 유지 |
| 방법론 | sampling, reward, 최적화의 평가·재현에 필요한 설명 유지 |

GPU 가속 기여는 Introduction의 기여 목록에서 유지한다. Related Work에서는 BODex 및 PMBS와 구별되는 계산 구조를 보여준다. 단순히 GPU 사용을 주장하는 것과 구체적인 분해·병렬화 방법을 기여로 설명하는 것은 구별해야 한다.

검증 가능한 가설과 설계의 연결을 더 선명하게 하자는 조언도 있었다. 이는 새 실험이나 별도 긴 섹션을 무조건 추가하라는 뜻이 아니다. 기존 반복 설명을 정리하고 현재 방법의 이유를 명확히 하는 방향이다.

## 6. 이전 평가의 정정과 한계

- 초기 응답은 RSS 2027의 새 규정을 확인하지 않은 채 실험 결과 부족을 과도하게 감점했다. 사용자가 지적했고, 에이전트가 잘못을 인정했다.
- 이후 판단은 Stage 1 기준으로 수정됐다. 앞선 대화에서는 가설의 가치와 결론 도출 가능성에 각각 잠정 3/4, 진행에 약한 지지 정도로 표현했으나, **이는 공식 점수나 신뢰할 수 있는 채택 확률이 아니다.**
- “2차에서 실험과 벤치마크를 많이 넣으면 통과한다”는 보장은 하지 않는다. Charter, 검증의 엄밀성, 과학적 통찰이 중요하다.
- 이 기록 자체는 현재 버전의 최종 심사 보고서가 아니다. 새 저장소의 원고가 바뀌었거나 상세 비교를 요청받으면 다시 읽는다.

## 7. 완료된 수정과 Git 상태

사용자는 RSS 템플릿의 참고문헌 링크 권장사항에 맞춘 수정을 요청했고, 완료 후 커밋을 명시적으로 요청했다.

완료 내용:

- 인용된 참고문헌 **22개 제목**을 `\href{URL}{제목}`으로 감쌌다.
- DOI 또는 공식 출판/학회 페이지를 사용했으며, cuRobo는 arXiv 링크를 사용했다.
- `references.bib`와 재컴파일한 `root.pdf`를 변경했다. `root.tex`는 이 작업에서 변경하지 않았다.
- PDF 6쪽, 본문 5쪽 + 참고문헌 1쪽 유지.
- 이전 PDF와 본문 5쪽의 추출 텍스트가 같음을 확인했다.
- 22개 목표 URL이 PDF 링크 annotation에 모두 존재하는지 검사했고, 참고문헌 페이지를 렌더링해 확인했다. 모든 원격 URL의 실시간 접속 성공을 일괄 검증했다는 뜻은 아니다.
- `\href`로 감싸면서 BibTeX의 대소문자 처리에 차이가 생겨, 참고문헌의 원래 title 필드 대소문자가 더 많이 유지됐고 줄바꿈도 일부 달라졌다. 참고문헌 텍스트/배치가 완전히 동일하다고 말하지 않는다.

완료 커밋:

`c0e7c66 — Add publisher links to bibliography titles`

커밋에는 `references.bib`, `root.pdf`가 포함됐다. 커밋 후 작업 트리는 깨끗했고, 이 인계 파일 생성 직전에도 추적 파일의 미커밋 변경은 없었다.

링크 관련 근거의 범위: 당시 공식 연결 LaTeX 템플릿의 RSS Hyperlinks 안내를 읽고 적용했다. CFP의 외부 웹사이트 제한과 FAQ의 보충자료 링크 제한도 존재한다. 이 대화에서 프로그램 위원회로부터 참고문헌 링크 예외에 대한 별도 답변을 받은 것은 아니다.

## 8. 다음 대화에서 이어갈 일

- 이 문서와 함께 최신 `.tex`, `.bib`, PDF 또는 해당 저장소를 제공하면 된다. 이 파일만으로 원고 전체를 재구성할 수는 없다.
- 우선 최신 원고가 위 구조와 같은지 확인한다.
- 현재 가장 최근 제안은 **Related Work를 짧게 유지하면서 Introduction과 중복을 줄이는 편집안**이다. 실제 수정은 아직 하지 않았다.
- 수정 요청을 받으면 기존 sampling/reward 정의를 무작정 희생하지 않고, 구체적인 편집과 컴파일 후 5+1쪽을 확인한다.
- 채택 가능성은 Stage 1 기준으로 평가한다. 결과가 미완성이라는 사실과 방법론 자체가 평가 불가능하게 미정의된 상태를 혼동하지 않는다.
- 사용자는 불필요한 확인 질문보다 구체적인 작업과 근거 있는 판단을 선호한다. 다만 이 문서를 넘긴 행위만으로 새로운 편집, 커밋 또는 제출까지 요청한 것으로 해석하지 않는다.

## 9. 원래 환경의 빌드 참고

- Windows PowerShell, MiKTeX, `.latexmkrc`, BibTeX/plainnat.
- 빌드 명령: `latexmk -pdf -interaction=nonstopmode -halt-on-error root.tex`.
- 원래 환경의 MiKTeX 경로: `C:\Users\INROL_Seoki\AppData\Local\Programs\MiKTeX\miktex\bin\x64`.
- 원래 환경에서는 Git safe.directory를 전역 변경하지 않고 `git -c 'safe.directory=E:/03 논문작성/04 RSS - Stone Stacking/latex' ...`로 사용했다.
- 새 저장소에서는 해당 환경에 맞게 경로를 다시 확인한다.

기존 별도 기록 `docs/review-handoff-20261114.md`도 있다. 이 문서는 그 파일의 내용을 재검증하거나 통합한 것이 아니라, 이번 대화의 판단과 변경을 추가로 기록한 것이다.
