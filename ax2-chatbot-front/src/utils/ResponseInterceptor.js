import { ResponseManager } from "./ResponseManager";

export const responseInterceptor = (response) => {

  if (!response || Object.keys(response).length === 0) {
    return { text: "" };
  }

  if (response.text !== undefined && !response.type) {
    return { text: response.text };
  }

  if (response.type) {
    return ResponseManager.processResponse(response);
  }

  return response;
};
