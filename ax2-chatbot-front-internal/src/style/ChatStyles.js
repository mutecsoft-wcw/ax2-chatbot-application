const gokBlue = "var(--gok-blue)";

export const chatComponentStyle = {
  borderRadius: "20px",
  width: "100%",
  maxWidth: "800px",
  height: "100%",
  boxShadow: "0 10px 25px rgba(0,0,0,0.1)",
  overflow: "hidden", // 라운드 코너 밖으로 내용 안나가게
};

export const textInputStyle = {
  placeholder: {
    text: "검색어를 입력하세요...",
  },
  containerStyle: {
    backgroundColor: "#f8f9fa",
    border: "1px solid #e9ecef",
    borderRadius: "25px",
    alignItems: "center",
    justifyContent: "center",
    display: "flex",
    padding: "5px 15px",
    width: "100%",
    fontSize: "16px", // 모바일 자동 줌 방지 (최소 16px)
  },
//   disabled: isProcessing,
};

export const messageStyle = {
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
};

export const submitButtonStyle = {
    position: "outside-end", 
    submit: {
      containerStyle: {
        default: {
          backgroundColor: gokBlue,
          borderRadius: "10px",
          width: "60px",
          height: "36px",
          marginRight: "6px",
          marginBottom: "6px",
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          cursor: "pointer",
          border: "none",
        },
        hover: { backgroundColor: "#1e5cbd" },
        click: { backgroundColor: "#154796" }
      },
      svg: { content: "" }, // 아이콘 대신 텍스트 사용
      text: {
        content: "전송",
        style: {
          default: {
            color: "white",
            fontSize: "14px",
            fontWeight: "bold",
          }
        }
      }
    },
    loading: {
      containerStyle: {
        default: { backgroundColor: "#a5c0ff", borderRadius: "10px" }
      },
      svg: { content: "" },
      text: { content: "대기", style: { default: { color: "white" } } },
    },
    stop: {
      containerStyle: {
        default: { backgroundColor: "#FF4D4F", borderRadius: "10px" }
      },
      svg: { content: "" },
      text: { content: "중지", style: { default: { color: "white" } } },
    },
    alwaysEnabled: true
  };

