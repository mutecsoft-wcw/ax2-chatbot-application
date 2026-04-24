import Icon from '../icon/Icon';
import '../css/Header.css';


const Header = ({ onLogoClick }) => (
    <header className="header-inner">
        <div className="logo-group" onClick={onLogoClick}>
            <Icon type="mark" height={36} />
            <div className="v-line"></div>
            <h1 className="header-title">건강지기 AI 챗봇</h1>
        </div>
    </header >
);

export default Header;