const gokBlue = "var(--gok-blue)";

export const chatComponentStyle = {
  borderRadius: "20px",
  width: "100%",
  height: "100%",
  boxShadow: "0 10px 25px rgba(0,0,0,0.1)",
  overflow: "hidden",
  backgroundColor: "white",
};

export const textInputStyle = {
  placeholder: {
    text: "건강 관련 궁금한 내용을 입력하세요.",
  },
  styles: {
    container: {
      border: "1px solid #dcdcdc",
      borderRadius: "12px",
      alignItems: "center",
      justifyContent: "center",
      display: "flex",
      padding: "8px 0",
      width: "80%",
      fontSize: "16px",
      marginLeft: "-40px"
    },
  },
};

export const messageStyle = {
  default: {
    shared: {
      innerContainer: {
        fontSize: "0.95rem",
        padding: "12px 16px",
        lineHeight: "1.5",
      },
      outerContainer: { margin: "10px 0" },
    },
    user: {
      bubble: {
        backgroundColor: gokBlue,
        color: "white",
        borderRadius: "18px 18px 2px 18px",
        marginLeft: "auto",
        maxWidth: "50%"
      },
    },
    ai: {
      bubble: {
        backgroundColor: "#f0f2f5",
        color: "#333",
        borderRadius: "18px 18px 18px 2px",
        marginRight: "auto",
        maxWidth: "80%"
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
        borderRadius: "10px",
        marginBottom: "2px",
        marginLeft: "8px",
        padding: "10px 7px",
        minWidth: "15px",
        height: "29px",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        transition: "opacity 0.2s",
      },
    },
    text: {
      content: "전송",
      styles: {
        default: { color: "white" },
        fontSize: "14px",
        fontWeight: "bold",
        whiteSpace: "nowrap",
      },
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

export const inputAreaStyles = {
  container: {
    display: "flex",
    alignItems: "flex-end",
    padding: "12px 16px",
    backgroundColor: "#fff",
    borderTop: "1px solid #f0f0f0",
  },
};
