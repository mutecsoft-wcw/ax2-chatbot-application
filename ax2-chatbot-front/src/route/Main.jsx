
const Main = ({ children }) => {
    return (
      <main style={{
        flex: 1,           // 푸터를 화면 하단으로 밀어내기 위함
        marginTop: '70px', // 헤더 높이만큼 여백
        padding: '2rem',
        width: '100%',
        maxWidth: '1200px',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center'
      }}>
        {children}
      </main>
    );
  };
  
  export default Main;