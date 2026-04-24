import aiAvarta from "../../img/icon.png";

export const chatStyle = {
  borderRadius: "10px",
  borderColor: "#dcdcdc",
  backgroundColor: "#f3f6fc",
  width: "100%",
//   maxWidth: "800px",
  height: "100%",
  fontFamily: "Pretendard, -apple-system, sans-serif",
};

export const messageStyles = {
  default: {
    shared: {
      bubble: {
        maxWidth: "85%",
        backgroundColor: "unset",
        marginTop: "20px",
        marginBottom: "20px",
        wordBreak: "break-word",
        whiteSpace: "pre-wrap",
      },
    },
    user: { bubble: { marginRight: "0px", color: "black" } },
    ai: { innerContainer: { borderRadius: "15px", backgroundColor: "white" } },
  },
};

export const avatarsStyles = {
  ai: {
    src: aiAvarta,
    styles: { position: "start", container: { marginLeft: "12px", marginRight: "5px" }, avatar: { paddingTop: "6px" } },
  },
  user: {
    src: "",
    styles: { position: "end", container: { marginRight: "12px", marginLeft: "5px", display: "none" }},
  },
};

export const inputAreaStyle = {
  backgroundColor: "#ffffff",
  borderTop: "1px solid #e0e0e0",
//   padding: "10px",
  display: "flex",
//   alignItems: "center",
//   justifyContent: "center",
  boxSizing: "border-box",
};

export const textInputStyles = {
  container: {
    borderRadius: "20px",
    border: "1px solid #969696",
    boxShadow: "unset",
    width: "80%",
  },
  text: { padding: "10px", paddingLeft: "15px", paddingRight: "34px", },
};

export const submitButtonStyles = {
  position: "outside-end",
  submit: {
    container: {
      default: {
        bottom: "1.1em",
        borderRadius: "25px",
        backgroundColor: "#f3f6fc",
        marginLeft: "5px"
      },
    },
    svg: {
      content:
        '<?xml version="1.0" encoding="utf-8"?> <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="m21.426 11.095-17-8A.999.999 0 0 0 3.03 4.242L4.969 12 3.03 19.758a.998.998 0 0 0 1.396 1.147l17-8a1 1 0 0 0 0-1.81zM5.481 18.197l.839-3.357L12 12 6.32 9.16l-.839-3.357L18.651 12l-13.17 6.197z"/></svg>',
      styles: {
        default: {
          width: "1.5em",
          filter:
            "brightness(0) saturate(100%) invert(10%) sepia(86%) saturate(6044%) hue-rotate(205deg) brightness(100%) contrast(100%)",
        },
      },
    },
  },
  loading: {
    svg: {
      styles: {
        default: {
          filter:
            "brightness(0) saturate(100%) invert(72%) sepia(0%) saturate(3044%) hue-rotate(322deg) brightness(100%) contrast(96%)",
        },
      },
    },
  },
  stop: {
    container: { hover: { backgroundColor: "#ededed" } },
    svg: {
      styles: {
        default: {
          filter:
            "brightness(0) saturate(100%) invert(59%) sepia(0%) saturate(0%) hue-rotate(348deg) brightness(96%) contrast(93%)",
        },
      },
    },
  },
};

export const reportUploadButtonStyles = [
    {
      position: "inside-end",
      styles: {
        button: {
          default: {
            svg: {
              content: `<svg viewBox="0 0 139 200" xmlns="http://www.w3.org/2000/svg"><path d="M93,90.8H49V51.5H32.3L71,13.7l38.7,37.8H93V90.8L93,90.8z M111,109.7c2.6,0,4.7-2.1,4.7-4.7V75.9h11.2v29.8 c0,8.4-6.8,15.2-15.2,15.2H30.4c-8.4,0-15.2-6.8-15.2-15.2V75.9h11.2V105c0,2.6,2.1,4.7,4.7,4.7H111L111,109.7z"/></svg>`,
              styles: {
                  default: {
                    //   paddingTop: "30px",
                    // height: "100%",
                  }
              }
            },
            text: {
              content: "",
              styles: {
                default: { color: "white", fontSize: "12px", },
              },
            },
            container: {
              default: {
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  marginRight: "10px", // 입력창과의 간격
                  marginLeft: "10px",
                  flexShrink: "0",
                //   height: "100%"
              },
            },
          },
        },
      },
    },
  ];
