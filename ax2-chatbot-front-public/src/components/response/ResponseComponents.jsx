import React from 'react';

// 이미지 그룹 컴포넌트
export const ImageGroup = ({ urls, onImageClick }) => (
    <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(120px, 1fr))',
        gap: '8px', 
        marginTop: '12px'
    }}>
        {urls.map((url, i) => (
            <img
                key={i} src={url} alt="답변 이미지"
                onClick={() => onImageClick?.(url)}
                style={{
                    width: '100%',
                    aspectRatio: '1/1',
                    objectFit: 'cover',
                    borderRadius: '12px',
                    border: '1px solid #eee',
                    cursor: 'pointer',
                    // 모바일 터치 하이라이트 제거
                    WebkitTapHighlightColor: 'transparent'
                }}
            />
        ))}
    </div>
);

// 동영상 프리뷰 컴포넌트
export const VideoPreview = ({ url, thumbnail, onOpen }) => (
    <div
        style={{
            position: 'relative',
            marginTop: '12px',
            cursor: 'pointer',
            borderRadius: '15px',
            overflow: 'hidden',
            WebkitTapHighlightColor: 'transparent'
        }}
        onClick={() => onOpen(url)}
    >
        <img src={thumbnail} alt="동영상 썸네일" style={{ width: '100%', display: 'block', minHeight: '150px', objectFit: 'cover' }} />
        <div style={{
            position: 'absolute',
            top: 0,
            left: 0,
            width: '100%',
            height: '100%',
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
            backgroundColor: 'rgba(0,0,0,0.3)'
        }}>
            <div style={{
                width: '60px', 
                height: '60px',
                backgroundColor: 'rgba(255, 255, 255, 0.9)',
                borderRadius: '50%',
                display: 'flex',
                justifyContent: 'center',
                alignItems: 'center',
                paddingLeft: '5px',
                boxShadow: '0 4px 10px rgba(0,0,0,0.2)'
            }}>
                <span style={{ color: 'rgb(0, 55, 100)', fontSize: '24px' }}>▶</span>
            </div>
        </div>
    </div>
);

// 파일 다운로드 컴포넌트
export const FileDownload = ({ name, url }) => (
    <div style={{
        display: 'flex',
        alignItems: 'center',
        padding: '12px 16px', 
        backgroundColor: '#f8f9fa',
        borderRadius: '12px',
        marginTop: '12px',
        border: '1px solid #e9ecef',
    }}>
        <span style={{ fontSize: '28px', marginRight: '12px' }}>📄</span>
        <div style={{ flex: 1, overflow: 'hidden' }}>
            <div style={{
                fontWeight: '600',
                fontSize: '0.9rem', 
                whiteSpace: 'nowrap',
                overflow: 'hidden',
                textOverflow: 'ellipsis',
                color: '#333',
                marginBottom: '2px'
            }}>{name}</div>
            <a
                href={url}
                download
                style={{
                    fontSize: '0.85rem',
                    color: 'rgb(0, 55, 100)',
                    textDecoration: 'none',
                    fontWeight: 'bold',
                    display: 'inline-block',
                    padding: '2px 0' 
                }}
            >
                다운로드
            </a>
        </div>
    </div>
);