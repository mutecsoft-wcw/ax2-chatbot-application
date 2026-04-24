import { useEffect, useRef, useState } from 'react';
import { chatApi } from '../api/chatApi';

export const useChatInit = (sessionId, updateSession, location, navigate) => {
    const [isLoaded, setIsLoaded] = useState(false);
    const isFetching = useRef(false);
    const hasFetched = useRef(false);
    const initialHistory = useRef([]);
    const initialQuery = useRef(location.state?.initialMessage || null);
    const isProcessed = useRef(false);

    useEffect(() => {
        // 이미 페칭 중이거나 완료되었다면 중복 실행 방지
        if (hasFetched.current || isFetching.current) return;

        const initChat = async () => {
            isFetching.current = true;
            try {
                const res = await chatApi.fetchHistory(sessionId);
                const data = res?.data || res;

                if (data) {
                    if (data.sessionId && data.sessionId !== sessionId) {
                        updateSession(data.sessionId);
                    }
                    initialHistory.current = data.history || [];
                }
                hasFetched.current = true;
            } catch (err) {
                console.error("데이터 로드 실패:", err);
            } finally {
                isFetching.current = false;
                setIsLoaded(true);

                // 초기 메시지가 있을 경우 처리 후 state 초기화
                if (location.state?.initialMessage) {
                    navigate(location.pathname, { replace: true, state: {} });
                }
            }
        };

        initChat();
    }, [sessionId, updateSession, navigate, location.pathname, location.state?.initialMessage]);

    return {
        isLoaded,
        initialHistory: initialHistory.current,
        initialQuery,
        isProcessed
    };
};