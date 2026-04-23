import React from 'react';
import * as Styles from '../../style/ModalStyles';

const MediaModal = ({ videoUrl, imageUrl, onClose }) => {
    if (!videoUrl && !imageUrl) return null;

    return (
        <div style={Styles.modalOverlay} onClick={onClose}>
            <div 
                style={videoUrl ? Styles.modalContent : { ...Styles.modalContent, maxWidth: '600px' }} 
                onClick={e => e.stopPropagation()}
            >
                {videoUrl ? (
                    <video src={videoUrl} controls autoPlay style={{ width: '100%' }} />
                ) : (
                    <img src={imageUrl} alt="미리보기" style={{ width: '100%', borderRadius: '15px' }} />
                )}
                <button type="button" style={Styles.closeBtn} onClick={onClose}>
                    닫기
                </button>
            </div>
        </div>
    );
};

export default MediaModal;