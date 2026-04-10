export const gokBlue = "rgb(0, 55, 100)";

export const containerStyle = {
  width: "100%",
  height: "calc(100dvh - 70px)",
  display: "flex",
  flexDirection: "column",
  alignItems: "center",
  padding: "10px", // 모바일 여백 축소
  backgroundColor: "#f4f7f9",
  boxSizing: "border-box",
};

export const chatComponentStyle = {
  borderRadius: "20px",
  width: "100%",
  maxWidth: "800px",
  height: "100%",
  boxShadow: "0 10px 25px rgba(0,0,0,0.1)",
  overflow: "hidden", // 라운드 코너 밖으로 내용 안나가게
};

export const getTextInputStyle = (isProcessing) => ({
  placeholder: {
    text: isProcessing ? "분석 중..." : "메시지를 입력하세요...",
  },
  containerStyle: {
    backgroundColor: "#f8f9fa",
    border: "1px solid #e9ecef",
    borderRadius: "25px",
    padding: "5px 15px",
    width: "100%",
    fontSize: "16px", // 모바일 자동 줌 방지 (최소 16px)
  },
  disabled: isProcessing,
});

export const uploadHeaderStyle = {
  width: "100%",
  maxWidth: "800px",
  display: "flex",
  alignItems: "center",
  padding: "12px 15px", // 모바일 맞춤 패딩
  borderRadius: "15px 15px 0 0",
  borderBottom: "1px solid #eee",
  zIndex: 1,
  justifyContent: "space-between",
  boxSizing: "border-box",
};

export const headerTitleStyle = {
  fontSize: "1rem", // 모바일 가독성
  fontWeight: "bold",
  color: "#333",
};

export const uploadButtonStyle = {
  backgroundColor: gokBlue,
  color: "white",
  border: "none",
  padding: "6px 12px",
  borderRadius: "8px",
  cursor: "pointer",
  fontSize: "0.85rem",
  display: "flex",
  alignItems: "center",
  gap: "5px",
  transition: "background-color 0.2s",
  whiteSpace: "nowrap", // 글자 줄바꿈 방지
};

export const getMessageStyles = (gokBlue) => ({
  default: {
    shared: {
      innerContainer: {
        fontSize: "0.95rem",
        padding: "10px 14px",
        maxWidth: "85%", // 모바일에서 말풍선이 너무 꽉 차지 않게
      },
      outerContainer: { margin: "8px 0" },
    },
    user: {
      bubble: {
        backgroundColor: gokBlue,
        color: "white",
        borderRadius: "18px 18px 2px 18px",
      },
    },
    ai: {
      bubble: {
        backgroundColor: "#f0f2f5",
        color: "#333",
        borderRadius: "18px 18px 18px 2px",
      },
    },
  },
});

export const inputAreaStyle = {
  backgroundColor: "white",
  borderTop: "1px solid #eee",
  padding: "10px", // 여백 최적화
};

export const submitButtonStyle = (gokBlue) => ({
  position: "outside-end",
  submit: {
    container: {
      backgroundColor: gokBlue,
      borderRadius: "50%",
      marginLeft: "8px",
      minWidth: "40px", // 터치 영역 확보
      minHeight: "40px",
      display: "flex",
      justifyContent: "center",
      alignItems: "center",
    },
    svg: { color: "white", width: "18px", height: "18px" },
  },
});

/* --- 모달 관련 스타일 --- */

export const modalOverlay = {
  position: "fixed",
  top: 0,
  left: 0,
  width: "100%",
  height: "100%",
  backgroundColor: "rgba(0,0,0,0.6)", // 약간 더 밝게 조정
  zIndex: 2000,
  display: "flex",
  justifyContent: "center",
  alignItems: "center",
  padding: "20px", // 모바일 화면 끝에 붙지 않게
  boxSizing: "border-box",
};

export const uploadButton = {
  backgroundColor: "var(--gok-blue)",
  color: "white",
  border: "none",
  borderRadius: "10px", 
  padding: "8px 14px",
  fontSize: "13px",
  fontWeight: "600",
  cursor: "pointer",
  display: "flex",
  alignItems: "center",
  justifyContent: "center",
  gap: "5px",
  flexShrink: 0, 
  minWidth: "fit-content",
  WebkitTapHighlightColor: "transparent", 
  boxShadow: "0 2px 6px rgba(74, 125, 255, 0.2)",
};

export const uploadModalContent = {
  backgroundColor: "white",
  padding: "20px", // 모바일 여백 축소
  borderRadius: "15px",
  width: "100%", // 모바일 기본 너비
  maxWidth: "450px", // PC 최대 너비
  textAlign: "center",
  position: "relative",
  boxSizing: "border-box",
  boxShadow: "0 10px 30px rgba(0,0,0,0.2)",
};

export const uploadModalHeader = {
  position: "relative",
  display: "flex",
  justifyContent: "center",
  alignItems: "center",
  padding: "10px 0 20px 0",
  borderBottom: "1px solid #eee",
  width: "100%",
  boxSizing: "border-box",
  marginBottom: "20px",
};

export const uploadModalCloseBtn = {
  position: "absolute",
  right: "0px", // 패딩 고려 조정
  top: "40%",
  transform: "translateY(-50%)",
  cursor: "pointer",
  fontSize: "28px", // 터치하기 좋게 크게
  color: "#666",
  padding: "10px", // 클릭/터치 범위 확대
  lineHeight: "1",
  WebkitTapHighlightColor: "transparent",
};

export const dropZoneStyle = {
  border: "2px dashed #ccc",
  borderRadius: "10px",
  padding: "30px 15px", // 모바일용 패딩
  backgroundColor: "#fafafa",
  cursor: "pointer",
  transition: "all 0.3s",
  fontSize: "0.9rem",
  wordBreak: "keep-all",
};

export const findFileBtn = {
  backgroundColor: "var(--gok-blue)",
  color: "white",
  border: "none",
  padding: "10px 25px",
  borderRadius: "20px",
  cursor: "pointer",
  marginTop: "15px",
  fontSize: "0.95rem",
};

export const modalContent = {
  position: "relative",
  width: "100%",
  maxWidth: "800px",
};

export const closeBtn = {
  position: "absolute",
  top: "-45px",
  right: "0",
  color: "white",
  background: "none",
  border: "none",
  fontSize: "1.5rem",
  cursor: "pointer",
  padding: "10px",
};
