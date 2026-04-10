import React, { useRef } from 'react';
import '../../css/FileUploadModal.css';


const FileUploadModal = ({ isOpen, onClose, onUpload }) => {
    const fileInputRef = useRef(null);

    if (!isOpen) return null;

    // 파일 검증 및 처리 로직
    const processFile = (file) => {
        if (!file) return;

        // 확장자 체크
        const isHtml = file.type === "text/html" || file.name.endsWith(".html");
        if (!isHtml) {
            alert("리포트 파일만 업로드 가능합니다.");
            return;
        }

        const reader = new FileReader();
        reader.onload = (e) => {
            const content = e.target.result;

            // 변조 방지 검증 (시스템 발송 리포트 시그니처 확인)
            // TODO[wcw] 리포트 HTML 내부에 포함되어야 할 고유 키워드 (예: GOK-HEALTH-REPORT)
            const isValidReport = content.includes("public/report") || content.includes("");

            if (!isValidReport) {
                alert("리포트 파일만 업로드 가능합니다.");
                return;
            }

            // 검증 통과 시 부모 컴포넌트로 파일 전달
            // (부모의 onUpload에서 서버 전송 및 메시지 추가 로직 수행)
            onUpload(file);

            // 업로드 직후 모달 닫기
            onClose();
        };

        reader.readAsText(file);
    };

    const handleFileChange = (e) => {
        const files = e.target?.files || e.dataTransfer?.files;
        if (files && files.length > 0) {
            processFile(files[0]);
        }
    };

    return (
        <div className='modal-overlay' onClick={onClose}>
            <div className='upload-modal-content' onClick={e => e.stopPropagation()}>
                <div className='upload-modal-header'>
                    <h3 className='upload-modal-title'>리포트 파일 업로드</h3>
                    <span className='upload-modal-close-btn' onClick={onClose}>&times;</span>
                </div>
                <div
                    className='drop-zone'
                    onDragOver={(e) => {
                        e.preventDefault();
                        e.currentTarget.style.borderColor = '#4c6ef5';
                        e.currentTarget.style.backgroundColor = '#f8f9ff';
                    }}
                    onDrop={(e) => {
                        e.preventDefault();
                        handleFileChange(e);
                    }}
                    onClick={() => fileInputRef.current.click()}
                    onDragLeave={(e) => {
                        e.currentTarget.style.borderColor = '#ccc';
                        e.currentTarget.style.backgroundColor = '#fff';
                    }}
                >
                    <p style={{ color: '#555', lineHeight: '1.6', marginBottom: '15px' }}>
                        여기로 HTML 파일을 드래그하거나<br />
                        <strong>클릭해서 선택하세요.</strong>
                    </p>
                    <button className='find-file-btn'>파일 찾기</button>
                    <input
                        type="file"
                        ref={fileInputRef}
                        onChange={handleFileChange}
                        style={{ display: 'none' }}
                        accept=".html"
                    />
                </div>
            </div>
        </div>
    );
};

export default FileUploadModal;