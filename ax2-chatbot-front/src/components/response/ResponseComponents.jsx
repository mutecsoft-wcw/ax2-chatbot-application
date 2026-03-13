import React from 'react';

// 이미지 답변 
export const ImageGroup = ({ urls, onImageClick }) => (
  <div style={{ 
    display: 'grid', 
    gridTemplateColumns: 'repeat(auto-fit, minmax(140px, 1fr))', 
    gap: '12px',      
    marginTop: '12px' 
  }}>
    {urls.map((url, i) => (
      <img 
        key={i} 
        src={url} 
        alt="답변 이미지" 
        onClick={() => onImageClick && onImageClick(url)} // 클릭 시 모달 함수 호출
        style={{ 
          width: '100%', 
          aspectRatio: '1 / 1', 
          objectFit: 'cover',
          borderRadius: '15px', 
          border: '1px solid #eee',
          cursor: 'pointer',
        }} 
        onMouseEnter={(e) => e.currentTarget.style.transform = 'scale(1.02)'}
        onMouseLeave={(e) => e.currentTarget.style.transform = 'scale(1)'}
      />
    ))}
  </div>
);

// 동영상 답변 
export const VideoPreview = ({ url, thumbnail, onOpen }) => (
  <div 
    style={{ position: 'relative', marginTop: '12px', cursor: 'pointer', borderRadius: '15px', overflow: 'hidden' }}
    onClick={() => onOpen(url)}
  >
    <img src={thumbnail} alt="동영상 썸네일" style={{ width: '100%', display: 'block' }} />
    <div style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%', display: 'flex', justifyContent: 'center', alignItems: 'center', backgroundColor: 'rgba(0,0,0,0.3)' }}>
      <div style={{ width: '50px', height: '50px', backgroundColor: 'white', borderRadius: '50%', display: 'flex', justifyContent: 'center', alignItems: 'center', paddingLeft: '4px' }}>
        <span style={{ color: 'rgb(0, 55, 100)', fontSize: '20px' }}>▶</span>
      </div>
    </div>
  </div>
);

// 리포트/파일 답변
export const FileDownload = ({ name, url }) => (
  <div style={{ 
    display: 'flex', 
    alignItems: 'center', 
    padding: '14px', 
    backgroundColor: '#f8f9fa', 
    borderRadius: '15px', 
    marginTop: '12px', 
    border: '1px solid #e9ecef' 
  }}>
    <span style={{ fontSize: '24px', marginRight: '12px' }}>📄</span>
    <div style={{ flex: 1, overflow: 'hidden' }}>
      <div style={{ fontWeight: 'bold', fontSize: '0.85rem', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis', color: '#333' }}>
        {name}
      </div>
      <a href={url} download style={{ fontSize: '0.8rem', color: 'rgb(0, 55, 100)', textDecoration: 'none', fontWeight: 'bold' }}>
        문서 다운로드
      </a>
    </div>
  </div>
);