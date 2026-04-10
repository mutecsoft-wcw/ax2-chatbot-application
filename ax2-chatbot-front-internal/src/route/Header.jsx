
const Header = ({ onLogoClick }) => (
    <header style={{
        backgroundColor: 'var(--gok-blue)',
        color: 'var(--gok-white)',
        padding: '1rem 2rem',
        display: 'flex',
        alignItems: 'center',
        boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
    }}>
        <h1 onClick={onLogoClick}
            style={{
                fontSize: '1.25rem', fontWeight: 'bold', margin: 0, cursor: "pointer", color: "white"
            }}>
            AX2 CHAT BOT
        </h1>
    </header>
);

export default Header;