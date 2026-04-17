import Icon from '../icon/Icon';


const Header = ({ onLogoClick }) => (
    <header style={{
        backgroundColor: 'var(--gok-blue)',
        color: 'var(--gok-white)',
        padding: '1rem 2rem',
        display: 'flex',
        alignItems: 'center',
        boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
        height: '70px'
    }}>
        <div className="logo-group" onClick={onLogoClick} style={{
            display: 'flex',
            alignItems: 'center',
            cursor: 'pointer'
        }}>
            <Icon type="mark" height={36} />
            <div className="v-line"></div>
            <h1 className="header-title" style={{
                color: "white",
                marginLeft: "10px"
            }}>AX2 CHATBOT</h1>
        </div>
    </header >
);

export default Header;