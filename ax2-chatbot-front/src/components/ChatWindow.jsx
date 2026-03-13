import React, { useState, useEffect, useRef } from 'react';

import { DeepChat } from 'deep-chat-react';
import { responseInterceptor } from '../utils/ResponseInterceptor';

const ChatWindow = () => {
    const chatRef = useRef(null);
    const [modalVideoUrl, setModalVideoUrl] = useState(null);
    const [modalImageUrl, setModalImageUrl] = useState(null);
    const gokBlue = 'rgb(0, 55, 100)';

    // 동영상 모달 실행을 위한 전역 함수 등록
    useEffect(() => {
        window.openVideoModal = (url) => setModalVideoUrl(url);
        window.openImageModal = (url) => setModalImageUrl(url);
    }, []);

    // 모달 닫았을 때 새로고침 방지
    const closeModals = (e) => {
        if (e) {
            e.preventDefault();
            e.stopPropagation(); // 부모 요소로 이벤트 전파 방지
        }
        setModalVideoUrl(null);
        setModalImageUrl(null);
    };

    return (
        <div style={containerStyle}>

            <DeepChat
                ref={chatRef}
                style={chatComponentStyle}
                messageStyles={getMessageStyles(gokBlue)}
                inputAreaStyle={inputAreaStyle}
                textInput={textInputStyle}
                submitButtonStyles={submitButtonStyle(gokBlue)}
                html={{ useHtml: true }}
                
                connect={{url: 'http://localhost:8000/stream-chat', method: 'POST', stream: true}}
                responseInterceptor={responseInterceptor}
                stream={true}


            />

            {/* 동영상 모달 */}
            {modalVideoUrl && (
                <div style={modalOverlay} onClick={() => setModalVideoUrl(null)}>
                    <div style={modalContent} onClick={e => e.stopPropagation()}>
                        <video src={modalVideoUrl} controls autoPlay style={{ width: '100%' }} />
                        <button style={closeBtn} onClick={closeModals}>닫기</button>
                    </div>
                </div>
            )}

            {/* 이미지 모달 */}
            {modalImageUrl && (
                <div style={modalOverlay} onClick={closeModals}>
                    <div style={{ ...modalContent, maxWidth: '600px' }} onClick={e => e.stopPropagation()}>
                        <img src={modalImageUrl} alt="미리보기" style={{ width: '100%', borderRadius: '15px' }} />
                        <button
                            type="button"
                            style={closeBtn}
                            onClick={closeModals}
                        >
                            닫기
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
};

// --- 스타일 변수 ---
const containerStyle = {
    width: '100%', height: 'calc(100vh - 70px)', display: 'flex', flexDirection: 'column',
    justifyContent: 'center', alignItems: 'center', padding: '20px', backgroundColor: '#f4f7f9'
};

const chatComponentStyle = {
    borderRadius: '20px', width: '100%', maxWidth: '800px', height: '100%',
    backgroundColor: '#ffffff', border: 'none', boxShadow: '0 10px 25px rgba(0,0,0,0.1)',
    display: 'flex', flexDirection: 'column'
};

const getMessageStyles = (gokBlue) => ({
    default: {
        shared: { innerContainer: { fontSize: '0.95rem', padding: '12px 16px' }, outerContainer: { margin: '10px 0' } },
        user: { bubble: { backgroundColor: gokBlue, color: 'white', borderRadius: '18px 18px 2px 18px', marginRight: '10px' } },
        ai: { bubble: { backgroundColor: '#f0f2f5', color: '#333', borderRadius: '18px 18px 18px 2px', marginLeft: '10px' } }
    }
});

const inputAreaStyle = { backgroundColor: '#ffffff', borderTop: '1px solid #eee', padding: '12px 15px' };

const textInputStyle = {
    placeholder: { text: '메시지를 입력하세요...' },
    containerStyle: { backgroundColor: '#f8f9fa', border: '1px solid #e9ecef', borderRadius: '25px', padding: '5px 15px', width: '100%', fontSize: '1rem' }
};

const submitButtonStyle = (gokBlue) => ({
    position: "outside-end",
    submit: {
        container: { backgroundColor: gokBlue, borderRadius: '50%', marginLeft: '10px' },
        svg: { color: 'white', width: '18px', height: '18px', marginRight: '2px' }
    },
    hover: { container: { backgroundColor: 'rgb(0, 75, 130)' } }
});

const modalOverlay = { position: 'fixed', top: 0, left: 0, width: '100%', height: '100%', backgroundColor: 'rgba(0,0,0,0.8)', zIndex: 1000, display: 'flex', justifyContent: 'center', alignItems: 'center' };
const modalContent = { position: 'relative', width: '90%', maxWidth: '800px' };
const closeBtn = { position: 'absolute', top: '-40px', right: 0, color: 'white', background: 'none', border: 'none', fontSize: '1.2rem', cursor: 'pointer' };

export default ChatWindow;