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
    text: "건강 관련 궁금한 내용을 입력하세요...",
  },
  styles: {
    container: {
      border: "1px solid lightgray",
      borderRadius: "10px",
      alignItems: "center",
      justifyContent: "center",
      display: "flex",
      padding: "5px 15px",
      width: "70%",
      fontSize: "16px", // 모바일 자동 줌 방지 (최소 16px)
    },
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

export const submitButtonStyles = {
  position: "outside-end",
  submit: {
    container: {
      default: {
        backgroundColor: gokBlue,
        borderRadius: "8px",
        margin: "0 0 2px 12px",
        padding: "11px",
      },
    },
    text: {
      content: "전송",
      styles: { default: { color: "white" } },
    },
    svg: { content: "" },
  },
  loading: {
    text: { content: "대기", styles: { default: { color: "white" } } },
    svg: { content: "" },
  },
  stop: {
    text: { content: "중지", styles: { default: { color: "white" } } },
    svg: { content: "" },
  },
  alwaysEnabled: true,
};
