# Robotiq 3-Finger Gripper for Isaac Sim

`robotiq_3f_isaac.urdf`는 Isaac Sim URDF Importer에서 독립적으로 불러올 수
있도록 정리한 Robotiq 3-Finger Adaptive Gripper 모델이다.

## 가져오기

1. Isaac Sim에서 **File > Import** 또는 **URDF Importer**를 연다.
2. 이 폴더의 `robotiq_3f_isaac.urdf`를 선택한다.
3. **Fix Base Link**는 단독 시험 시 켜고, 로봇에 결합할 때는 목적에 맞게
   설정한다.
4. 로봇과 결합할 때 root link인 `palm`을 로봇의 tool flange에 fixed joint로
   연결한다.

모델에는 `palm`과 세 손가락의 관절 12개(가동 11개, 고정 1개)가 들어 있다.
원본 모델은 실제 하드웨어의 내부 연동을 mimic joint로 단순화하지 않으므로,
Isaac Sim에서 손가락 관절을 구동하려면 drive 설정 또는 별도 제어 로직이
필요하다.

## 출처와 변경 사항

- 출처: `ros-industrial-attic/robotiq`, `kinetic-devel`
- 원본 커밋: `45196f6558fe8ba9d89bc8a105396c68c3e7e892`
- 패키지: `robotiq_3f_gripper_visualization`
- 라이선스: BSD 3-Clause (`LICENSE` 참조)
- visual mesh 경로를 실제 존재하는 DAE 파일로 수정
- collision mesh는 원본 STL 사용
- ROS `package://` URI를 URDF 기준 상대 경로로 변경
- 원본 생성 URDF에서 `palm` link 바깥에 있던 inertial을 link 안으로 이동
- 원본의 비현실적인 180도 손가락 관절 범위를 실제 형상에 맞는 범위로 제한

## 손가락 관절 제한

- 각 손가락 `joint_1`: 0~70도
- 각 손가락 `joint_2`: 0~90도
- 각 손가락 `joint_3`: -70~0도(Isaac Sim 기본 관절값 포함)
- 양쪽 scissor 관절은 원본 범위(-0.25~0.25 rad 부근)를 유지

URDF의 limit은 각 관절의 과회전을 막는다. 다만 Isaac Sim에서 충돌 자체도
막으려면 URDF Importer의 self-collision을 활성화하고, 지나치게 큰 drive 속도나
physics time step을 사용하지 않아야 한다.
