import { useEffect } from 'react';

export const useChatActions = (chatRef) => {
    useEffect(() => {
        window.handleChatAction = (action) => {
            if (!chatRef.current) return;

            if (action === "START_SURVEY") {
                chatRef.current.submitUserMessage({
                    text: "__START_SURVEY__",
                    role: "user"
                });
            }

            if (action === "CANCEL_SURVEY") {
                chatRef.current.submitUserMessage({
                    text: "__CANCEL_SURVEY__",
                    role: "user"
                });
            }
        };

        // 컴포넌트가 사라질 때 전역 함수 제거
        return () => {
            delete window.handleChatAction;
        };
    }, [chatRef]); 
};